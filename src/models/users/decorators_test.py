
def requires_login1(func):
   print("Hi!")
   func()

@requires_login1
def my_function():
    print("Hello world!")
    return "Hi"
