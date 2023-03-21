import csv
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


# Initializing an empty list to store the scraped data
data = []
product_urls = []
for page in range(1, 11):
    url = f'https://www.amazon.in/s?k=bags&page={page}'
    response = requests.get(url, headers=headers)

    # Parsing the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finding all the product blocks on the page
    product_blocks = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Extractingg the required data from each product block and append it to the data list
    for block in product_blocks:
        product_url = 'https://www.amazon.in' + block.find('a', {'class': 'a-link-normal'})['href']
        product_urls.append(product_url)

print("Total number of urls:",len(product_urls))

# Scraping additional data from each product URL
for url in product_urls:
#u1="https://www.amazon.in/Skybags-Brat-Black-Casual-Backpack/dp/B08Z1HHHTD/ref=ice_ac_b_dpb?keywords=bags&qid=1679323885&sr=8-2"
    response = requests.get(url.strip(), headers=headers)

    # Parsing the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    #Extracting the product ddetails from the page
    product_name = soup.find('span', {'id': 'productTitle'})
    if product_name is not None:
        product_name = soup.find('span', {'id': 'productTitle'}).text.strip() 
    product_price = soup.find('span', {'class': 'a-offscreen'})
    if product_price is not None:
        product_price=soup.find('span', {'class': 'a-offscreen'}).text.strip()
    product_rating = soup.find('span', {'class': 'a-icon-alt'})
    if product_rating is not None:
        product_rating=soup.find('span', {'class': 'a-icon-alt'}).text.split()[0]
    product_review_count =soup.find('span', {'id': 'acrCustomerReviewText'})
    if product_review_count is not None:
        product_review_count=soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip()

    # Extracting the additional data from the page
    description = soup.find('ul', {'class': "a-unordered-list a-vertical a-spacing-mini"})
    if description is not None:
        description = soup.find('ul', {'class': "a-unordered-list a-vertical a-spacing-mini"}).text.strip().replace('\n', '').replace('<br>', '')
    '''product_description = soup.find('div', {'class': "aplus-v2 desktop celwidget"})
    if product_description is not None:
        product_description = soup.find('div', {'class': "aplus-v2 desktop celwidget"}).text.strip()'''
    product_description1 = soup.find('div',{'class': "celwidget aplus-module 3p-module-b aplus-standard"})
    if product_description1 is not None:
        product_description1 = soup.find('div',{'class': "celwidget aplus-module 3p-module-b aplus-standard"}).text.strip().replace('\n', '').replace('<br>', '')
    manufacturer = soup.select_one("#detailBullets_feature_div ul li:contains('Manufacturer')")
    if manufacturer is not None:
        manufacturer = soup.select_one("#detailBullets_feature_div ul li:contains('Manufacturer')").text.split(":")[1].strip()[35:]
        #Manufacturer=manufacturer[35:]
    asin = soup.select_one("#detailBullets_feature_div ul li:contains('ASIN')")
    if asin is not None:
        asin = soup.select_one("#detailBullets_feature_div ul li:contains('ASIN')").text.split(":")[1].strip()[35:]
        #Asin=asin[35:]
    # Adding the data to the data dictionary
    data.append({
        'Product URL': url.strip(),
        'Product Name': product_name,
        'Product Price':  product_price,
        'Rating': product_rating,
        'Number of reviews': product_review_count,
        'Description': description,
        'ASIN': asin,
        #'Product Description': product_description + product_description1,
        'Product Description': product_description1,
        'Manufacturer': manufacturer
    })

    # Printing the progress
    print(f'Scraped data for {url.strip()}')
'''for item in data :
    print(data)'''

# Writing the data to a CSV file
with open('product_data.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    for item in data:
        writer.writerow(item)

print('Done.')