# from typing import Type


# class Parent:
#     def __new__(cls: Type):
#         print("calling __new__")
#         return super().__new__(cls)


# class Child(Parent):
#     def __new__(cls: Type):
#         print("in child __new__")
#         return super().__new__(cls)

# c = Child()


# decorator for logging
def logging(func):
    def wrapper(*args, **kwargs):
        print("in wrapper")
        print(func.__name__, args, kwargs)
        res = func(*args, **kwargs)
        return res
    return wrapper

# this is some example class you do not want to/can not modify
class Working:
    def Do(self):
        print("I am working")
    def pr(self,printit):   # other example method
        print(printit)
        print("exiting pr")
    def bla(self):          # other example method
        print("in working bla")
        self.pr("saybla")
        print("back in working bla")


# this is how to make a new class with some methods logged:
class MutantWorking(Working):
    pr=logging(Working.pr)
    bla=logging(Working.bla)
    Do=logging(Working.Do)

    def check_super(self):
        print(super)
        print(super())
        print(super().bla)
        print(Working)
        print(Working.bla)
        print(Working.bla(self))
        print(super() == Working)


h=MutantWorking()
print("*")
print(h.bla())
print("**")

h.pr("Working")                                                  
print("***")

h.Do()
print("****")
h.check_super()
print("*****")

k = MutantWorking()

print(h.bla)
print(k.bla)
print(h.bla == k.bla)
print(Working.bla)