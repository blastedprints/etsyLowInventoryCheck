import requests
import json
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime
from config import creds

def check_and_send_low_stock_email():
    url = f'https://openapi.etsy.com/v3/application/shops/{creds.ETSY_SHOP_ID}/listings/active'
    headers = {'x-api-key': creds.ETSY_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        listings = json.loads(response.content)['results']

        low_stock_products = []
        for listing in listings:
            for offering in listing['offerings']:
                quantity = offering['quantity']
                if quantity < creds.MINIMUM_QUANTITY:
                    product_title = listing['title']
                    style = offering['property_values'][0]['value']  # Assuming the first property is style
                    low_stock_products.append(f"{product_title} - {style} ({quantity} left)")

        if low_stock_products:
            email_body = f"""\
            <html><body>
                <div style="max-width: 600px; margin: 20px auto; background-color: #fff; padding: 30px; border-radius: 8px;">
                    <h1 style="color: #FF6347; margin-bottom: 20px;">Low Stock Alert</h1>
                    <ul style="list-style: none; padding: 0;">
                        """ + "\n".join(f"<li>{product}</li>" for product in low_stock_products) + """
                    </ul>
                </div>
            </body></html>
            """

            msg = MIMEText(email_body, 'html')
            msg['Subject'] = 'Etsy Low Stock Alert'
            msg['From'] = creds.EMAIL_FROM
            msg['To'] = creds.EMAIL_TO

            with smtplib.SMTP(creds.SMTP_SERVER, creds.SMTP_PORT) as server:
                server.starttls()
                server.login(creds.EMAIL_FROM, creds.EMAIL_PASSWORD)
                server.sendmail(creds.EMAIL_FROM, creds.EMAIL_TO, msg.as_string())

            print(f"{datetime.now()}: Low stock email sent!")
        else:
            print(f"{datetime.now()}: No low stock items found.")

    else:
        print(f"{datetime.now()}: Error fetching Etsy listings: {response.status_code}")

# Schedule the task to run daily at a specific time (e.g., 9 AM UTC)
schedule.every().day.at("07:16").do(check_and_send_low_stock_email)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute for pending tasks
