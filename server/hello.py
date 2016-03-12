from __future__ import print_function
import recsys.algorithm
from recsys.algorithm.factorize import SVD

svd = SVD(filename='/var/www/test/bookrate')
def rec(userid):
    try:
        return svd.recommend(userid, is_row=True)
    except KeyError:
        return []

if __name__ == '__main__':
    rec(276729)
    res = rec(4017)
    print(rec(0))
    print(res[1:])
