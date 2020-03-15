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

	Test access to Investigate
'''
import requests
import json
from datetime import datetime

# get token from token.txt
fa = open("token.txt", "r")
investigate_api_key = fa.readline()
fa.close()


# URL needed for the domain status and category
investigate_url = "https://investigate.api.umbrella.com/domains/categorization/"

# domain that will be checked
domain = "internetbadguys.com"

#create header for authentication
headers = {
  'Authorization': 'Bearer ' + investigate_api_key
}

# assemble the URI, show labels give readable output
get_url = investigate_url + domain + "?showLabels"

# do GET request for the domain status and category
req = requests.get(get_url, headers=headers)

# time for timestamp of verdict domain
time = datetime.now().isoformat()

# error handling if true then the request was HTTP 200, so successful
if(req.status_code == 200):
    # retrieve status for domain
    output = req.json()
    domain_output = output[domain]
    domain_status = domain_output["status"]
    # walk through different options of status
    if(domain_status == -1):
        print("SUCCESS: The domain %(domain)s is found MALICIOUS at %(time)s" % {'domain': domain, 'time': time})
    elif(domain_status == 1):
        print("SUCCESS: The domain %(domain)s is found CLEAN at %(time)s" % {'domain': domain, 'time': time})
    else:
        print("SUCCESS: The domain %(domain)s is found UNDEFINED / RISKY at %(time)s" % {'domain': domain, 'time': time})
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" % {'error': req.status_code})
