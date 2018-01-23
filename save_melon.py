import requests

def save():
    response = requests.get('https://www.melon.com/chart/index.htm')
    f = open('melon.html', 'wt')
    f.write(response.text)
    f.close()

if __name__ == '__main__':
    save()