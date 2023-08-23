---
tags: Debugging
title: TCP socket 連線被清除的錯誤排查
description: 連線會在一段時間後關閉，發生什麼事了？
image: https://i.imgur.com/fRevWCC.png
---

服務是放在 Ubuntu 18 的 Docker 之中，它會在啟動之初和 Redis 進行連線，
但是這連線會在一段時間之後，莫名失效：對服務來說連線還在，但是對 Redis 來說卻不在。

本文將是撰寫這個狀況的排查過程。

## 怎麼確認連線狀況

我們在三個地方進行連線狀況的檢查，分別是 Redis、Ubuntu（Host）和承載服務的容器（Container）。

![列出狀態連線](https://i.imgur.com/2Wo5cac.png)

> /我們使用 [netstat](https://man7.org/linux/man-pages/man8/netstat.8.html)，
> 但也可以使用更現代的 [ss](https://man7.org/linux/man-pages/man8/ss.8.html)。

```bash
$ netstat -tn | grep ESTABLISHED
tcp 0 0 172.0.0.1:53558 172.0.0.2:6379 ESTABLISHED
tcp 0 0 172.0.0.1:37672 172.0.0.2:6379 ESTABLISHED
```

上述範例是列出在 Host 上和 Redis（port 6379）建立的連線。
同樣的指令可以在容器內部和 Redis 上看到，只是 Redis 的 `grep` 就會改成 `LISTEN`

## 行為表現

當連線建立之後的一段時間後（約五到三十分鐘，不固定，但不會超過三十分鐘），
Redis 就會收到 TCP `RST`，然後把連線關掉：

![TCP 封包截圖](https://i.imgur.com/52vv4vK.png)

在時間 *14:28:29.395914*（封包編號 2886）時，client 和 Redis 建立完成連線，
在 *14:28:29.443402*（封包編號 2919）時，完成一系列 Redis 商務邏輯的使用。
過了約五分鐘，Redis 回應 TCP Keep-Alive（僅有標頭的封包，編號 3855），
但這是預期的封包，因為我們在 Redis 設定了 300 秒的
[TCP Keep-Alive](https://redis.io/docs/reference/clients/#tcp-keepalive)。

但令人疑惑的是，client 卻在下一個封包（編號 3856）回應 TCP `RST`。

當我們透過上述方法確認連線狀況時，
不管從 Host 還是 Container 的角度來看，連線都還在。
所以，這個 TCP `RST`，究竟是誰發的？

## Smoking gun 1 - system-network

就結論來說，這個是錯誤方向，不過在這裡記錄一下。

Ubuntu 基本都會裝上 systemd 去管理很多系統服務，其中一個就是 system-network。
相關的 issue（[docker0 interface keeps losing IPv4 ipaddress](https://github.com/moby/moby/issues/40217#issuecomment-708276691)）
表現了很類似的特徵，故而開始朝著方向追。
但是在機器上透過 `networkctl list` 列出的資料卻不符合 issue 上的說明：

```bash
$ networkctl list
IDX LINK            TYPE     OPERATIONAL SETUP
  1 lo              loopback carrier    unmanaged
  2 ens3            ether    routable   configured
  3 ens4            ether    off        unmanaged
  4 docker0         ether    no-carrier unmanaged
942 br-788fecf403ed ether    routable   unmanaged
944 veth6af5546     ether    degraded   unmanaged

6 links listed.
```

由上可知，docker 相關的 link（`docker0`、`br-*` 和 `veth*`）都不是透過 system-network 去管理了。

> 其中的 degraded 代表該 link 沒有 public IP，因為是虛擬介面，所以這樣是正常的。

## 重新思考行為表現

我們知道 Host 認為他的的連線還在，所以有個應用在 netstat 感知到變化之前就拒絕掉封包了，
所以我們必須去了解 netstat 的運作流程。

??? note "推薦使用 ss"
    [`ss`](https://man7.org/linux/man-pages/man8/ss.8.html) 是被認為[應該取代
    netstat 的工具](https://training.linuxfoundation.org/resources/tutorials/an-introduction-to-the-ss-command/)。

    > the netstat command has been deprecated in favor of the faster,
    > more human-readable ss command.
    
    事實上，很多工具已經被認為是過時的，以 Linux foundation 中推薦的
    [networking 工具](https://wiki.linuxfoundation.org/networking/net-tools)為例：

    | program | obsoleted by |
    | - | - |
    | arp | ip neigh |
    | ifconfig | ip addr |
    | ipmaddr | ip maddr |
    | iptunnel | ip tunnel |
    | route | ip route |
    | nameif | ifrename |
    | mii-tool | ethtool |

    `ss` 是透過 [socket_diag](https://man7.org/linux/man-pages/man7/sock_diag.7.html)
    去取得 OS's kernel 的連線資訊，包括：

    -   [socket](https://www.tutorialspoint.com/unix_sockets/socket_structures.htm)
    -   [routing table](https://www.halolinux.us/kernel-reference/routing-data-structures.html)
    -   [connection tracking](https://arthurchiao.art/blog/conntrack-design-and-implementation/)

netstat 是透過 `/proc` 的資料夾來取得現有的連線資訊，
換句話說，對 netstat 來說，連線資訊其實是 user-space 而非 kernel space：

![Kernel routing 的簡易流程圖](https://i.imgur.com/CcKOuXx.png)

上面這張圖很複雜，但是既然徵狀是 TCP `RST` 那我們就專注於 layer3 的流程。
在進到 user-space 之前，會有三大塊：

-   pre-routing，紀錄（conntrack）、修正（mangle）、轉址對應（NAT）
-   routing decision，判斷是否送給 user-space
-   input，修正（mangle）、篩選（filter）

mangle 和 filter 都是 iptables 等防火牆服務會跟 OS 註冊 Hooks 來達成，
在 Linux 中，實踐這個 Hook 的就是 [Netfilter](https://en.wikipedia.org/wiki/Netfilter)。
在雲原生環境的 [Cilium](https://cilium.io/) 則是透過 Linux 中的 [eBPF](https://ebpf.io/) 實踐。

NAT 則是用來修正 IP 來達到溝通，經典的用法就是把
[本地 IP 轉成外部 IP](https://arthurchiao.art/blog/conntrack-design-and-implementation-zh/#151-网络地址转换nat)。

那 pre-routing 的 conntrack 是什麼呢？

## Smoking gun 2 - conntrack

conntrack（connection tracking）被設計來[追蹤協定的流程狀態](https://blog.cloudflare.com/conntrack-tales-one-thousand-and-one-flows/)，
這裡的流程也可稱為連線狀態，但要注意這個「連線」並不是 L4 意義上的連線，
最明顯的特徵就是 conntrack 仍會去追蹤 UDP、ICMP 這類非「連線」的協定。

什麼是流程狀態？舉個例子，當你收到 TCP `ACK`，你可以知道目前這個封包目的是什麼嗎？

-   完整收到上一個資料的「確認通知」？
-   Keep-Alive 通知？
-   三次交握完成通知？
-   四次揮手的階段或完成通知？

在不知道現在流程的狀態下，你怎麼辨別這個 `ACK` 是帶有惡意的 `ACK` 還是正常的 `ACK`？

??? example "TCP ACK Scan"
    透過在所有 port 上面發送 ACK 我可以確保目前該節點開通了哪些 port（包含那些 client port），
    如果 port 被開通，我就會收到 TCP RST，反之則會沒有任何回應。

    如果我想要讓這類的封包都不給任何回應，我就需要讓 conntrack 有能力辨別哪個 ACK 是正確的 ACK。

為了記錄這些流程，你可以想像 conntrack 會追蹤至少六種的資料：

-   [協定種類](https://elixir.bootlin.com/linux/v5.19.17/source/include/net/netfilter/nf_conntrack.h#L32)
-   source IP, port
-   destination IP, port
-   connection state

```bash
$ conntrack -L
udp 17 29 src=172.0.0.1 dst=172.0.0.3 sport=138 dport=138 [UNREPLIED] src=172.0.0.3 dst=172.0.0.1 sport=138 dport=138 mark=0 use=1
tcp 6 110 TIME_WAIT src=172.0.0.1 dst=172.0.0.4 sport=40286 dport=80 src=172.0.0.4 dst=172.0.0.1 sport=80 dport=40286 [ASSURED] mark=0 use=1
```

分析一下輸出：

-   conntrack 收到一個 UDP 封包；
-   [協定編號 17](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)；
-   29 秒後這個資料將會被清除，根據協定的不同，達到特定狀態後這個值將會被重置；
-   `UNREPLIED` 代表這個 UDP「連線」沒有收到回覆，這是 [UDP 特有的狀態](https://elixir.bootlin.com/linux/v5.19.17/source/include/net/netns/conntrack.h#L37)；
-   IP 和 Port
-   mark，根據商務邏輯標記這個連線，例如 iptables 的阻擋等等；
-   [use](https://elixir.bootlin.com/linux/v5.19.17/source/include/net/netfilter/nf_conntrack.h#L60) 是 counter 用來記錄 GC 狀態。

在第二行中，TCP 連線最後進入 [`ASSURED`](https://thermalcircle.de/doku.php?id=blog:linux:connection_tracking_3_state_and_examples#nfconnstatus_detail) 狀態，
代表這個連線已經建立起來不會被因為倒數計時而被回收，但是它仍會在 TCP 結束連線後被回收。

> 預設可以記錄 256K 個流程資訊，你可以透過 `cat /proc/sys/net/nf_conntrack_max` 來確認。
>
> 如果你想知道不同協定得到的狀態有哪些，可以參考這篇
> [blog](https://www.cnblogs.com/huenchao/p/6225770.html)。

??? success "conntrack 的教學資源"
    conntrack 很複雜，光是理解這個套件存在目的就需要一些時間，底層實作更是複雜。
    網路上有找到一些教程：

    1. [Connection tracking (conntrack) - Part 1: Modules and Hooks](https://thermalcircle.de/doku.php?id=blog:linux:connection_tracking_1_modules_and_hooks)
    2. [Connection tracking (conntrack) - Part 2: Core Implementation](https://thermalcircle.de/doku.php?id=blog:linux:connection_tracking_2_core_implementation)
    3. [Connection tracking (conntrack) - Part 3: State and Examples](https://thermalcircle.de/doku.php?id=blog:linux:connection_tracking_3_state_and_examples)

    Fedora Magazine 關於 conntrack 的介紹：

    1. [Network address translation part 1 – packet tracing](https://fedoramagazine.org/network-address-translation-part-1-packet-tracing/)
    2. [Network address translation part 2 – the conntrack tool](https://fedoramagazine.org/network-address-translation-part-2-the-conntrack-tool/)
    3. [Network address translation part 3 – the conntrack event framework](https://fedoramagazine.org/conntrack-event-framework/)
    4. [Network address translation part 4 – Conntrack troubleshooting](https://fedoramagazine.org/network-address-translation-part-4-conntrack-troubleshooting/)

### 連線表被塞滿會發生什麼事

有個 [cloudflare blog](https://blog.cloudflare.com/conntrack-tales-one-thousand-and-one-flows/#canconntracktablefillup)
說明這件事，簡單來說，可能會把新的封包丟棄並捨棄 conntrack 表格中那些非 `ASSURED` 的連線。

### 連線表被重置後會發生什麼事

如同前面提到的「TCP ACK Scan」，
如果 conntrack 收到沒有註冊的 TCP `ACK`，預設會回應 TCP `RST`。

這和我們觀察到的行爲表現一樣，但我們的連線表被重置了嗎？

#### 連線表被重置了嗎

因為表徵是一樣的，服務感知不到 TCP Keep-Alive，但是卻透過 tcpdump 觀察到 TCP `RST`，
所以我們開始懷疑是不是 conntrack 的問題，順著這樣的思維，嘗試尋找證據。

```bash
$ conntrack -L | grep 6379 | grep -n ESTABLISHED | wc -l
conntrack v1.4.4 (conntrack-tools): 171 flow entries have been shown.
25
```

這個指令告訴我們，現在和 Redis（port 6379）的連線有 25 條，
接著定期去檢查這個指令的結果，就會發現一段時間之後，它被清空了：

```bash
$ watch -c 'conntrack -L | grep 6379 | grep -n ESTABLISHED | wc -l'
conntrack v1.4.4 (conntrack-tools): 90 flow entries have been shown.
0
```

透過 syslog 也可以追查到當 conntrack 顯示為 0 的時候，有這樣相關的紀錄：

```bash
$ tail -f /var/log/syslog | grep DHCP
Jul 4 10:52:38 my-host systemd-networkd[913]: ens3: DHCP lease lost
Jul 4 10:52:38 my-host systemd-networkd[913]: ens3: DHCPv4 address 172.1.0.1/20 via 172.1.0.2
```

可以看到當 conntrack 被清空時（`conntrack -L` 為零），DHCP Server 的請求被了送進來，
這種巧合，足以讓我們繼續深入追蹤。也進一步發現一些相關 issue：

-   [systemd-networkd removes IPv4 address during DHCP renewal](https://github.com/systemd/systemd/issues/16071)
-   [DHCP Renew Causing Interface To Restart](https://github.com/systemd/systemd/issues/15421)

也注意到 systemd.networkd 在管理連線的時候，可能會尊重 DHCP 的請求並重新綁定本地位置：

> [KeepConfiguration](https://systemd.network/systemd.network.html#KeepConfiguration=)
>
> Takes a boolean or one of "static", "dhcp-on-stop", "dhcp". When "static",
> systemd-networkd will not drop static addresses and routes on starting up process.
> When set to "dhcp-on-stop", systemd-networkd will not drop addresses and routes on
> stopping the daemon. When "dhcp", the addresses and routes provided by a DHCP server
> will never be dropped even if the DHCP lease expires. This is contrary to the DHCP
> specification, but may be the best choice if, e.g., the root filesystem relies on this
> connection. The setting "dhcp" implies "dhcp-on-stop", and "yes" implies "dhcp" and
> "static". Defaults to "dhcp-on-stop" when systemd-networkd is running in initrd, "yes"
> when the root filesystem is a network filesystem, and "no" otherwise.

不過不管原因是什麼，最終我們的解法是在 DHCP Server 中綁定靜態 IP，
避免每隔三十分鐘重新設定一次 IP。

## 哪裡可以加速

在處理這問題的時候其實花了很多時間，主要是因為對 Linux 底層處理連線的不清楚。
重新順一下排查的脈絡：

-   在 Client、Server（Redis）、Firewall 三端執行 TCP Dump，看到連線被正常建立。
-   Server 預設會每五分鐘做一次 TCP Keep-Alive，當它送出 Keep-Alive `ACK` 封包：
    -   Firewall 有看到 `ACK` 封包；
    -   Client 有看到 `ACK` 封包，並且接著回應 `RST` 封包；
    -   Firewall、Server 都收到 `RST`，並且釋放相關資源。
-   此時透過 netstat 在 Client 上得知對應用程式來說，連線仍然存在；
-   懷疑 TCP Keep-Alive 的某種封包錯誤，並嘗試把頻率從 5 分鐘降到 30 分鐘；
-   檢查封包其中的格式和各個設定；
-   懷疑 Linux 底層實作，網路上查各種可能；
-   最終推測 conntrack 的表重置，並透過 syslog 得到 DHCP 的說明。

其實排查過程很重要的一點是 log，但卻常常被忽略，
我們應該在 TCP Dump 的過程，一起去監聽 Log 的輸出。

既然排查出是 client 的問題，我們也可以試著在相同環境的其他節點看看是否有連線錯誤問題。
最後就是雖然非系統管理者平常不應該在線上環境中操作相關節點，但是當進入排查的流程時，
需要盡快讓相關人員有權限可以進到節點進行各種實驗，否則每次做操作都需要大家約時間，簡直曠日費時。

最後，這段的排查很大程度是同事 Angus 做的，在這邊僅作簡單紀錄，
若未來有任何人因為這篇文章得到幫助，僅以此表達對 Angus 的感謝。
