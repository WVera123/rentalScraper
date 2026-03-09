from funda import Funda

def get_funda_listings():
    f = Funda()

    results = f.search_listing(
        location=['arnhem', 'doorwerth', 'oosterbeek', 'ede', 'wolfheze', 'renkum'],
        offering_type="rent",
        price_max=1400,
        sort="newest",
        object_type=["apartment", "house"],
    )

    listings = []

    for r in results:
        title = r["title"]
        price = r["price"]
        city = r["city"]
        url = r["detail_url"]

        price_formatted = f"€ {price:,}".replace(",", ".")

        listings.append({
            "title": title,
            "price": price_formatted,
            "city": city,
            "url": "https://www.funda.nl" + url
        })

    return listings