# -*- coding: utf-8 -*-

# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Print a tree of classes in a module."""

from __future__ import print_function, unicode_literals

import functools
import importlib
import operator
import sys


def mrotree(cls, matchfunc=None):
    """Return a tree of cls, its subclasses, their subclasses and so on.

    If matchfunc is not None, only add classes to the tree if
    matchfunc(cls) is true.
    """
    result = {}
    # cls.__subclasses__() doesn't work if cls is type.
    subclasses = type.__subclasses__(cls)
    subclasses.sort(key=operator.attrgetter('__name__'))
    for subclass in subclasses:
        if matchfunc(subclass):
            name = subclass.__name__
            result[name] = mrotree(subclass, matchfunc)
    return result


def print_tree(treedict, begin_characters='', ascii_only=False):
    """Print a tree stored in a dictionary."""
    items = sorted(treedict.items())

    for index, (name, value) in enumerate(items):
        for character in begin_characters:
            print(character, end=' '*3)

        if index == len(items)-1:
            # This is the last item.
            if ascii_only:
                print_template = '`-- %s'
            else:
                print_template = '└── %s'
            new_begin_characters = begin_characters + ' '
        else:
            # This is not the last item.
            if ascii_only:
                print_template = '|-- %s'
                new_begin_characters = begin_characters + '|'
            else:
                print_template = '├── %s'
                new_begin_characters = begin_characters + '│'

        print(print_template % name)
        print_tree(value, new_begin_characters, ascii_only)


# Simple command-line interface.

def error(usage):
    print(usage, file=sys.stderr)
    sys.exit(1)


def is_from_module(cls, module):
    """Return True if a class comes from a module."""
    return cls.__module__ == module.__name__ and cls.__name__ in dir(module)


def main():
    usage = "Usage: %s MODULE CLASS [-a|--ascii]" % sys.argv[0]

    if len(sys.argv) < 3:
        # Missing arguments.
        error(usage)

    modulename = sys.argv[1]
    classname = sys.argv[2]

    ascii_only = False
    for option in sys.argv[3:]:
        if option in {'-a', '--ascii'}:
            ascii_only = True
        else:
            error(usage)

    module = importlib.import_module(modulename)
    cls = getattr(module, classname)
    is_from_the_module = functools.partial(is_from_module, module=module)

    tree = mrotree(cls, matchfunc=is_from_the_module)
    print(classname)
    print_tree(tree, ascii_only=ascii_only)


if __name__ == '__main__':
    main()
