from dataclasses import dataclass

@dataclass
class AuthKeys():
    role_id: str
    external_id: str

@dataclass
class User():
    name: str
    id: str
    reports: list[str]
    creds: list[AuthKeys]

@dataclass
class Report():
    user_id: User
    id: str
    process_state: str
    datetime_started: str
    datetime_completed: str
