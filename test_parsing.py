from urllib.request import urlopen, Request
import requests


req = Request(
    url='https://coinmarketcap.com/currencies/bnb/',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
)

data = urlopen(req).read().decode("utf-8")
# print(data)

start_index = 0
end_index = data.find('alt="BNB"')
url = ''

while True:
    if data[end_index] == '"':
        start_index = end_index - 1
        while data[start_index] != '"':
            start_index -= 1

        if 'https' in data[start_index + 1: end_index]:
            url = data[start_index + 1: end_index]
            break
    end_index -= 1

print(url)

response = requests.get(url)
with open('data.png', 'wb') as file:
    file.write(response._content)
