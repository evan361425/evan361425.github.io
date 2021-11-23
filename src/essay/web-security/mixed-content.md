# 什麼是 Mixed Content

-   同一個網站擁有多個網站的資源
    -   JS
    -   CSS
    -   圖片等等
-   影響網站行為
-   \<a href=“http://evil.com”> 不是！

---

## 哪些需要注意

-   除了影片、聲音、圖像都應該要擋
-   圖像也要注意 把垃圾桶的圖標和儲存起來的圖標交換
-   舊的瀏覽器可能防護不夠
    -   IE8 以下

---

## 防護

-   http:// => https://
-   從本地端送資料而不是從別的網站要
-   Header: Content Security Policy
    -   upgrade-insecure-requests
        -   cascades into \<iframe>
    -   blocking resources
-   掃描工具：
    -   [HTTPSChecker](https://httpschecker.net/how-it-works#httpsChecker)
    -   [Mixed Content Scan](https://github.com/bramus/mixed-content-scan)
