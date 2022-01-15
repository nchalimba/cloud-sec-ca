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
    file = None
    currentTimeStamp = None
    while not file:
        time.sleep(1)
        response = s3_client.list_objects_v2(Bucket="7342c6f2-8", Prefix=prefix)
        objects = response.get("Contents", None)
        if objects and len(objects) > 0:
            objects.sort(key=lambda x: x["LastModified"])
            print(objects)


if __name__ == "__main__":
    main()
