from distutils import command
import time
import boto3
import os
from os.path import expanduser


home = expanduser("~")
ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
s3_client = boto3.client(
    "s3", aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY
)
prefix = "input"


def main():
    while True:
        time.sleep(10)
        response = s3_client.list_objects_v2(Bucket="7342c6f2-8", Prefix=prefix)
        objects = response.get("Contents", None)

        if not objects or len(objects) == 0:
            continue

        objects.sort(key=lambda x: x["LastModified"])  # oldest first
        for current_file in objects:
            # TODO: get name
            file_key = current_file["Key"]
            filename = get_filename_from_key(file_key)
            filename_split = filename.split("_")
            if len(filename_split) < 2:
                print("File with name {} has false name format".format(filename))
                continue
            group_name = filename_split[1]
            create_certificate(group_name, filename)
            move_file(filename)


def get_filename_from_key(key: str) -> str:
    filename_list = key.split("/")[1].split(".")
    filename_list.pop()
    return ".".join(filename_list)


def create_certificate(group_name: str, filename: str):
    target_pki_folder = "{}/pki".format(os.getcwd())
    command1 = 'echo "{0}" | {1}/cloud-sec-ca/easy_rsa/easyrsa init-pki'.format(
        "yes", home
    )
    command2 = 'echo "{0}" | {1}/cloud-sec-ca/easy_rsa/easyrsa build-ca nopass'.format(
        group_name, home
    )
    command3 = (
        'echo "{0}" | {1}/cloud-sec-ca/easy_rsa/easyrsa gen-req {2} nopass'.format(
            group_name, home, filename
        )
    )
    command4 = (
        'echo "{0}" | {1}/cloud-sec-ca/easy_rsa/easyrsa sign-req server {2}'.format(
            "yes", home, filename
        )
    )

    total_command = "{0} && {1} && {2} && {3}".format(
        command1, command2, command3, command4
    )
    print("Command: {}".format(total_command))
    stream = os.popen(command)
    output = stream.read()
    print(output)

    # TODO: upload crt
    folder = "certificates"
    pass


def move_file(filename: str):
    folder = "done"


if __name__ == "__main__":
    main()
