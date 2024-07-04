import stripe

stripe.api_key = "sk_test_51PYAfPRrnWZoSf4Vf5sEUCEys1olebpof755PM5QiOfAzDuR75HwRfm3Bc6m0NAiORgYTepykvsQHsdTr4kWYtXV00vi0jFSXp"

basic_room = stripe.Product.create(
  name="Basic room",
  description="20PLN",
)

# fancy_room = stripe.Product.create(
#   name="Fancy room",
#   description="$30",
# )

room_price = stripe.Price.create(
  unit_amount=2000,
  currency="pln",
  product=basic_room['id'],
)

# Save these identifiers
print(f"Success! Here is your starter subscription product id: {basic_room.id}")
print(f"Success! Here is your starter subscription price id: {room_price.id}")

# Success! Here is your starter subscription product id: prod_QPgbu0gPZVgHO1
# Success! Here is your starter subscription price id: price_1PYrDxRrnWZoSf4VzBKC5a2j