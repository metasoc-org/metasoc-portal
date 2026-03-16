#!/bin/bash
# ============================================================
# MetaSOC — Auto Deploy Script
# Ejecuta cada hora via cron para sincronizar con Cloudflare Pages
# ============================================================

set -e

# ── CONFIG ──────────────────────────────────────────────────
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"   # Raíz del repo
LOG_FILE="$REPO_DIR/scripts/deploy.log"
MAX_LOG_LINES=500
# ─────────────────────────────────────────────────────────────

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  echo "[$(timestamp)] $1" | tee -a "$LOG_FILE"
}

# Rotar log si es muy grande
if [ -f "$LOG_FILE" ] && [ "$(wc -l < "$LOG_FILE")" -gt "$MAX_LOG_LINES" ]; then
  tail -n 200 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

log "========================================================"
log "MetaSOC Auto-Deploy iniciado"
log "Directorio: $REPO_DIR"

# Verificar que estamos en un repo git
if [ ! -d "$REPO_DIR/.git" ]; then
  log "ERROR: No se encontró repositorio git en $REPO_DIR"
  log "Ejecuta 'git init' primero y conecta con GitHub."
  exit 1
fi

cd "$REPO_DIR"

# Actualizar el timestamp en incidents.json
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
log "Actualizando timestamp → $TIMESTAMP"

# Actualizar last_updated en el JSON usando Python (más portable que sed)
python3 - <<EOF
import json, sys
path = "$REPO_DIR/site/data/incidents.json"
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data['meta']['last_updated'] = "$TIMESTAMP"
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("JSON actualizado correctamente")
EOF

# Verificar si hay cambios
if git diff --quiet && git diff --cached --quiet; then
  log "Sin cambios detectados — nada que hacer."
  exit 0
fi

# Git add + commit + push
log "Cambios detectados, preparando commit..."
git add -A

COMMIT_MSG="chore: auto-update [$(timestamp)]"
git commit -m "$COMMIT_MSG"
log "Commit: $COMMIT_MSG"

git push origin main 2>&1 | while IFS= read -r line; do
  log "GIT: $line"
done

log "✅ Deploy completado. Cloudflare Pages detectará el push automáticamente."
log "========================================================"
