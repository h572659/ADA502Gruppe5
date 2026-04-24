from decouple import config
from keycloak import KeycloakOpenID
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from .models import User


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=("http://158.37.66.185:8001/realms/ADA_502/protocol/openid-connect/auth"
                      "?prompt=login"),
    
    #authorizationUrl=("http://localhost:8080/realms/ADA_502/protocol/openid-connect/auth"
                      #"?prompt=login"),
    
    tokenUrl="http://158.37.66.185:8001/realms/ADA_502/protocol/openid-connect/token"
  
    #tokenUrl="http://localhost:8080/realms/ADA_502/protocol/openid-connect/token"
)

ROLE_HIERARCHY = {
    "admin": {"admin"},
    "user": {"user", "admin"},
}

keycloak_openid = KeycloakOpenID(
    server_url=config("SERVER_URL", default="http://keycloak:8080"),
    realm_name=config("realm", default="ADA_502"),
    client_id = "" 
)

#Get Token 
def get_jwttoken(token: str = Depends(oauth2_scheme)):
    #token = req.headers["Authorization"]
    #token = token.split(" ").pop(1)
    #print(token)
    #print(f"Mottatt token: {token[:10]}...")
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
