---
description: 超文本傳輸協定的說明和注意事項。
image: https://i.imgur.com/LoH4gTS.png
---

# HTTP

HTTP（HyperText Transfer Protocol）超文本傳輸協定的說明和注意事項。

## OSI 中扮演的角色

傳輸層（Transport Layer）之上，通常包辦會議層、表現層、應用層，
在 HTTP/3 後，連傳輸層也一起包進去了，
詳見 [QUIC 官網](https://www.chromium.org/quic/)和[實際封包內容](https://quic.xargs.org/)。

在 [TCP](./tcp.md) 之上雖然可以確保連線的穩定，
但是我們需要更高層次的會話（Session）機制：*這次請求的人，就是一個月前登入的那個使用者*。
這種驗證邏輯，在任何傳輸層協定都無法辦到，因為這已經牽涉到「應用邏輯」了。

從上面也可以得知，HTTP 其實就是一種針對應用程式邏輯的協定，
所謂的超文本（Hypertext）就是不再像底層協定那樣，
透過位元（bit）去做一些參數設定，例如 [TCP 選項](./tcp.md/#tcp_2)，
而是透過純文字來控制參數，例如 HTTP 用 [HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) 去控制協定版本。

整個協定非常單純的分成三個區塊：協定資訊，參數設定，溝通內容。
並分別用 [CRLF](https://developer.mozilla.org/en-US/docs/Glossary/CRLF) 這個換行符號，
來代表要這三個區塊的位置。

### 協定資訊

這是請求（或回應）的第一行。

如果是請求方，內容就包括你用了什麼版本的 HTTP，
你針對應用程式的哪個地方（[HTTP Path](https://developer.mozilla.org/en-US/docs/Web/API/URL/pathname)），
做什麼樣的請求（[HTTP Method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)）。

如果是回應，則是會有版本和回應的狀態（[HTTP Status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)）。

### 參數設定

讓這個協定擁有非常多眉角的地方，位置在請求（或回應）的第二行到下一個空行：

```text
GET / HTTP/2
header1: value
header2: value

payload
```

上述範例就可以看到[標頭](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)（Header）總共有兩個，
這是因為第二行到下一個空行之間總共有兩行。

標頭的格式很單純，大小寫有差，行首到冒號之前為鍵（key），不可以有空格；
冒號後為值（value），需要忽略前面的空格。

由此而誕生極其複雜的應用設定環境。
身為使用者通常你不用太擔心這件事情，因為偉大的瀏覽器和相關規範，例如
[W3C](https://www.w3.org/standards/)、
[IANA](https://www.iana.org/assignments/message-headers/message-headers.xhtml#perm-headers)
和很受公信的 [MDN](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/The_web_and_web_standards) 等等，
都幫你管理好了，但是身為應用程式的開發者，你可能就要開始頭大了。

## 維運要注意的標頭

### Access-Control-Max-Age

[MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Max-Age)

它是用來處理 Preflight 請求的快取。

## 資安要注意的標頭

### X-Forwarded-For

IP

### Meta

set the cookie

### Content-Encoding

避免 [CRLF Injection](https://www.praetorian.com/blog/using-crlf-injection-to-bypass-akamai-web-app-firewall/)
