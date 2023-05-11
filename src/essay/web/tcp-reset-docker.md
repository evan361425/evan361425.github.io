# Docker Bridge 環境下的 TCP Reset

查找 [conntrack](https://arthurchiao.art/blog/conntrack-design-and-implementation-zh/) 設定：

```bash
sysctl -a | grep 'conntrack'
```

查找 conntrack 下的網路資訊：

```bash
conntrack -S
```

查找 kernel 資訊

```bash
dmesg -T
```
