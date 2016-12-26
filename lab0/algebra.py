# Section 3: Algebraic simplification

# This code implements a simple computer algebra system, which takes in an
# expression made of nested sums and products, and simplifies it into a
# single sum of products. The goal is described in more detail in the
# problem set writeup.

# Much of this code is already implemented. We provide you with a
# representation for sums and products, and a top-level simplify() function
# which applies the associative law in obvious cases. For example, it
# turns both (a + (b + c)) and ((a + b) + c) into the simpler expression
# (a + b + c).

# However, the code has a gap in it: it cannot simplify expressions that are
# multiplied together. In interesting cases of this, you will need to apply
# the distributive law.

# Your goal is to fill in the do_multiply() function so that multiplication
# can be simplified as intended. 

# Testing will be mathematical:  If you return a flat list that
# evaluates to the same value as the original expression, you will
# get full credit.


# We've already defined the data structures that you'll use to symbolically
# represent these expressions, as two classes called Sum and Product,
# defined below. These classes both descend from the abstract Expression class.
#
# The top level function that will be called is the .simplify() method of an
# Expression.
#
# >>> expr = Sum([1, Sum([2, 3])])
# >>> expr.simplify()
# Sum([1, 2, 3])


### Expression classes _____________________________________________________

# Expressions will be represented as "Sum()" and "Product()" objects.
# These objects can be treated just like lists (they inherit from the
# "list" class), but you can test for their type using the "isinstance()"
# function.  For example:
#
# >>> isinstance(Sum([1,2,3]), Sum)
# True
# >>> isinstance(Product([1,2,3]), Product)
# True
# >>> isinstance(Sum([1,2,3]), Expression) # Sums and Products are both Expressions
# True

class Expression:
    "This abstract class does nothing on its own."
    pass

class Sum(list, Expression):
    """
    A Sum acts just like a list in almost all regards, except that this code
    can tell it is a Sum using isinstance(), and we add useful methods
    such as simplify().

    Because of this:
      * You can index into a sum like a list, as in term = sum[0].
      * You can iterate over a sum with "for term in sum:".
      * You can convert a sum to an ordinary list with the list() constructor:
         the_list = list(the_sum)
      * You can convert an ordinary list to a sum with the Sum() constructor:
         the_sum = Sum(the_list)
    """
    def __repr__(self):
        return "Sum(%s)" % list.__repr__(self)
    
    def simplify(self):
        """
        This is the starting point for the task you need to perform. It
        removes unnecessary nesting and applies the associative law.
        """
        terms = self.flatten()
        if len(terms) == 1:
            return simplify_if_possible(terms[0])
        else:
            return Sum([simplify_if_possible(term) for term in terms]).flatten()

    def flatten(self):
        """Simplifies nested sums."""
        terms = []
        for term in self:
            if isinstance(term, Sum):
                terms += list(term)
            else:
                terms.append(term)
        return Sum(terms)


class Product(list, Expression):
    """
    See the documentation above for Sum. A Product acts almost exactly
    like a list, and can be converted to and from a list when necessary.
    """
    def __repr__(self):
        return "Product(%s)" % list.__repr__(self)
    
    def simplify(self):
        """
        To simplify a product, we need to multiply all its factors together
        while taking things like the distributive law into account. This
        method calls multiply() repeatedly, leading to the code you will
        need to write.
        """
        factors = []
        for factor in self:
            if isinstance(factor, Product):
                factors += list(factor)
            else:
                factors.append(factor)
        result = Product([1])
        for factor in factors:
            result = multiply(result, simplify_if_possible(factor))
        return result.flatten()

    def flatten(self):
        """Simplifies nested products."""
        factors = []
        for factor in self:
            if isinstance(factor, Product):
                factors += list(factor)
            else:
                factors.append(factor)
        return Product(factors)

def simplify_if_possible(expr):
    """
    A helper function that guards against trying to simplify a non-Expression.
    """
    if isinstance(expr, Expression):
        return expr.simplify()
    else:
        return expr

# You may find the following helper functions to be useful.
# "multiply" is provided for you; but you will need to write "do_multiply"
# if you would like to use it.

