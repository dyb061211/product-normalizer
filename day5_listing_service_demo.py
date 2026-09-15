from ai.listing_service import generate_listing
from ai.schemas import ProductInput

product=ProductInput(
    sku="A001",
    title="Portable Camping Chair",
    color="Green",
    category="Outdoor",
    price=29.99
)

result=generate_listing(product)

print(type(result))
print(result)