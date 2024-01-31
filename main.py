# Author:  Luke Moll
# Date:    2024-01-30

import requests
from bs4 import BeautifulSoup


# this class might be helpful to scrape multiple websites in the future
class WebScraper:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def get_response(self):
        # returns whether the website is responding or not
        if self.response.status_code == 200:
            return True
        else:
            return False

    def get_title(self):
        # prints the text of all "h1" tags the website contains
        headline = self.soup.find("h1").get_text()
        print(headline + "\n")

    def get_links(self):
        # prints the href attribute (the link) of all "a" tags the website contains
        link_counter = 0
        link_list = []
        for link in self.soup.find_all("a"):
            links = link.attrs["href"]
            if '#' not in links:
                link_list.append(links)
                print(links)
                link_counter += 1
        print(link_counter, "links found\n")
        print("would you like to save the found links?")
        print("1 - yes")
        print("2 - no")
        x = self.get_user_input()
        if x == 1:
            self.save_links(link_list)
        elif x == 2:
            print("exiting")
            return

    @staticmethod
    def save_links(link_list):
        print("Which file format?")
        print("1 - .txt file")
        while True:
            x = int(input())
            if x == 1:
                with open('links.txt', 'w') as f:
                    for link in link_list:
                        f.write("%s\n" % link)  # puts every link in a separate line
                print("links saved in 'links.txt'")
                break
            else:
                print("wrong selection, try again")

    @staticmethod
    def get_user_input():
        while True:
            x = int(input())
            if x in [1, 2]:
                return x
            print("wrong selection, try again")


def main():
    scraper = WebScraper("https://luke.molls.org/")  # change this to scrape different website
    actions = {1: "Request response", 2: "Get the title", 3: "Get every link", 4: "End program"}
    while True:
        print("Scraping " + scraper.url)
        for key, value in actions.items():
            print(f"{key} - {value}")

        x = int(input())

        if x == 1:
            if scraper.get_response():
                print("request successful\n")
            elif not scraper.get_response():
                print("request failed\n")
        elif x == 2:
            scraper.get_title()
        elif x == 3:
            scraper.get_links()
        elif x == 4:
            break
        else:
            print("wrong selection, try again\n")


if __name__ == "__main__":
    main()
