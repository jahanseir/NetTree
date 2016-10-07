import unittest
from node import Node
from point import Point
from metrics import *

class TestNode(unittest.TestCase):
    def test_init(self):
        p = Point([3, 4])        
        n = Node(p)
        self.assertEqual(n.point, p)
        self.assertEqual(n.level, None)
        n = Node(p, 10)
        self.assertEqual(n.level, 10)
        self.assertEqual(n.rel, [n])
        
    def test_attachChild(self):
        ch = Node(Point([3, 4]), 9)
        ch2 = Node(Point([6, 7]), 9)
        ch3 = Node(Point([1, 2]), 9)
        ch4 = Node(Point([1, 9]), 10)
        par = Node(Point([1, 2]), 10).attachChild(ch)
        root = Node(Point([1, 2]), 11).attachChild(par).attachChild(ch4)
        self.assertEqual(par.ch[0], ch)
        self.assertEqual(ch.par, par)
        par.attachChild(par)            
        self.assertEqual(len(par.ch), 1)
        par.attachChild(ch3)
        self.assertEqual(par.ch[0], ch3)
        par.attachChild(ch)
        self.assertEqual(len(par.ch), 2)
        par.attachChild(ch2)
        self.assertEqual(par.ch[2], ch2)
          
    def test_detachChild(self):
        ch = Node(Point([3, 4]), 9)
        ch2 = Node(Point([6, 7]), 9)
        ch3 = Node(Point([1, 2]), 9)
        ch4 = Node(Point([1, 9]), 10)
        par = Node(Point([1, 2]), 10).attachChild(ch).attachChild(ch2).attachChild(ch3)
        root = Node(Point([1, 2]), 11).attachChild(par).attachChild(ch4)
        par.detachChild(ch)
        self.assertEqual(par.ch[0], ch3)
        self.assertEqual(ch.par, None)
        par.detachChild(par)
        self.assertSetEqual(set(par.ch), {ch2, ch3})
                   
    def test_attachParent(self):        
        root = Node(Point([1, 2]), 11)
        par = Node(Point([1, 2]), 10).attachParent(root)
        ch = Node(Point([3, 4]), 9).attachParent(par)
        ch2 = Node(Point([6, 7]), 9).attachParent(par)
        ch3 = Node(Point([1, 2]), 9).attachParent(par)
        ch4 = Node(Point([1, 9]), 10).attachParent(root)
        self.assertSetEqual(set(root.ch), {par, ch4})
        self.assertSetEqual(set(par.ch), {ch, ch2, ch3})
        self.assertEqual(ch.par, par)
        self.assertEqual(ch2.par, par)
        self.assertEqual(ch3.par, par)
        self.assertEqual(par.par, root)
        self.assertEqual(ch4.par, root)
        par.attachParent(par)
        self.assertEqual(par.par, root)
        
    def test_detachParent(self):        
        root = Node(Point([0]), 11)
        n1 = Node(Point([0]), 10).attachParent(root)
        n2 = Node(Point([0]), 9).attachParent(n1)
        n3 = Node(Point([0]), 8).attachParent(n2)
        n4 = Node(Point([0]), 7).attachParent(n3)
        n5 = Node(Point([1]), 10).attachParent(root)
        n6 = Node(Point([2]), 9).attachParent(n1)
        n7 = Node(Point([3]), 9).attachParent(n1)
        n8 = Node(Point([4]), 8).attachParent(n2)
        n9 = Node(Point([5]), 8).attachParent(n2)
        n10 = Node(Point([6]), 7).attachParent(n3)
        n4.detachParent()
        self.assertEqual(n4.par, None)
        self.assertListEqual(n3.ch, [n10])
        n3.detachParent()
        self.assertEqual(n3.par, None)
        self.assertSetEqual(set(n2.ch), {n8, n9})
        n1.detachParent()
        self.assertEqual(n1.par, None)
        self.assertListEqual(root.ch, [n5])      
        
    def test_findLeaves(self):
        root = Node(Point([0]), 11)
        n1 = Node(Point([0]), 10).attachParent(root)
        n2 = Node(Point([0]), 9).attachParent(n1)
        n3 = Node(Point([0]), 8).attachParent(n2)
        n4 = Node(Point([0]), 7).attachParent(n3)
        n5 = Node(Point([1]), 10).attachParent(root)
        n6 = Node(Point([2]), 9).attachParent(n1)
        n7 = Node(Point([3]), 9).attachParent(n1)
        n8 = Node(Point([4]), 8).attachParent(n2)
        n9 = Node(Point([5]), 8).attachParent(n2)
        n10 = Node(Point([6]), 7).attachParent(n3)
        root.findLeaves()
        self.assertSetEqual(root.leaves, {Point([0]), Point([1]), Point([2]), Point([3]), Point([4]), Point([5]), Point([6])})
        self.assertSetEqual(n1.leaves, {Point([0]), Point([2]), Point([3]), Point([4]), Point([5]), Point([6])})
        self.assertSetEqual(n2.leaves, {Point([0]), Point([4]), Point([5]), Point([6])})
        self.assertSetEqual(n3.leaves, {Point([0]), Point([6])})
        self.assertSetEqual(n4.leaves, {Point([0])})
        self.assertEqual(root.verifyLeaves()[1], True)
        
    def test_child(self):
        par = Node(Point([1, 2]), 10)
        ch = Node(Point([3, 4]), 9).attachParent(par)
        self.assertEqual(par.child(), ch)
        self.assertEqual(ch.child(), None)
        
    def test_dist(self):
        n1 = Node(Point([1, 2]), 10)
        n2 = Node(Point([4, 6]), 9)
        n3 = Node(Point([7, 9]), 9)
        n4 = Node(Point([7, 10]), 9)
        self.assertEqual(n1.dist(Euclidean(), n2)[0], 5)
        self.assertEqual(n4.dist(Euclidean(), n1, n2), (5, n2))
        self.assertEqual(n4.dist(Euclidean(), n1, n2, n3), (1, n3))
        self.assertEqual(n4.dist(Euclidean(), n1, n2, n3, n4), (0, n4))
        self.assertEqual(n4.dist(Euclidean(), *{n1, n2, n3, n4}), (0, n4))

if __name__ == "__main__":
    unittest.main()
