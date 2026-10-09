
from pydantic import BaseModel, Field, ConfigDict


class CitizenProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Basic information
    age: int | None = Field(
        default=None,
        ge=0,
        le=120,
        description="Citizen's age in years"
    )

    state: str | None = Field(
        default=None,
        description="State or union territory of residence"
    )

    district: str | None = Field(
        default=None,
        description="District of residence"
    )

    # Education and employment
    occupation: str | None = Field(
        default=None,
        description="Occupation, such as student, farmer, or employee"
    )

    education_level: str | None = Field(
        default=None,
        description="Education level, such as engineering or school"
    )

    percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Percentage in the relevant examination"
    )

    institution_type: str | None = Field(
        default=None,
        description="Type of institution, such as government or private"
    )

    # Financial information
    annual_family_income: float | None = Field(
        default=None,
        ge=0,
        description="Annual family income in Indian rupees"
    )

    # Other attributes that may matter for particular schemes
    community_category: str | None = Field(
        default=None,
        description="Community category, if voluntarily provided"
    )

    gender: str | None = None

    disability_status: bool | None = Field(
        default=None,
        description="Whether the citizen has a disability"
    )

    marital_status: str | None = None

    domicile_status: bool | None = Field(
        default=None,
        description="Whether the citizen meets the relevant domicile requirement"
    )
