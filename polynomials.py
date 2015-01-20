
"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

"""
def rename(newname):
    """decorate function adding attr name with value newname"""
    def decorator(f):
        f.__name__ = newname
        return f
    return decorator

def add_coef(coefs):
    """decorate function adding attr coefs with tuple value removing trailing zeros from coefs"""
    while coefs[-1] == 0:
        coefs = coefs[:-1]
    def decorator(f):
        f.coefs = coefs
        return f
    return decorator

def polyname(coefs):
    """Returns a string representation (ascending order) of a polynomial given coefficients 'coefs' """
    i = len(coefs)-1
    poly_name = ''
    for coef in reversed(coefs):
        if coef == 0:
            i = i-1
            continue
        if coef != 1 or i==0:
            poly_name = poly_name + ' + ' + str(coef) 
        if i ==0:
            continue
        if coef != 1:
            poly_name = poly_name + ' * '
        else:
            poly_name = poly_name + ' + '
        poly_name = poly_name + 'x'
        if i !=1:
            poly_name = poly_name + '**'+str(i)
        i = i-1
    return poly_name[3:]

def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""
    # your code here (I won't repeat "your code here"; there's one for each function)
    new_name = polyname(coefs)
    @add_coef(coefs)
    @rename(new_name)       
    def polynomial(x):
        total = 0
        for i,coef in enumerate(coefs):
            total = total + coef*x**i
        return total
    return polynomial
            

def test_poly():
    global p1, p2, p3, p4, p5, p9 # global to ease debugging in an interactive session

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x**2 + 20 * x + 10
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    assert p9(2) == 512
    p4 =  add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert same_name(power(poly((1, 1)), 10).__name__,
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11,22,33)
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9,18,27) 
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1) 
    assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)

    assert deriv(p1).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573


def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""
    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
    return canonical_name(name1) == canonical_name(name2)

def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    return hasattr(x,'coefs')

def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    p1_coefs, p2_coefs = p1.coefs, p2.coefs
    new_coefs = tuple([i+j for i,j in zip(p1_coefs,p2_coefs)])
    if len(p1_coefs) != len(p2_coefs):
        greater = p1_coefs if len(p1_coefs)>len(p2_coefs) else p2_coefs
        distance = abs(len(p1_coefs)-len(p2_coefs))
        new_coefs = new_coefs + greater[-distance:]
    return poly(new_coefs)

def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    negative_coefs = tuple([-coef for coef in p2.coefs])
    return add(p1,poly(negative_coefs))

def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    p1_coefs, p2_coefs = p1.coefs, p2.coefs
    new_coefs = []
    for i in range(len(p1_coefs+p2_coefs)):
        coef = 0
        for j in range(i+1):
            if j<len(p1_coefs) and i-j<len(p2_coefs):
                coef = coef + p1_coefs[j]*p2_coefs[i-j]
        new_coefs.append(coef)
    return poly(tuple(new_coefs))

def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    result = poly((1,))
    for i in range(n):
        result = mul(p,result)
    return result
        

    
def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    dev_coefs = tuple([coef*i for i,coef in enumerate(p.coefs)][1:])
    return poly(dev_coefs)
    

def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    int_coefs = tuple([C]+[coef/float(i+1) for i,coef in enumerate(p.coefs)])
    return poly(int_coefs)

test_poly()