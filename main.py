import requests
from bs4 import BeautifulSoup
import smtplib
import os

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
SEND_TO = os.environ["SEND_TO"]


url = "https://www.amazon.com/s?k=malin+and+goetz+shampoo&crid=ECUPL2NF3AWI&" \
      "sprefix=malin+and%2Caps%2C1133&ref=nb_sb_ss_ts-doa-p_2_9"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
price = soup.find("span", class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = 20


product = soup.find("h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2").get_text()

quote = f"Your product {product}has just dropped below $30!\n\nVisit {url}\n\nBuy it now before the deal runs out!"

if price_as_float < 30:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=SEND_TO,
                            msg=f"Subject:Amazon Price Alert!\n\n{quote}.")
