---
description: Google 設計的 L4 負載均衡器，本篇詳解該論文。
image: https://i.imgur.com/tTQo0cN.png
---

# Maglev

本篇針對 2016 年的論文
[Maglev: A Fast and Reliable Software Network Load Balancer](https://static.googleusercontent.com/media/research.google.com/zh-TW//pubs/archive/44824.pdf)
進行說明。

## 概述

![不像傳統 LB 使用 active-standby 來避免連線問題，Maglev 透過一些設計達到水平擴展的能力。](https://i.imgur.com/LzeEwyQ.png)

Maglev 是個軟體 L4 負載均衡器，他被建構在一般的 Linux 機器上，
所以可以很大地節省維護硬體設備的特殊專業。
除此之外，他不像硬體設備那樣通常都是 active-standby，
而是每台設備都能有效地處理封包，輕易達到水平擴展。
在使用 8 core、128 GiB 和 10 Gbps NIC 的當代（2016）硬體下，
每台設備達到約 12 Mpps 的處理能力。

![Maglev 基本上只有處理 L3 和 L4](https://i.imgur.com/ccF7zsw.png)

網路在傳輸時，實際的邏輯會被封裝好幾層，這就是 [OCI 分層](./network-routing.md)。
當 Maglevs 前面的 *路由器*（router）收到封包的時候，會透過 ECMP 決定分派哪個 Maglev。
此時，Maglev 根據 L3 和 L4 的資訊組成一個組合，稱為 5-tuple[^1]，
也就是：來源 IP、目的 IP、來源阜、目的阜、協定類別。
透過這個組合，依照 consistent hashing 指定應用叢集裡的最終處理節點。

![封包流程從使用者到 router 再到 Maglev，最後則是實際的服務。](https://i.imgur.com/hmcsgMB.png)

說起來簡單，但是論文內介紹的一些實作，做起來卻並不簡單。

### 背景知識

在開始講細節前，先簡單補足一下背景知識。

#### ECMP

Equal-cost multi-path routing (ECMP) 是一種路由演算法，我們來透過實際案例了解他吧！

假設有一個路由器 (R) 連接到三台伺服器 (S1, S2, S3) 和一台客戶端機器 (C)。
從 R 到達伺服器有兩個等價成本的路徑，*路徑 1* (R -> 介面 1) 和*路徑 2* (R -> 介面 2)。
ECMP 的封包流動如下：

-   客戶端啟動流量：客戶端 C 向伺服器 S1 發送封包。
-   封包到達路由器：封包到達路由器 R。
-   ECMP 選擇：由於有兩個等價成本的路徑 (*路徑 1* 和*路徑 2*) 可達 S1，因此 ECMP 將發揮作用。
  路由器使用雜湊算法（基於源和目的地 IP 地址等因素）來確定此特定封包的路徑。
    -   假設雜湊函數為此封包選擇了*路徑 1* (介面 1)。
-   封包轉發：路由器 R 將封包轉發到介面 1，朝向伺服器 S1。

現在，想像客戶端 C 向伺服器 S1 發送另一個封包。ECMP 將再次根據雜湊算法計算路徑。
有兩種可能性：

-   如果雜湊函數再次選擇路徑 1，此封包將遵循與前一個封包相同的路徑。
-   如果雜湊函數這次選擇了路徑 2 (介面 2)，則封包將採取不同的路由到達 S1，從而實現負載平衡。

ECMP 的優點：

-   增加頻寬：通過利用多條路徑，ECMP 可以分佈流量並潛在提高整體網路吞吐量。
-   容錯性：如果一條路徑不可用，流量可以自動重新路由到剩餘路徑，從而提供冗餘。

需要考慮的事項：

-   連線的處理：如果封包走到另外一台設備，原本的連線根據實作可能會中斷

然而 Maglev 透過一些手段，來避免連線的中斷。

#### Linux Bypass

Linux 在[處理封包的時候](https://www.thebyte.com.cn/network/networking.html)是複雜的，
這是因為他需要處理很多 L3/L4 的實作邏輯。
而在 Maglev 實作中，則是使用 Linux [kernel bypass](https://blog.cloudflare.com/kernel-bypass) 這個模組，透過客製化達到高效性。

## 實作細節

### 服務發現

![透過設定得知有哪些 VIP、這些 VIP 對應哪些 Backend Pool (BP) 以及每個 BP 對應哪些 IP，並由 Health Checkers 來決定哪些節點可用。](https://i.imgur.com/8JjFpnT.png)

透過 Config Manager 分發所有上游的設定，包含上游服務各個節點的實體 IP 和代表服務的 VIP
同時會有個 Health Checker 檢查上游並決定哪些上游可以接收封包。

由於分散式的架構，兩台 Maglev 有可能會有短暫的時間不是同個設定，
這時透過 consistent hashing 可以選擇到相同的上游，這段詳見 [Consistent Hashing](#Consistent Hashing)。

最後 Maglev 也會透過設定得到的 VIP 來透過 Boarder Gateway Protocol (BGP) 做 IP 的發布。

### Forwarder

### Packet Pool

### Consistent Hashing

## 測試

## 延伸

### Sharding

[^1]: 參閱第三段 3，Forwarder Design and Implementation
*[VIP]: Virtual IP，虛擬 IP，透過中間人去把虛擬的 IP 轉化成實體 IP。
