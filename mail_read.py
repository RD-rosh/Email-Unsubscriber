from dotenv import load_dotenv
import os
import email
import imaplib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlparse

load_dotenv()
username = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# Connect to mail
def connect_to_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')
    return mail

#Get unsubscribe links from mails ]
def read_mails():
    mail = connect_to_mail()
    date_since = (datetime.now() - timedelta(days=3)).strftime('%d-%b-%Y')
    #get mail ids that body contains unsubscribe
    _, search_data = mail.search(None, f'(SINCE {date_since} BODY "unsubscribe")')
    #get matching mailIds
    mail_ids = search_data[0].split()

    visited_domains = set() #to stop iterative printing of same domains 
    links = []

    for num in mail_ids:
        _, data = mail.fetch(num, "(RFC822)") #RFC822 is a mail format (header and body) for each mailID
        msg = email.message_from_bytes(data[0][1])

        #if msg has multiple parts, walks thru each part and HTMl content is decoded
        for part in msg.walk() if msg.is_multipart() else [msg]:
            if part.get_content_type() == 'text/html':
                html_content = decode_payload(part)
                if html_content:
                    links.extend(extract_links(html_content, visited_domains))

    mail.logout()
    return links

# Decode html content
def decode_payload(part):
    try:
        #decode using UTF8
        return part.get_payload(decode=True).decode('utf-8')
    except UnicodeDecodeError:
        try:
            #if cannot decode using utf8, use ISO8859
            return part.get_payload(decode=True).decode('ISO-8859-1')
        except UnicodeDecodeError:
            print("Could not decode part of the email.")
            return None


#extract html content
def extract_links(html_content, visited_domains):
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_links = []
    
    #find if content has <a> tags in it for hyperllinks
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'unsubscribe' in href.lower():
            #get domain_name to avoid duplicates
            domain = urlparse(href).netloc
            if domain and domain not in visited_domains:
                visited_domains.add(domain)
                extracted_links.append(href)
    return extracted_links


