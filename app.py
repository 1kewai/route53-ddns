import boto3
import requests

def check_my_ip() -> str:
    try:
        ip_raw = requests.get("http://checkip.dyndns.com/")
        ip_raw.close()
        return str(ip_raw.text.split(':')[1].strip().rstrip('</body></html>\r\n'))
    except Exception as e:
        print("Error occured whie fetching global IP : {}".format(str(e)))
        return "0"

check_my_ip()
