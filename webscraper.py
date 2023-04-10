import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com"

# Make a request to the website and get the content
response = requests.get(url)
content = response.content

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Find all the quote containers
quote_containers = soup.find_all("div", class_="quote")

# Iterate through each container and extract the quote and author
for container in quote_containers:
    quote = container.find("span", class_="text").text
    author = container.find("small", class_="author").text
    print(f"Quote: {quote}\nAuthor: {author}\n")