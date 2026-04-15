#!/bin/bash
# ================================================================
# WordFix — Kubernetes Status Script
# Shows overview of all pods, services, and PVCs
# ================================================================

set -euo pipefail

NAMESPACE="wordfix"
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=== Pods ===${NC}"
kubectl get pods -n "$NAMESPACE" -o wide
echo ""

echo -e "${CYAN}=== Services ===${NC}"
kubectl get svc -n "$NAMESPACE"
echo ""

echo -e "${CYAN}=== Persistent Volume Claims ===${NC}"
kubectl get pvc -n "$NAMESPACE"
echo ""

echo -e "${CYAN}=== StatefulSets ===${NC}"
kubectl get statefulsets -n "$NAMESPACE"
echo ""

echo -e "${CYAN}=== Deployments ===${NC}"
kubectl get deployments -n "$NAMESPACE"
