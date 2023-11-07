import config
from package_calc import calc
from package_show.module_showInfo import show_info

# from package_show.module_showRules import show_rules 
    # yes

from package_show import module_showRules 
show_rules = module_showRules.show_rules
    # yes

# import package_show
# show_rules = package_show.module_showRules.show_rules
    # no

def multi_lines_input():
    cfg = config.cfg()
    cfg.show_info()
    show_info()
    show_rules()
    while True:
        exp = input("Please input an expression: ")
        if(exp == "quit"):
            break  
        else: 
            res = calc(exp)
            if(res): print("The result is: " + str(res))
            else: print("The expression is illegal.")

def test_condition5():
    from package_calc.subpackage_exp import module_expAnalysis
    module_expAnalysis.test_condition5()

def test_condition6():
    from package_calc import module_calc
    module_calc.test_condition6()

if __name__ == "__main__":
    multi_lines_input()
    # test_condition6()