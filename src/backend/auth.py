from decouple import config
from keycloak import KeycloakOpenID
from fastapi import HTTPException, status, Depends, Request

from .models import User

ROLE_HIERARCHY = {
    "admin": {"admin"},
    "user": {"user", "admin"},
}

keycloak_openid = KeycloakOpenID(
    server_url=config("SERVER_URL", default="http://localhost:8000")
    realm_name=config("realm"),
    client_id=""
)

#Get Token 
def get_jwttoken(req: Request):
    token = req.headers["Authorization"]
    token = token.split(" ").pop(1)
    print(token)
    return token

async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

#Decode token
async def get_payload(token = Depends(get_jwttoken)) -> dict:
    try:
        return keycloak_openid.decode_token(
            token,  
            await get_idp_public_key()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    print(payload)
    client_id = payload.get("azp")
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("resource_access", {}).get(client_id, {}).get("roles", []),
            locations=payload.get("locations", [])
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def verify_admin_role(user: User = Depends(get_user_info)):
    roles: list = user.realm_roles 
    roles.extend(user.client_roles)
    print(roles)
    return verify_role(roles, "admin")

def verify_user_role(user: User = Depends(get_user_info)):
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    print(roles)
    return verify_role(roles, "user")

def verify_role(roles: list, role: str):
    allowed_roles = ROLE_HIERARCHY.get(role, {role})
    if any(user_role in allowed_roles for user_role in roles):
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized, action",
        headers={"WWW-Authenticate": "Bearer"},
    )
