import unittest
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,'GreedyPermutation')))
from point import Point
from node import Node
from covertree import CoverTree
from CHeap import CHeap
from CPoint import CPoint
from metrics import *
from greedypermutation import GreedyPermutation
import random
import os
        
class TestCoverTree(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.ct1 = 'c:\\ct1.txt'
        self.ctwithoutparentcondition = 'c:\\ctwithoutparentcondition.txt'
        f1 = open(self.ct1, 'w')
        print('Euclidean', file=f1)
        print(',', file=f1)
        print('2 1 1', file=f1)
        print(',', file=f1)
        print('0 0', file=f1)
        print('1 32', file=f1)
        print('2 16', file=f1)
        print('3 4', file=f1)
        print(',', file=f1)
        print('inf 0', file=f1)
        print('4 0 0', file=f1)
        print('4 1 0', file=f1)
        print('3 1 1', file=f1)
        print('3 2 1', file=f1)
        print('2 0 0', file=f1)
        print('1 0 0', file=f1)
        print('1 3 0', file=f1)
        f1.close()
        f2 = open(self.ctwithoutparentcondition, 'w')
        print('Euclidean', file=f2)
        print(',', file=f2)
        print('2 1 1', file=f2)
        print(',', file=f2)
        print('0 0', file=f2)
        print('1 22', file=f2)
        print('2 12', file=f2)
        print('3 7', file=f2)
        print('4 3', file=f2)
        print(',', file=f2)
        print('inf 0', file=f2)
        print('4 0 0', file=f2)
        print('4 1 0', file=f2)
        print('3 0 0', file=f2)
        print('3 2 0', file=f2)
        print('2 0 0', file=f2)
        print('2 3 0', file=f2)
        print('1 3 3', file=f2)
        print('1 4 3', file=f2)
        f2.close()
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        try:
            os.remove(self.ct1)
            os.remove(self.ctwithoutparentcondition)
        except OSError: pass
        
    def test_init(self):
        ct = CoverTree(Euclidean())
        self.assertEqual(ct.root, None)
        self.assertEqual(ct.tau, 2)
        self.assertEqual(ct.cc, 1)
        self.assertEqual(ct.cp, 1)
        self.assertEqual(ct.cr, 12)
        ct = CoverTree(Euclidean(), 3, 2, 4)
        self.assertEqual(ct.tau, 3)
        self.assertEqual(ct.cp, 2)
        self.assertEqual(ct.cc, 4)
        self.assertEqual(ct.cr, 27)
        self.assertRaises(TypeError, CoverTree, .9, 2, 4)
        self.assertRaises(TypeError, CoverTree, 2, 5, 4)
        
    def test_levelof(self):
        p1 = Point([0])
        p2 = Point([32])
        metric = Euclidean()
        ct = CoverTree(metric)
        self.assertEqual(ct.levelof(p1.dist(metric, p2)[0])[0], 4)
        ct = CoverTree(Euclidean(), 3)
        self.assertEqual(ct.levelof(p1.dist(metric, p2)[0])[0], 3)
        ct = CoverTree(Euclidean(), 3, 1, 2)
        self.assertListEqual(ct.levelof(p1.dist(metric, p2)[0]), [2, 3])
        self.assertEqual(metric.counter, 3)
             
    def test_addJump(self):
        metric = Euclidean()
        ct = CoverTree(metric)
        p1 = Point([0])
        p2 = Point([32])
        n1, n3 = Node(p1, float('inf')), Node(p1, float('-inf'))
        n2 = Node(p1, 4).attachParent(n1).attachChild(n3)
        ct.levels[float('inf')] = {p1:n1}
        ct.levels[float('-inf')] = {p1:n2}
        ct.levels[4] = {p1:n3}
        n4 = ct.addJump(p2, n1, ct.levelof(p1.dist(Euclidean(), p2)[0])[0])
        self.assertSetEqual({v.point for v in ct.levels[float('inf')].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[4].values()}, {p1, p2})
        self.assertSetEqual({v.point for v in ct.levels[float('-inf')].values()}, {p1, p2})
        self.assertSetEqual(set(n2.rel), {n2, n4})
        self.assertSetEqual(set(n4.rel), {n2, n4})
        self.assertEqual(metric.counter, 4)
        
    def test_splitJump(self):
        metric = Euclidean()
        ct = CoverTree(metric)
        p1 = Point([0])
        n1, n2 = Node(p1, float('inf')), Node(p1, float('-inf'))
        ct.root = n1.attachChild(n2)
        ct.levels[float('inf')] = {p1:n1}
        ct.levels[float('-inf')] = {p1:n2}
        ct.splitJump(n1, n2, 5)
        self.assertEqual(len(ct.levels), 3)
        self.assertSetEqual({v.point for v in ct.levels[float('inf')].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[5].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[float('-inf')].values()}, {p1})
        
    def test_insert(self):
        metric = Euclidean()
        ct = CoverTree(metric)
        p1 = Point([0])
        p2 = Point([32])
        p3 = Point([16])
        p4 = Point([4])
        root = ct.insert(p1, None)        
        n4 = ct.insert(p4, root)
        self.assertEqual(metric.counter, 5)
        n2 = ct.insert(p2, root)
        self.assertEqual(metric.counter, 11)
        n3 = ct.insert(p3, n2)
        self.assertEqual(metric.counter, 25)
        self.assertSetEqual({v.point for v in ct.levels[float('inf')].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[4].values()}, {p1, p2})
        self.assertSetEqual({v.point for v in ct.levels[3].values()}, {p2, p3})
        self.assertSetEqual({v.point for v in ct.levels[2].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[1].values()}, {p1, p4})
        self.assertSetEqual({v.point for v in ct.levels[float('-inf')].values()}, {p1, p2, p3, p4})
        # test relatives
        self.assertSetEqual(set(root.rel), {root})
        self.assertSetEqual(set(root.child().rel), set(n2.rel))
        self.assertSetEqual(set(n2.child().rel), {n2.child(), n3, n4.par})
        self.assertSetEqual(set(n3.rel), {n3, n4.par, n2.child()})
        self.assertSetEqual(set(n4.par.rel), {n4.par, n3.child(), n2.child().child()})
        self.assertSetEqual(set(n4.par.child().rel), set(n4.rel))
        self.assertEqual(ct.verifyRelatives(), True)
        self.assertEqual(ct.isCoverTree(), True)
        
    def test_findParentFromPred(self):
        ct = CoverTree(Euclidean(), 3)
        p1 = CPoint([0])
        p2 = CPoint([239])
        p3 = CPoint([158])
        p4 = CPoint([80])
        p5 = CPoint([198])
        p6 = CPoint([220])
        perm = CHeap([p1, p2, p3, p4, p5, p6], Euclidean()).makePerm()
        n1 = ct.insert(perm[0], None)
        n2 = ct.insert(perm[1], n1)
        par = ct.findParentFromPred(perm[2])
        self.assertEqual(par, n2)
        ct.insert(perm[2], par)
        par = ct.findParentFromPred(perm[3])
        self.assertEqual(par, n1.child())
        ct.insert(perm[3], par)
        par = ct.findParentFromPred(perm[4])
        self.assertEqual(par, n2)
        ct.insert(perm[4], par)
        par = ct.findParentFromPred(perm[5])
        self.assertEqual(par, n2.child())
        ct.insert(perm[5], par)
        self.assertSetEqual({v.point for v in ct.levels[float('inf')].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[4].values()}, {p1, p2})
        self.assertSetEqual({v.point for v in ct.levels[3].values()}, {p1, p2, p3, p4, p5})
        self.assertSetEqual({v.point for v in ct.levels[2].values()}, {p2, p6})
        self.assertSetEqual({v.point for v in ct.levels[float('-inf')].values()}, {p1, p2, p3, p4, p5, p6})
        ct2 = CoverTree(Euclidean())
        perm = CHeap([CPoint([0]), CPoint([16]), CPoint([25]), CPoint([35]), CPoint([68])], Euclidean()).makePerm()
        ct2.insert(perm[0], None)
        n1 = ct2.insert(perm[1], ct2.root)
        n2 = ct2.insert(perm[2], n1)
        ct2.insert(perm[3], ct2.root.child())
        par = ct2.findParentFromPred(perm[4])
        self.assertEqual(par, n2)
        
    def test_buildFromGP(self):
        p1 = CPoint([0])
        p2 = CPoint([1])
        p3 = CPoint([8])
        p4 = CPoint([15])
        p5 = CPoint([28])
        p6 = CPoint([32])
        p7 = CPoint([-1])
        p8 = CPoint([-10])
        perm = CHeap([p1, p2, p3, p4, p5, p6, p7, p8], Euclidean()).makePerm()
        ct = CoverTree(Euclidean())
        ct.buildFromGP(perm)
        self.assertSetEqual({v.point for v in ct.levels[float('inf')].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[4].values()}, {p1, p6})
        self.assertSetEqual({v.point for v in ct.levels[3].values()}, {p1, p4, p8})
        self.assertSetEqual({v.point for v in ct.levels[2].values()}, {p3, p4, p6})
        self.assertSetEqual({v.point for v in ct.levels[1].values()}, {p5, p6})
        self.assertSetEqual({v.point for v in ct.levels[0].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[-1].values()}, {p1, p2, p7})
        self.assertSetEqual({v.point for v in ct.levels[float('-inf')].values()}, {p1, p2, p3, p4, p5, p6, p7, p8})
        self.assertEqual(ct.verifyRelatives(), True)
        self.assertEqual(ct.isCoverTree(), True)
        
        num, dim = 20, 2
        perm = CHeap([CPoint([random.randint(-1000, 1000) for d in range(dim)]) for i in range(num)], Euclidean()).makePerm()
        ct3 = CoverTree(Euclidean())
        ct3.buildFromGP(perm)        
        self.assertEqual(ct3.verifyRelatives(), True)
        self.assertEqual(ct3.isCoverTree(), True)
        
    def test_augmentRelatives(self):
        ct = CoverTree(Euclidean())
        p1 = Point([0])
        p2 = Point([32])
        p3 = Point([16])
        p4 = Point([4])
        root = ct.insert(p1, None, False)
        n2 = ct.insert(p2, root, False)
        ct.insert(p3, n2, False)
        ct.insert(p4, root.child(), False)
        for k1 in ct.levels:
            for k2 in ct.levels[k1]:
                self.assertSetEqual(set(ct.levels[k1][k2].rel), {ct.levels[k1][k2]})
        self.assertEqual(ct.verifyRelatives(), False)
        ct.augmentRelatives();         
        self.assertEqual(ct.verifyRelatives(), True)
        ct2 = CoverTree(Euclidean())
        ct2.importFrom('sample.txt', False)
        self.assertEqual(ct2.verifyRelatives(), False)
        ct2.augmentRelatives();         
        self.assertEqual(ct2.verifyRelatives(), True)
        
    def test_findNode(self):
        ct = CoverTree(Euclidean())
        p = Point([0])
        n1 = ct.findNode(p, None, float('-inf'))[1]
        self.assertEqual(ct.levels[float('-inf')][p], n1)
        self.assertEqual(ct.tops[p], n1)
        n2 = ct.findNode(p, n1, 1)[1]
        self.assertEqual(ct.levels[1][p], n2)
        self.assertEqual(ct.tops[p], n2)
        n3 = ct.findNode(p, n2, 2)[1]
        self.assertEqual(ct.tops[p], n3)
        self.assertEqual(n3.child(), n1)
        self.assertEqual(n1.par, n3)
        p2 = Point([1])        
        n5 = ct.findNode(p2, None, 1)[1]
        n4 = ct.findNode(p2, n5, float('-inf'))[1]
        n5.attachParent(n3)        
        n2 = ct.findNode(p, n3, 1)[1]
        self.assertEqual(ct.tops[p], n3)
        self.assertEqual(ct.tops[p2], n5)
        self.assertSetEqual(set(n3.ch), {n5, n2})
        self.assertEqual(n2.par, n3)
        self.assertEqual(n2.child(), n1)
        n6 = ct.findNode(p, n3, 5)[1]
        self.assertEqual(n6.child(), n3)
        self.assertEqual(ct.tops[p], n6)
        n7 = ct.findNode(p, n6, 4)[1]
        self.assertEqual(n6.child(), n7)
        self.assertEqual(n7.par, n6)
        self.assertEqual(n7.child(), n3)
        self.assertSetEqual({item for item in ct.levels[1].values()}, {n2, n5})
    
    def test_bruteForceNN(self):
        ct = CoverTree(Euclidean())
        p1 = Point([0])
        p2 = Point([64])
        p3 = Point([17])
        p4 = Point([43])
        p5 = Point([26])
        p6 = Point([35])
        p7 = Point([30])
        p8 = Point([31])
        ct.insert(p1, None)
        n2 = ct.insert(p2, ct.root)
        n3 = ct.insert(p3, ct.root.child())
        n4 = ct.insert(p4, n2)
        n5 = ct.insert(p5, n3)
        n6 = ct.insert(p6, n4)
        n7 = ct.insert(p7, n5)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 5), ct.root.child())
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 4), n4)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 3), n5)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 2), n6)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 1), n7)
        self.assertEqual(ct.bruteForceNN(p8, n2, 1), n6)
        ct = CoverTree(Euclidean())
        p1 = Point([0])        
        p2 = Point([17])
        p3 = Point([19])
        p4 = Point([20])
        p5 = Point([43])
        p6 = Point([48])
        p7 = Point([64])
        ct.insert(p1, None)
        n7 = ct.insert(p7, ct.root)
        n2 = ct.insert(p2, ct.root.child())
        n3 = ct.insert(p3, n2)
        n4 = ct.insert(p4, n3)
        n6 = ct.insert(p6, n7)
        n5 = ct.insert(p5, n6)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, float('inf')), ct.root)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 5), ct.root.child())
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 4), n2)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 3), n2)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 2), n5)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 1), n5)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, 0), n3)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, -1), n4)
        self.assertEqual(ct.bruteForceNN(p8, ct.root, float('-inf')), n4.child())
        
    def test_restrictedNN(self):
        num, dim = 20, 2
        perm = CHeap([CPoint([random.randint(-1000, 1000) for d in range(dim)]) for i in range(num)], Euclidean()).makePerm()
        ct = CoverTree(Euclidean())
        ct.buildFromGP(perm)
        query = CPoint([random.randint(-1000, 1000) for d in range(dim)])
        self.assertEqual(ct.bruteForceNN(query, ct.root, float('-inf')), ct.restrictedNN(query, ct.root, float('-inf')))
        
    def test_coarsening(self):
        ct = CoverTree(Euclidean())
        p1 = Point([0])
        p2 = Point([64])
        p3 = Point([96])
        p4 = Point([112])
        p5 = Point([128])
        p6 = Point([512])
        p7 = Point([516])
        p8 = Point([518])
        p9 = Point([521])
        p10 = Point([545])
        p11 = Point([578])
        p12 = Point([768])
        p13 = Point([896])
        p14 = Point([998])
        p15 = Point([1000])
        p16 = Point([1024])
        ct.insert(p1, None)
        n16 = ct.insert(p16, ct.root)
        n6 = ct.insert(p6, ct.root.child())
        n5 = ct.insert(p5, ct.root.child().child())
        n2 = ct.insert(p2, n5.par.child())
        n3 = ct.insert(p3, n2)
        n4 = ct.insert(p4, n3)
        n11 = ct.insert(p11, n6)
        n10 = ct.insert(p10, n11)
        n9 = ct.insert(p9, n6.child().child())
        n7 = ct.insert(p7, n9.par.child())
        n8 = ct.insert(p8, n7)
        n12 = ct.insert(p12, n6)
        n13 = ct.insert(p13, n12)
        n15 = ct.insert(p15, n16)
        n14 = ct.insert(p14, n15)
        self.assertEqual(ct.verifyRelatives(), True)
        self.assertEqual(ct.isCoverTree(), True)
        self.assertEqual(ct.isNetTree(), False)
        ct2 = ct.coarsening(3)
        self.assertEqual(ct2.isCoverTree(), True)
        self.assertEqual(ct2.isNetTree(), True)
        self.assertSetEqual({v.point for v in ct2.levels[float('inf')].values()}, {p1})
        self.assertSetEqual({v.point for v in ct2.levels[3].values()}, {p1, p16})
        self.assertSetEqual({v.point for v in ct2.levels[2].values()}, {p1, p5, p6, p11, p12, p13, p16})
        self.assertSetEqual({v.point for v in ct2.levels[1].values()}, {p1, p2, p3, p4, p5, p6, p9, p10, p11, p15, p16})
        self.assertSetEqual({v.point for v in ct2.levels[0].values()}, {p6, p7, p8, p9, p14, p15})
        self.assertSetEqual({v.point for v in ct2.levels[float('-inf')].values()}, {p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16})
        
        num, dim = 20, 2
        perm = CHeap([CPoint([random.randint(-1000, 1000) for d in range(dim)]) for i in range(num)], Euclidean()).makePerm()
        ct3 = CoverTree(Euclidean())
        ct3.buildFromGP(perm)        
        self.assertEqual(ct3.verifyRelatives(), True)
        self.assertEqual(ct3.isCoverTree(), True)
        self.assertEqual(ct3.isNetTree(), False)
        ct4 = ct3.coarsening(3)
        self.assertEqual(ct4.isNetTree(), True)
        self.assertEqual(ct4.isCoverTree(), True)        
    
    def test_refining(self):
        p1 = Point([0])
        p2 = Point([32])
        p3 = Point([36])
        p4 = Point([38])
        p5 = Point([43])
        p6 = Point([65])
        p7 = Point([70])
        p8 = Point([72])
        p9 = Point([513])
        p10 = Point([515])
        p11 = Point([517])
        p12 = Point([520])
        ct = CoverTree(Euclidean(), 8)
        n1 = ct.insert(p1, None)
        n9 = ct.insert(p9, n1)
        n6 = ct.insert(p6, n1.child())
        n2 = ct.insert(p2, n1.child().child())
        n3 = ct.insert(p3, n2)        
        n5 = ct.insert(p5, n6)
        n4 = ct.insert(p4, n5)
        n7 = ct.insert(p7, n6.child())
        n8 = ct.insert(p8, n6.child())
        n10 = ct.insert(p10, n9)
        n11 = ct.insert(p11, n9.child())
        n12 = ct.insert(p12, n9.child())
        self.assertEqual(ct.verifyRelatives(), True)
        self.assertEqual(ct.isCoverTree(), True)
        self.assertEqual(ct.isNetTree(), True)
        ct2 = ct.refining(3)
        self.assertEqual(ct2.isCoverTree(), True)
        self.assertEqual(ct2.isNetTree(), False)
        self.assertSetEqual(set(ct2.root.ch), {Node(Point([0]), 9), Node(Point([513]), 9)})
        self.assertEqual(ct2.root.child().child(), Node(Point([0]), 7))
        self.assertSetEqual(set(ct2.levels[7][Point([0])].ch), {Node(Point([0]), 6), Node(Point([65]), 6)})
        self.assertEqual(ct2.levels[6][Point([0])].child(), Node(Point([0]), 5))
        self.assertSetEqual(set(ct2.levels[5][Point([0])].ch), {Node(Point([0]), 4), Node(Point([32]), 4)})
        self.assertSetEqual(set(ct2.levels[4][Point([32])].ch), {Node(Point([32]), 3), Node(Point([43]), 3)})
        self.assertEqual(ct2.levels[3][Point([32])].child(), Node(Point([32]), float('-inf')))
        self.assertSetEqual(set(ct2.levels[3][Point([43])].ch), {Node(Point([43]), 2), Node(Point([38]), 2)})
        self.assertEqual(ct2.levels[2][Point([43])].child(), Node(Point([43]), float('-inf')))
        self.assertEqual(ct2.levels[2][Point([38])].child(), Node(Point([38]), 1))
        self.assertSetEqual(set(ct2.levels[1][Point([38])].ch), {Node(Point([36]), 0), Node(Point([38]), 0)})
        self.assertEqual(ct2.levels[0][Point([36])].child(), Node(Point([36]), float('-inf')))
        self.assertEqual(ct2.levels[0][Point([38])].child(), Node(Point([38]), float('-inf')))
        self.assertEqual(ct2.levels[6][Point([65])].child(), Node(Point([65]), 3))
        self.assertEqual(ct2.levels[2][Point([65])].child(), Node(Point([65]), float('-inf')))
        if ct2.levels[3][Point([65])].ch[1].point.pt == [70]:
            self.assertSetEqual(set(ct2.levels[3][Point([65])].ch), {Node(Point([65]), 2), Node(Point([70]), 2)})
            self.assertEqual(ct2.levels[2][Point([70])].child(), Node(Point([70]), 1))
            self.assertSetEqual(set(ct2.levels[1][Point([70])].ch), {Node(Point([70]), 0), Node(Point([72]), 0)})
        else:
            self.assertSetEqual(set(ct2.levels[3][Point([65])].ch), {Node(Point([65]), 2), Node(Point([72]), 2)})
            self.assertEqual(ct2.levels[2][Point([72])].child(), Node(Point([72]), 1))
            self.assertSetEqual(set(ct2.levels[1][Point([72])].ch), {Node(Point([70]), 0), Node(Point([72]), 0)})
        self.assertEqual(ct2.root.ch[1].child(), Node(Point([513]), 3))
        self.assertSetEqual(set(ct2.levels[3][Point([513])].ch), {Node(Point([513]), 2), Node(Point([520]), 2)})
        self.assertEqual(ct2.levels[2][Point([513])].child(), Node(Point([513]), 1))
        self.assertSetEqual(set(ct2.levels[1][Point([513])].ch), {Node(Point([513]), 0), Node(Point([515]), 0)})
        self.assertSetEqual(set(ct2.levels[2][Point([520])].ch), {Node(Point([517]), 1), Node(Point([520]), 1)})
        
        num, dim = 20, 2
        perm = CHeap([CPoint([random.randint(-1000, 1000) for d in range(dim)]) for i in range(num)], Euclidean()).makePerm()
        ct3 = CoverTree(Euclidean(), 16)
        ct3.buildFromGP(perm)
        self.assertEqual(ct3.verifyRelatives(), True)
        self.assertEqual(ct3.isNetTree(), True)
        self.assertEqual(ct3.isCoverTree(), True)
        ct4 = ct3.refining(2)
        self.assertEqual(ct4.isCoverTree(), True)
        self.assertEqual(ct4.isNetTree(), True)
        
    def test_dynamicInsert(self):
        p1 = Point([0])
        p2 = Point([32])
        p3 = Point([63])
        p4 = Point([2])
        p5 = Point([56])
        p6 = Point([70])
        p7 = Point([50])
        p8 = Point([256])
        ct = CoverTree(Euclidean())
        ct.dynamicInsert(p1)
        ct.dynamicInsert(p2)
        ct.dynamicInsert(p3)
        ct.dynamicInsert(p4)
        ct.dynamicInsert(p5)
        ct.dynamicInsert(p6)
        ct.dynamicInsert(p7)
        ct.dynamicInsert(p8)
        self.assertEqual(ct.isCoverTree(), True)
        self.assertEqual(ct.verifyRelatives(), True)
        
        num, dim = 50, 2
        ct2 = CoverTree(Euclidean(), 2)
        for i in range(num):
            ct2.dynamicInsert(Point([random.randint(-1000, 1000) for d in range(dim)]))
        self.assertEqual(ct2.verifyRelatives(), True)
        self.assertEqual(ct2.isCoverTree(), True)
        
    def test_dynamicInsert2(self):
        ct = CoverTree(Euclidean())
        ct.dynamicInsert2(Point([0]))
        ct.dynamicInsert2(Point([50]))
        ct.dynamicInsert2(Point([25]))
        ct.dynamicInsert2(Point([38]))
        ct.dynamicInsert2(Point([45]))
        ct.dynamicInsert2(Point([41]))
        ct.dynamicInsert2(Point([31]))
        ct.dynamicInsert2(Point([60]))
        ct.dynamicInsert2(Point([256]))
        self.assertEqual(ct.isCoverTree(), True)
        self.assertEqual(ct.verifyRelatives(), True)
        
        num, dim = 20, 2
        ct2 = CoverTree(Euclidean(), 4)
        for i in range(num):
            ct2.dynamicInsert2(Point([random.randint(-1000, 1000) for d in range(dim)]))
        self.assertEqual(ct2.isNetTree(), True)
        self.assertEqual(ct2.verifyRelatives(), True)
        self.assertEqual(ct2.isCoverTree(), True)
    
    def test_importFrom(self):
        p1 = Point([0])
        p2 = Point([32])
        p3 = Point([16])
        p4 = Point([4])
        ct = CoverTree(Euclidean())
        ct.importFrom(self.ct1)
        self.assertSetEqual({v.point for v in ct.levels[float('inf')].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[4].values()}, {p1, p2})
        self.assertSetEqual({v.point for v in ct.levels[3].values()}, {p2, p3})
        self.assertSetEqual({v.point for v in ct.levels[2].values()}, {p1})
        self.assertSetEqual({v.point for v in ct.levels[1].values()}, {p1, p4})
        self.assertSetEqual({v.point for v in ct.levels[float('-inf')].values()}, {p1, p2, p3, p4})
        self.assertEqual(ct.verifyRelatives(), True)
        self.assertEqual(ct.isCoverTree(), True)
        
    def test_exportTo(self):
        ct1 = CoverTree(Euclidean())
        p1 = Point([0, 0, 0])
        p2 = Point([32, 0, 0])
        p3 = Point([16, 0, 0])
        p4 = Point([4, 0, 0])
        root = ct1.insert(p1, None)
        n2 = ct1.insert(p2, root)
        ct1.insert(p3, n2)
        ct1.insert(p4, root.child())
        outfile = 'output.txt'
        ct1.exportTo(outfile)
        ct2 = CoverTree(Euclidean())
        ct2.importFrom(outfile)
        self.assertSetEqual({v.point for v in ct1.levels[float('inf')].values()}, {v.point for v in ct2.levels[float('inf')].values()})
        self.assertSetEqual({v.point for v in ct1.levels[4].values()}, {v.point for v in ct2.levels[4].values()})
        self.assertSetEqual({v.point for v in ct1.levels[3].values()}, {v.point for v in ct2.levels[3].values()})
        self.assertSetEqual({v.point for v in ct1.levels[2].values()}, {v.point for v in ct2.levels[2].values()})
        self.assertSetEqual({v.point for v in ct1.levels[1].values()}, {v.point for v in ct2.levels[1].values()})
        self.assertSetEqual({v.point for v in ct1.levels[float('-inf')].values()}, {v.point for v in ct2.levels[float('-inf')].values()})
        try: os.remove('output.txt')
        except OSError: pass
            
    def test_uncompressLevels(self):
        ct = CoverTree(Euclidean())
        ct.importFrom(self.ct1)
        ulevels = ct.uncompressLevels()
        self.assertSetEqual(set(ulevels[float('inf')]), {Node(Point([0]), float('inf'))})
        self.assertSetEqual(set(ulevels[4]), {Node(Point([0]), 4), Node(Point([32]), 4)})
        self.assertSetEqual(set(ulevels[3]), {Node(Point([0]), 4), Node(Point([32]), 3), Node(Point([16]), 3)})
        self.assertSetEqual(set(ulevels[2]), {Node(Point([0]), 2), Node(Point([32]), 3), Node(Point([16]), 3)})
        self.assertSetEqual(set(ulevels[1]), {Node(Point([0]), 1), Node(Point([32]), 3), Node(Point([16]), 3), Node(Point([4]), 1)})
        self.assertSetEqual(set(ulevels[float('-inf')]), {Node(Point([0]), float('-inf')), Node(Point([4]), float('-inf')), Node(Point([16]), float('-inf')), Node(Point([32]), float('-inf'))})
    
    def test_isCoverTree(self):
        ct = CoverTree(Euclidean())
        ct.importFrom(self.ct1)
        self.assertEqual(ct.isCoverTree(), True)
        ct2 = CoverTree(Euclidean())
        ct2.importFrom(self.ctwithoutparentcondition)
        self.assertEqual(ct2.isCoverTree(), False)
        self.assertEqual(ct2.isCoverTree(False), True)
    
    def test_isNetTree(self):
        ct = CoverTree(Euclidean())
        ct.importFrom(self.ct1)
        self.assertEqual(ct.isNetTree(), False)
        perm = CHeap([CPoint([2 ** i]) for i in range(15)], Euclidean()).makePerm()
        ct2 = CoverTree(Euclidean(), 4)
        ct2.buildFromGP(perm)
        self.assertEqual(ct2.isNetTree(), True)
        dim = 2
        num = 50
        perm = CHeap([CPoint([random.randint(-1000, 1000) for d in range(dim)]) for i in range(num)], Euclidean()).makePerm()
        ct3 = CoverTree(Euclidean(), 4)
        ct3.buildFromGP(perm)
        self.assertEqual(ct3.isNetTree(), True)
        self.assertEqual(ct3.isCoverTree(), True)
        
    def test_verifyRelatives(self):
        ct = CoverTree(Euclidean())
        ct.importFrom(self.ct1)
        self.assertEqual(ct.verifyRelatives(), True)
        rels = ct.root.ch[1].ch[1].rel
        elem = ct.root.child().child()
        self.assertIn(elem, rels)
        rels.remove(elem)
        self.assertNotIn(elem, rels)
        self.assertEqual(ct.verifyRelatives(), False)

if __name__ == "__main__":
    unittest.main()