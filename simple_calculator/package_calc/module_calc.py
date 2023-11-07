def str2int(s):
    return int(s)

def add(a, b):
    return a + b

def mult(a, b):
    return a * b

def test_condition6():
    # print(__name__)
    from ..package_show.module_showInfo import show_info 
        # ImportError: attempted relative import beyond top-level package
    show_info()

if __name__ == '__main__':
    print('This is module_calc.py')