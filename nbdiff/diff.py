"""Implementing the Hunt-McIllroy Algorithm"""


def lcs_dynamic(a, b, i=None, j=None):
    '''Longest common subsequence, implemented with dynamic programming.
    See p. 2 of (Hunt, J.W. and McIllroy, M.D., 1978).'''
    if i is None:
        i = len(a) - 1
    if j is None:
        j = len(b) - 1
    if i == -1 or j == -1:
        return 0
    elif a[i] == b[j]:
        return 1 + lcs_dynamic(a, b, i-1, j-1)
    else:
        return max(lcs_dynamic(a, b, i, j-1), lcs_dynamic(a, b, i-1, j))


def lcs(a, b):
    '''Longest common subsequence.'''
    V = [(line, i) for i, line in enumerate(b)]
    sorted_v = sorted(V)
    def f(j):
        return j == len(sorted_v)-1 or sorted_v[j][0]!=sorted_v[j+1][0]

    E = [(serial, f(j))
            for j,(line,serial) in enumerate(sorted_v)]
    actual_E = [
    ]
    E.insert(0, (-1,True))
    print E

    P = []
    for i in range(0, len(a)):
        good_j = -1
        for j in range(0, len(b)):
            if E[j][1] and a[i] == sorted_v[j][0]:
                good_j = j
                break

        P.append(good_j)

    print 'P = ', P
    K = [(-1, -1, None), (len(a)+1, len(b)+1, None)]
    k = 0
    for i in range(1, len(a)+1):
        merge(K, k, i-1, E, P[i-1])
    return K


def merge(K, k, i, E, pi):
    r = 0
    c = K[0]
    while True:
        break_please = False
        j = E[pi+1][0]
        S = K[r:k+2]
        print 'E = ', E
        print 'S = ', S
        print 'pi={pi}; i = {i}; j={j}'.format(i=i, j=j, pi=pi)

        for subs, e in enumerate(S):
            s = subs + r
            print 's =', s
            if s+1 >= len(K):
                break
            ks = K[s]
            print 'ks = ', ks[1]
            ksp1 = K[s+1]
            print 'ksp1 = ', ksp1[1]
            if j < ksp1[1] and j > ks[1]:
                if ksp1[1] >= j:
                    K[r] = c
                    r = r + 1
                    c = (i, j, K[s])
                    print 'c = ', c
                if s == k:
                    K.insert(k+2, K[k+1])
                    k = k + 1
                break_please = True
                break
            # do something

        if break_please:
            break

        if E[pi][1]:
            break
        else:
            pi = pi+1
    print 'Bottom'
    print 'K = ', K
    print 'c = ', c
    print 'r = ', r
    K[r] = c
    print 'New K = ', K
