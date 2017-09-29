import os
import csv
import filecmp
from collections import Counter


def getData(file):
#Input: file name
#Ouput: return a list of dictionary objects where 
#the keys will come from the first row in the data.

#Note: The column headings will not change from the 
#test cases below, but the the data itself will 
#change (contents and size) in the different test 
#cases.

	#Your code here:
	filereader = csv.DictReader(open(file))
	info_list = []

	for x in filereader:
		info_list.append(x)

	#print(info_list)
	emptylist = []
	#return emptylist
	return info_list

#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName
	#print (data)
	inlist = data
	mylist = []
	mydict = {}

	#Your code here:
	if col == "First":
		inlist = sorted(inlist, key=lambda k:k['First'])
		#print(inlist)

	if col == "Last":
		inlist = sorted(inlist, key=lambda k:k['Last'])
		#print(inlist)

	if col == "Email":
		inlist = sorted(inlist, key=lambda k:k['Email'])
		#print(inlist)

	part1 = inlist[0].get("First")
	part2 = inlist[0].get("Last")

	outstring = part1 + " " + part2

	return outstring
	print(outstring)



#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g 
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	fresh = 0
	soph = 0
	jun = 0
	sen = 0
	#Your code here:
	for line in data:

		if line.get("Class") == "Freshman":
			fresh = fresh + 1
		if line.get("Class") == "Sophomore":
			soph = soph + 1
		if line.get("Class") == "Junior":
			jun = jun + 1
		if line.get("Class") == "Senior":
			sen = sen + 1
	mylist = [("Freshman", fresh), ("Sophomore", soph), ("Junior", jun), ("Senior", sen)]
	ordered = sorted(mylist, key = lambda x:x[1], reverse = True)
	return ordered

# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB
	datelist = []
	#Your code here:
	for line in a:
		date = line.get("DOB")
		datelist.append(date)

	#print(datelist)

	daylist = []
	for x in datelist:
		x = x.split("/")
		daylist.append(x[1])

	daylist = sorted(daylist)
	print(daylist)

	mycount = Counter(daylist)
	almost = mycount.most_common(1)[0][0]
	return int(almost)



# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB
	datelist = []
	#Your code here:
	for line in a:
		dob = line.get("DOB")
		datelist.append(dob)
	#print(datelist)

	yearlist = []
	for x in datelist:
		x = x.split("/")
		yearlist.append(x[2])
	#print(yearlist)

	agelist = []
	for x in yearlist:
		x = int(x)
		x = 2017-x
		agelist.append(x)

	avg = sum(agelist)/float(len(agelist))
	avg = int(avg)
	return(avg)
	#print(agelist)

#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None

	#Your code here:
	#print (data)
	inlist = a
	mylist = []
	mydict = {}

	#Your code here:
	if col == "First":
		inlist = sorted(inlist, key=lambda k:k['First'])
		#print(inlist)

	if col == "Last":
		inlist = sorted(inlist, key=lambda k:k['Last'])
		#print(inlist)

	if col == "Email":
		inlist = sorted(inlist, key=lambda k:k['Email'])
		#print(inlist)


	csvfile = str(fileName)

	#csvfile.open()
	#print(inlist)

	newlist = (x for x in inlist)
	#print(newlist)
	#print type(newlist)

	with open(csvfile, "w") as output:
		writer = csv.writer(output, lineterminator='\n')
		#writer = csv.writer(output)
		for line in newlist:
			#print(line)
			#writer.writerow(line)
			FirstOut = line["First"]
			LastOut = line["Last"]
			EmailOut = line["Email"]
			ClassOut = line["Class"]
			DOBOut = line["DOB"]

			OutLine = (FirstOut, LastOut, EmailOut)

			#print(FirstOut)
			writer.writerow(OutLine)

	#csvfile.close()
################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)
	
	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()

