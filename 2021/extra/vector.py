#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Vector Module

"Vector module"

# Programmed by CoolCat467

__title__ = 'Vector'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0


import math
from functools import wraps

def vmathop(function):
    "Vector math operator decorator"
    @wraps(function)
    def wrapped_op(self, rhs, *args, **kwargs):
        if hasattr(rhs, '__len__'):
            if len(rhs) == len(self):
                return function(self, rhs, *args, **kwargs)
            raise TypeError('Right hand side operator length is not same as own')
##        return function(self, [rhs]*len(self), *args, **kwargs)
        raise AttributeError('Right hand side operator has no length attribute')
    return wrapped_op

def simpleop(function):
    "Return new `self` class instance built from application of function on items of self and rhs."
    def apply(values):
        return function(*values)
    def operator(self, rhs):
        return self.__class__(*map(apply, zip(self, rhs)))
    return operator

def onlylen(length):
    "Return wrapper that only runs function if length matches length."
    def wrapper(function):
        @wraps(function)
        def wrapped_func(self, *args, **kwargs):
            if len(self) == length:
                return function(self, *args, **kwargs)
            raise TypeError(f'Vector is not a {length}d vector!')
        return wrapped_func
    return wrapper

##def vmagop(function):
##    def operator(self, rhs):
####        if hasattr(rhs, '__iter__'):
####            return function(self.magnitude, self.from_iter(rhs).magnitude)
##        return function(self.magnitude, rhs)
##    return operator

class Vector:
    "Vector Object. Takes n arguments as input and creates n length vector, or type length vector."
    __slots__ = ('_v',)
    def __init__(self, *args, type_=None):
        if type_ is None:
            self._v = tuple(args)
        else:
            args = args[:type_]
            self._v = tuple(list(args) + [0]*(type_-len(args)))
    
    def __repr__(self):
        args = ', '.join(map(str, self._v))
        return f'{self.__class__.__name__}({args})'
    
    def __len__(self):
        return len(self._v)
    
    def __iter__(self):
        return iter(self._v)
    
    def __getitem__(self, index):
        try:
            return self._v[index]
        except IndexError:
            raise IndexError('Index out of range for this vector')
    
    @classmethod
    def from_iter(cls, iterable, type_=None):
        "Return Vector from iterable."
        return cls(*iterable, type_=type_)
    
    @property
    def magnitude(self):
        "Magnitude of this vector"
        return math.sqrt(sum(map(lambda x: math.pow(x, 2), self._v)))
    
    def copy(self):
        "Return a copy of this vector"
        return Vector(*self._v)
    
    def normalize(self):
        "Normalize this vector."
        mag = self.magnitude
        self._v = tuple(map(lambda x:x/mag, self._v))
        return self
        
    @classmethod
    def is_instance(cls, obj):
        "Return True if obj is instance of this class."
        return isinstance(obj, cls)
    
    def __neg__(self):
        "Return negated vector"
        return self.__class__(*[-x for x in self._v])
    
    def __abs__(self):
        "Return abs'd vector"
        return self.__class__(*[abs(x) for x in self._v])
    
    def __round__(self):
        return self.__class__(*[round(x) for x in self._v])
    
    @vmathop
    @simpleop
    def __add__(x, y):
        "Add two vectors or iterables"
        return x + y
    
    @vmathop
    @simpleop
    def __sub__(x, y):
        "Subtract two vectors or iterables"
        return x - y
    
    @vmathop
    @simpleop
    def __mul__(x, y):
        "Multiply two vectors or iterables"
        return x * y
    
    @vmathop
    @simpleop
    def __truediv__(x, y):
        "Divide two vectors or iterables"
        return x / y
    
    def __gt__(self, rhs):
        if hasattr(rhs, '__iter__'):
            for x, y in zip(self, rhs):
                if not x > y:
                    return False
            return True
##            return self.magnitude > self.from_iter(rhs).magnitude
            raise TypeError('Cannot compare iterables')
        return all(map(lambda x:x>rhs, self))
    
    def __ge__(self, rhs):
        if hasattr(rhs, '__iter__'):
            for x, y in zip(self, rhs):
                if not x >= y:
                    return False
            return True
##            return self.magnitude > self.from_iter(rhs).magnitude
            raise TypeError('Cannot compare iterables')
        return all(map(lambda x:x>=rhs, self))
    
    def __lt__(self, rhs):
        if hasattr(rhs, '__iter__'):
##            return self.magnitude > self.from_iter(rhs).magnitude
            raise TypeError('Cannot compare iterables')
        return all(map(lambda x:x<rhs, self))
    def __eq__(self, rhs):
        return tuple(self) == tuple(rhs)
##    
##    def __ne__(self, rhs):
##        return list(self) != rhs
    
##    @vmagop
##    def __gt__(x, y):
##        return x > y
##    
##    @vmagop
##    def __ge__(x, y):
##        return x >= y
##    
##    @vmagop
##    def __lt__(x, y):
##        return x < y
##    
##    @vmagop
##    def __le__(x, y):
##        return x <= y
    
    def __hash__(self):
        return hash(self._v)
    
    def set_length(self, new_length):
        "Set length of this vector by normalizing it and then scaleing it."
        mag = new_length / self.magnitude
        self._v = (self * ([mag]*len(self)))._v
    
    @onlylen(3)
    @vmathop
    def cross(self, other):
        "Returns the cross product of this vector with another IF both are 3d vectors"
        x, y, z = self
        bx, by, bz = other
        return self.__class__( y*bz - by*z,
                               z*bx - bz*x,
                               x*by - bx*y)
    
    @onlylen(2)
    def get_heading(self):
        "Returns the arc tangent (mesured in radians) of self.y/self.x."
        x, y = self
        return math.atan2(y, x)


def run():
    pass





if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
