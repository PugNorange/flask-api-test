#
# Example of how to call kizer module API
# Kizer Module API v1
# Created by Che Blankenship on 08/25/2021
#

# Libs
import requests
import json
import boto3
from boto3 import session
from botocore.client import Config
from boto3.s3.transfer import S3Transfer

# Modules
from modules.KML3DA import KML3DA

# Load the config file
with open('config.json', 'r') as f:
    configFile = json.load(f)


# Example of how to call KML3DA API
def apiCallExample():
    url = configFile['production']['baseUrl'] + 'v1/kml3da'
    files = {'inputCSV': open('Paths2.csv', 'rb')}
    getdata = requests.post(url, files=files)
    print(json.dumps(json.loads(getdata.text), indent=4, sort_keys=True))



# run to call v1/kml3da
apiCallExample()
