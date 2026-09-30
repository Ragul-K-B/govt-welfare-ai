from db.mongodb import db


collection = db["schemes"]

# Count total schemes
total = collection.count_documents({})

print(f"\nTotal schemes in MongoDB: {total}\n")

# Display all schemes
schemes = collection.find(
    {},
    {
        "_id": 0,
        "scheme_id": 1,
        "name": 1
    }
).sort("scheme_id", 1)

for scheme in schemes:
    print(f"{scheme['scheme_id']} -> {scheme['name']}")

print("\nVerification completed.")