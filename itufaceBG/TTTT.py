import requests
headers = {
    'Connection': 'close',
}
data = requests.get('http://finup-lend-app-schedule.lendapp.beta/test/pushToLend',headers=headers)
print(data.status_code)