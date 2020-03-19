'''
Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

What does this script :  

	Check reputation of all domain into the domains.csv file
'''
from datetime import datetime
import json
import requests

# get token from token.txt
fa = open("token.txt", "r")
investigate_api_key = fa.readline()
fa.close()
#create header for authentication and set limit of sample return to 1
headers = {
'Authorization': 'Bearer ' + investigate_api_key,
'limit': '1'
}

def retrieve_categorie(header):
	get_url = "https://investigate.api.umbrella.com/domains/categories/"
	# do GET request for the domain status and category
	request_get = requests.get(get_url, headers=headers)
	if(request_get.status_code == 200):
		# store all categories into a variable named output
		output = request_get.json() 
		return output

def check_categorization(header,file,categories):
	investigate_url = "https://investigate.api.umbrella.com/domains/categorization/"
	# time for AlertTime and EventTime when domains are added to Umbrella
	time = datetime.now().isoformat()
		
	# loop through .txt file and append every domain to list, skip comments
	domain_list = []
	with open('domains.csv') as inputfile:
		for line in inputfile:
			if line[0] == "#" or line.strip() == "Site":
				pass
			else:
				domain_list.append(line.strip())

	fh = open("./output/resultat_categorie.txt", "w")
	fi = open("./output/resultat_reputation.txt", "w")
	# loop through all domains
	for domain in domain_list:
		print(domain)
		# assemble the URI, show labels give readable output
		get_url = investigate_url + domain
		# do GET request for the domain status and category
		request_get = requests.get(get_url, headers=headers)
		if(request_get.status_code == 200):
			# store categorization into the output variable
			output = request_get.json()
			resp2=json.dumps(output,sort_keys=True,indent=4, separators=(',', ': '))
			print(resp2)
			fh.write(resp2)
			fh.write('\r\n')
			# FIRST let's retreive the domain status
			domain_output = output[domain] #we need this as the domain name in the json result is always changing
			domain_status = domain_output["status"] #a now we can retreive the status for the domain name
			# walk through different options of status
			if(domain_status == -1):
				print("SUCCESS: The domain %(domain)s is found MALICIOUS at %(time)s" % {'domain': domain, 'time': time})
				fi.write(domain+'; DANGEROUS ;'+time+';')
			elif(domain_status == 1):
				print("SUCCESS: The domain %(domain)s is found CLEAN at %(time)s" % {'domain': domain, 'time': time})
				fi.write(domain+'; CLEAN ;'+time+';')			
			else:
				print("SUCCESS: The domain %(domain)s is found UNDEFINED / RISKY at %(time)s" % {'domain': domain, 'time': time})
				fi.write(domain+'; UNKNOWN;'+time+';')
			# SECOND let's retreive Domain Categories
			domain_categories=[]
			domain_categories = domain_output["content_categories"]
			for cat in domain_categories:
				la_categorie=categories.get(cat)
				print (la_categorie)
				fi.write(la_categorie +' + ')
			fi.write('\r\n')
		# if(associated sample has a Threat Score of higher or equal then 90)
			# POST request to Enforcement API
	fh.close()

if __name__ == '__main__':
	categories=retrieve_categorie(headers)
	check_categorization(headers,'domains.csv',categories)
	