#!/usr/bin/env bash
set -euo pipefail

DEVICE="${1:-/dev/sdb}"
MOUNT_POINT="/var/lib/swainjohn"

if [[ ! -b "$DEVICE" ]]; then
  echo "[ERROR] Block device not found: $DEVICE"
  exit 1
fi

cryptsetup luksFormat --type luks2 "$DEVICE"
cryptsetup open "$DEVICE" swainjohn_data
mkfs.ext4 -F /dev/mapper/swainjohn_data
mkdir -p "$MOUNT_POINT"
mount /dev/mapper/swainjohn_data "$MOUNT_POINT"
chmod 700 "$MOUNT_POINT"

cat <<EOF > /etc/fstab
/dev/mapper/swainjohn_data  $MOUNT_POINT  ext4  defaults,nofail  0  2
EOF

echo "[INFO] Encrypted storage mounted at $MOUNT_POINT"
