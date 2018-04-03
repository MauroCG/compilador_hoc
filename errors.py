import sys

_num_errors = 0

def error(lineno, message, filename=None):
    global _num_errors
    if not filename:
        errmsg = "{}: {}".format(lineno, message)
    else:
        errmsg = "{}:{}: {}".format(filename,lineno,message)

    print(errmsg, file=sys.stderr)
    _num_errors += 1

def errors_reported():
    return _num_errors

def clear_errors():
    global _num_errors
    _num_errors = 0
