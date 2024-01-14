import inspect
import sys

class Structure():
    _fields = ()

    @staticmethod
    def _init():
        locs = sys._getframe(1).f_locals
        self = locs.pop('self')
        for name, val in locs.items():
            setattr(self, name, val)

    @classmethod
    def set_fields(cls):
        cls._fields = list(inspect.signature(cls).parameters)

    @classmethod
    def create_init(cls):
        args = ','.join(cls._fields)
        code = 'def __init__(self, {0}):\n'.format(args)
        statements = [ '    self.{0} = {0}'.format(name) for name in cls._fields]
        code += '\n'.join(statements)
        locs = { }
        exec(code, locs)
        cls.__init__ = locs['__init__']

    def __repr__(self):
        return f"{type(self).__name__}({','.join(repr(getattr(self, name)) for name in self._fields)})"

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self._fields:
           super().__setattr__(name, value)
        else:
            raise AttributeError(f"No attribute - {name}")
        