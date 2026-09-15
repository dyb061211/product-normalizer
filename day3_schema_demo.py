from ai.schemas import ProductInput,GeneratedListing
import json

data = {
    "sku": "A001",
    "listing_title": "Green Portable Camping Chair",
    "bullet_points": [
        "Portable design.",
        "Green color.",
        "Suitable for outdoor use.",
    ],
    "description": "A portable green camping chair."
}


listing=GeneratedListing.model_validate(data)
print(listing)
print(type(listing))
print(listing.listing_title)
print(listing.bullet_points)
print(GeneratedListing.model_json_schema())