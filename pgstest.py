import requests
from lxml import html
import json
# please specify
filename = "type+category.json"

url = 'https://www.pcgs.com/prices/detail/eagle-type-coins-proofs/-2/most-active'

print(url)
final_data = []

res = requests.get(url)

tree = html.fromstring(res.content)

# dic = {}

header = tree.xpath("//tr[@class='text-uppercase text-nowrap']")
dtpts = []
for data_point in header[0]:
	for i in data_point.iter('th'):
		dtpts.append(i.text.strip())

count = len(dtpts)


pcgs = tree.xpath("//tr[@class='bg-pale ']/td[1] | //tr[@class='bg-light ']/td[1] | //tr[@class = 'bg-pale major expandable ']/td[1] | //tr[@class='bg-light major expandable ']/td[1]")
description = tree.xpath("//tr[@class='bg-pale ']/td[2]  | //tr[@class='bg-light ']/td[2] | //tr[@class = 'bg-pale major expandable ']/td[2] | //tr[@class='bg-light major expandable ']/td[2]")

desig = tree.xpath("//tr[@class='bg-pale ']/td[3]/text()[1]  | //tr[@class='bg-light ']/td[3]/text()[1] | //tr[@class = 'bg-pale major expandable ']/td[3]/text()[1] | //tr[@class='bg-light major expandable ']/td[3]/text()[1]")
# print(description)

prices = []

for i in range(4,count+1):
	price = tree.xpath("//tr[@class='bg-pale ']/td["+str(i)+"]   | //tr[@class='bg-light ']/td["+str(i)+"] | //tr[@class = 'bg-pale major expandable ']/td["+str(i)+"] | //tr[@class='bg-light major expandable ']/td["+str(i)+"]")
	ls = []
	for j in range(len(price)):
		lst = []
		for p in price[j].iter('a'):
			if(p.text != None):
				lst.append(p.text)
				# print(p.text)
		for p in price[j].iter('span'):
			if(p.text  != None):
				lst.append(p.text)
		ls.append(lst)
	prices.append(ls)
	
for i in range(len(pcgs)):
	pcg = pcgs[i].text.strip()
	pcg_link =""
	if(pcg == ""):
		for p in pcgs[i].iter('div'):
			pcg = p.text.strip()
			pcg_link = ""
	if(pcg == ""):
		for p in pcgs[i].iter('a'):
			pcg = p.text.strip()
			pcg_link = p.attrib.get('href')
			# print(" a",pcg)

	dic = {}

	dic[dtpts[0]] = pcg
	dic[dtpts[1]] = description[i].text.strip()
	dic[dtpts[2]] = desig[i].strip()
	dic['pcg_link'] = pcg_link

	for j in range(count-3):
		dic[dtpts[j+3]] = prices[j][i]
	

	final_data.append(dic)

for i in final_data:
	print(i)
# home_dict["Details"] = final_data
# filename = i["heading"]+i["category"]+'.json'

json_object = json.dumps(final_data, indent = 4)
with open(filename, "w") as outfile: 
    outfile.write(json_object)





