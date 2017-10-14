from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

testurl = "http://py4e-data.dr-chuck.net/known_by_Fikret.html"

url = input('Enter link - ')
#url = testurl
count = int(input('Enter count - '))
position = int(input("Enter position - "))

print("Retrieving: ", url)

html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

linklist = []
names = []
#url2 = urllib.request.urlopen(names[position], context=ctx).read()
#print(url2)

for x in range(count):
	#print(x)
	html = urllib.request.urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html, 'html.parser')
# Retrieve all of the anchor tags
	tags = soup('a')
#for tag in tags:
    #print(tag.get('href', None))
    #linklist.append(tag)

	for tag in tags:
		mytag = tag.get('href', None)
		linklist.append(mytag)
#another test for commit
	#print(linklist)
	newlink = linklist[position-1]
	del linklist[:]
	print("Retrieving: ", newlink)

	url = newlink