import json
import os

FILE_NAME = "seen_listings.json"


def load_seen():
    if not os.path.exists(FILE_NAME):
        return set()

    with open(FILE_NAME, "r") as f:
        data = json.load(f)

    return set(data)


def save_seen(seen):
    with open(FILE_NAME, "w") as f:
        json.dump(list(seen), f)


def get_new_listings(all_listings, seen_urls):
    new_listings = {}

    for source, listings in all_listings.items():
        for listing in listings:
            url = listing.get("url")

            if url not in seen_urls:
                seen_urls.add(url)
                new_listings.setdefault(source, []).append(listing)
    return new_listings