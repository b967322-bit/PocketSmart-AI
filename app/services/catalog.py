from urllib.parse import quote_plus

PLATFORMS = {
    "Amazon": "https://www.amazon.in/s?k={q}",
    "Flipkart": "https://www.flipkart.com/search?q={q}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={q}",
    "Swiggy": "https://www.swiggy.com/search?query={q}",
    "Zomato": "https://www.zomato.com/search?q={q}",
    "OYO": "https://www.oyorooms.com/search?location={q}",
}

def search_url(platform, query):
    template = PLATFORMS.get(platform, PLATFORMS["Amazon"])
    return template.format(q=quote_plus(query))

def enrich_recommendations(result):
    for item in result.get("recommendations", []):
        platform = item.get("platform") or "Amazon"
        query = item.get("name") or item.get("category") or "budget recommendation"
        item["platform"] = platform
        item["search_url"] = search_url(platform, query)
    return result
