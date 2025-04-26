#!/bin/bash

# 啟動 Docker 服務（in container）
echo "啟動 Docker 服務..."
dockerd > /var/log/dockerd.log 2>&1 &

# 等待 Docker 完全啟動
echo "等待 Docker 啟動..."
while ! docker info > /dev/null 2>&1; do
    sleep 1
done
echo "Docker 已啟動！"

# 啟動 SSH Server（可選）
echo "啟動 SSH 服務..."
/usr/sbin/sshd -D &
SSHD_PID=$!

# 等待 SSH 服務啟動
sleep 2

# 檢查 sshd 是否啟動成功
if ps -p $SSHD_PID > /dev/null; then
    echo "SSH 服務已啟動！"
else
    echo "SSH 啟動失敗！"
    exit 1
fi

# 最後執行容器的預設命令（讓容器保持運行）
exec "$@"
