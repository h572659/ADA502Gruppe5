from decouple import config
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from keycloak import KeycloakOpenID

from models import User

bearer_scheme = HTTPBearer(auto_error=True)


def get_keycloak_openid() -> KeycloakOpenID:
    return KeycloakOpenID(
        server_url=config("KEYCLOAK_SERVER_URL"),
        realm_name=config("KEYCLOAK_REALM"),
        client_id=config("KEYCLOAK_CLIENT_ID"),
    )


def get_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


def get_idp_public_key(keycloak_openid: KeycloakOpenID):
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


def get_payload(token=Depends(get_jwt_token)) -> dict:
    keycloak_openid = get_keycloak_openid()
    try:
        return keycloak_openid.decode_token(
            token,
            key=get_idp_public_key(keycloak_openid),
            options={
                "verify_signature": True,
                "verify_iss": True,
                "verify_exp": True,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_info(payload: dict = Depends(get_payload)) -> User:
    client_id = payload.get("azp") or config("KEYCLOAK_CLIENT_ID")
    try:
        return User(
            id=payload.get("sub", ""),
            username=payload.get("preferred_username", ""),
            first_name=payload.get("given_name", ""),
            last_name=payload.get("family_name", ""),
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
    roles: list = [*user.realm_roles, *user.client_roles]
    return verify_role(roles, "admin")


def verify_sadmin_role(user: User = Depends(get_user_info)):
    roles: list = [*user.realm_roles, *user.client_roles]
    return verify_role(roles, "app_admin")


def verify_user_role(user: User = Depends(get_user_info)):
    roles: list = [*user.realm_roles, *user.client_roles]
    return verify_role(roles, "user")


def verify_suser_role(user: User = Depends(get_user_info)):
    roles: list = [*user.realm_roles, *user.client_roles]
    return verify_role(roles, "app_user")


def verify_role(roles: list, role: str):
    if role in roles:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Missing required role: {role}",
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_user_path(request: Request, user: User = Depends(get_user_info)):
    rpath: str = request.url.path
    paths: list = user.locations
    return verify_path(paths, rpath)


def verify_user_locquery(request: Request, user: User = Depends(get_user_info)):
    rquery: str = request.url.query
    if len(rquery) > 0:
        qparam = rquery.split("=").pop(1).split(",")
        parameters: list = user.locations
        return verify_parameters(parameters, qparam)
    return False


def verify_path(paths: list, path: str):
    if path in paths:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Not authorized to access this sensor(s): {path}",
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_parameters(user_parameters: list, query_parameters: list):
    sparam = set(user_parameters)
    sdiff = [x for x in query_parameters if x not in sparam]
    ssdiff = f'{",".join(sdiff)}'
    if len(sdiff) == 0:
        sdiff = query_parameters
    try:
        user_parameters.index(sdiff.pop(0))
        return True
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to access this sensor(s): {ssdiff}",
            headers={"WWW-Authenticate": "Bearer"},
        )
