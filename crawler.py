import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

visited = set()
to_visit = ["https://i-investng.com"]

all_urls = []


def normalize_url(url):
    """Normalize URL by removing trailing slash and fragment."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")  # remove trailing slash
    normalized = urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))
    return normalized


while len(to_visit) > 0:
    current = to_visit.pop()

    if current in visited:
        continue

    visited.add(current)
    all_urls.append(current)

    try:
        res = requests.get(current, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = normalize_url(urljoin(current, a["href"]))  # type: ignore
            if (
                link.startswith("https://i-investng.com")
                and link not in visited
                and link not in to_visit
            ):
                to_visit.append(link)
                print(link)

    except Exception as e:
        print(e)
        pass

with open("urls.txt", "w") as file:
    for url in all_urls:
        file.write(url + "\n")  # Add a newline after each URL

print("URLs written to urls.txt")

print("Printing all urls")
print(all_urls)
