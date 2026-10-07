import os
from fastapi.security import HTTPBearer

security_scheme = HTTPBearer(auto_error=False)


def get_jwt_secret() -> str:
    return os.getenv("JWT_SECRET", "change-this-secret")
