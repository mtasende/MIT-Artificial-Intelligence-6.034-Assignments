# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5 or Python v2.6
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = '2'


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
    return x**3

def factorial(x):
    if(x<0):
        raise Exception, "factorial: Input must be a positive integer."
    else:
        resp = 1
        for i in range(2,x+1):
            resp = resp*i
    return resp


def count_pattern(pattern, lst):
    N = len(pattern)
    M = len(lst)
    #print "pattern = ",pattern
    #print "lst = ",lst
    #print "N M =  ",N," ",M
    numCoincidencias = 0
    for i in range(0,M-N+1):
        indPat = 0
        indLst = i

        #print "i = ",i

        coincidencia = 0
        while(lst[indLst] == pattern[indPat]):
            #print "en el while, indPat=  ",indPat,"indLst=  ",indLst
            indPat = indPat+1
            indLst = indLst+1
            if(indPat==N): #Se encontraron N simbolos coincidentes
                coincidencia=1
                break

        numCoincidencias = numCoincidencias + coincidencia
    return numCoincidencias


# Problem 2.2: Expression depth

def depth(expr):
    #Acepta tuplas o listas de elementos. Todo lo demas son elementos de profundidad cero.
    if(not isinstance(expr,(list,tuple))):
        return 0
    else:
        N = len(expr)
        md = 0
        for i in range(0,N):
            md = max((md,depth(expr[i])+1))
        return md



# Problem 2.3: Tree indexing

def tree_ref(tree, index):
    N = len(index)
    #print "N = ",N
    #print "index = ",index
    ind = index[0]
    #print "ind = ", ind
    if(N==1):
        if(not isinstance(ind,(int,long))):
            raise Exception, "tree_ref: Index must be an integer or long value"
        elif(ind<0):
            raise Exception, "tree_ref: Index must be positive or zero"
        elif(ind>=len(tree)):
            raise Exception, "tree_ref: Index is out of the tree"
        else:
            return tree[ind]
    else:
        if (not isinstance(ind, (int, long))):
            raise Exception, "tree_ref: Index must be an integer or long value"
        elif (ind < 0):
            raise Exception, "tree_ref: Index must be positive or zero"
        elif (ind >= len(tree)):
            raise Exception, "tree_ref: Index is out of the tree"
        else:
            return tree_ref(tree[ind],index[1:N+1])



# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = ""

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = ""

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = ""

# How many hours did this lab take?
HOURS = ""


def main():
    pat = ['a','b']
    lst = ['a','b','c','d','e']
    print count_pattern(pat,lst)

    print "Depth"
    print depth('x')
    print depth(('+',('expt','x'),('expt','y',2),(5,6)))

    print "tree_ref"
    tree = (((1,2),3),(4,(5,6)),7,(8,9,10))
    print "tree1 result:   ",tree_ref(tree,(3,1))
    print "tree2 result:   ",tree_ref(tree,(1,1,1))
    print "tree3 result:   ", tree_ref(tree, (1,))

if __name__ == '__main__':
    main()