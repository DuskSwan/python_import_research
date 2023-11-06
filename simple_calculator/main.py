from package_calc import calc
from package_show.module_showInfo import show_info
from package_show.module_showRules import show_rules
import config

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

if __name__ == "__main__":
    multi_lines_input()