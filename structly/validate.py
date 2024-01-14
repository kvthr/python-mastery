from functools import wraps
import inspect

class Validator:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    # Collect all derived classes into a dict
    validators = {}
    @classmethod
    def __init_subclass__(cls):
        cls.validators[cls.__name__] = cls
    
    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)

class Typed(Validator):
    expected_type = object

    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f"Expected {cls.expected_type}")
        return super().check(value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass


class ValidatedFunction:
    def __init__(self, func):
        self.func = func
        self.signature = inspect.signature(func)
        self.annotations = dict(func.__annotations__)
        self.retcheck = self.annotations.pop('return', None)

    def __call__(self, *args, **kwargs):
        bound = self.signature.bind(*args, **kwargs)

        for name, val in self.annotations.items():
            val.check(bound.arguments[name])

        result = self.func(*args, **kwargs)

        if self.retcheck:
            self.retcheck.check(result)

        return result

def validated(func):
    """
    Type check enforcement - Decorator
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        annotations = dict(func.__annotations__)
        bound = signature.bind(*args, **kwargs)
        retcheck = annotations.pop("return", None)

        errors = []
        for name, val in annotations.items():
            try:
                val.check(bound.arguments[name])
            except Exception as e:
                errors.append(f"    {name}: {e}")
        if errors:
            raise TypeError('Bad Arguments\n' + '\n'.join(errors))

        result = func(*args, **kwargs)
        if retcheck:
            try:
                retcheck.check(result)
            except Exception as e:
                raise TypeError(f'Bad return: {e}') from None
        return result
    
    return wrapper

def enforce(**types):
    '''
    Enforces types for the kwargs specified
    '''
    def validated(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            retcheck = types.pop("return_", None)
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            errors = []

            for name, val in types.items():
                try:
                    val.check(bound.arguments[name])
                except Exception as e:
                    errors.append(f"    {name}: {e}")
            if errors:
                raise TypeError('Bad Arguments\n' + '\n'.join(errors))

            result = func(*args, **kwargs)
            if retcheck:
                try:
                    retcheck.check(result)
                except Exception as e:
                    raise TypeError(f'Bad return: {e}') from None
            return result
        
        return wrapper
    
    return validated
