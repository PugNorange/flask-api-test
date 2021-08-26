#
# app.py
# Kizer modules API
# Created by Che Blankenship on 07/27/2021
#

import io
import os
import csv
import json
from flask import Flask, flash, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename

import boto3
from boto3 import session
from botocore.client import Config
from boto3.s3.transfer import S3Transfer
import uuid

# Modules
from modules.KML3DA import KML3DA

# Config
with open('config.json', 'r') as f:
    configFile = json.load(f)
#Use the API Keys you generated at Digital Ocean
ACCESS_ID   = configFile['production']['accessId']
SECRET_KEY  = configFile['production']['secretKey']
# Initiate session
session = session.Session()



app = Flask(__name__)

# current directory
dirPath = os.path.dirname(os.path.realpath(__file__))


# base route
@app.route("/", methods=['GET', 'POST'])
def index():
    return "This is v1 Kizer modules API."



# Generate a spider web 
@app.route('/v1/kml3da', methods=['POST'])
def loadFile():
    sessionUUID = str(uuid.uuid1())
    # check if the post request has the file content
    inputCSVFile = request.files['inputCSV']
    if 'inputCSV' not in request.files:
        flash('No file part')
        return redirect('/')

    # KML3DA class
    testkml = KML3DA()
    # load the input csv file
    bytesData   = inputCSVFile.read()
    # save it temporary on temp file
    tempCsvFilePath = dirPath + '/' + 'temp-' + sessionUUID + '.csv'
    tempCsvFile = open('temp-' + sessionUUID + '.csv', 'wb')
    tempCsvFile.write(bytesData)
    tempCsvFile.close()
    # get the file path to pass it to kml3da module
    testkml.generateKML(dirPath, tempCsvFilePath, "result-" + sessionUUID, "Red", "Green")
    # Process of uploading to Digital Ocean Spaces
    client = session.client(
        's3',
        region_name='sfo3',
        endpoint_url='https://sfo3.digitaloceanspaces.com',
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=SECRET_KEY
    )
    bucketAccessUrl = 'https://kizer-api-bucket.sfo3.digitaloceanspaces.com/'
    folderName = 'kml3da'
    outputFileName = 'result-' + sessionUUID + '.kml'
    transfer = S3Transfer(client)
    # upload to Digital Ocean Space
    transfer.upload_file(
        outputFileName,     # dir path and file name
        'kizer-api-bucket', # digital ocean space name
        folderName + '/' + outputFileName # save to folder/file name
    )
    # This makes the file you are have specifically uploaded public by default.
    response = client.put_object_acl(
        ACL='public-read',
        Bucket='kizer-api-bucket',
        Key="%s/%s" % (folderName, outputFileName)
    )
    # delete the temp/result files generated on local
    os.remove('temp-' + sessionUUID + '.csv')
    os.remove(outputFileName)
    # define where the file is saved on cloud.
    resultSavedLocation = bucketAccessUrl + folderName + '/' + outputFileName
    # return json data
    return jsonify(
        status=200,
        message='KML3DA API successfuly executed!',
        data=resultSavedLocation,
    )




if __name__ == "__main__":
    app.run(host='0.0.0.0')
