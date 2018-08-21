import json
import urllib.request
from time import sleep

# type token contract address
token_addr = ""
if not token_addr:
    print("Define token_addr")
    exit(0)
url_get_token_addr = 'http://api.ethplorer.io/getTokenInfo/{0}?apiKey=freekey'.format(token_addr)
res = json.load(urllib.request.urlopen(url_get_token_addr))

holders_cnt = res['holdersCount']
num_pages = (holders_cnt+9)//10
denom = 10 ** int(res['decimals'])

template_url = "https://ethplorer.io/service/service.php?data={0}&page=tab%3Dtab-holders%26holders%3D{1}"
for i in range(num_pages):
    page = i+1
    url = template_url.format(token_addr, page)
    data = ''
    while len(data) == 0:
        try:
            data = json.load(urllib.request.urlopen(url))
        except urllib.error.HTTPError:
            sleep(1)
            continue

    print('----------------------------page {}------------------------------------'.format(page))
    for account in data['holders']:
        print("account: {0} balance: {1}".format(account['address'], format(account['balance']/denom, ",")))
