import requests


urls = ['https://coinmarketcap.com/rankings/exchanges/{}', 'https://coinmarketcap.com/{}']
coins = []
exchanges = []
results = [exchanges, coins]
for result_array, url in zip(results,urls):
   for i in range(3):
      response = requests.get(url.format(i))
      response = response.content.decode()
      response = response.split('\n')
      for r in response:
          if '<tr id=\"' in r:
              result = r.split("id-")[1]
              result = result.split("\"")[0]
              result_array.append(result)
          if not 'exchanges' in url:
              if '<span class=\"hidden-xs\">' in r:
                  result = r.split('hidden-xs\">')[1]
                  result = result.split('<')[0]
                  result_array.append(result)

print(coins)
print(exchanges)
