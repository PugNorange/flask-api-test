#
# app.py
# Kizer modules API
# Created by Che Blankenship on 07/27/2021
#

import io
import csv
from flask import Flask, send_file


app = Flask(__name__)


# base route
# @app.route("/")
# def index():
#     return "This is v1 Kizer modules API."


# GET result KML file.
# @app.route("/v1/kml3da/get-kml")
@app.route("/")
def kmlDownload():
    # open file
    with open("Paths1.KML", "r") as f:
        data = f.read()
    # define string memory
    proxy = io.StringIO(data)
    # define bytes memory
    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode())
    mem.seek(0)

    # # for row in f:
    # proxy = io.StringIO()
    # writer = csv.writer(proxy)
    # # writer.writerow(row)
    # writer.writerow(f)
    # # Creating the byteIO object from the StringIO Object
    # mem.write(proxy.getvalue().encode())
    # # seeking was necessary. Python 3.5.2, Flask 0.12.2
    # mem.seek(0)
    #
    # proxy.close()

    return send_file(
        mem,
        as_attachment=True,
        attachment_filename='paths-result.kml',
        mimetype='text/kml'
    )


# # GET result KML file.
# @app.route("/v1/kml3da/get-kml")
# def kmlDownload():
#     row = ['hello', 'world']
#     proxy = io.StringIO()
#     writer = csv.writer(proxy)
#     writer.writerow(row)
#     # Creating the byteIO object from the StringIO Object
#     mem = io.BytesIO()
#     mem.write(proxy.getvalue().encode())
#     # seeking was necessary. Python 3.5.2, Flask 0.12.2
#     mem.seek(0)
#     proxy.close()
#
#     return send_file(
#         mem,
#         as_attachment=True,
#         attachment_filename='kml-result.csv',
#         mimetype='text/csv'
#     )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
