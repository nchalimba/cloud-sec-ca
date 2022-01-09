from flask import Flask
import subprocess
from os.path import expanduser
import boto3
from datetime import datetime

home = expanduser("~")
s3_client = boto3.client("s3")
app = Flask(__name__)


@app.route("/certificate")
def get_certificate():
    process = subprocess.run(
        [
            "touch",
            home + "/Documents/cis/cis21-assignment8/server/sample.txt",
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if process.returncode != 0:
        return "INTERNAL_SERVER_ERROR", 500

    process = subprocess.run(
        [
            "ls",
            home + "/Documents/cis/cis21-assignment8/server/",
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    print(process.stdout)
    s3_client.upload_file(
        "sample.txt", "7342c6f2-8", "sample_{}.txt".format(str(datetime.now()))
    )
    return "OK"


if __name__ == "__main__":
    app.run()
