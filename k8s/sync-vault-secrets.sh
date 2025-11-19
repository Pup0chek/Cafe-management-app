#!/usr/bin/env bash
set -e

VAULT_CONTAINER="vault"
VAULT_ADDR="http://127.0.0.1:8200"
VAULT_TOKEN="root"

get_secret () {
  local key="$1"
  docker exec \
    -e VAULT_ADDR="$VAULT_ADDR" \
    -e VAULT_TOKEN="$VAULT_TOKEN" \
    "$VAULT_CONTAINER" \
    vault kv get -field="$key" secret/cafe
}

echo "[*] Читаю секреты из Vault..."

POSTGRES_PASSWORD=$(get_secret POSTGRES_PASSWORD)
SECRET_KEY=$(get_secret SECRET_KEY)
DEBUG=$(get_secret DEBUG)
ALLOWED_HOSTS=$(get_secret ALLOWED_HOSTS)

echo "[*] Удаляю старые Kubernetes Secrets (если есть)..."
kubectl -n cafe delete secret postgres-secret django-secret 2>/dev/null || true

echo "[*] Создаю postgres-secret из Vault..."
kubectl -n cafe create secret generic postgres-secret \
  --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD"

echo "[*] Создаю django-secret из Vault..."
kubectl -n cafe create secret generic django-secret \
  --from-literal=SECRET_KEY="$SECRET_KEY" \
  --from-literal=DEBUG="$DEBUG" \
  --from-literal=ALLOWED_HOSTS="$ALLOWED_HOSTS"

echo "[+] Готово! Секреты в Kubernetes теперь взяты из Vault."
