#!/bin/bash

# ============================
# Configuración
# ============================
DASHBOARD_DIR="/home/tfg-audit/hosts"
DASHBOARD_FILE="dashboard.py"
PORT=5006
ADDRESS="0.0.0.0"

# Orígenes permitidos (VirtualBox / local)
ORIGINS=(
#  "--allow-websocket-origin=localhost:${PORT}"
#  "--allow-websocket-origin=127.0.0.1:${PORT}"
  "--allow-websocket-origin=192.168.56.103:${PORT}"
)

# ============================
# Comprobaciones básicas
# ============================
if [ ! -f "${DASHBOARD_DIR}/${DASHBOARD_FILE}" ]; then
  echo " No se encuentra ${DASHBOARD_FILE} en ${DASHBOARD_DIR}"
  exit 1
fi

echo "📊 Lanzando dashboard de auditorías..."
echo "➡  URL: http://<IP_AUDITORA>:${PORT}/dashboard"

# ============================
# Lanzar Panel
# ============================
cd "${DASHBOARD_DIR}" || exit 1

python3 -m panel serve "${DASHBOARD_FILE}" \
  --address "${ADDRESS}" \
  --port "${PORT}" \
  "${ORIGINS[@]}"
