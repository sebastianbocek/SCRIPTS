import requests
from bs4 import BeautifulSoup
import re

# Common subpages to try for contact info
COMMON_PATHS = ['/contact', '/about', '/support', '/contact-us', '/contacts']
HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 10

def extract_emails(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract emails from visible text
    text = soup.get_text()
    text_emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))

    # Extract emails from mailto links
    mailto_emails = set()
    for a in soup.find_all('a', href=True):
        if a['href'].startswith("mailto:"):
            email = a['href'].split("mailto:")[1].split('?')[0]
            if '@' in email:
                mailto_emails.add(email)

    # Combine and clean
    all_emails = text_emails | mailto_emails
    cleaned_emails = {email.strip().strip(".,;:\u200b") for email in all_emails}
    return cleaned_emails

def scrape_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 200:
            return extract_emails(response.text)
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
    return set()

def normalize_url(url):
    if not url.startswith("http"):
        url = "http://" + url
    return url.rstrip("/")

def main():
    input_file = "websites.txt"
    output_file = "emails.txt"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_urls = [line.strip() for line in f if line.strip()]
    
    all_emails = set()

    for base_url in raw_urls:
        base_url = normalize_url(base_url)
        print(f"\n🔍 Scraping: {base_url}")

        # Scrape main page
        all_emails |= scrape_page(base_url)

        # Scrape common subpages
        for path in COMMON_PATHS:
            full_url = base_url + path
            all_emails |= scrape_page(full_url)

    # Clean, sort, and write only the emails
    final_emails = sorted(all_emails)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(final_emails))

    print(f"\n✅ Done! {len(final_emails)} emails saved to {output_file}")

if __name__ == "__main__":
    main()
