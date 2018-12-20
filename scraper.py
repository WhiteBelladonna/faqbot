from bs4 import BeautifulSoup
import requests

sitelink = "https://tickets.leipziger-messe.de/app.php/api/v1/frontend/contingent/5b7a8f9fc8599262770218f5?language=de"

def crawlTickets():
    page = requests.get(sitelink)
    soup = BeautifulSoup(page.content, "html.parser")

    html = list(soup.children)
    rem = list(html)[0]
    rem = rem.split(",")

    remaining = rem[0]
    remaining = remaining[19:]

    sold = rem[3]
    sold = sold[16:]

    max = rem[4]
    max = max[12:]
    max = max[:-1]

    return remaining, sold, max