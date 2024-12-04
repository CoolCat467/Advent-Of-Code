#!/usr/bin/env python3  # noqa: EXE001
# Vector Module

"Vector module."  # noqa: D300

# Programmed by CoolCat467

__title__ = "Vector"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import math
from functools import wraps


def vmathop(function):
    "Vector math operator decorator."  # noqa: D300

    @wraps(function)
    def wrapped_op(self, rhs, *args, **kwargs):
        if hasattr(rhs, "__len__"):
            if len(rhs) == len(self):
                return function(self, rhs, *args, **kwargs)
            raise TypeError("Operand length is not same as own")
        return function(self, [rhs] * len(self), *args, **kwargs)

    ##        raise AttributeError('Operand has no length attribute')
    return wrapped_op


def simpleop(function):
    "Return new `self` class instance built from application of function on items of self and rhs."  # noqa: D300

    def apply(values):
        return function(*values)

    @wraps(function)
    def operator(self, rhs):
        return self.__class__(
            *map(apply, zip(self, rhs, strict=False)),
            dtype=self.dtype,
        )

    return operator


def onlylen(length):
    "Return wrapper that only runs function if length matches length."  # noqa: D300

    def wrapper(function):
        @wraps(function)
        def wrapped_func(self, *args, **kwargs):
            if len(self) == length:
                return function(self, *args, **kwargs)
            raise TypeError(f"Vector is not a {length}d vector!")

        return wrapped_func

    return wrapper


##def vmagop(function):
##    def operator(self, rhs):
####        if hasattr(rhs, '__iter__'):
####            return function(self.magnitude, self.from_iter(rhs).magnitude)
##        return function(self.magnitude, rhs)
##    return operator


class Vector:
    """Vector Object. Takes n arguments as input and creates n length vector, or type length vector.
    dtype argument changes internal data type.
    """  # noqa: D205

    __slots__ = ("__v", "dtype")

    def __init__(self, *args, dims=None, dtype=tuple):  # noqa: D107
        self.dtype = dtype
        if not hasattr(dtype, "__getitem__"):
            raise TypeError("Data type class is not subscriptable!")
        if dims is None:
            ##            self.__v = tuple(args)
            self.__v = self.dtype(args)
        else:
            args = args[:dims]
            ##            self.__v = tuple(list(args) + [0]*(dims-len(args)))
            self.__v = self.dtype(list(args) + [0] * (dims - len(args)))

    def __repr__(self):  # noqa: D105
        args = ", ".join(map(repr, self.__v))
        return f"{self.__class__.__name__}({args})"

    def __len__(self):  # noqa: D105
        return len(self.__v)

    def __iter__(self):  # noqa: D105
        return iter(self.__v)

    def __getitem__(self, index):  # noqa: D105
        if not isinstance(index, int):
            raise TypeError("Index is not an integer.")
        if index > len(self):
            raise IndexError("Index out of range for this vector")
        ##        if isinstance(index, str):
        ##            index = ord(index.upper())-88
        return self.__v[index]

    def __setitem__(self, index, value):  # noqa: D105
        if not hasattr(self.__v, "__setitem__"):
            dtype = self.dtype.__name__
            raise TypeError(
                f"'{dtype}' does not support item assignment. Change vector dtype.",
            )
        if not isinstance(index, int):
            raise TypeError("Index is not an integer.")
        if index > len(self):
            raise IndexError("Index out of range for this vector")
        self.__v[index] = value

    @classmethod
    def from_iter(cls, iterable, dims=None, dtype=tuple):
        "Return Vector from iterable."  # noqa: D300
        return cls(*iterable, dims=dims, dtype=dtype)

    @classmethod
    def from_radians(cls, radians):
        "Return 2d unit vector from measure in radians."  # noqa: D300
        return cls(math.cos(radians), math.sin(radians))

    @property
    def magnitude(self):
        "Magnitude of this vector."  # noqa: D300
        ##        return math.sqrt(sum(self ** 2))
        return math.hypot(*self.__v)

    def copy(self):
        "Return a copy of this vector."  # noqa: D300
        return self.from_iter(self.__v, dtype=self.dtype)

    def reverse(self):
        "Return a copy of self, but order of elements is reversed."  # noqa: D300
        return self.from_iter(reversed(self))

    def normalize(self):
        "Normalize this vector."  # noqa: D300
        mag = self.magnitude
        ##        self.__v = tuple(map(lambda x:x/mag, self.__v))
        self.__v = self.dtype(x / mag for x in self.__v)
        ##        self.__v = list(map(lambda x:x/mag, self.__v))
        return self

    def normalized(self):
        "Return normalized vector."  # noqa: D300
        mag = self.magnitude
        return self / mag

    def __neg__(self):
        "Return negated vector."  # noqa: D300
        return self.from_iter(-x for x in self.__v)

    def __pos__(self):
        "Return unary positive of self."  # noqa: D300
        return self.from_iter(+x for x in self.__v)

    def __abs__(self):
        "Return abs'd vector."  # noqa: D300
        return self.from_iter(abs(x) for x in self.__v)

    def __round__(self):
        "Return vector but each element is rounded."  # noqa: D300
        return self.from_iter(round(x) for x in self.__v)

    def __bool__(self):
        "Return True if any element is true, False otherwise."  # noqa: D300
        return any(self.__v)

    @vmathop
    @simpleop
    def __add__(self, rhs):
        "Add two vectors/iterables or add number to each element."  # noqa: D300
        return self + rhs

    __radd__ = __add__

    @vmathop
    @simpleop
    def __sub__(self, rhs):
        "Subtract two vectors/iterables or subtract number from each element."  # noqa: D300
        return self - rhs

    @vmathop
    @simpleop
    def __rsub__(self, lhs):
        "Subtract but from left hand side."  # noqa: D300
        return lhs - self

    @vmathop
    @simpleop
    def __mul__(self, rhs):
        "Multiply two vectors/iterables or multiply each element by number."  # noqa: D300
        return self * rhs

    __rmul__ = __mul__

    @vmathop
    @simpleop
    def __truediv__(self, rhs):
        "Divide two vectors/iterables or divide each element by number."  # noqa: D300
        return self / rhs

    @vmathop
    @simpleop
    def __rtruediv__(self, lhs):
        "Division but from left hand side."  # noqa: D300
        return lhs / self

    @vmathop
    @simpleop
    def __pow__(self, rhs):
        "Get element to the power of number or matching item in vector/iterable for each element."  # noqa: D300
        return self**rhs

    @vmathop
    @simpleop
    def __rpow__(self, lhs):
        "Power, but from left hand side."  # noqa: D300
        return lhs**self

    def __eq__(self, rhs):  # noqa: D105
        return self.__v == rhs

    def __ne__(self, rhs):  # noqa: D105
        return self.__v != rhs

    ##    @vmagop
    ##    def __gt__(x, y):
    ##        return x > y
    ##
    ##    @vmagop
    ##    def _ge__(x, y):
    ##        return x >= y
    ##
    ##    @vmagop
    ##    def __lt__(x, y):
    ##        return x < y
    ##
    ##    @vmagop
    ##    def __le__(x, y):
    ##        return x <= y

    def __hash__(self):  # noqa: D105
        return hash(self.__v)

    def set_length(self, new_length):
        "Set length of this vector by normalizing it and then scaling it."  # noqa: D300
        mag = new_length / self.magnitude
        ##        self.__v = (self * ([mag]*len(self))).__v
        return self * (mag * len(self))

    @onlylen(3)
    @vmathop
    def cross(self, other):
        "Returns the cross product of this vector with another IF both are 3d vectors."  # noqa: D300, D401
        # pylint: disable=C0103
        x, y, z = self
        bx, by, bz = other
        return self.__class__(
            y * bz - by * z,
            z * bx - bz * x,
            x * by - bx * y,
        )

    def dot(self, other):
        "Return the dot product of this vector with another."  # noqa: D300
        ##        return sum(self * other)
        return math.fsum(self * other)

    @onlylen(2)
    def get_heading(self):
        "Returns the arc tangent (measured in radians) of self.y/self.x."  # noqa: D300, D401
        # pylint: disable=C0103
        x, y = self
        return math.atan2(y, x)


