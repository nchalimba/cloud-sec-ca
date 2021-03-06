from flask import Flask
import subprocess
from os.path import expanduser
import boto3
from datetime import datetime
import time
import os

home = expanduser("~")
ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# s3_client = boto3.client("s3")
s3_client = boto3.resource(
    "s3", aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY
)

app = Flask(__name__)


@app.route("/certificate")
def get_certificate():
    target_pki_folder = "{}/pki".format(os.getcwd())
    # remove pki folder if existing
    # command_1 = "rm -rf {}/cloud-sec-ca/easy_rsa/pki".format(home)
    command_2 = "{}/cloud-sec-ca/easy_rsa/easyrsa init-pki".format(home)
    command_3 = "{}/cloud-sec-ca/easy_rsa/easyrsa build-ca nopass".format(home)
    command = "{0} && {1}".format(command_2, command_3)
    print("Command: {}".format(command))
    stream = os.popen(command)
    output = stream.read()
    # process = subprocess.run(command, capture_output=True, shell=True)

    """
    process = subprocess.run(
        ["rm", "-rf", "{}/cloud-sec-ca/easy_rsa/pki".format(home)],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if process.returncode != 0:
        return "INTERNAL_SERVER_ERROR", 500

    process = subprocess.run(
        [
            "{}/cloud-sec-ca/easy_rsa/easyrsa".format(home),
            "init-pki",
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if process.returncode != 0:
        return "INTERNAL_SERVER_ERROR", 500

    process = subprocess.run(
        ["{}/cloud-sec-ca/easy_rsa/easyrsa".format(home), "build-ca", "nopass"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    """
    print(output)
    timeout = 5
    counter = 0
    while (
        not os.path.exists("{}/ca.crt".format(target_pki_folder)) and counter < timeout
    ):
        print("ca creation in progress...")
        time.sleep(1)
        counter += 1

    # if process.returncode != 0:
    #   return "INTERNAL_SERVER_ERROR", 500
    print("uploading file")
    s3_client.meta.client.upload_file(
        "{}/ca.crt".format(target_pki_folder),
        "7342c6f2-8",
        "ca_{}.crt".format(str(datetime.now())),
    )
    return "OK"


if __name__ == "__main__":
    app.run()
