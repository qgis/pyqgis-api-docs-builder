:tocdepth: 1

Frequently Asked Questions
==========================

What are Virtual Methods?
-------------------------

While base Python allows overriding any base class method from a subclass, **only** methods marked as ``virtual`` can be
safely overridden in a Python subclass of a PyQGIS class.

PyQGIS exposes the underlying c++ classes and objects from QGIS, and in c++ methods which are designed to be
overridden must be explicitly marked as ``virtual`` methods. Accordingly, attempting to override any other non-virtual
methods from Python will result in an inconsistent behavior. The overridden method would **only** be called when
the caller itself is Python code, but will be completely ignored if the caller is the underlying QGIS c++ code. This
should always be avoided as it will result in subtle, extremely hard to fix bugs.

Instead, only override methods which are explicitly marked as ``virtual`` in the class documentation.
