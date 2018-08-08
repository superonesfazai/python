#!/usr/bin/python3.5
#coding: utf-8

def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.
    Takes module, class, list, dictionary, or string."""
    method_list = [method for method in dir(object) if callable(getattr(object, method))]
    process_func = collapse and (lambda s: ''.join(s.split())) or (lambda s: s)
    print('\n'.join(['%s %s' % (method.ljust(spacing),
                      process_func(str(getattr(object, method).__doc__))) for method in method_list]))

if __name__ == '__main__':
    # print(info.__doc__)
    from time import sleep

    print(info(sleep))