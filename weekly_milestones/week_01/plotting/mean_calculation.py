import pandas as pd

def mean(x):
    return sum(x)/len(x)

def mean1(x):
    sm = 0
    for item in x: 
        sm = sm + item
    return sm/len(x)

def std_error(x):
    sm = 0
    xm = mean(x)
    for item in x: 
        sm = sm + (item - xm)**2
    return pow((sm/(len(x)-1)), 0.5)

x = [2, 3, 4, 3, 5, 3, 1]
result = mean(x)
result1 = std_error(x)
print(result, result1, pd.Series(x).std())

assert result == pd.Series(x).mean()
assert round(result1, 4) == round(pd.Series(x).std(),4)

