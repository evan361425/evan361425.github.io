# 網路怎麼傳

概略圖講述網路的傳輸流程。實際上怎傳了什麼和一些元件運作原理請看「[網路傳了什麼](network-details.md)」

## 概略圖

![網路在傳輸層之下做了什麼？](https://i.imgur.com/KkGJZ0b.png)

圖中上半部是在講網路傳輸過程，下半部是一些介紹。

左右兩邊都有 _Socket API_，即是 BSD Socket，他是一個被包裝的程式庫。當開發者要進行 HTTP 溝通時就會透過 _Socket API_ 來建立連線，並選定想要的傳輸層協定進行溝通。

以 HTTP 為例，大部分情況都是使用 [TCP](tcp.md)（連結中有附使用 API 的程式碼），之後 _Socket API_ 就會在程式庫內部把相關資料拆層一個個片段（segment）並添加一些 TCP 的資訊。包裝完之後，就會再包裝成封包（packet）。

![片段、封包、訊框的架構圖](https://www.rfwireless-world.com/images/Segment-vs-Packet-vs-Frame.jpg)

當包裝成一個個的封包之後，會丟給 _網卡_ 來處理成一個個的訊框並透過收發器和網路線（也可能是 Wi-Fi 等等，詳見[網路傳了什麼](network-details.md)）傳遞到網際網路。

### 網際網路

網際網路中藍色圈圈代表路由器，綠色長方體代表交換器，傳輸到路由器前可能會經過多台交換器，而路由器中其實也有交換器的功能（含有 MAC 值）。

路由器和路由器之間（中間可能夾雜交換器）的溝通非常非常複雜（根據 [Xiaobo Zhou](https://www.coursera.org/instructor/~26632591) 的說法，是 OSI 階層裡最複雜的層級），裡面包括最佳路徑搜尋、排隊的策略、緩衝的管理等等。不過我們這裡就單純假設路由器知道要把訊號送給誰。

傳一傳最後就會交到目的端，目的端再把相關資訊反譯到應用層級的資訊。

## 各層有哪些服務

圖的左下角有簡介一些我自己知道的服務和協定。

以傳輸層為例，在到你的應用程式之前會有負載平衡器、代理伺服器等等。他負責的協定有 TCP、UDP 和 ICMP 等等。這裡提一下 ICMP 對應到 _Socket API_ 其實是沒有包裝的，而是使用 Raw Socket 接口。ICMP 的用途是檢查目的端的網路層服務狀態，最有名的實作就是 [ping](https://zh.wikipedia.org/wiki/Ping)（送 ping 過去要 pong 回來）。

在資料連結層中可能還有 [ATM](https://www.gartner.com/en/information-technology/glossary/atm-asynchronous-transfer-mode)（Asynchronous Transfer Mode），他異於乙太網的無連接式通訊（connection-less），會在交換器間建立連線，也就是當連線被中斷時（沒有回應）會要求來源端重新建立其他路徑的連線，這樣可以確保連線的品質和限縮網路延遲的最大值，但是[會降低頻寬的使用率](https://www.coursera.org/learn/packet-switching-networks-algorithms)。
