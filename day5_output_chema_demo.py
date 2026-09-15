from ai.schemas import GeneratedListing

data = {
    "sku": "A001",
    "listing_title": "Portable Camping Chair",
    "bullet_points": [
        "Portable design",
        "Green color",
        "Suitable for outdoor use"
    ],
    "description": "A portable green camping chair."
}

listing = GeneratedListing.model_validate(data)

print(listing)