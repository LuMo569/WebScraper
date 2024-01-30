# Author:  Luke Moll
# Date:    2024-01-30

import requests
from bs4 import BeautifulSoup

url = "https://luke.molls.org/"  # change to scrape different website
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
posts = soup.find_all("div", class_="post-item")


def getresponse():
    # returns whether the website is responding or not
    if response.status_code == 200:
        return True
    else:
        return False


def gettitle():
    # prints the text of all "h1" tags the website contains
    headline = soup.find("h1").get_text()
    print(headline + "\n")


def getlinks():
    # prints the href attribute (the link) of all "a" tags the website contains
    link_counter = 0
    for link in soup.find_all("a"):
        links = link.attrs["href"]
        if '#' not in links:
            print(links)
            link_counter += 1
    print(link_counter, "links found")
    print("\n")


while True:

    print("Scraping " + url)
    print("Possible actions:")
    print("1 - request response")
    print("2 - get the title")
    print("3 - get every link")
    print("4 - end program")

    x = int(input())

    if x == 1:
        if getresponse():
            print("request successful\n")
        elif not getresponse():
            print("request failed\n")
    elif x == 2:
        gettitle()
    elif x == 3:
        getlinks()
    elif x == 4:
        break
    else:
        print("wrong selection, try again\n")

