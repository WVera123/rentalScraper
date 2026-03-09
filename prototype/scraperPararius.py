from pypararius import Pararius

def get_pararius_listings():
    p = Pararius()

    locations = ['arnhem', 'doorwerth', 'oosterbeek', 'ede', 'wolfheze', 'renkum']
    allowed_cities = set(locations)

    seen = set()
    listings = []
    for location in locations:
        results = p.search_listing(
            location=location,
            price_max=1400,
            sort="newest",
        )

        for r in results:
            url = r["url"]

            if url in seen:
                continue
            seen.add(url)

            # extract city from URL
            city_from_url = url.split("/")[4].replace("-gld", "")

            if city_from_url not in allowed_cities:
                continue

            title = r["title"]
            price = r["price"]
            neighbourhood = r.get("neighbourhood", "")

            price_formatted = f"€ {price:,}".replace(",", ".")

            listings.append({
                "title": title,
                "price": price_formatted,
                "neighbourhood": neighbourhood,
                "url": url
            })
    return listings