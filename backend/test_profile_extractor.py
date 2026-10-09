
from llm.profile_extractor import extract_citizen_profile

message = (
    "I'm 23, studying engineering in Tamil Nadu, "
    "and my family income is around 2 lakh per year."
)

profile = extract_citizen_profile(message)

print(profile.model_dump_json(indent=2))
