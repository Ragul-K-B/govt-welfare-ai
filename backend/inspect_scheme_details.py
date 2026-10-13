
from db.mongodb import schemes_collection

fields = [
    "description",
    "benefits",
    "documents",
    "application",
    "sources",
]

total = 0
missing_counts = {field: 0 for field in fields}

for scheme in schemes_collection.find(
    {},
    {
        "_id": 0,
        "scheme_id": 1,
        "name": 1,
        **{field: 1 for field in fields}
    }
):
    total += 1

    print(f"\n{scheme.get('scheme_id')} - {scheme.get('name')}")

    for field in fields:
        value = scheme.get(field)

        is_missing = (
            value is None
            or value == ""
            or value == []
            or value == {}
        )

        if is_missing:
            missing_counts[field] += 1

        status = "MISSING" if is_missing else "PRESENT"
        print(f"  {field}: {status}")

print(f"\n{'=' * 40}")
print(f"Total schemes inspected: {total}")
print("\nMissing field counts:")

for field, count in missing_counts.items():
    print(f"  {field}: {count}/{total}")
