class Calculator:

    def __init__(self, number):
        self.number = number

    
    def __add__(self, other):
        return self.number + other.number
    
    def __sub__(self, other):
        return self.number - other.number    
    
    def __mul__(self, other):
        return self.number * other.number
    
    def __truediv__(self, other):
        return self.number // other.number

    

calc_1 = Calculator(10)
calc_2 = Calculator(2)

print(calc_1 + calc_2)
print(calc_1 - calc_2)
print(calc_1 * calc_2)
print(calc_1 / calc_2)
