from datetime import datetime
import json
import requests
import re
from time import sleep
from decimal import *

def retrieve_categorie(headers):
	get_url = "https://investigate.api.umbrella.com/domains/categories/"
	# do GET request for the domain status and category
	request_get = requests.get(get_url, headers=headers)
	if(request_get.status_code == 200):
		# store all categories into a variable named output
		output = request_get.json() 
		return output
		
def check_categorization(header,domain_list,categories):
	
	# time for AlertTime and EventTime when domains are added to Umbrella
	time = datetime.now().isoformat()

	fh = open("./output/resultat.txt", "w")
	line_out='domain;found;category;status;securerank2;asn_score;prefix_score;rip_score;attack;threat_type'
	fh.write(line_out)
	fh.write('\n')
	# loop through all domains
	for domain in domain_list:
		print(domain)
		investigate_url = "https://investigate.api.umbrella.com/domains/categorization/"
		get_url = investigate_url + domain
		# do GET request for the domain status and category
		request_get = requests.get(get_url, headers=headers)
		if(request_get.status_code == 200):
			# store categorization into the output variable
			output = request_get.json()
			domain_output = output[domain] #we need this as the domain name in the json result is always changing
			domain_status = domain_output["status"] #a now we can retreive the status for the domain name
			# walk through different options of status
			if(domain_status == -1):
				print("SUCCESS: The domain %(domain)s is found MALICIOUS at %(time)s" % {'domain': domain, 'time': time})
				status='DANGEROUS'
			elif(domain_status == 1):
				print("SUCCESS: The domain %(domain)s is found CLEAN at %(time)s" % {'domain': domain, 'time': time})
				status='CLEAN'				
			else:
				print("SUCCESS: The domain %(domain)s is found UNDEFINED / RISKY at %(time)s" % {'domain': domain, 'time': time})
				status='UNKNOWN'
			# SECOND let's retreive Domain Categories
			domain_categories=[]
			domain_categories = domain_output["content_categories"]
			for cat in domain_categories:
				la_categorie=categories.get(cat)	
		# Third let's retrieve security vlaues for this domain
		investigate_url = "https://investigate.api.umbrella.com/security/name/"
		get_url = investigate_url + domain
		sleep(0.3)
		request_get = requests.get(get_url, headers=headers)
		if(request_get.status_code == 200):
			output = request_get.json()
			resp2=json.dumps(output,sort_keys=True,indent=4, separators=(',', ': '))
			print(resp2)	
			if output["found"]==1:
				found='FOUND'
			else:
				found='NOT FOUND'
			line_out=domain+';'+found+';'+la_categorie+';'+status+';'+str(round(output["securerank2"],2))+';'+str(round(output["asn_score"],2))+';'+str(round(output["prefix_score"],2))+';'+str(round(output["rip_score"],2))+';'+output["attack"]+';'+output["threat_type"]
			fh.write(line_out)
			fh.write('\n')
	fh.close()
		
if __name__ == '__main__':
	print('This script extract every domain name contained into a web page and retrieves all domain\'s security information from Umbrella Investigate BackEnd')
	print()
	print('==================================================================================================================================')
	print()	
	url=input("enter a HTTP domain a URL to check ( ex www.cars.com ) : ")
	# cleanup
	url = url.replace('https://','')
	url = url.replace('HTTPS://','')
	url = url.replace('http://','')
	url = url.replace('HTTP://','')

	url='https://' + url
	html=requests.get(url).text
	links = re.findall('"((http|ftp)s?://.*?)"', html)
	domains =[]
	for link in links:
		#print (link[0])
		domain=link[0].replace("https://","")
		domain=domain.replace("http://","")
		domain=domain.split('/')
		if domain[0] not in domains:
			domains.append(domain[0])
	# get token from token.txt
	fa = open("token.txt", "r")
	investigate_api_key = fa.readline()
	fa.close()
	#create header for authentication and set limit of sample return to 1
	headers = {
	'Authorization': 'Bearer ' + investigate_api_key,
	'limit': '1'
	}			
	categories=retrieve_categorie(headers)
	check_categorization(headers,domains,categories)
	