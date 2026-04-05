from pypararius import Pararius

p = Pararius()

# Search for listings
results = p.search_listing('amsterdam', price_max=2000)
for r in results[:3]:
    print(r['title'], r['price'])

# Get full listing details
listing = p.get_listing(results[0]['url'])
print(listing['title'], listing['city'])
print(listing.summary())