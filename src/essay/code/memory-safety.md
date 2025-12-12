---
title: 記憶體安全的解方討論
---

ACM 在 [Vol. 23 No.5](https://queue.acm.org/issuedetail.cfm?issue=3775067)
中分享了多篇關於編寫程式時的記憶體安全問題，這邊做了一些簡單心得和整理。

寫好 C++ 來避免記憶體安全問題是困難的。
甚至改進 C++ 來避免安全問題出現這件事[也是困難的](https://github.com/carbon-language/carbon-lang/blob/trunk/docs/project/difficulties_improving_cpp.md)，
所以才會有 Carbon、Cyclone 或 Rust 這類語言，從根本上避免 C 或 C++ 最臭名昭彰記憶體安全問題。
記憶體安全問題的種類有很多，
也有相關 [CWE](https://cwe.mitre.org/data/definitions/1399.html) 去列舉，
以下是最常見的一個種類 use-after-free
（Chromium 專案中該種類[佔有 36.1%](https://www.chromium.org/Home/chromium-security/memory-safety/)）
的範例：

```cpp
#include <string>
#include <string_view>

std::string_view GetName() {
    std::string first = "Hello";
    std::string last = "World";
    return first + last; 
}

int main() {
    std::string_view name = GetName();
    printf("%s", name.data()); 
}
```

`first + last`  的型別是暫時性物件，它的生命週期將在作用域（scope）後就會被銷毀，
而 `string_view` 為了效能僅包裝指標，並沒有實際擁有字串的值，
這就是典型使用不存在記憶體 use-after-free 的記憶體安全問題。
最後的 `printf` 因為該記憶體的實際值已經不在了，
就可能會印出亂數或直接崩潰等不確定行為（undefined behavior）。

透過這些漏洞其實可以延伸很多攻擊手法，包括竊取資料、脅持服務以進行勒索、納入殭屍網路等等。
不只是安全問題，這也包括可用性問題，一但因為出錯導致無法提供服務將會直接造成業務上、信任上或財務上的損失。
其中一個有趣[案例 CVE-2019-8641](https://googleprojectzero.blogspot.com/2020/01/remote-iphone-exploitation-part-1.html)，
就是透過 iMessager 傳送圖片時解析圖片工具時的記憶體安全漏洞（緩衝區溢出），進一步延伸到能夠控制整台手機，
受害者甚至不需要點開圖片就會被攻擊，完全突破 iPhone 的沙盒機制。

這篇將著重在兩個點，解決記憶體安全問題的困境與實務上的解方。

## 困境

確實，改用安全的語言看起來好處多多，但是別忘了，代價是什麼？

最直觀的做法就是用新語言重寫或重構。
好處很明顯，高效能、捨棄技術債、技術和工具的現代化，而且最重要的是記憶體安全。
但是重構是一件成本非常高昂的任務，而且常常因為現實狀況導致重構的結果四不像，
現實狀況就包括：
一旦重寫失敗，會危及業務正常運作的壓力、
短暫下線服務來進行維護或替換是不可接受的、
現有團隊不了解系統的運作機制、
將資源用於重寫壓縮既有功能的交付量，
這些都表明重構必須基於業務因素或商業決策，否則軟體或技術優勢將無法彌補商務帶來的損失。
那些一廂情願希望重寫的人其實正好展現出他們**缺乏對於維護和理解別人程式碼的能力**。

??? example "成功和失敗範例"
    - [Adobe 產品重構的故事](https://medium.com/adobetech/we-decided-to-rewrite-our-software-you-wont-believe-what-happened-next-dd03574f6654)
    - [Sonos 重構失敗](https://www.theverge.com/2025/1/13/24342282/sonos-app-redesign-controversy-full-story)導致 CEO 下台的案例

## 實務上的解方

美國等西方加共同訂定出[記憶體安全路線圖案例](https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps)，嘗試協助規劃將產品過度到記憶體安全語言中。
