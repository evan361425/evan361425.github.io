# Tomcat 的 max_packet_size

[Tomcat](https://tomcat.apache.org/index.html) 中，若 HTTP 表頭過大，會回應 413。但是根據 [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/413) 413 代表 Payload Too Large，也就是 HTTP Body 過大，為什麼會有這差異？

為了避免 Header 過大，我們不是應該設置 [maxHttpHeaderSize](https://tomcat.apache.org/tomcat-7.0-doc/config/http.html) 嗎？為什麼會需要設置 [packetSize](https://tomcat.apache.org/tomcat-7.0-doc/config/ajp.html) 這和 Header 看起來沒什麼關係的設置呢？

Tomcat 是一個提供 [Web 容器](https://zh.wikipedia.org/wiki/Java_Servlet)的產品，儘管本身提供 web-server 的功能，但是大部分情況仍和第三方的 web-server 做串接。

## web server

- Apache HTTP Server
- Microsoft IIS
- iPlanet Web Server

不同的 Server 會需要使用不同的 [connector](https://tomcat.apache.org/connectors-doc/index.html) 來和 Tomcat 做溝通。

以上述順序來說，各自分別需要

- mod_jk
- ISAPI redirector
- NSAPI redirector

來把 HTTP 請求傳送給 Tomcat。

## worker

對應 web server 來說，實際處理相關 HTTP 請求的服務，稱為 worker（backend）。

雖然本文謹做 Tomcat 的介紹，實際仍有：

- Jetty
- JBoss
- ...

綜上述所說，我們可以整理出以下關係：

![Web Server 和各節點的關係](https://www.plantuml.com/plantuml/png/NOzDou9G48Ntyoi6zu8VktVnOhI9Lf622sbniy74wroREmOH_VVC8g7bEVFC0oVpQaJ7teBlMXwCc1vhrm-EYJNNcoKKgjLmOmcgJL7iS6rROZsWyHZ1byMWf2Fc95UI0E-0-A4TCzNgP7w8N_rg-ridy82gTDBHEwSGOIXjSzRm7sFymrcrfyj8NY5URWaaIqWdS793HdoQ5Zq1)

上關係圖看到 **Web Server** 和 Worker 的溝通是透過 AJP（_Apache JServ Protocol_）這協定所形成的。

> [HTTP Connector](https://tomcat.apache.org/tomcat-7.0-doc/config/http.html) 的設置說明。
> [AJP Connector](https://tomcat.apache.org/tomcat-7.0-doc/config/ajp.html) 的設置說明。

## AJP

回到一開始的問題，為什麼 HTTP Header 過大，Tomcat 要回 413？根據 [AJP](https://tomcat.apache.org/connectors-doc/ajp/ajpv13a.html) 中 **Request Packet Structure** 的說明，他會把 HTTP Header 和一些資訊整合進二進位的編碼資料中，並傳送給 Worker。

以上述狀況來考慮，對 Worker 來說，他收到的 HTTP Request 中的 Header 不單單只是 Header，而是在他們世界中的 packet。封包過大，就回 413，聽起來很合理...

最後就是為什麼要設置 `maxHttpHeaderSize` 和 `packetSize`？原來 `maxHttpHeaderSize` 是用來給 HTTP Connector 的設置，而 `packetSize` 是用來給 AJP Connector 的。
