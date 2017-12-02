from random import randrange
from math import log
a = 'TCGGCTGCATTTCGA'
s={(3,13),(4,8),(5,7),(9,10)}#exemple

def e(a: str, i: int, j: int) -> {0,1}:
    """Retourner 1 si i,j sont couplés, 0 sinon."""
    def couple(a: str, i: int, j:int) -> bool:
        return {a[i-1], a[j-1]} in [ {'A','T'}, {'C','G'} ]

    if couple(a,i,j):
        return 1
    else:
        return 0

def tailleMaxRec(a: str, i: int, j: int) -> int:
    n= len(a)
    assert 1 <= i <= n and 1 <= j <= n, 'impossible de tronquer'
    
    if a == '' or i >= j:
        return 0
##
##    def couple(i: int, j:int) -> bool:
##        return {a[i-1], a[j-1]} in [ {'A','T'}, {'C','G'} ]
##    
##    def e(i: int, j: int) -> {0,1}:
##        if couple(i,j):
##            return 1
##        else:
##            return 0

    return max(tailleMaxRec(a, i+1, j-1) + e(a,i,j),
               max([tailleMaxRec(a, i, k-1) + tailleMaxRec(a, k, j)
                    for k in range(i+1, j+1)]) )

def tailleMaxIter(a: str, i: int, j: int) -> int:
    n= len(a)
    E=dict()
    E[(1,1)] = 0
    for i in range(2, n+1):
        E[(i,i)] = 0
        E[(i,i-1)] = 0
    for p in range(1, n):
        for i in range(1, n-p+1):
            E[(i,i+p)] = max( E[(i+1,i+p-1)] + e(a, i, i+p),
                             max ( E[(i,k-1)] + E[(k,i+p)]
                                  for k in range(i+1, i+p+1)))
    return E[(i,j)]

def SeqAleatoire(n: int) -> str:
    return ''.join(['A','T','C','G'][randrange(4)] for i in range(n))#i peu d'importance


def test1() -> None:
    print("E_3_13 calcule par l'algorithme recursive =", tailleMaxRec(a, 3, 13))
    print("E_3_13 calcule par l'algorithme iterative =", tailleMaxIter(a, 3, 13))
    print('10 executions de la fonction recursive prennent',
          timeit.timeit("tailleMaxRec(a, 3, 13)", number=10,
                        setup="from __main__ import tailleMaxRec, a"), 'secondes')
    print('10 executions de la fonction iterative prennent',
          timeit.timeit("tailleMaxIter(a, 3, 13)", number=10,
                        setup="from __main__ import tailleMaxIter, a"), 'secondes')
    
def testRec() -> None:
    n = 1
    lt0 = 0
    while True:
        a = SeqAleatoire(n)
        t1 = timeit.timeit("tailleMaxRec(a, 1, n)", number=1,
                        setup="from __main__ import tailleMaxRec",
                           globals=locals())
        print('''CRec({0:d})  = {1:7f}, log'(CRec({0:d})) = {2:7f}'''.format(
            n, t1, log(t1) - lt0))
        print()
        if t1 > 600: 
            break
        n = n + 1
        lt0 = log(t1)

def testIter() -> None:
    n = 1
    while True:
        a = SeqAleatoire(n)
        t2 = timeit.timeit("tailleMaxIter(a, 1, n)", number=1,
                setup="from __main__ import tailleMaxIter",
                   globals=locals())
##        print('CIter({0:d}) = {1:7f}, CIter({0:d})/{0:d}^3 = {2:9f}'.format(
##            n, t2, t2 / n**3))
##        print()
        if t2 > 300:
            print(n)
            break
        n = n + 1
        
if __name__ == '__main__':
    import timeit
    testIter()
