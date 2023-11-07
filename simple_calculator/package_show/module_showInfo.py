import os,sys

def show_info():
    print("This is module showInfo")
    print("This is a simple calculator can only calculate + and * with integers.")

def test_condition2():
    # current_path = os.path.abspath(__file__)
    # current_cont = os.path.dirname(current_path)
    # parent_cont = os.path.dirname(current_cont)
    # sys.path.append(parent_cont)
    sys.path.append('.')

    from config import cfg
    cfg().show_info()

def test_condition3():
    # current_path = os.path.abspath(__file__)
    # current_cont = os.path.dirname(current_path)
    # parent_cont = os.path.dirname(current_cont)
    # sys.path.append(parent_cont)
    sys.path.append('.')
    from package_calc.module_calc import add
    print(add(1,2))

def test_condition5():
    from ..config import cfg
    cfg().show_info()

if __name__ == '__main__':
    print('This is module_showInfo.py')
    # test_condition2()
    test_condition3()
    for p in sys.path: print(p)