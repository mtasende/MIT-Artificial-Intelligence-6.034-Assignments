from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    tree = [hypothesis]
    for rule in rules:
        cons = rule.consequent()
        antec = rule.antecedent()

        #Busco "matches"
        isInConsequent = False
        for pattern in cons:
            dictMatch = match(pattern,hypothesis)
            if(dictMatch != None):
                isInConsequent = True
                #print "Match!"
                #print rule
                break

        if(isInConsequent):
            listaTemp = []
            if(not isinstance(antec,list)): #Es una expresion simple
                expP = populate(antec, dictMatch)
                expP = backchain_to_goal_tree(rules, expP)
                tree.append(expP)
            else:
                for exp in antec:
                    expP = populate(exp,dictMatch)
                    expP = backchain_to_goal_tree(rules,expP)
                    listaTemp.append(expP)

            if(isinstance(antec,AND)):
                tree.append(AND(listaTemp))
            elif(isinstance(antec,OR)):
                tree.append(OR(listaTemp))

    return simplify(OR(tree))


def main():
    # Here's an example of running the backward chainer - uncomment
    # it to see it work:
    print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')

if __name__ == '__main__':
    main()

