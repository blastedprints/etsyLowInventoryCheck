import requests
import json
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime

# Etsy API Credentials (Replace with your actual credentials)
ETSY_API_KEY = 'mrkcx0b9acyaop6v6xdnanfx'
ETSY_SHOP_ID = 'blastedprints'

# Email Configuration (Replace with your credentials and settings)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # Or your SMTP server's port
EMAIL_FROM = 'support@blastedprints.com'
EMAIL_TO = 'support@blastedprints.com'  # Or the recipient's email
EMAIL_PASSWORD = 'kvhf pdfg ewle iizz'
MINIMUM_QUANTITY = 4

def check_and_send_low_stock_email():
    url = f'https://openapi.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/listings/active'
    headers = {'x-api-key': ETSY_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        listings = json.loads(response.content)['results']

        low_stock_products = []
        for listing in listings:
            for offering in listing['offerings']:
                quantity = offering['quantity']
                if quantity < MINIMUM_QUANTITY:
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
            msg['From'] = EMAIL_FROM
            msg['To'] = EMAIL_TO

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_FROM, EMAIL_PASSWORD)
                server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

            print(f"{datetime.now()}: Low stock email sent!")
        else:
            print(f"{datetime.now()}: No low stock items found.")

    else:
        print(f"{datetime.now()}: Error fetching Etsy listings: {response.status_code}")

# Schedule the task to run daily at a specific time (e.g., 9 AM MST)
schedule.every().day.at("07:16").do(check_and_send_low_stock_email)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute for pending tasks
