import sys
import re
import urllib.request

def strip_tags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

def fetch_emails(domain_name):
    emails = set()
    page_counter = 0
    try:
        while page_counter < 50:
            url = f'http://www.google.com/search?q=%40{domain_name}&hl=en&lr=&ie=UTF-8&start={page_counter}&sa=N'
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
            with urllib.request.urlopen(request) as response:
                text = response.read().decode('utf-8')
                found_emails = re.findall(r'[\w\.\-]+@'+re.escape(domain_name), strip_tags(text))
                emails.update(found_emails)
            page_counter += 10
    except IOError:
        print("Cannot connect to Google Web.")
    return emails

if len(sys.argv) != 2:
    print("\nUsage: python3 script.py <domain>\n")
    sys.exit(1)

domain_name = sys.argv[1]
emails = fetch_emails(domain_name)

for email in emails:
    print(email)
