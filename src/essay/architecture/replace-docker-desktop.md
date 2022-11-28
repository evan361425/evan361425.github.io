# 取代 Docker Desktop

Docker Desktop 在[特定條件](https://www.docker.com/blog/updating-product-subscriptions/)下要錢了，該用什麼取代？

現有工具：

-   [lima](https://github.com/lima-vm/lima)，建置 VM 在 macOS 上，並提供 runC 的介面。
-   [nerdctl](https://github.com/containerd/nerdctl)，在 lima 之上建置 containerd。
-   [colima](https://github.com/abiosoft/colima)，把上述兩者整合起來（預設使用 docker，你可以透過 `colima start --runtime containerd` 來調整），讓你可以快速建置環境。
-   [finch](https://github.com/runfinch/finch)，把上述兩者（`lima`, `nerdctl`）整合起來並提供指令介面
-   [podman](https://docs.podman.io/en/latest/index.html)，All-in-one。

關於什麼是 container runtime/engine 有一篇超清楚的文章
[A breakdown of container runtimes for Kubernetes and Docker](https://www.techtarget.com/searchitoperations/tip/A-breakdown-of-container-runtimes-for-Kubernetes-and-Docker)。

![Container runtime 在 Docker 和 Kubernetes 之間的定位](https://i.imgur.com/kF4MT6b.png)

!!! archive ""

    由於許多工具已經開源（開篇那段），你不需要這麼艱難的自己啟一個 VM 來做事，所以這篇文章下面你應該不需要看了😂

    — 2022/11/28

---

你自己建立一個 VM（Linux based）去支撐 Docker，這也是本篇的重點。

> [為什麼要 Docker 要用 VM？](../../feedback/distributed-systems-with-node.js/container.md#docker)

## 移除 Docker Desktop

1. 點選右上角蟲蟲圖案
2. 最下面的 Uninstall

### 重新安裝 Docker

```bash
$ brew install docker
# Optional: docker-compose
$ brew install docker-compose
```

## 準備工具

-   [Vagrant](https://www.vagrantup.com)
-   [VirtualBox](https://www.virtualbox.org)

```bash
brew install vagrant
brew install virtualbox
```

## Provision

建立 Vagrantfile：

```Vagrantfile
# encoding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure('2') do |config|
  # ubuntu 14.x
  # config.vm.box = 'ubuntu/trusty64'
  # ubuntu 16.x
  config.vm.box = 'ubuntu/xenial64'
  # ubuntu 18.x
  # config.vm.box = 'ubuntu/bionic64'
  # ubuntu 20.x
  # config.vm.box = 'ubuntu/focal64'

  # Optional: hostmanager
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.hostmanager.include_offline = true
  config.vm.hostname = 'docker.local'

  # 任一 IP 即可
  # 本機要連結到此 Docker 需要先指定位置
  # export DOCKER_HOST=tcp://192.168.66.4:2375
  # 或者透過 hostmanager 指定的 host name
  # export DOCKER_HOST=tcp://docker.local:2375
  # 但是這會需要更多時間去讓機器去辨認 IP
  config.vm.network 'private_network', ip: '192.168.66.4'

  # guest 代表 VM port，host 代表本機 port
  config.vm.network 'forwarded_port', guest: 2375, host: 2375, id: 'dockerd'
  # 使用 ID 方便記憶
  config.vm.network 'forwarded_port', guest: 80, host: 80, id: 'http'
  # Protocol 有需要，要改
  config.vm.network 'forwarded_port', guest: 2000, host: 2000, id: 'xray', protocol: 'udp'

  config.vm.provision "docker"
  config.vm.provision 'shell', path: 'provision.sh'
end
```

建立 provision.sh

```sh
# Configure Docker to listen on a TCP socket
# https://stackoverflow.com/a/42204921/12089368
# https://dev.to/dhwaneetbhatt/run-docker-without-docker-desktop-on-macos-306h
mkdir /etc/systemd/system/docker.service.d

echo '[Service]
ExecStart=
ExecStart=/usr/bin/dockerd --containerd=/run/containerd/containerd.sock' > /etc/systemd/system/docker.service.d/docker.conf

echo '{
  "hosts": ["fd://", "tcp://0.0.0.0:2375"]
}' > /etc/docker/daemon.json

# Reload configuration
systemctl daemon-reload
systemctl restart docker.service
```

## Go

建立 VM

```sh
# Build VM + provision
$ vagrant up
# play with VM
$ vagrant ssh
# 更新 IP 設定
$ vagrant reload
```

設定 Docker Daemon 路徑

```sh
# IP 或是 Host 詳見上面的 Vagrantfile
$ export DOCKER_HOST=tcp://192.168.66.4:2375
```

開始使用 Docker！
