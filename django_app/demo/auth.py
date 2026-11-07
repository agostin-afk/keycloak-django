"""
Helpers de autenticação Keycloak.
"""
from django.conf import settings


def keycloak_logout(request):
    """
    Monta a URL de logout do Keycloak (end_session_endpoint).
    Usado por OIDC_OP_LOGOUT_URL_METHOD.
    """
    id_token = request.session.get("oidc_id_token", "")
    logout_url = (
        f"{settings.OIDC_OP_LOGOUT_ENDPOINT}"
        f"?id_token_hint={id_token}"
        f"&post_logout_redirect_uri={request.build_absolute_uri('/')}"
    )
    return logout_url
