from functools import wraps


def requires_login2(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print("Hi!")
        return func(*args, **kwargs)
    return decorated_function


@requires_login2
def my_function(x, y):
    return x + y

print( my_function(5,6) )