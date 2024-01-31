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
        return self.response.status_code == 200

    def get_title(self):
        return self.soup.find("h1").get_text()

    def get_links(self):
        return [link.attrs["href"] for link in self.soup.find_all("a") if '#' not in link.attrs["href"]]

    @staticmethod
    def save_links(links):
        with open('links.txt', 'w') as f:
            for link in links:
                f.write("%s\n" % link)  # puts every link in a separate line
        print("links saved in 'links.txt'")

    @staticmethod
    def get_user_input(valid_inputs):
        while True:
            user_input = int(input())
            if user_input in valid_inputs:
                return user_input
            print("wrong selection, try again")


def main():
    # changes to let user choose url:
    # print("Please enter the URL you want to scrape:")
    # url = input()
    # scraper = WebScraper(url)
    scraper = WebScraper("https://luke.molls.org/")  # change this to scrape different website
    actions = {1: "Request response", 2: "Get the title", 3: "Get every link", 4: "End program"}
    while True:
        print("Scraping " + scraper.url)
        for key, value in actions.items():
            print(f"{key} - {value}")

        user_choice = scraper.get_user_input(actions.keys())

        if user_choice == 1:
            print("request successful\n") if scraper.get_response() else print("request failed\n")
        elif user_choice == 2:
            print(scraper.get_title())
        elif user_choice == 3:
            links = scraper.get_links()
            print("\n".join(links))
            print(len(links), "links found")
            print("would you like to save the found links?")
            print("1 - yes")
            print("2 - no")
            if scraper.get_user_input([1, 2]) == 1:
                print("Which file format?")
                print("1 - .txt file")
                if scraper.get_user_input([1]) == 1:
                    scraper.save_links(links)
        elif user_choice == 4:
            break
        else:
            print("wrong selection, try again\n")


if __name__ == "__main__":
    main()
