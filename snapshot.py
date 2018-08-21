import json
import urllib.request
from time import sleep

template_url = 'https://ethplorer.io/service/service.php?data={0}&page=tab%3Dtab-holders%26pageSize%3D{1}&showTx=all'
margin_holders = 10
# type token contract address
token_addr = ""
if not token_addr:
    print("Define token_addr")
    exit(0)


def get_token_info(_token_addr):
    url_get_token_addr = 'http://api.ethplorer.io/getTokenInfo/{0}?apiKey=freekey'.format(_token_addr)
    return json.load(urllib.request.urlopen(url_get_token_addr))


def get_token_data(_token_addr, _holders_cnt):
    url = template_url.format(token_addr, holders_cnt)
    data = ''
    while len(data) == 0:
        try:
            data = json.load(urllib.request.urlopen(url))
        except urllib.error.HTTPError:
            sleep(1)
            continue
    return data


# get num. of holders / token decimals
token_info = get_token_info(token_addr)
holders_cnt = token_info['holdersCount'] + margin_holders
denom = 10 ** int(token_info['decimals'])

res_holders_cnt = 0
new_holders_cnt = holders_cnt
while res_holders_cnt != new_holders_cnt:
    token_data = get_token_data(token_addr, holders_cnt)
    # num of holders in output
    res_holders_cnt = len(token_data['holders'])
    # num of total holders
    new_holders_cnt = token_data['pager']['holders']['total']
    holders_cnt = new_holders_cnt + margin_holders

for account in token_data['holders']:
    print("account: {0} balance: {1}".format(account['address'], format(account['balance']/denom, ",")))
