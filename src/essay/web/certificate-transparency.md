# Certificate Transparency

因為 CA (Certificate Authorities)簽出來的簽證（Certificate）可能不被信任（錯誤設定、被攻擊、公司倒閉等等），所以需要讓每個 CA 去把簽發出來的憑證記錄在一個公開的地方（或者稱其為日誌，log）讓大家審核。

這個公開的日誌稱作簽證透明化（Certificate Transparency，CT），其要能：

-   輕易確認這是正確的日誌。透過比對 STH (signed tree head)
-   輕易查找特定憑證是否存在。透過 Markle tree 的特性
-   若該日誌因任何原因出錯（程式碼有 bug、錯誤設定、任何邊際情況等等）要能輕易發現該錯。檢查 STH
-   不影響現有簽發簽證的延時，在簽證上添加擴充（X.509v3 extension）
    -   SCT (Signed Certificate Timestamp)用做確保已進單一（instantly）日誌中
    -   MMD (Maximum Merge Delay)標明在時限內該簽證可能不會在各個日誌中達成一致性
-   每個簽證需要兩個以上的 SCT，簽證效期越長需要越多，但不能太多否則會增加簽發時的延時和 TLS 交握的大小
-   MMD 為 24 小時。越低越安全，反之則能達到較強的容錯效果
-   只承認 CA 簽發的簽證避免紀錄日誌太多

當審核發現有問題時，就可以透過既有機制撤銷該憑證（OCSP[^1]、CRL、CRLSet 等等）。就不會再像之前那樣，發現問題時，已經是好幾天之後了。

## Referrer

-   [RFC😆](https://datatracker.ietf.org/doc/html/rfc6962)
-   [CT 作者針對該技術的說明，算是第一篇完整說明](https://queue.acm.org/detail.cfm?id=2668154)
-   [CT 官網圖畫式說明，從基礎開始了解](https://certificate.transparency.dev/howctworks/)
-   [Markle Town 是 CloudFlare 針對 CT 得到的簽證資料後做統計](https://ct.cloudflare.com)
-   [全世界最大的 CA — Let's Encrypt 說明如何實作 CT Logs](https://letsencrypt.org/2019/11/20/how-le-runs-ct-logs.html)
-   [Google 開發出用來在 SQL 之上建立 Markle Tree 結構的代理](https://github.com/google/trillian/)
-   [MDN 針對瀏覽器支援程度做的說明](https://developer.mozilla.org/en-US/docs/Web/Security/Certificate_Transparency#browser_requirements)
-   [開放大家透過 CT 搜尋簽證的 UI](https://ui.ctsearch.entrust.com/ui/ctsearchui)
-   [Google 工程師抱怨 OCSP 的無用，並說明替代方案](https://www.imperialviolet.org/2014/04/19/revchecking.html)

[^1]: 建議不要使用 OCSP，可以看 Referrer 中的連結。
