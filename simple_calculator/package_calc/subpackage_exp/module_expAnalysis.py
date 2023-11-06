def legal_exp(exp):
    print("This is the analysis function in the module_expAnalysis.py file.")
    legal_str = "0123456789+* "
    for ch in exp:
        if ch not in legal_str:
            print("The expression is illegal with charactor: " + ch)
            return False
    return True

def parse_expression(expression):
    operators = ['+', '-', '*', '/']  # 可支持的操作符列表
    expression = expression.replace(' ', '')
    # find operator position
    for operator in operators:
        if operator in expression:
            operator_pos = expression.index(operator)
            break
    # draw out the expression
    operator = expression[operator_pos]
    num1 = expression[:operator_pos]
    num2 = expression[operator_pos + 1:]

    return num1, operator, num2