def multiply(expr1, expr2):
    """
    This function makes sure that its arguments are represented as either a
    Sum or a Product, and then passes the hard work onto do_multiply.
    """
    # Simple expressions that are not sums or products can be handled
    # in exactly the same way as products -- they just have one thing in them.
    if not isinstance(expr1, Expression): expr1 = Product([expr1])
    if not isinstance(expr2, Expression): expr2 = Product([expr2])
    return do_multiply(expr1, expr2)


def do_multiply(expr1, expr2):
    """
    You have two Expressions, and you need to make a simplified expression
    representing their product. They are guaranteed to be of type Expression
    -- that is, either Sums or Products -- by the multiply() function that
    calls this one.

    So, you have four cases to deal with:
    * expr1 is a Sum, and expr2 is a Sum
    * expr1 is a Sum, and expr2 is a Product
    * expr1 is a Product, and expr2 is a Sum
    * expr1 is a Product, and expr2 is a Product

    You need to create Sums or Products that represent what you get by
    applying the algebraic rules of multiplication to these expressions,
    and simplifying.

    Look above for details on the Sum and Product classes. The Python operator
    '*' will not help you.
    """

    expr2S = expr2

    #Primero simplifico, si hace falta
    expr1S = simplIfNecessary(expr1)
    expr2S = simplIfNecessary(expr2)

    #Ahora estan simplificados, pero hay que ver que son:
    if(isinstance(expr1S,Product)):
        if(isinstance(expr2S,Product)):
            return multiplyProdProd1(expr1S,expr2S)
        else:
            return multiplySum2Prod1(expr2S, expr1S)
    else:
        if(isinstance(expr2S,Product)):
            return multiplySum2Prod1(expr1S,expr2S)
        else:
            return multiplySumSum2(expr1S,expr2S)


    #Ahora tengo dos sumas de productos simples.
    sumaSimpL = []
    print "expr1S= ",expr1S
    print "expr2S= ",expr2S
    for term1 in expr1S:
        for term2 in expr2S:
            if(depth(term1)==0):
                term1=[term1]
            if (depth(term2) == 0):
                term2 = [term2]
            sumaSimpL.append(term1+term2)

    return Sum(sumaSimpL)


def simplIfNecessary(expr):
    expr1S = expr
    if (isinstance(expr, Product)):
        if (depth(expr) > 1):
            expr1S = expr.simplify()
    elif (isinstance(expr, Sum)):
        simplificado1 = True
        if (depth(expr) > 2):
            simplificado1 = False
        elif (depth(expr) == 2):
            for term in expr:
                if (not isinstance(term, Product)):
                    simplificado1 = False
        if (not simplificado1):
            expr1S = expr.simplify()
    return expr1S


#Multiplica dos productos de profundidad 1
def multiplyProdProd1(prod1,prod2):
    return Product(prod1+prod2)

#Multiplica un producto de profundidad 1 con una suma de profundidad 1, o una suma de prof=2 con productos de prof=1 en ella
#Devuelve una suma de productos de profundidad 2, siempre
def multiplySum2Prod1(suma,prod):
    listaTemp = []
    for term in suma:
        if(depth(term)==0):
            listaTemp.append(multiplyProdProd1( Product([term]) , prod ))
        else:
            listaTemp.append(multiplyProdProd1(term, prod))
    return Sum(listaTemp)

#Multiplica una suma de profundidad 1 o 2, con una suma de profundidad 1 o 2
#Devuelve una suma de profundidad 2 siempre
def multiplySumSum2(suma1,suma2):
    listaTemp = []
    for term in suma1:
        if(depth(term)==0):
            listaTemp += multiplySum2Prod1(suma2,Product([term]))
        else:
            listaTemp += multiplySum2Prod1(suma2,term)
    return Sum(listaTemp)


#Funcion auxiliar agregada
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


#Testing...
def main():
    fact1 = Sum([2,5])
    fact2 = Sum([Product([7,6]),9])
    res = Product([fact1,fact2]).simplify()
    print "Resultado:  ",res
    print "Largo de la suma: ",len(res)
    i=0
    for term in res:
        print "term ",i," es de clase: ",type(res).__name__
        i += 1


if __name__ == '__main__':
    main()
