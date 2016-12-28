# classtree

This is a simple program that prints a tree of classes in a
Python module.

Example:

    $ python3.4 classtree.py builtins OSError
    OSError
    ├── BlockingIOError
    ├── ChildProcessError
    ├── ConnectionError
    │   ├── BrokenPipeError
    │   ├── ConnectionAbortedError
    │   ├── ConnectionRefusedError
    │   └── ConnectionResetError
    ├── FileExistsError
    ├── FileNotFoundError
    ├── InterruptedError
    ├── IsADirectoryError
    ├── NotADirectoryError
    ├── PermissionError
    ├── ProcessLookupError
    └── TimeoutError
