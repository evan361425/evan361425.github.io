# 網路傳了什麼

乙太網（Ethernet）和其之上的網路協定（Internet Protocol, IP）傳了什麼？

!!! info "其他還有什麼？"

    - 建議先讀過「乙太網、網路協定怎麼傳？」這篇
    - 傳輸層中的 [TCP](tcp.md)

## 乙太網

![乙太網的訊框格式](https://imgur.com/jAyEtKR)

### 收發器相關

-   [_前文_](https://terms.naer.edu.tw/detail/17545904/)[^1]（Preamble or Syncword）：是用來告知目的地端：「現在有訊息要送給你了，準備接收囉」，避免讓網卡一直做事。
-   [_框起始定界符_](https://terms.naer.edu.tw/detail/17499940/)（Start Frame Delimiter, SFD）：是用來分界待會的訊號就是真正有價值的資訊。
-   [_訊框間隔_](https://terms.naer.edu.tw/detail/17562349/)(Inter Frame Gap, IPG)：

![上述資訊都是透過資料收發器（Physical layer transceiver circuitry, PHY）來做的。](https://res.cloudinary.com/rsc/image/upload/b_rgb:FFFFFF,c_pad,dpr_2.0,f_auto,h_300,q_auto,w_600/c_pad,h_300,w_600/F7092227-01)

??? example "前文和框起始定界符的範例"

    ```
    10101010 10101010 10101010 10101010 10101010 10101010 10101010 10101011
    ```

### 表頭資訊

-   目的位置（MAC destination）
-   來源位置（MAC source）
-   乙太種類（EtherType）或訊框長度：若該值小於 `1501` 代表訊框長度反之大於 `1535` 則是代表種類

??? info "EtherType 的更多訊息"

    `1500` 是 Ethernet 802.3 的最大傳輸單位（[MTU](https://en.wikipedia.org/wiki/Maximum_transmission_unit)），但是若使用其他協定則是改為填寫 `1535` 以上（不含）的值。

    因為 `1536` 以十六進位表達是 `0x600` 所以以此為起始，協定種類的選擇有[這些](https://en.wikipedia.org/wiki/EtherType#Values)。

    這樣其他協定的長度要怎麼計算？可以通過前面提的 _訊框間隔_ 或 _檢核和_ 來確認。但有些特殊協定仍需要指定長度。

### 檢核和

需要透過檢核和來查驗本訊框是否受到干擾而有錯誤訊息，這類檢核和在此的名稱叫做[框檢查順序](https://terms.naer.edu.tw/detail/17499850/)（Frame check sequence, FCS）。

乙太網使用的檢核和是 CRC，其透過多項式相除得到的商的一些特性滿足高錯誤檢查率，也就是四個位元組就能檢查多個位元組的資訊（除了收發器相關之外的訊息都含）。

[^1]: 翻譯都根據「雙語詞彙、學術名詞暨辭書資訊網」定義。

## 網路協定

Wiki 都講得很詳細，不贅述了，主要有分兩個版本：

-   [IPv4](https://zh.wikipedia.org/wiki/IPv4#报文结构)
-   [IPv6](https://zh.wikipedia.org/wiki/IPv6#IPv6封包)

這邊提一下 IPv6 有幾點要注意：

-   _通信類別_、_流標記_ 都是為了 _服務品質控制_ Quality of Service, QoS）。
-   _跳段數限制_ 用來限制路由次數。

!!! info "服務品質控制"

    當網路壅塞（congestion）的時候，需要先處理等級比較高的（通信類別）或者透過反壓（back-pressure）等機制（服務品質控制）來有效處理高流量。
