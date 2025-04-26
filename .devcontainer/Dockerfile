FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# 安裝系統工具 & Docker & VSCode Remote Dev 套件
RUN apt update && apt install -y \
    sudo \
    openssh-server \
    git \
    curl \
    vim \
    htop \
    net-tools \
    bash-completion \
    unzip \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    gnupg \
    lsb-release \
    zsh \
    docker.io \
    iputils-ping \
    && apt clean

# 建立使用者 dev
RUN useradd -m -s /bin/bash dev && echo "dev:dev123" | chpasswd && adduser dev sudo

# 確保 dev 使用者有權限寫入 Docker 日誌
RUN touch /var/log/dockerd.log && chown dev:dev /var/log/dockerd.log

# Docker group 權限給 dev
RUN usermod -aG docker dev

# 啟用 bash 彩色提示、自動補齊、自訂 prompt
RUN echo "force_color_prompt=yes" >> /home/dev/.bashrc && \
    echo "if [ -f /etc/bash_completion ]; then . /etc/bash_completion; fi" >> /home/dev/.bashrc && \
    echo "alias ll='ls -alF --color=auto'" >> /home/dev/.bashrc && \
    echo "export PS1='\\n\\[\\e[38;5;75m\\]Steven\\[\\e[0m\\] @ \\[\\e[37m\\]\\h\\n\\[\\e[38;5;220m\\]\\w\\[\\e[0m\\] \\n\\[\\e[92m\\]\\$\\[\\e[0m\\] '" >> /home/dev/.bashrc && \
    echo "echo 'HI Steven, Have a Cool Day!!\n\n( ￣□￣)/ 敬禮!! <(￣一￣ ) <(￣一￣ ) '" >> /home/dev/.bashrc && \
    chown dev:dev /home/dev/.bashrc

    # 設定 SSH
RUN mkdir /var/run/sshd
RUN echo "Port 22" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin no" >> /etc/ssh/sshd_config
RUN echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
RUN echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config

# VSCode Remote Dev 支援
RUN mkdir -p /home/dev/.vscode-server/extensions
RUN chown -R dev:dev /home/dev/.vscode-server

# Docker-in-Docker 需要
VOLUME /var/lib/docker

# Entrypoint 腳本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 設定開放的端口
EXPOSE 22

# 設定默認命令
ENTRYPOINT ["/entrypoint.sh"]
