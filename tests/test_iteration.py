# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:36:51 2013

@author: user
"""
import pdb
try:
    from .. import iteration
    from .. import dectools
except ValueError:
    try:
        import iteration
        import dectools
        print 'Running from within cloudtb'
    except:
        import sys
        sys.path.insert(1, '..')
        import iteration
        import dectools
        print 'Running as outside module'

import unittest
import random

def get_ranges(number):
        return (range(n, n + 100) for n in range(number))

@dectools.pdb_on_exception
def test_basic(self):
    a1 = xrange(0, 100)
    self.assertIterEqual(a1, self.get_object(a1))

@dectools.pdb_on_exception
def test_add(self):
    a1, a2 = get_ranges(2)
    self.assertIterEqual(a1 + a2, self.get_object(a1) 
        + self.get_object(a2))

@dectools.pdb_on_exception
def test_extend(self):
    a1, a2 = get_ranges(2)
    b1 = self.get_object(a1)
    
    a1.extend(a2)    
    b1.front_extend(a2)
    self.assertIterEqual(a1, b1)

@dectools.pdb_on_exception
def test_extend_front(self):
    a1, a2 = get_ranges(2)
    b1 = self.get_object(a1)
    b1.front_extend(a2)
    self.assertIterEqual(a2 + a1, b1)

@dectools.pdb_on_exception
def test_slice(self, recreate = True):
    a1 = range(-100, 1000)
    b1 = self.get_object(a1)
    
    b1[100]
    start, stop, step = 0, None, 5
    self.assertIterEqual(a1[start:stop:step],
                     b1[start:stop:step])
    
    start = 100
    if recreate: b1 = self.get_object(a1)
    print type(b1)
    self.assertIterEqual(a1[start:stop:step],
                     b1[start:stop:step])
    
    stop = 450
    if recreate: b1 = self.get_object(a1)
    self.assertIterEqual(a1[start:stop:step],
                     b1[start:stop:step])

    step = 1
    if recreate: b1 = self.get_object(a1)
    self.assertIterEqual(a1[start:stop:step],
                     b1[start:stop:step])

@dectools.pdb_on_exception
def test_slice_repeat(self, reobject = False):
    st, end = 100, 1233
    a1 = range(st, end)
    b1 = self.get_object(a1)
    start, stop, step = 0, end, 5
    a1 = a1[start:stop:step]
    b1 = b1[start:stop:step]
    
    if reobject:
        b1 = self.get_object(b1)
    
    start, stop, step = 0, end / 10, 12
    a1 = a1[start:stop:step]
    b1 = b1[start:stop:step]
    self.assertIterEqual(a1, b1)

@dectools.pdb_on_exception
def test_getitem(self, recreate = True):
    a1 = range(-100, 1000)
    b1 = self.get_object(a1)
    for index in xrange(100, 1000, 33):
        if recreate:
            b1 = self.get_object(a1)
        self.assertEqual(a1[index], b1[index])

class std_iterator(object):
    def test_basic(self):
        return test_basic(self)
#    def test_add(self):
#        return test_add(self)
    def test_extend(self):
        return test_extend(self)
    def test_extend_front(self):
        return test_extend_front(self)
    def test_slice(self):
        return test_slice(self)
    def test_slice_repeat(self):
        return test_slice_repeat(self)
    def test_getitem(self):
        return test_getitem(self)
    def assertIterEqual(self, iter1, iter2):
        iter1, iter2 = iter(iter1), iter(iter2)
        try:
            next(next(iter1) != n for n in iter2)
        except StopIteration:
            self.fail()
        
class bitterTest(unittest.TestCase, std_iterator):
    def get_object(self, *args, **kwargs):
        return iteration.biter(*args, **kwargs)

    def test_slice_repeat(self):
        return test_slice_repeat(self, reobject = True)
    

class soliditerTest(unittest.TestCase, std_iterator):
    def get_object(self, *args, **kwargs):
        return iteration.soliditer(*args, **kwargs)
    
    def test_getitem(self):
#        pdb.set_trace()
        return test_getitem(self, recreate = False)
    
if __name__ == '__main__':
    unittest.main()        