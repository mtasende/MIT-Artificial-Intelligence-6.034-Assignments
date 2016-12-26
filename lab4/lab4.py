from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

cantLlamadas = 0

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    global cantLlamadas
    cantLlamadas += 1

    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    # Add your forward checking logic here.
    Xvar = state.get_current_variable()
    if(Xvar == None):
        return True

    xval = Xvar.get_assigned_value()
    constraints = state.get_constraints_by_name(Xvar.get_name())

    for const in constraints:
        if(const.get_variable_i_name() == Xvar.get_name()):
            YvarName = const.get_variable_j_name()
            Yvar = state.get_variable_by_name(YvarName)
            for yval in Yvar.get_domain():
                if(not const.check(state,value_i=xval,value_j=yval)):
                    Yvar.reduce_domain(yval)
        elif(const.get_variable_j_name() == Xvar.get_name()):
            YvarName = const.get_variable_i_name()
            Yvar = state.get_variable_by_name(YvarName)
            for yval in Yvar.get_domain():
                if(not const.check(state,value_i=yval,value_j=xval)):
                    Yvar.reduce_domain(yval)

        if(Yvar.domain_size()==0):
            return False

    #Si no devolvi False todavia es que ninguna restriccion fallo
    return True


# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    global cantLlamadas
    cantLlamadas += 1

    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    variables = state.get_all_variables()
    singletons = [s for s in variables if s.domain_size()==1]
    visitados = []

    while(len(singletons) > 0):
        Xvar = singletons.pop()
        visitados.append(Xvar)
        xDom = Xvar.get_domain()
        xval = xDom[0]

        constraints = state.get_constraints_by_name(Xvar.get_name())

        for const in constraints:
            if (const.get_variable_i_name() == Xvar.get_name()):
                YvarName = const.get_variable_j_name()
                Yvar = state.get_variable_by_name(YvarName)
                for yval in Yvar.get_domain():
                    if (not const.check(state, value_i=xval, value_j=yval)):
                        Yvar.reduce_domain(yval)
            elif (const.get_variable_j_name() == Xvar.get_name()):
                YvarName = const.get_variable_i_name()
                Yvar = state.get_variable_by_name(YvarName)
                for yval in Yvar.get_domain():
                    if (not const.check(state, value_i=yval, value_j=xval)):
                        Yvar.reduce_domain(yval)

            if (Yvar.domain_size() == 0):
                return False

        singletons = [s for s in variables if ((s.domain_size() == 1) and (not (s in visitados)))]

    return True


## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.
import math

def euclidean_distance(list1, list2):
    """ Calculate the Hamming distance between two lists """
    # Make sure we're working with lists
    # Sorry, no other iterables are permitted
    assert isinstance(list1, list)
    assert isinstance(list2, list)

    dist = 0

    # 'zip' is a Python builtin, documented at
    # <http://www.python.org/doc/lib/built-in-funcs.html>
    for item1, item2 in zip(list1, list2):
        dist += (item2 - item1)**2
    return math.sqrt(dist)

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2,verbose=1)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance,5)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    Nyes = len(yes)
    Nno = len(no)
    Ntot = Nyes + Nno

    contadorYes = {x:yes.count(x) for x in yes}
    Iyes = 0
    for x in contadorYes.keys():
        if(contadorYes[x] != 0):
            Iyes -= (float(contadorYes[x])/Nyes)*math.log(float(contadorYes[x])/Nyes,2)

    contadorNo = {x: no.count(x) for x in no}
    Ino = 0
    for x in contadorNo.keys():
        if (contadorNo[x] != 0):
            Ino -= (float(contadorNo[x]) / Nno) * math.log(float(contadorNo[x]) / Nno, 2)

    return (Nyes*Iyes + Nno*Ino)/Ntot


#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2,verbose=1)
#evaluate(idtree_maker(senate_votes, information_disorder), senate_group1, senate_group2,verbose=1)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 540
rep_classified = limited_house_classifier(house_people, house_votes, N_1)
print rep_classified

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67  #Entre 200 y 200 empeora por el overfitting, seguramente
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
print  senator_classified

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)
print  old_senator_classified


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "6"
WHAT_I_FOUND_INTERESTING = "Everything, as usual"
WHAT_I_FOUND_BORING = "Nothing!"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
