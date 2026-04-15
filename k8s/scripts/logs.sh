#!/bin/bash
# ================================================================
# WordFix — Kubernetes Logs Script
# Usage: ./logs.sh <service-name> [extra-kubectl-args]
# Example: ./logs.sh web --tail=100
#          ./logs.sh celery-worker -f
# ================================================================

set -euo pipefail

NAMESPACE="wordfix"

if [ -z "${1:-}" ]; then
  echo "Usage: $0 <service-name> [kubectl-log-args]"
  echo ""
  echo "Available services:"
  echo "  db, auth-db, redis, rabbitmq"
  echo "  web, gateway, auth-service"
  echo "  celery-worker, celery-beat, nginx"
  exit 1
fi

SERVICE="$1"
shift

kubectl logs -n "$NAMESPACE" -l "app.kubernetes.io/name=$SERVICE" "$@"
