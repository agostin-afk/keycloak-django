import base64
import hashlib
import json
import secrets
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

User = get_user_model()


def home(request):
    context = {
        "user": request.user,
        "is_authenticated": request.user.is_authenticated,
        "keycloak_admin": "http://localhost:8080/admin",
        "realm": getattr(settings, "REALM", "demo"),
    }
    if request.user.is_authenticated:
        oidc_data = request.session.get("oidc_id_token_payload", {}) or {}
        context["roles"] = (
            oidc_data.get("roles")
            or oidc_data.get("realm_access", {}).get("roles", [])
        )
    return render(request, "home.html", context)


def _pkce_pair():
    verifier = secrets.token_urlsafe(64)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest())
        .decode("ascii")
        .rstrip("=")
    )
    return verifier, challenge


@require_GET
def login_keycloak(request):
    """Inicia o login: redireciona ao Keycloak com scope=openid (compatível com o realm)."""
    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    verifier, challenge = _pkce_pair()

    request.session["oidc_state"] = state
    request.session["oidc_nonce"] = nonce
    request.session["oidc_code_verifier"] = verifier
    request.session["oidc_next"] = request.GET.get("next", "/protegido/")

    params = {
        "client_id": settings.OIDC_RP_CLIENT_ID,
        "response_type": "code",
        "scope": "openid",
        "redirect_uri": request.build_absolute_uri("/callback/"),
        "state": state,
        "nonce": nonce,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    url = f"{settings.OIDC_OP_AUTHORIZATION_ENDPOINT}?{urlencode(params)}"
    return HttpResponseRedirect(url)


@require_GET
def oidc_callback(request):
    """Troca o authorization code por tokens e faz login no Django."""
    error = request.GET.get("error")
    if error:
        desc = request.GET.get("error_description", error)
        return HttpResponseBadRequest(f"Erro do Keycloak: {desc}")

    code = request.GET.get("code")
    state = request.GET.get("state")
    if not code or not state:
        return HttpResponseBadRequest("Callback sem code/state")

    if state != request.session.get("oidc_state"):
        return HttpResponseBadRequest("State inválido (possível CSRF)")

    verifier = request.session.get("oidc_code_verifier")
    redirect_uri = request.build_absolute_uri("/callback/")

    # Troca code → tokens (Django fala com Keycloak pela rede Docker)
    token_url = settings.OIDC_OP_TOKEN_ENDPOINT
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": settings.OIDC_RP_CLIENT_ID,
        "client_secret": settings.OIDC_RP_CLIENT_SECRET,
        "code_verifier": verifier,
    }
    try:
        resp = requests.post(token_url, data=data, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        body = getattr(e.response, "text", "") if hasattr(e, "response") else ""
        return HttpResponse(
            f"Falha ao trocar code por token: {e}\n{body}",
            status=502,
            content_type="text/plain",
        )

    tokens = resp.json()
    access_token = tokens.get("access_token", "")
    id_token = tokens.get("id_token", "")

    # UserInfo
    userinfo = {}
    try:
        ui = requests.get(
            settings.OIDC_OP_USER_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15,
        )
        if ui.ok:
            userinfo = ui.json()
    except requests.RequestException:
        pass

    # Claims do id_token (sem validar assinatura — só demo local)
    payload = {}
    if id_token and id_token.count(".") == 2:
        try:
            pad = "=" * (-len(id_token.split(".")[1]) % 4)
            payload = json.loads(
                base64.urlsafe_b64decode(id_token.split(".")[1] + pad)
            )
        except Exception:
            payload = {}

    # Merge userinfo + payload
    claims = {**payload, **userinfo}
    username = (
        claims.get("preferred_username")
        or claims.get("email")
        or claims.get("sub")
        or "keycloak-user"
    )
    email = claims.get("email", "") or ""
    first_name = claims.get("given_name", "") or claims.get("name", "").split(" ")[0]
    last_name = claims.get("family_name", "")

    user, _created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "first_name": first_name, "last_name": last_name},
    )
    if not _created:
        user.email = email or user.email
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name
        user.save()

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    request.session["oidc_id_token"] = id_token
    request.session["oidc_id_token_payload"] = claims
    request.session.pop("oidc_state", None)
    request.session.pop("oidc_code_verifier", None)

    next_url = request.session.pop("oidc_next", "/protegido/")
    return redirect(next_url)


@login_required
def protegido(request):
    oidc_data = request.session.get("oidc_id_token_payload", {}) or {}
    roles = oidc_data.get("roles") or oidc_data.get("realm_access", {}).get(
        "roles", []
    )
    claims_pretty = (
        json.dumps(oidc_data, indent=2, ensure_ascii=False) if oidc_data else "{}"
    )
    context = {
        "user": request.user,
        "roles": roles,
        "claims": claims_pretty,
        "email": getattr(request.user, "email", "") or oidc_data.get("email", ""),
        "name": (
            f"{getattr(request.user, 'first_name', '')} "
            f"{getattr(request.user, 'last_name', '')}"
        ).strip()
        or oidc_data.get("name", request.user.username),
    }
    return render(request, "protegido.html", context)


def logout_view(request):
    id_token = request.session.get("oidc_id_token", "")
    django_logout(request)
    if id_token:
        params = urlencode(
            {
                "id_token_hint": id_token,
                "post_logout_redirect_uri": request.build_absolute_uri("/"),
            }
        )
        return HttpResponseRedirect(f"{settings.OIDC_OP_LOGOUT_ENDPOINT}?{params}")
    return redirect("/")
