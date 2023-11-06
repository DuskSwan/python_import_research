from .subpackage_exp.module_expAnalysis import legal_exp,parse_expression
from .module_calc import add,str2int,mult

def calc(exp):
    if not legal_exp(exp): return False
    n,ch,m = parse_expression(exp)
    n = str2int(n)
    m = str2int(m)
    if(ch == '+'): return add(n,m)
    elif(ch == '*'): return mult(n,m)
    else: return False