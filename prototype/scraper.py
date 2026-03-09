from scraperFunda import get_funda_listings
from scraperPararius import get_pararius_listings
from seleniumNederwoon import get_nederwoon_listings
from seleniumRebo import get_rebo_listings
from sendEmail import send_email
from listingTracker import load_seen, save_seen, get_new_listings
import os
from dotenv import load_dotenv


def collect_all_listings():
    return {
        "Funda": get_funda_listings(),
        "Pararius": get_pararius_listings(),
        "Rebo": get_rebo_listings(),
        "Nederwoon": get_nederwoon_listings(),
    }


if __name__ == "__main__":
    all_listings = collect_all_listings()
    seen_urls = load_seen()

    new_listings = get_new_listings(all_listings, seen_urls)
    if not new_listings:
        print("No new listings found.")
        save_seen(seen_urls)
        exit()

    html = """
    <html>
    <body style="font-family: Arial, sans-serif; background:#f5f5f5; padding:20px;">
    <h2>Nieuwe huurwoningen</h2>
    """

    for source, listings in new_listings.items():

        html += f"""
        <h3 style="margin-top:30px;">{source}</h3>
        """

        if not listings:
            html += "<p>No listings found.</p>"
            continue

        for listing in listings:
            title = listing.get("title", "No title")
            price = listing.get("price", "No price")
            url = listing.get("url", "#")
            city = listing.get("city", "")

            html += f"""
            <div style="
                background:white;
                padding:12px;
                margin-bottom:10px;
                border-radius:8px;
                box-shadow:0 1px 3px rgba(0,0,0,0.1);
            ">
                <div style="font-size:16px; font-weight:bold;">
                    {title}
                </div>

                <div style="color:#555; margin:4px 0;">
                    {price}
                </div>

                <a href="{url}" style="
                    color:white;
                    background:#007BFF;
                    padding:6px 10px;
                    text-decoration:none;
                    border-radius:5px;
                    font-size:14px;
                    display:inline-block;
                ">
                    View listing
                </a>
            </div>
            """

    html += """
    <hr style="margin-top:30px;">
    <p style="color:#888;font-size:12px;">
    Generated automatically by your rental scraper.
    </p>
    </body>
    </html>
    """

    subject = "Nieuwe huurwoningen gevonden!"

    sender = "verawandel9@gmail.com"
    #recipients = ["verawandel@gmail.com", "larsvanoostrum1@gmail.com"]
    recipients = ["verawandel@gmail.com"]
    load_dotenv()
    password = os.getenv("EMAIL_PASSWORD")

    send_email(subject, html, sender, recipients, password)
    save_seen(seen_urls)
    print("Email sent with all new listings.")