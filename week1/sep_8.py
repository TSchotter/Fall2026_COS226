# bubble sort

x = [6,5,2,9,1,3,7]
counter = 0
'''
#Bubble Sort
for i in range(len(x)): # i = [0,n]
    flag = False
    for j in range(len(x)-1-i): #j = [0,n-1-i]
        counter += 1
        if x[j] > x[j+1]: # need to swap
            counter += 3 # 3 write operations
            x[j],x[j+1] = x[j+1],x[j]
            flag = True
    if(not flag): # exit early if pass didn't swap anything
        break
'''
# Selection Sort
for i in range(len(x)-1):         # i = [0, n-1]
    s = i # keep track of smallest value we've seen
    for j in range(i+1, len(x)):     # j = [i+1, n]
        counter += 1
        if x[j] < x[s]: # if what we're looking at is smaller than smallest
            counter += 1 # 1 write operation
            s = j # update smallest
    # perform swap
    counter += 1
    if s != i:
        counter += 3 # 3 write operations
        x[s], x[i] = x[i], x[s]

print(x)
print(counter)
