import boto3
import requests
import auth

def check_my_ip() -> str:
    try:
        ip_raw = requests.get("http://checkip.dyndns.com/")
        ip_raw.close()
        return str(ip_raw.text.split(':')[1].strip().rstrip('</body></html>\r\n'))
    except Exception as e:
        print("Error occured whie fetching global IP : {}".format(str(e)))
        return "0"

def create_aws_record(zoneid :str, domain :str, record :str, type :str) -> None:
    client = boto3.client(
        'route53',
        aws_access_key_id=auth.aws_access_key_id,
        aws_secret_access_key=auth.aws_access_secret,
        region_name="ap-northeast-1"
    )

    client = boto3.client(
        'route53',
        aws_access_key_id=auth.aws_access_key_id,
        aws_secret_access_key=auth.aws_access_secret,
        region_name="ap-northeast-1"
    )
    client.change_resource_record_sets(
    HostedZoneId=zoneid,
    ChangeBatch={
        'Comment': 'AutomaticDDNS',
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
        create_aws_record(auth.zoneid, domain, ip, "A")

main_job()