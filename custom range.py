class Counter:
    
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.step > 0):     
            if (self.start < self.end):
                x = self.start
                self.start += self.step
                return x
            raise StopIteration
        else:
            raise ValueError
        
    
counter_1 = Counter(0, 200, 10)

for i in counter_1:
    print(i)

