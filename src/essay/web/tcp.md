# TCP

Transmission Control Protocol 傳輸控制協定的作用說明。

## OSI 中扮演的角色

Network 之上，Application 之下。

Network 中的 IP 是一種不考慮連線的協定，他只需要把封包路由給指定的目的地，在此之上 TCP 透過反覆確認段（segment）來確保兩端的連線是否仍存在。

## 流程

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

```c++
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

## Connect

以連線到 google.com 中產生的多個封包做說明。

### 三次握手

### SEQuence number

### AWKnowledge number

### 四次揮手

!!! note "為什麼揮手要四次，握手僅三次就可以？"

    待撰寫

## 問題

他會有遺失、重複寄送和失序的問題，為什麼？

遺失：很可能實際有送到指定位置，但是因為傳輸過程訊號被干擾了，導致[檢驗和](https://notfalse.net/27/tcp-error-control)的檢查失敗。

重複寄送：建立在遺失之上的問題，當目的地收到並回傳 `AWK` 時，發送方很可能沒收到這個訊號，就誤以為沒送成功，就再送一次。

失序：原本是照 1,2,3,... 的順序送出去，收到卻很可能是 3,1,4,...，這可能是因爲壅塞或網路延遲造成的，甚至可能每個封包路由路徑不同（IP 的協定會決定這一系列的封包怎麼送）