class Vector1(Vector):
    "Vector1. Same as Vector, but stuck being 1d and has x attribute."  # noqa: D300

    def __init__(self, x=0, **kwargs):  # noqa: D107
        ##        kwargs['dims'] = 1
        if "dtype" not in kwargs:
            kwargs["dtype"] = list
        super().__init__(x, **kwargs)

    @classmethod
    def from_iter(cls, iterable, dtype=list):
        "Return Vector2 from iterable."  # noqa: D300
        nxt = iter(iterable).__next__
        return cls(nxt(), dtype=dtype)

    def _get_x(self):
        return self[0]

    def _set_x(self, value):
        self[0] = value

    x = property(_get_x, _set_x, doc="X component")


class Vector2(Vector1):
    "Vector2. Same as Vector, but stuck being 2d and has x and y attributes."  # noqa: D300

    def __init__(self, x=0, y=0, **kwargs):  # noqa: D107
        ##        kwargs['dims'] = 2
        if "dtype" not in kwargs:
            kwargs["dtype"] = list
        Vector.__init__(self, x, y, **kwargs)

    @classmethod
    def from_iter(cls, iterable, dtype=list):
        "Return Vector2 from iterable."  # noqa: D300
        nxt = iter(iterable).__next__
        return cls(nxt(), nxt(), dtype=dtype)

    def _get_y(self):
        return self[1]

    def _set_y(self, value):
        self[1] = value

    y = property(_get_y, _set_y, doc="Y component")


class Vector3(Vector2):
    "Vector3. Same as Vector, but stuck being 3d and has x, y, and z attributes."  # noqa: D300

    def __init__(self, x=0, y=0, z=0, **kwargs):  # noqa: D107
        ##        kwargs['dims'] = 3
        if "dtype" not in kwargs:
            kwargs["dtype"] = list
        Vector.__init__(self, x, y, z, **kwargs)

    @classmethod
    def from_iter(cls, iterable, dtype=list):
        "Return Vector2 from iterable."  # noqa: D300
        nxt = iter(iterable).__next__
        return cls(nxt(), nxt(), nxt(), dtype=dtype)

    def _get_z(self):
        return self[2]

    def _set_z(self, value):
        self[2] = value

    z = property(_get_z, _set_z, doc="Z component")


class Vector4(Vector3):
    "Vector4. Same as Vector, but stuck being 4d and has x, y, z, and w attributes."  # noqa: D300

    def __init__(self, x=0, y=0, z=0, w=0, **kwargs):  # noqa: D107
        ##        kwargs['dims'] = 4
        if "dtype" not in kwargs:
            kwargs["dtype"] = list
        Vector.__init__(self, x, y, z, w, **kwargs)

    @classmethod
    def from_iter(cls, iterable, dtype=list):
        "Return Vector2 from iterable."  # noqa: D300
        nxt = iter(iterable).__next__
        return cls(nxt(), nxt(), nxt(), nxt(), dtype=dtype)

    def _get_w(self):
        return self[3]

    def _set_w(self, value):
        self[3] = value

    w = property(_get_w, _set_w, doc="W component")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
