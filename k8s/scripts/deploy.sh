#!/bin/bash
# ================================================================
# WordFix — Kubernetes Deploy Script (Development)
# Builds Docker images and deploys all services to local K8s
# ================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
K8S_DIR="$SCRIPT_DIR/.."
NAMESPACE="wordfix"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; exit 1; }

# ── Pre-flight checks ───────────────────────────────────────────
info "Checking prerequisites..."
command -v docker   >/dev/null 2>&1 || fail "docker not found"
command -v kubectl  >/dev/null 2>&1 || fail "kubectl not found"
kubectl cluster-info >/dev/null 2>&1 || fail "Kubernetes cluster not reachable"
ok "Prerequisites OK"

# ── Step 1: Build Docker images ─────────────────────────────────
info "Building Docker images..."

echo "  -> wordfix/monolith"
docker build -t wordfix/monolith:latest \
  -f "$PROJECT_ROOT/wordfix-backend/docker/Dockerfile" \
  "$PROJECT_ROOT/wordfix-backend" \
  --quiet

echo "  -> wordfix/api-gateway"
docker build -t wordfix/api-gateway:latest \
  -f "$PROJECT_ROOT/services/api-gateway/Dockerfile" \
  "$PROJECT_ROOT" \
  --quiet

echo "  -> wordfix/auth-service"
docker build -t wordfix/auth-service:latest \
  -f "$PROJECT_ROOT/services/auth-service/Dockerfile" \
  "$PROJECT_ROOT" \
  --quiet

echo "  -> wordfix/frontend"
docker build -t wordfix/frontend:latest \
  -f "$PROJECT_ROOT/wordfix-frontend/Dockerfile.prod" \
  "$PROJECT_ROOT/wordfix-frontend" \
  --quiet

ok "All 4 images built"

# ── Step 2: Apply namespace ──────────────────────────────────────
info "Creating namespace..."
kubectl apply -f "$K8S_DIR/namespace.yaml"
ok "Namespace '$NAMESPACE' ready"

# ── Step 3: Apply secrets and configmaps ─────────────────────────
info "Applying secrets..."
kubectl apply -f "$K8S_DIR/secrets/"
ok "Secrets applied"

info "Applying configmaps..."
kubectl apply -f "$K8S_DIR/configmaps/"
ok "ConfigMaps applied"

# ── Step 4: Apply storage ────────────────────────────────────────
info "Applying persistent volume claims..."
kubectl apply -f "$K8S_DIR/storage/"
ok "PVCs applied"

# ── Step 5: Deploy infrastructure ────────────────────────────────
info "Deploying infrastructure (db, auth-db, redis, rabbitmq)..."
kubectl apply -f "$K8S_DIR/infra/"

for sts in db auth-db redis rabbitmq; do
  echo "  -> Waiting for $sts..."
  kubectl rollout status statefulset/"$sts" -n "$NAMESPACE" --timeout=120s
done
ok "Infrastructure ready"

# ── Step 6: Deploy applications ──────────────────────────────────
info "Deploying applications..."
kubectl apply -f "$K8S_DIR/apps/"

for deploy in web gateway auth-service celery-worker celery-beat nginx; do
  echo "  -> Waiting for $deploy..."
  kubectl rollout status deployment/"$deploy" -n "$NAMESPACE" --timeout=180s
done
ok "All applications deployed"

# ── Step 7: Summary ─────────────────────────────────────────────
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  WordFix Kubernetes deployment complete!  ${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
kubectl get pods -n "$NAMESPACE" -o wide
echo ""
kubectl get svc -n "$NAMESPACE"
echo ""
echo -e "${CYAN}Access the application:${NC}"
echo -e "  Frontend:  ${GREEN}http://localhost:30080${NC}"
echo -e "  Admin:     ${GREEN}http://localhost:30080/admin/${NC}"
echo -e "  API:       ${GREEN}http://localhost:30080/api/v1/health/${NC}"
echo ""
