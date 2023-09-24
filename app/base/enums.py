from enum import Enum


class RoleEnum(Enum):
    EMPLOYER = "EMPLOYER"
    JOBSEEKER = "JOBSEEKER"
    ADMIN = "ADMIN"


class JobCategoryEnum(Enum):
    CONSTRUCTION = "CONSTRUCTION"
    FARMING = "FARMING"
    WAREHOUSE = "WAREHOUSE"
    PLUMBING = "PLUMBING"
    GENERAL = "GENERAL"
