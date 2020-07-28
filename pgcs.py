import requests
from lxml import html
from pcgssubpage import subpagedata
import json

data = []

res = requests.get('https://www.pcgs.com/prices/')

tree = html.fromstring(res.content)


boxes = tree.xpath("//div[@class='box']")

json_data = []



for box in boxes:
	

	for heading in box.iter('h3'):
		head = heading.text.strip()
	for category in box.iter('a'):
		dic_homepage = {}
		dic_homepage["heading"] = head
		dic_homepage["category"] = category.text.strip()
		dic_homepage["category_link"] = "https://www.pcgs.com"+category.attrib.get('href')
		# print(dic_homepage)
		data.append(dic_homepage)



for i in data:
	jsn = subpagedata(i)
	print(jsn)
	filename = i["heading"]+i["category"]+'.json'
	json_object = json.dumps(jsn, indent = 4)
	with open(filename, "w") as outfile: 
	    outfile.write(json_object) 
	





