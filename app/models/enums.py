from enum import Enum

class ReactionType(str, Enum):
    SIGH = "sigh"
    FACEPALM = "facepalm"
    CRINGE = "cringe"
    SEEN = "seen" # "Просмотрено". Высшая степень безразличия.

class UserStatus(str, Enum):
    CONTEMPLATING_THE_VOID = "contemplating_the_void"
    PRETENDING_TO_WORK = "pretending_to_work"
    ON_THE_VERGE = "on_the_verge"
    RUNNING_ON_CAFFEINE = "running_on_caffeine"