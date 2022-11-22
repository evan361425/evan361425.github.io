# TCP

Transmission Control Protocol 傳輸控制協定的作用說明。

## OSI 中扮演的角色

Network 之上，Application 之下。

Network 中的 IP 是一種不考慮連線的協定，他只需要負責把封包路由給指定的目的地。在此之上的 TCP
則會透過類似於 HTTP session 的機制，反復確認段（segment）裡的訊號和編號來確保兩端的連線。

換句話說，TCP 是被設計成雙向（bidirectional）、序列性（ordered）和可靠（reliable）的資料傳輸協定。

-   可靠：透過反覆寄送確認信號（Acknowledge，或簡稱 ACK）
-   序列：透過 Sequence(或簡稱 SEQ) 和 ACK 的編號確認順序
-   雙向：開啟連線時，這個連線雙方都可以寫入和讀取的

## 內容物

![TCP 標頭格式](https://i.imgur.com/3nh6DOI.png)

> Source from [鄭中勝](https://notfalse.net/26/tcp-seq)

TCP 會透過上述各種編號和訊號來完成連線所需的溝通。當建立連線（三次握手）後，雙方就不存在監聽方和發起方。兩者皆可以做監聽和送訊息，同時雙方也都可以要求中斷連線，並且雙方都要同意關閉才能真正完整關閉連線（四次揮手）。其完整生命的程如下：

![TCP 狀態流程](https://imgur.com/jeS7mge.png)

### TCP 信號

-   URG
-   ACK
-   PSH
-   RST
-   SYN
-   FIN

### 三次握手

![三次握手的範例](https://i.imgur.com/tsr9hCN.png)

> Source from [鄭中勝](https://notfalse.net/26/tcp-seq)

彼此會在三次握手中確認接下來的 `SEQ` 號碼：

-   主動方（或稱發起方、客戶端）送出要求連線的同步信號（Synchronous 或稱 SYN）
-   監聽方（或稱服務端、私服端）允許連線（AWK）並同樣賦予同步信號（SYN）
-   主動方允許連線

### 四次揮手

主動關閉（Active Close）的那方可以根據需求關閉連線，但是對被動關閉（Passive Close）的那方來說，傳送的資料可能還沒完成，這時就需要等應用層資料都送出去之後，才會再一次做關閉的動作。

![TCP 四次揮手流程](https://i.imgur.com/qFzjzri.png)

所以流程大致如下：

-   *主動方* 要求關閉連線 `FIN`，並進入 `FIN_WAIT1` 狀態。
-   *被動方* 告知收到這個資訊 `AWK`。
-   *主動方* 進入等待 `FIN_WAIT2` 狀態。
-   *被動方* 確保資料都送完後，關閉連線 `FIN`。
-   *主動方* 告知收到這個資訊 `AWK`，此時被動方不用管有沒有收到這個 `AWK`。
-   *主動方* 進入 `TIME_WAIT` 狀態，等到超過兩次 MSL（Maximum Segment Lifetime）的時間後，關閉連線。

這時你就會注意到一件事，身為主動關閉的那方，是需要付出代價的！他需要進入等待對方關閉的狀態（`FIN WAIT 1` 或 `FIN WAIT 2`）；相較而言，被動那方就只要確認關閉後，就可以瀟灑說再見了。

之所以要進入 `TIME_WAIT` 這個狀態是因為如果直接使用這個來源埠，下次的連線很可能會收到上次連線的重送（Retransmission）資訊。

### TCP 選項

大部分都是在握手階段確認的，[詳見](https://www.geeksforgeeks.org/options-field-in-tcp-header/)：

-   0: End of options
-   1: no-op
-   2: MSS(Maximum TCP Segment Size)，協商段的大小
-   3: Window Scaling，提高客戶端可用頻寬
-   4: SACK（Selective ACK），加速重傳的機制
-   8: Timestamp，精準 RTT
-   34: TFO（TCP Fast Open）

Kernel options 可以參考 [sysctl-explorer](https://sysctl-explorer.net/net/)

### Congestion Control

[BBR](https://github.com/evan361425/evan361425.github.io/issues/34), [Queue-Discipline](https://sysctl-explorer.net/net/core/default_qdisc/)

### 範例

以連線到 google.com 中產生的多個封包做說明。

> 如果是 HTTP/3 就不是 TCP 了，到時要看看用什麼網站比較好。

#### 三次握手

MSS(Maximum TCP Segment Size) v.s. MTU(Maximum Transmission Unit):

```text
MTU = MSS + 40 (IP header + TCP header)
```

#### SEQuence number

TBD

#### AWKnowledge number

TBD

#### Options

TBD

## BSD Socket API

TCP 在 Berkeley Socket 之上的流程。

Socket 為包裝底層運作的 API，包括 Data Link Layer 和 Network Layer。

![TCP 在 Berkeley Socket 之上的流程，made by OnionBulb](https://i.imgur.com/oZrUYJQ.png)

| 名稱   | 功能                                            |
| ------ | ----------------------------------------------- |
| Socket | 建立 Socket 來監聽（listen）連線                |
| Bind   | 綁定 address 和 port，可設定 IP 遮罩            |
| Listen | 監聽 TCP 連線和限制連線數，UDP 不需要呼叫本函式 |
| Accept | 迴圈去接受連線，並進行後續的交握行為            |

> 各流程簡介

??? note "實作範例"

    綁定 port 和位置（IPv4）後建立連線：

    ```c
    bzero((char *)&server, sizeof(struct sockaddr_in));
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(sd, (struct sockaddr *)&server, sizeof(server)) == -1) {
        fprintf(stderr, "Can't bind name to socket\n");
        exit(1);
    }
    ```

    ```c
    listen(sd, 5); // (1)

    while (1) {
        client_len = sizeof(client);
        new_sd = accept(sd, (struct sockaddr *)&client, &client_len); // (2)
        if (new_sd == -1) {
            fprintf(stderr, "Can't accept client\n");
            exit(1);
        }
        // ...
    }
    ```

    1. 限制最高五個連線
    2. 拿 `new_sd` 去讀寫資料，`sd` 則繼續監聽連線請求。

## 問題

??? question "為什麼會有遺失、重複寄送和失序的問題？"

    遺失：很可能實際有送到指定位置，但是因為傳輸過程訊號被干擾了，導致[檢驗和](https://notfalse.net/27/tcp-error-control)的檢查失敗。

    重複寄送：建立在遺失之上的問題，當目的地收到並回傳 `AWK` 時，發送方很可能沒收到這個訊號，就誤以為沒送成功，就再送一次。

    失序：原本是照 1,2,3,... 的順序送出去，收到卻很可能是 3,1,4,...，這可能是因爲壅塞或網路延遲造成的，甚至可能每個封包路由路徑不同（IP 的協定會決定這一系列的封包怎麼送）

??? question "當 TCP 連線被開滿了，會發生什麼事？"

    需要先定義被開滿了是什麼意思，是部分進入 `TIME_WAIT` 狀態嗎，還是所有都是 Active 的狀態？

    如果是 `TIME_WAIT` 的狀況可以考慮關閉 `TIME_WAIT` 的連線。
    
    若都是 Active 的狀態，且資源的允許下則可以考慮用 Virtual IP 建立更多連線，因為 TCP 的每個連線都是以 IP 和 Port 為一個組合。詳見 [The Road to 2 Million Websocket Connections in Phoenix](https://www.phoenixframework.org/blog/the-road-to-2-million-websocket-connections)。

??? question "如何關閉 TIME_WAIT 狀態的連線？"

    你可以賦予該連線一個選項：[`SO_REUSEADDR`](http://www.unixguide.net/network/socketfaq/4.5.shtml)，在 Linux 中，你也可以調整 [`TCP_TW_REUSE` 或 `TCP_TW_RECYCLE`](https://docs.ukcloud.com/articles/vmware/vmw-ref-twreuse.html)：

    > This socket option tells the kernel that even if this port is busy (in the TIME_WAIT state), go ahead and reuse it anyway. If it is busy, but with another state, you will still get an address already in use error. It is useful if your server has been shut down, and then restarted right away while sockets are still active on its port. You should be aware that if any unexpected data comes in, it may confuse your server, but while this is possible, it is not likely.

    或者調整 Maximum Segment Lifetime(MSL)：
    
    ```bash
    # 看一下現在狀態
    $ sysctl net.ipv4.tcp_fin_timeout
    # VI 改
    $ vi /proc/sys/net/ipv4/tcp_fin_timeout
    # Hot reload
    $ sysctl -p /etc/sysctl.conf
    ```

??? question "什麼是 TCP Timeout？"

    就是應用層的某些 HTTP Client 套件會寫的 Connection Timeout，通常系統層的預設為十分鐘。

現在有一個狀況：

-   網路頻寬正常偏高，但沒有突破限制。
-   應用層的資源使用率低，CPU/Mem 維持在 5% 左右。
-   HTTP 的延時非常高，數十秒

??? question "請問上述狀況可能的原因？"

    當然不能一概而論，不過有遇過這個經驗。那次的原因是因為下游的服務系統層連線數被吃滿了，但是資源使用率仍在正常的水平。

    因為系統層連線被吃滿了，所以開始造成服務需要花很多時間才能建立連線（等待其他連線被關閉），同時下游服務會因為 TCP 天生的機制開始反壓（back-pressure），在上游仍會有一定的網路頻寬耗用率。

    這時的解決辦法除了前面「當 TCP 連線被開滿了，會發生什麼事？」的解決之道之外，有幾個應用層面的處理機制：

    -   新增節點，恩，單純而暴力
    -   分散服務，就是提供微服務
    -   應用程式的調整，因為單一應用請求會打很多個不同資料庫的請求：
        -   使用[事件機制](../../feedback/designing-data-intensive-applications/derived-stream.md)，降低前端需要定期確認資料是否更新
        -   使用快取，並利用快取減少需要和多個資料庫溝通的過程
        -   和資料庫的溝通中增加一個代理器，只需要和他建立連線即可
        -   調整前端應用層協定
            - [GraphQL](../../feedback/distributed-systems-with-node.js/protocol.md#graphql)
            - [HTTP/3](https://github.com/evan361425/evan361425.github.io/issues/27)
