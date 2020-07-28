import requests
from lxml import html


def subpagedata(home_dict):
	url = home_dict["category_link"]
	print(url)
	final_data = []

	res = requests.get(url)

	tree = html.fromstring(res.content)

	# dic = {}

	header = tree.xpath("//tr[@class='text-uppercase text-nowrap']")

	if(header != []):


		dtpts = []
		# print(header[0])
		for data_point in header[0]:
			for i in data_point.iter('th'):
				# print(i.text.strip())
				dtpts.append(i.text.strip())

		count = len(dtpts)
		# print(dtpts)
		pcgs = tree.xpath("//tr[@class='bg-pale ']/td[1] | //tr[@class='bg-light ']/td[1] | //tr[@class = 'bg-pale major expandable ']/td[1] | //tr[@class='bg-light major expandable ']/td[1]")
		# description = tree.xpath("//tr[@class='bg-pale ']/td[2]/text()[2]  | //tr[@class='bg-light ']/td[2]/text()[2] | //tr[@class = 'bg-pale major expandable ']/td[2]/text()[2] | //tr[@class='bg-light major expandable ']/td[2]/text()[2]")
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
			pcg_link = ""
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

		# for i in final_data:
			# print(i)
		home_dict["Details"] = final_data

		return home_dict









































# data_point = tree.xpath("//tr[@class='text-uppercase text-nowrap'][2]/th/text()")
# count = 0
# dtpts = []
# for i in data_point:
# 	# print(i.strip())
# 	dic[i.strip()] = []
# 	dtpts.append(i.strip())
# 	count += 1 