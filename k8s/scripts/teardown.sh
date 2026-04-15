#!/bin/bash
# ================================================================
# WordFix — Kubernetes Teardown Script
# Deletes the entire wordfix namespace and all its resources
# ================================================================

set -euo pipefail

NAMESPACE="wordfix"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}This will delete the entire '$NAMESPACE' namespace and all resources.${NC}"
read -p "Are you sure? (y/N): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

echo -e "${RED}Deleting namespace '$NAMESPACE'...${NC}"
kubectl delete namespace "$NAMESPACE" --timeout=120s

echo -e "${GREEN}Namespace '$NAMESPACE' deleted successfully.${NC}"
echo ""
echo "Note: PersistentVolumes may still exist. To clean up completely:"
echo "  kubectl get pv | grep $NAMESPACE"
echo "  kubectl delete pv <pv-name>"
