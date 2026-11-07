# Keycloak + Django — Demo simples

Projeto mínimo para **demonstrar** Keycloak como Identity Provider com Django via **OpenID Connect** (Authorization Code + PKCE).

---

## Pré-requisitos

- Docker Desktop (ou Docker Engine + Compose)
- Portas **8080** e **8000** livres

---

## Subir do zero (recomendado se deu erro antes)

No terminal, na pasta do projeto:

```bash
cd keycloak-django-demo

# Para e remove containers antigos (importante!)
docker compose down -v

# Sobe de novo (rebuild)
docker compose up --build
```

**Espere 40–90 segundos.** No log do Keycloak você deve ver algo como:

```
Listening on: http://0.0.0.0:8080
Imported realm demo
```

Quando o Django imprimir `Starting development server at http://0.0.0.0:8000/`, está pronto.

### URLs

| Serviço              | URL                       | Login            |
|----------------------|---------------------------|------------------|
| Django (app)         | http://localhost:8000     | —                |
| Keycloak Admin       | http://localhost:8080     | `admin` / `admin`|
| Admin Console direto | http://localhost:8080/admin | `admin` / `admin`|

### Usuários do realm `demo`

| Usuário   | Senha        | Roles           |
|-----------|--------------|-----------------|
| `admin`   | `admin123`   | admin, user     |
| `aluno`   | `aluno123`   | user            |
| `auditor` | `auditor123` | auditor, user   |

---

## Se ainda der erro

### 1. Keycloak: “connection was reset” / não abre

O Keycloak demora para iniciar. Verifique:

```bash
docker compose ps
docker compose logs keycloak --tail 50
```

- Se o container estiver **Restarting** ou **Exited**, o log mostra o motivo.
- Em máquina com pouca RAM, feche outros programas e tente de novo.
- Confirme que nada mais está na porta 8080:
  ```bash
  # Windows (PowerShell)
  netstat -ano | findstr :8080
  # Linux / macOS
  lsof -i :8080
  ```

### 2. Django: `{"detail": "Not Found"}`

Isso **não** é a resposta da nossa app (ela devolve HTML). Quase sempre significa:

- Outro processo já estava usando a porta **8000**, ou
- O container Django ainda não subiu e você bateu em outro serviço.

Faça:

```bash
docker compose down
docker compose up --build
```

Abra exatamente: **http://localhost:8000/** (com a barra no final, se quiser).

Logs do Django:

```bash
docker compose logs django --tail 50
```

### 3. Login redireciona, mas volta com erro

Espere o Keycloak terminar de importar o realm `demo` e tente de novo.  
No Admin Console, confira se o realm **demo** aparece no seletor (canto superior esquerdo).

---

## Parar tudo

```bash
docker compose down
```

Apagar dados também:

```bash
docker compose down -v
```

---

## Fluxo rápido para a apresentação

1. `http://localhost:8000` → página pública  
2. **Entrar com Keycloak** → login `aluno` / `aluno123`  
3. Área protegida (mostra usuário e roles)  
4. `http://localhost:8080` → Admin Console (`admin`/`admin`) → realm **demo**  
5. **Sair** na app → SSO logout no Keycloak  

---

## O que mudou nesta versão

- Removido Postgres (Keycloak usa H2 embutido em `start-dev`) — menos falhas
- Variáveis corretas do Keycloak 26: `KC_BOOTSTRAP_ADMIN_USERNAME` / `KC_BOOTSTRAP_ADMIN_PASSWORD`
- Django espera o Keycloak responder antes de iniciar
- Hostname relaxado para ambiente local

Somente para demonstração / estudo. Não use em produção.
