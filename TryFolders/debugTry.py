from random import choices
def UC(a,b):
    coinToss = choices([0,1],k=len(a))
    print(coinToss)
    offspring1=[]
    for i in range(len(coinToss)):
        offspring1.append(a[i] if coinToss[i]==1 else b[i])
    offspring2=[]
    for i in range(len(coinToss)):
        offspring2.append(b[i] if coinToss[i]==1 else a[i])
    return offspring1, offspring2
a=choices([0,1],k=10)
b=choices([0,1],k=10)
print(a,b)
print(UC(a, b))