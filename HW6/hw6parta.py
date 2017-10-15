from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

testurl = "http://py4e-data.dr-chuck.net/comments_42.html"

#url = testurl
url = input('Enter link - ')

html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

tags = soup.find_all('span')
print(tags)

numlist = []

for tag in tags:
	# Look at the parts of a tag
	print('TAG:', tag)
	print('URL:', tag.get('href', None))
	print('Contents:', tag.contents[0])
	print('Attrs:', tag.attrs)

	mystring = tag.string
	mynum = int(mystring)
	print(mystring)

	numlist.append(mynum)

mysum = sum(numlist)
print("The count is ", len(numlist))
print("The total number is ", mysum)

