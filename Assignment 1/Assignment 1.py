##How This Works##
'''
By: Andrew Storus

***This should read from a file called SpaceStation.txt in the directory of this file and write to a text file called Output.txt***

1) The Text File is Opened and read into a list called data

2) This data is fed into a mergesort function which sorts the data from latest finish time to earliest finish time

3) This data is then run through the selection algorithm. The current finish time is set to the start time read from the text file
    Iterate through the tasks with the latest start time, if that task has a start time earlier than the current finish time, select it, else go to the next task in the sorted list
    when a task is selected, set the current finish time to be that tasks finish time
    stop when the current finish time is greater than or equal to the end time specified from the text file

4) These tasks are put in a new list which stores their project number as well as their length

5) From this new list, create a new list containing all possible subsets of the sums of the lengths

6) Loop through all these newly created subsets, select all pairs which sum to the total time of the selected tasks

7) From the newly selected pairs, take their difference and sort them lowest to highest

8) Iterate over all the pairs from lowest to highest. Check the one with the lowest difference first.
If its two subsets contain all the elements and no duplicates, it is the correct division for the problem

'''
from math import pow as power

startIndx = 1
finishIndx = 2
taskIndx = 0
lengthIndx = 1
differenceIndx = 2
sumIndx = 0
slctdTasksIndx = 1

'''mergesort algorithm python implementation adapted from Interactivepython tutorial'''
def mergesort(List):
    if len(List) > 1:
        left = List[:len(List)//2]
        right = List[len(List)//2:]

        mergesort(left)
        mergesort(right)

        i=0
        j=0
        k=0

        while i < len(left) and j < len(right):
            if left[i][finishIndx] > right[j][finishIndx]:
                List[k] = left[i]
                i += 1
            else:
                List[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            List[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            List[k] = right[j]
            j += 1
            k += 1

def returnSubsets(List, Sublist):

    numSublists = int(power(2, len(List)))
    bitArray = [int(digit) for digit in bin(numSublists - 1)[2:]]
    mostSigBit = int(power(2, len(bitArray) - 1))
    msbIndx = len(bitArray) - 1
#iterate from 0b0000000 to 0b1111111
#each task is given a bit, when that bit is 1, add its value to the sum for this subset
#append that as a new subset
    for i in range(1, numSublists):
        Indexes = []
        sum = 0
        j = mostSigBit
        k = msbIndx
        while j != 0:
            if i & j == j:
                sum += List[k][lengthIndx]
                Indexes.append(k)
            j /= 2
            k -= 1
        Sublist.append([sum,Indexes])


def optimalSubsets(subsets, possibleCombos, targetVal):
#loop over all subsets to get ones which sum to the target Value
    for i in range(len(subsets)):
        for j in range(i, len(subsets)):
            Sum = subsets[i][sumIndx] + subsets[j][sumIndx]
            if i != j:
                if Sum == targetVal:
                    possibleCombos.append([subsets[i], subsets[j], abs(subsets[i][sumIndx] - subsets[j][sumIndx])])
    possibleCombos.sort(key = lambda x: x[differenceIndx])
	
#Read in data
data = []
f = open("SpaceStation.txt", 'r')
words = f.read().split("\n")

Times = words[0].split()
startTime = int(Times[0])
finishTime = int(Times[1])
numProjects = int(words[1])

newFile = open("Output.txt", 'w')

for indx,w in enumerate(words[2:]):
    data.append(w.split())
    data[indx] = [int(i) for i in data[indx]]
#Sort the data by finish time
mergesort(data)
currentEndTime = startTime
ptr = 0
chosen = []
for i in range(len(data)):
    chosen.append(0)
#Algorithm described in step 3 of the above program comment
while currentEndTime < finishTime:
    if data[ptr][startIndx] < currentEndTime:
        if chosen[ptr] == 0:
            currentEndTime = data[ptr][finishIndx]
            chosen[ptr] = 1
            ptr = 0
        else:
            ptr += 1
    else:
        ptr += 1

selectedTasks = []
selectedProjectNumbers = []

print "printing data"
#Create a new list with the selected tasks numbers and their time length
for i in range(len(chosen)):
    if chosen[i] == 1:
        selectedTasks.append([data[i][taskIndx], data[i][finishIndx] - data[i][startIndx]])
        selectedProjectNumbers.append(data[i][taskIndx])
        print data[i]

Sum = 0
for i in selectedTasks:
    Sum += i[lengthIndx]

optimalCandidates = []

print "\n\nprinting selected tasks \n\n"
for i in selectedTasks:
    print i
#create subsets from all possible combinations
returnSubsets(selectedTasks, optimalCandidates)

print "\n\n"
print "printing optimalCandidates - sum of set, indexes in set"
for i in optimalCandidates:
    print i
print "\n\n"

y1 = []
#create a list containing all the pairs of subsets which sum to the target value
optimalSubsets(optimalCandidates, y1, Sum)

print "\n\n"
print "sorted subsets that sum to 119 lowest to highest distance set1 sum, set1 elements, set2 sum, set2 elements, difference"
for i in y1:
    print i
print "\n\n"

print "\n\n"
print "pritns concatenated lists of choices\n\n"

partitions = []
taskIndexes = []

group1ProjectIndexes = []
group2ProjectIndexes = []
#Check that the selected groups actually contain all the tasks
for i in y1:
    indexes = i[0][1] + i[1][1]
    print indexes
    if all(x in indexes for x in [0, 1, 2, 3, 4, 5, 6]):
        group1ProjectIndexes = i[0][1]
        group2ProjectIndexes = i[1][1]
        partitions.append(i)
        break

print "\n\ngroup 1 and 2 projects\n\n"

print group1ProjectIndexes
print group2ProjectIndexes

group1 = []
group2 = []
#retrieve the actual project numbers from the original data read in
for i in group1ProjectIndexes:
    group1.append(selectedProjectNumbers[i])

for i in group2ProjectIndexes:
    group2.append(selectedProjectNumbers[i])

print "\n\n"

print group1
print group2
#write the output to a text file
with open("Output.txt", "a") as myfile:
    myfile.write("Selected Projects : ")
    for i in selectedProjectNumbers:
        myfile.write(str(i) + "\t")
    myfile.write("\nGroup 1 Projects : ")

    for i in group1:
        myfile.write(str(i) + "\t")
    Sum = 0
    for i in group1ProjectIndexes:
        Sum += selectedTasks[i][1]
    myfile.write("\nTotal Time = " + str(Sum))
    myfile.write("\nGroup 2 Projects : ")
    for i in group2:
        myfile.write(str(i) + "\t")
    Sum = 0
    for i in group2ProjectIndexes:
        Sum += selectedTasks[i][1]
    myfile.write("\nTotal Time = " + str(Sum))

newFile.close()
