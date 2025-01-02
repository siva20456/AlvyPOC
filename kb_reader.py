# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse

# base_url = 'https://certification.talview.com/support/solutions'

# def is_valid_url(url, base_domain):
#     parsed_url = urlparse(url)
#     if parsed_url.netloc == base_domain and not any(exclusion in parsed_url.path for exclusion in ['/login', '/account', '/admin','javascript:print()']):
#         return True
#     return False

# def scrape_page(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     page_title = soup.title.string if soup.title else 'No Title'
#     paragraphs = soup.find_all('p')
#     headings_h3 = soup.find_all('h3')
#     spans = soup.find_all('span')
#     headings_h1 = soup.find_all('h1')
    
#     page_paragraphs = [para.get_text() for para in paragraphs]
#     page_headings_h3 = [h3.get_text() for h3 in headings_h3]
#     page_spans = [span.get_text() for span in spans]
#     page_headings_h1 = [h1.get_text() for h1 in headings_h1]
    
#     print(f"Page Title: {page_title}")
#     print(f"Paragraphs: {page_paragraphs[:3]}...")  # Display the first 3 paragraphs
#     print(f"Headings (h3): {page_headings_h3[:3]}...")  # Display the first 3 h3 headings
#     print(f"Spans: {page_spans[:3]}...")  # Display the first 3 span elements
#     print(f"Headings (h1): {page_headings_h1[:3]}...")
    
#     # Extracting all links from the page and filter unwanted URLs
#     links = soup.find_all('a', href=True)
#     valid_links = [urljoin(url, link['href']) for link in links if is_valid_url(urljoin(url, link['href']), urlparse(base_url).netloc)]

#     print(f"Page Title: {page_title}")
#     print(f"Paragraphs: {page_paragraphs[:3]}...")  # Display the first 3 paragraphs
#     return valid_links  # Return valid links to crawl next

# # Crawl the base URL
# def crawl_site(start_url):
#     visited_urls = set()  # To track visited pages
#     urls_to_visit = [start_url]

#     while urls_to_visit:
#         current_url = urls_to_visit.pop()
#         if current_url in visited_urls:
#             continue
        
#         visited_urls.add(current_url)
#         print(f"Scraping URL: {current_url}")
        
#         # Scrape the page and get all valid links
#         next_urls = scrape_page(current_url)
        
#         # Add new URLs to the list (to visit later)
#         for next_url in next_urls:
#             if next_url not in visited_urls:
#                 urls_to_visit.append(next_url)

# # Start crawling from the base URL
# crawl_site(base_url)


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


base_url = 'https://certification.talview.com/support/solutions'


def is_valid_url(url, base_domain):
    parsed_url = urlparse(url)
    
    if parsed_url.netloc == base_domain and not any(exclusion in parsed_url.path for exclusion in ['/login', '/account', '/admin']):
        return True
    return False


def scrape_page(url, file):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    page_title = soup.title.string if soup.title else 'No Title'
    
    
    paragraphs = soup.find_all('p')
    headings_h3 = soup.find_all('h3')
    spans = soup.find_all('span')
    headings_h1 = soup.find_all('h1')
    
    
    page_paragraphs = [para.get_text() for para in paragraphs]
    page_headings_h3 = [h3.get_text() for h3 in headings_h3]
    page_spans = [span.get_text() for span in spans]
    page_headings_h1 = [h1.get_text() for h1 in headings_h1]
    
    file.write(f"Page URL: {url}\n")
    file.write(f"Page Title: {page_title}\n\n")
    print(page_headings_h1,page_headings_h3,page_spans,page_paragraphs)
    
    if len(page_paragraphs) > 1:
        for para in page_paragraphs:  
            if len(para) > 1:
                file.write(f"- {para}\n")
    
    if len(page_headings_h3) > 0:
        for h3 in page_headings_h3:  
            if len(para) > 1:
                file.write(f"- {h3}\n")
    
    if len(page_spans) >0:
        for span in page_spans:  
            if len(para) > 1:
                file.write(f"- {span}\n")
    
    if len(page_headings_h1) > 0:
        for h1 in page_headings_h1: 
            if len(para) > 1:
                file.write(f"- {h1}\n")
    
    file.write("\n" + "-"*50 + "\n\n")
    
    
    links = soup.find_all('a', href=True)
    valid_links = [urljoin(url, link['href']) for link in links if is_valid_url(urljoin(url, link['href']), urlparse(base_url).netloc)]

    return valid_links 


def crawl_site(start_url, output_file):
    visited_urls = set() 
    urls_to_visit = [start_url]

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue
        
        visited_urls.add(current_url)
        print(f"Scraping URL: {current_url}")
        
        
        next_urls = scrape_page(current_url, output_file)
        
        
        for next_url in next_urls:
            if next_url not in visited_urls:
                urls_to_visit.append(next_url)


with open('chat_bot_kb/scraped_file.txt', 'w', encoding='utf-8') as file:
    file.write("This is Assistant Chat Bot Knowledge Base for proctoring software where users will attend exams. If they found any problems on their system you have to halp them out. \n")
    file.write("You are an online exam assistant designed exclusively to help students with issues related to the exam platform and process **only** based on the provided knowledge base or session context, such as login problems, technical difficulties, and exam guidelines. Do not answer questions about coding, exam solutions, or unrelated topics. Do not provide information about the company, competitors, or internal processes. Maintain privacy and confidentiality at all times. For any out-of-scope questions, politely decline and redirect the user to relevant exam resources. Always prioritize clarity, politeness, and professionalism. \n")
    file.write("You are a specialized assistant trained to answer questions **only** based on the provided knowledge base or session context. For any query outside this scope, politely decline to answer and suggest consulting relevant resources. Always prioritize clarity, politeness, and accuracy, strictly adhering to the information within the loaded knowledge base or explicitly marked context.")
    crawl_site(base_url, file)

print("Scraping and writing to file completed.")
