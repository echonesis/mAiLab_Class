#!/usr/bin/python

def simpleGenRandomNumber(n, llimit=0, ulimit=1):
    import random
    result = [random.uniform(llimit, ulimit) for i in xrange(n)]
    return result

if __name__ == '__main__':
    # For basic questions
    # Basic #1
    # In this part, the built-in Python functions would be used.
    num_random = 5
    print 'Basic 1> Generate', num_random, 'Random Number'
    print simpleGenRandomNumber(num_random)

    # Basic #2
    import numpy as np
    import time
    print 'Basic 2>'
    n1 = [10**1, 10**2, 10**3, 10**4, 10**5]
    usedTime = list()
    for iCnt in n1:
        t1 = time.time()
        result1 = simpleGenRandomNumber(iCnt, -1, 1)
        usedTime.append(time.time() - t1)
        print 'Case for N =', iCnt
        print 'Mean =', np.mean(result1), '; STD =', np.std(result1)

    # Advanced #1
    print 'Advanced 1>'
    for i in range(len(n1)):
        print 'Case for N =', n1[i]
        print 'Used Sys Time =', usedTime[i], '(s)'

'''
Sample Output:
Basic 1> Generate 5 Random Number
[0.8517352415235713, 0.9608042046044872, 0.1512693660183837, 0.6074746239442333, 0.5267800150194317]
Basic 2>
Case for N = 10
Mean = -0.240647969028 ; STD = 0.424100623283
Case for N = 100
Mean = -0.0732104451873 ; STD = 0.596035030544
Case for N = 1000
Mean = 0.0287190524504 ; STD = 0.58627480244
Case for N = 10000
Mean = -0.00509101610347 ; STD = 0.578908223166
Case for N = 100000
Mean = 0.00342896915716 ; STD = 0.576555864097
Advanced 1>
Case for N = 10
Used Sys Time = 1.00135803223e-05 (s)
Case for N = 100
Used Sys Time = 4.10079956055e-05 (s)
Case for N = 1000
Used Sys Time = 0.000274896621704 (s)
Case for N = 10000
Used Sys Time = 0.00268888473511 (s)
Case for N = 100000
Used Sys Time = 0.0347440242767 (s)
'''
