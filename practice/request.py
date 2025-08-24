import requests, json

print("Request lib test")

response = requests.get("http://www.python.org")
print(response.json)

print("Status code: " + str(response.status_code))

print("----Header Response----")
for header,value in response.request.headers.items():
    print(header , '-->',value)


print("----Header request----")
for header,value in response.request.headers.items():
    print(header,'-->',value)

