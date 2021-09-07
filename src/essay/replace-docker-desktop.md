# 取代 Docker Desktop

Docker Desktop 在[特定條件](https://www.docker.com/blog/updating-product-subscriptions/)下要錢了，該用什麼取代？

現有工具：

- [Lima](https://github.com/lima-vm/lima)

除此之外，還可自己建立一個 VM（Linux based）去支撐 Docker。

> [為什麼要用 VM？](../feedback/distributed-systems-with-node.js/container.md#docker)

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

- [Vagrant](https://www.vagrantup.com)
- [VirtualBox](https://www.virtualbox.org)

```bash
$ brew install vagrant
$ brew install virtualbox
```

## Provision

建立 Vagrantfile：

```Vagrantfile
# encoding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"

# Connet to Docker:
# export DOCKER_HOST=tcp://192.168.66.4:2375

Vagrant.configure('2') do |config|
  # ubuntu 14.x
  # config.vm.box = 'ubuntu/trusty64'
  # ubuntu 16.x
  config.vm.box = 'ubuntu/xenial64'
  # ubuntu 18.x
  # config.vm.box = 'ubuntu/bionic64'
  # ubuntu 20.x
  # config.vm.box = 'ubuntu/focal64'

  config.vm.network 'private_network', ip: '192.168.66.4'
  config.vm.network 'forwarded_port', guest: 2375, id: 'dockerd'

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
```

設定 Docker Daemon 路徑

```sh
$ export DOCKER_HOST=tcp://192.168.66.4:2375
```

開始使用 Docker！
