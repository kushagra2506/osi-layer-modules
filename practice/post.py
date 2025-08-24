import requests, json

data_dictionary = {"id": "0123456789"}




headers = {
    "Content-Type": "application/json",
    "Accept":"application/json"
}

res = requests.get("http://127.0.0.1:42001",cookies="PHPSESSID")





print(res.text)