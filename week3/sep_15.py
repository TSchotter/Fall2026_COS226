import time
import random

def bubbleSort(x):
    for i in range(len(x)):
        didSwap = False
        for j in range(len(x)-1-i): # run one and i less time
            if x[j] > x[j+1]: # left bigger than right
                # swap
                x[j], x[j+1] = x[j+1], x[j]
                didSwap = True
        if not didSwap: # did not swap, leave early
            return

def startMergeSort(x): # start the merge sort recursive
    splitM(x, 0, len(x)-1)

def splitM(x, start, end):
    if (end-start) <= 0: # we're done splitting
        return

    middleIndex = (end-start)//2 + start
    splitM(x, start, middleIndex)
    splitM(x, middleIndex+1,end)

    merge(x, start, middleIndex, end)

def merge(x, start, middleIndex, end):
    tempSpace = x[start: middleIndex+1] # right-hand side non-inclusive, so +1
    L = 0
    R = middleIndex + 1
    while (True):
        # if left side not done, and 
        #   either right side done or less than right side
        if L < len(tempSpace) and (R > end or tempSpace[L] < x[R]): # pick left
            x[start] = tempSpace[L]
            L += 1
        elif R <= end:   # pick right
            x[start] = x[R]
            R += 1
        else:
            return
        start += 1

def quickSortDNF(x):
    # kicks off recursion process
    quickSortDNFRecursive(x, 0, len(x)-1)

def quickSortDNFRecursive(x, start, end):
    if (end <= start): 
        # list is small enough that we know it's in order
        return

    lt, gt = dnfPartition(x, start, end)

    # left half: everything strictly less than pivot
    quickSortDNFRecursive(x, start, lt-1)

    # right half: everything strictly greater than pivot
    # (values from lt to gt are already equal to the pivot)
    quickSortDNFRecursive(x, gt+1, end)


def quickSortLomuto(x):
    # kicks off recursion process
    quickSortLomutoRecursive(x, 0, len(x)-1)

def quickSortLomutoRecursive(x, start, end):
    if (end <= start):
        # list is small enough that we know it's in order
        return

    p = lomutoPartition(x, start, end)

    # left half
    quickSortLomutoRecursive(x, start, p-1)

    # right half
    quickSortLomutoRecursive(x, p+1, end)


def quickSortNaive(x):
    # kicks off recursion process
    quickSortNaiveRecursive(x, 0, len(x)-1)

def quickSortNaiveRecursive(x, start, end):
    if (end <= start):
        # list is small enough that we know it's in order
        return

    p = naivePartition(x, start, end)

    # left half
    quickSortNaiveRecursive(x, start, p-1)

    # right half
    quickSortNaiveRecursive(x, p+1, end)


def quickSortHoare(x):
    # kicks off recursion process
    quickSortHoareRecursive(x, 0, len(x)-1)

def quickSortHoareRecursive(x, start, end):
    if (end <= start):
        # list is small enough that we know it's in order
        return

    p = hoarePartition(x, start, end)

    # Hoare does not put the pivot in a final fixed slot,
    # so the left recurse includes p (unlike Lomuto/naive)
    quickSortHoareRecursive(x, start, p)

    # right half
    quickSortHoareRecursive(x, p+1, end)


def dnfPartition(x, start, end):
    # Dutch National Flag: 3-way partition
    # x[start .. lt-1]  < pivot
    # x[lt    .. gt]    == pivot
    # x[gt+1  .. end]   > pivot
    # this has the advantage of keeping the pivots all together and no
    #   longer considering them in the recursive partitioning
    pivot = x[end]
    lt = start  # next spot for values less than pivot
    i = start   # current value we are looking at
    gt = end    # next spot for values greater than pivot

    while i <= gt:  # we'll continue as long as our checker variable is less than our right-hand bound (gt)
        if x[i] < pivot:  # what we're looking at is less than the pivot we've picked
            x[lt], x[i] = x[i], x[lt]  # swap it to the "less than" side.
            lt += 1  # move the "less than" bound to the right
            i += 1  # move the checker variable to the right
        elif x[i] > pivot:  # what we're looking at is greater than the pivot we've picked
            x[gt], x[i] = x[i], x[gt]  # swap it to the "greater than" side.
            gt -= 1  # move the "greater than" bound to the left
            # do not move i; the value swapped in has not been checked yet, it might need to be placed in the lt *OR* gt side.
        else:
            # equal to pivot, leave it in the middle band
            i += 1

    return lt, gt  # equal-to-pivot range (the outside world knows where the start and end points are, so we don't need to return them)


def lomutoPartition(x, start, end):
    pivot = x[end]
    i = start # i at the start
    for j in range(i, end): # j at start, to end-1
        if x[j] <= pivot: # check if we need to swap
            x[i], x[j] = x[j], x[i]
            i += 1 # increase i if we swap
    # swap i and pivot
    x[i], x[end] = x[end], x[i]

    return i # return where pivot is


def hoarePartition(x, start, end):
    # two pointers walk inward; swap inversions around the pivot
    # after return: x[start .. p] <= pivot, x[p+1 .. end] >= pivot
    pivot = x[start]
    i = start - 1  # will move right
    j = end + 1    # will move left

    while i < j:
        i += 1
        while x[i] < pivot: # find something on the left that does not belong
            i += 1
        j -= 1
        while x[j] > pivot: # find something on the right that does not belong
            j -= 1
        if i < j: # pointers have not crossed; swap the inversion
            x[i], x[j] = x[j], x[i]

    return j # pointers crossed; split is between them


def naivePartition(x, start, end):
    pivot = x[end]
    # create empty list that we fill.
    copy = []
    # find things less than pivot
    for i in range(start, end):
        # anything less than pivot, add it to "copy"
        if x[i] <= pivot:
            copy.append(x[i])

    partitionIndex = start + len(copy)        
    copy.append(pivot) # add the pivot

    # find things greater than pivot
    for i in range(start, end):
        # anything greater than pivot, add it to "copy"
        if x[i] > pivot:
            copy.append(x[i])
    
    # place all things in copy into same spot on x
    for i in range(len(copy)):
        x[start+i] = copy[i]

    # hand relevant info back up
    return partitionIndex

random.seed(0)
n = 20000

x = []

for i in range(n):
    x.append(random.randint(0,20000))

# before the sort
start = time.time()
startMergeSort(x)
print(x[100:200])
end = time.time()
print(end-start) # number of seconds difference between two

