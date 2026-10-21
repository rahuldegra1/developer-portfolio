import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Target a standard website
url = "https://quotes.toscrape.com/"

# 2. Download the raw HTML of the page
response = requests.get(url)
html_content = response.text

# 3. Feed the chaotic HTML to BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# 4. Command the scraper to find specific HTML tags
# (On this site, quotes are in <span class="text"> and authors are in <small class="author">)
raw_quotes = soup.find_all("span", class_="text")
raw_authors = soup.find_all("small", class_="author")

# 5. Clean the text and pair them up in a list of dictionaries
scraped_data = []
for i in range(len(raw_quotes)):
    scraped_data.append(
        {
            "Quote": raw_quotes[i].text.strip(
                "“”"
            ),  # Strips the smart quotes off the edges
            "Author": raw_authors[i].text,
        }
    )

# 6. The Pandas Bridge
df = pd.DataFrame(scraped_data)

print("--- Successfully Scraped Data ---")
print(df.head())
