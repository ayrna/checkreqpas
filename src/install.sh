#!/usr/bin/env bash
set -euo pipefail

PY_VER="3.12.3"
PY_TGZ="Python-${PY_VER}.tgz"
PY_DIR="Python-${PY_VER}"
PY_URL="https://www.python.org/ftp/python/${PY_VER}/${PY_TGZ}"

echo "==> [1/7] Actualizando repositorios..."
sudo apt update

echo "==> [2/7] Instalando SSH server..."
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl restart ssh

echo "==> [3/7] Instalando dependencias de compilación para Python..."
sudo apt install -y \
  build-essential \
  wget \
  ca-certificates \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  libffi-dev \
  libncursesw5-dev \
  libgdbm-dev \
  liblzma-dev \
  tk-dev \
  uuid-dev

echo "==> [4/7] Descargando Python ${PY_VER}..."
cd /usr/src
sudo wget -q "${PY_URL}" -O "${PY_TGZ}"

echo "==> [5/7] Compilando e instalando Python ${PY_VER} (puede tardar)..."
sudo tar xzf "${PY_TGZ}"
cd "${PY_DIR}"
sudo ./configure --enable-optimizations
sudo make -j"$(nproc)"
sudo make altinstall

echo "==> [6/7] Instalando pip para python3.12..."
sudo python3.12 -m ensurepip
sudo python3.12 -m pip install --upgrade pip

echo "==> [7/7] Instalando paquetes requeridos..."
sudo python3.12 -m pip install --break-system-packages \
  panel==1.8.5 \
  pandas==3.0.0 \
  bokeh==3.8.2 \
  param==2.3.1 \
  pyviz_comms==3.0.6 \
  numpy==2.4.1

sudo apt install -y ansible
echo
echo "=================================="
echo "INSTALACIÓN COMPLETADA"
echo "=================================="

echo "Versiones instaladas:"
python3.12 --version
python3.12 -m pip --version

echo
echo "Estado de SSH:"
sudo systemctl status ssh --no-pager | head -n 5