import requests

def fetch_links(links):
    success_links = []
    failed_links = []

    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                success_links.append(link)
            else:
                failed_links.append((link, response.reason))
        except Exception as err:
            failed_links.append((link, str(err)))

    return success_links, failed_links



