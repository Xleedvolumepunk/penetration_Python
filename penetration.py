import requests
from concurrent.futures import ThreadPoolExecutor

def check_path(url, wordlist, threads, proxy=None, output_file=None):
    with open(wordlist, 'r') as f:
        paths = f.readlines()
    paths = [path.strip() for path in paths]

    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    else:
        proxies = None

    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for path in paths:
            full_url = url + path
            future = executor.submit(make_request, full_url, proxies)
            results.append(future)

    with open(output_file, 'w') as output:
        for result in results:
            response = result.result()
            if response is not None and response.status_code != 404:
                output.write(f"URL: {response.url} | Status Code: {response.status_code}\n")
                print(f"URL: {response.url} | Status Code: {response.status_code}")

def make_request(url, proxies):
    try:
        response = requests.head(url, proxies=proxies)
        if response.status_code == 405:
            response = requests.get(url, proxies=proxies)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred for URL: {url} - {e}")

if name == '__main__':
    url = 'http://0.0.0.0:1111/'  
    wordlist = 'wordlist.txt' 
    threads = 10
    proxy = None 
    output_file = 'output.txt'

    check_path(url, wordlist, threads, proxy, output_file)