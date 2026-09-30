from retrieval.prepare_documents import get_scheme_documents


schemes = get_scheme_documents()

print("Number of schemes:", len(schemes))

for scheme in schemes[:2]:
    print("\nScheme ID:", scheme["scheme_id"])
    print("Text:")
    print(scheme["text"])