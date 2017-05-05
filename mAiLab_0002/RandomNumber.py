#!/usr/bin/perl

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
    For Basic part, the following is the sample output:
    Basic 1> Generate 5 Random Number
    [0.38554052795997207, 0.6136228008082, 0.6787578153203891, 0.6489740564293955, 0.7710917185546308]
    Basic 2>
    Case for N = 10
    Mean = -0.312901186771 ; STD = 0.466520661607
    Case for N = 100
    Mean = -0.0747169104398 ; STD = 0.565906534055
    Case for N = 1000
    Mean = -0.0157894681898 ; STD = 0.592963060275
    Case for N = 10000
    Mean = -0.0011872676824 ; STD = 0.5807030628
    Case for N = 100000
    Mean = -0.0019084834785 ; STD = 0.576954618766
    '''

