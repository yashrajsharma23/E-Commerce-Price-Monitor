import smtplib
from bs4 import BeautifulSoup
import urllib
import urllib.request
import re
import os


def scrap_product(url):

    price_tag = None
    title_tag = None
    website = None

    if len(url) < 5:
        return None

    if url.find('www.amazon') > 0:
        website = 'AMAZON'
    elif url.find('www.flipkart') > 0:
        website = 'FLIPKART'
    else:
        return None

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        with urllib.request.urlopen(req) as response:
            html = response.read()
    except:
        return None

    if not html:
        return None

    soup = BeautifulSoup(html, 'lxml')
    title = ''
    if website == 'AMAZON':
        price_tag = soup.find_all(id="priceblock_ourprice")
        if price_tag.__len__() == 0:
            price_tag = soup.find_all(id="displayedPrice")
        title_tag = soup.find_all(id='productTitle')
    elif website == 'FLIPKART':
        price_tag = soup.find_all("div", {"class": "_30jeq3 _16Jk6d"})
        title_tag = soup.find_all("span", {"class": "B_NuCI"})

    if len(price_tag) == 0:
        return None

    price_text = price_tag[0].get_text()
    if len(title_tag) > 0:
        title = title_tag[0].get_text()
    currency = re.sub('([^₹$])+', '', price_text)
    price_str = re.sub('([^0-9.])+', '', price_text)
    price = float(price_str)

    return price, title, currency


def product_response(doc):
    product_data = doc.to_dict()
    product_data['pid'] = doc.id

    return product_data


def send_email_notification(email, product_title, price):
    print(email, product_title, price)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(os.environ.get('EMAIL_ID'), os.environ.get('EMAIL_PASSWORD'))

    subject = 'Price Fell Down <DO NOT REPLY>'
    body = f"The Price for the Product: {product_title} has now decreased to Rs. {price}."

    msg = f"Subject: {subject}\n\n{body}"

    print(msg)
    server.sendmail(
        os.environ.get('EMAIL_ID'),
        email,
        msg.encode('utf-8')
    )

    # quit the server
    server.quit()

