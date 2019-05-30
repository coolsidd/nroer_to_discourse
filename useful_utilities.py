#!/usr/bin/env python

def debug_func(func):
    from pprint import pprint
    def wrapper(*args,**kwargs):
        print("ARGS:")
        pprint(args)
        print("KWARGS:")
        pprint(kwargs)
        print("DONE: {}".format(func.__name__))
        res = func(*x)
        print("RESULT: {}".format(res.__str__()))
        return res
    return wrapper
