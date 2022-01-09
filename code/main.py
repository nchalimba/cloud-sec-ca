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
    # remove pki folder if existing
    # command_1 = "rm -rf {}/cloud-sec-ca/easy_rsa/pki".format(home)
    command_2 = "{}/cloud-sec-ca/easy_rsa/easyrsa init-pki".format(home)
    command_3 = "{}/cloud-sec-ca/easy_rsa/easyrsa build-ca nopass".format(home)
    command = "{0} && {1}".format(command_2, command_3)
    process = subprocess.run(command, capture_output=True, shell=True)

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

    if process.returncode != 0:
        return "INTERNAL_SERVER_ERROR", 500

    s3_client.upload_file(
        "{}/cloud-sec-ca/easy_rsa/pki/ca.crt".format(home),
        "7342c6f2-8",
        "ca_{}.crt".format(str(datetime.now())),
    )
    return "OK"


if __name__ == "__main__":
    app.run()
