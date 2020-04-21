from datetime import datetime
import json
import requests
'''
Copyright (c) 2020 Cisco and/or its affiliates.

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

	it retrieves all umbrella categories and their index. The result is stored into a text file
'''

# get token from token.txt
fa = open("token.txt", "r")
investigate_api_key = fa.readline()
fa.close()
# URL needed for the domain status and category

investigate_url = "https://investigate.api.umbrella.com/domains/categories/"

#create header for authentication and set limit of sample return to 1
headers = {
'Authorization': 'Bearer ' + investigate_api_key,
'limit': '1'
}

# time for AlertTime and EventTime when domains are added to Umbrella
time = datetime.now().isoformat()
	
fh = open("categories.txt", "w")
get_url = investigate_url
# do GET request for the domain status and category
request_get = requests.get(get_url, headers=headers)
if(request_get.status_code == 200):
	# store all categories into a variable named output
	output = request_get.json() 
	#display output into a readable format   BUT #output is actually a list
	resp2=json.dumps(output,sort_keys=True,indent=4, separators=(',', ': '))
	print(resp2)
	#store it in the text file
	fh.write(resp2)
	fh.write('\r\n')
	#display all categories key and values
	for cle,valeur in output.items():
		print (cle+' '+ valeur)
fh.close()