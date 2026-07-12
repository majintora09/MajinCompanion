from enum import Enum


class Capability(str, Enum):
    REASON = "reason"
    PLAN = "plan"
    REMEMBER = "remember"

    READ_FILES = "read_files"
    WRITE_FILES = "write_files"
    GENERATE_CODE = "generate_code"

    REVIEW = "review"
    SESSION_SUMMARY = "session_summary"