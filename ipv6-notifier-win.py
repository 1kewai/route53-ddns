import boto3
import auth
import time
import subprocess
import re

def check_my_ip():
  ip_raw = subprocess.run(["ipconfig"], stdout=subprocess.PIPE)
  ips = str(ip_raw.stdout).replace(" ","").split("\\n")
  address = ""
  for ip in ips:
      if ip.startswith("IPv6 アドレス . . . . . . . . . . . .:"):
          address = ip[5:ip.find("prefixlen")]
          break
  return address

def create_aws_record(zoneid :str, domain :str, record :str, type :str) -> None:
    client = boto3.client(
        'route53',
        aws_access_key_id=auth.aws_access_key_id,
        aws_secret_access_key=auth.aws_access_secret,
        region_name="ap-northeast-1"
    )
    print("Updating {} to {}".format(domain, record))
    client.change_resource_record_sets(
    HostedZoneId=zoneid,
    ChangeBatch={
        'Comment': 'AutomaticDDNS-v6',
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': domain,
                    'Type': type,
                    'TTL': 30,
                    'ResourceRecords': [
                        {
                            'Value': record
                        },
                    ],
                }
            },
        ]
    }
)

def main_job():
    ip = check_my_ip()
    for domain in auth.domains:
        create_aws_record(auth.zoneid, domain, ip, "AAAA")

main_job()