# TCP

Transmission Control Protocol 傳輸控制協定的作用說明。

## OSI 中扮演的角色

Network 之上，Application 之下。

Network 中的 IP 是一種不考慮連線的協定，他只需要把封包路由給指定的目的地，在此之上的 TCP 則
會透過類似於 HTTP session 的機制，反復確認段（segment）裡的編號來確保兩端的連線是否仍存在。

由上述可知道 TCP 是被設計成雙向（bidirectional）、序列性（ordered）和可靠（reliable）的
資料傳輸協定。

-   可靠：透過反覆寄送沒被確認（Acknowledge）收到的段
-   序列：透過 SYN/ACK 的編號確認順序
-   雙向：開啟連線時，這個連線是可以同時寫入和讀取的

![TCP 狀態流程](https://imgur.com/jeS7mge.png)

當三次握手建立連線後（`SYN`, `SYN+AWK`, `AWK`），雙方就不存在監聽方和發起方。兩者皆是同樣的
角色，同時雙方也都可以要求中斷連線，並且雙方都要同意關閉才能真正完整關閉連線（[四次揮手](#_5)）。

## BSD Socket API

TCP 在 Berkeley Socket 之上的流程，Socket 為包裝底層運作的 API，包括 Data Link Layer 和 Network Layer。

![TCP 在 Berkeley Socket 之上的流程，made by OnionBulb](https://i.imgur.com/oZrUYJQ.png)

### 各流程簡介

| 名稱   | 功能                                            |
| ------ | ----------------------------------------------- |
| Socket | 建立 Socket 來監聽（listen）連線                |
| Bind   | 綁定 address 和 port，可設定 IP 遮罩            |
| Listen | 監聽 TCP 連線和限制連線數，UDP 不需要呼叫本函式 |
| Accept | 迴圈去接受連線，並進行後續的交握行為            |

### 實作範例

```c
/* Bind an address to the socket */
bzero((char *)&server, sizeof(struct sockaddr_in));
server.sin_family = AF_INET;
server.sin_port = htons(port);
server.sin_addr.s_addr = htonl(INADDR_ANY);
if (bind(sd, (struct sockaddr *)&server, sizeof(server)) == -1) {
  fprintf(stderr, "Can't bind name to socket\n");
  exit(1);
}

/* queue up to 5 connect requests */
listen(sd, 5);

while (1) {
  client_len = sizeof(client);
  /* Do things(read and write) on new_sd, sd continue to listen requests */
  if ((new_sd = accept(sd, (struct sockaddr *)&client, &client_len)) == -1) {
    fprintf(stderr, "Can't accept client\n");
    exit(1);
  }
}
```

## 範例

以連線到 google.com 中產生的多個封包做說明。

### 三次握手

### SEQuence number

### AWKnowledge number

### 四次揮手

!!! note "為什麼揮手要四次，握手僅三次就可以？"

    主動關閉（Active Close）的那方可以根據需求關閉連線，但是對被動關閉（Passive Close）的
    那方來說，傳送的資料可能還沒完成，這時就需要等應用層資料都送出去之後，才會再一次做關閉的動作。
    所以流程大致如下：

    ```
    active-FIN → passive-AWK → ... 等待資料送完 ... → passive-FIN → active-AWK
    ```

    這時你就會注意到一件事，身為主動關閉的那方，是需要付出代價的！他需要進入
    等待對方關閉的狀態（`FIN WAIT 1` 或 `FIN WAIT 2`）；相較而言，
    被動那方就只要確認關閉後，就可以瀟灑說再見了。

## 問題

??? question "為什麼會有遺失、重複寄送和失序的問題？"

    遺失：很可能實際有送到指定位置，但是因為傳輸過程訊號被干擾了，導致[檢驗和](https://notfalse.net/27/tcp-error-control)的檢查失敗。

    重複寄送：建立在遺失之上的問題，當目的地收到並回傳 `AWK` 時，發送方很可能沒收到這個訊號，就誤以為沒送成功，就再送一次。

    失序：原本是照 1,2,3,... 的順序送出去，收到卻很可能是 3,1,4,...，這可能是因爲壅塞或網路延遲造成的，甚至可能每個封包路由路徑不同（IP 的協定會決定這一系列的封包怎麼送）

??? question "當 TCP 連線被開滿了，會發生什麼事？"

    需要先定義被開滿了是什麼意思，是部分進入 `TIME_WAIT` 狀態嗎，還是所有都是 Active 的狀態？

??? question "如何關閉 TIME_WAIT 狀態的連線？"

    你可以賦予該連線一個選項：[`SO_REUSEADDR`](http://www.unixguide.net/network/socketfaq/4.5.shtml)：

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
