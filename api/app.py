#
# app.py
# Kizer modules API
# Created by Che Blankenship on 07/27/2021
#

from flask import Flask, send_file
app = Flask(__name__)



# GET result KML file.
@app.route("/v1/kml3da/get-kml")
def index():
    return "Hello from ViralML!!!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
