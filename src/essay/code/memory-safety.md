---
title: 記憶體安全的解方討論
---

ACM 在 [Vol. 23 No.5](https://queue.acm.org/issuedetail.cfm?issue=3775067)
中分享了多篇關於編寫程式時的記憶體安全問題，這邊做了一些簡單心得和整理。

寫好 C++ 來避免記憶體安全問題是困難的，因為它們的**預設行為**並不是記憶體安全。
甚至改進 C++ 來避免安全問題出現這件事[也是困難的](https://github.com/carbon-language/carbon-lang/blob/trunk/docs/project/difficulties_improving_cpp.md)，
所以才會有 Carbon、Cyclone 或 Rust 這類語言或工具，從根本上避免 C 或 C++ 最臭名昭彰記憶體安全問題。
記憶體安全問題的種類有很多，
也有相關 [CWE](https://cwe.mitre.org/data/definitions/1399.html) 去列舉，
但大致可區分為空間和時間的記憶體安全。空間代表存取不應存取的記憶體位置，例如緩衝區溢位；
時間代表錯誤順序去值型記憶體操作，例如初始化前就開始讀取。
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
這些錯誤操作看似可以透過靜態分析找出來，但在一些複雜場景中，即使用上複雜的測試手段，
仍可能會有漏網之魚，例如 [libwebp 漏洞](https://blog.isosceles.com/the-webp-0day/#:~:text=the%20vulnerable%20versions,directly%20into%20that%20allocation.)。

透過這些漏洞其實可以延伸很多攻擊手法，包括竊取資料、脅持服務以進行勒索、納入殭屍網路等等。
不只是安全問題，這也包括可用性問題，一但因為出錯導致無法提供服務將會直接造成業務上、信任上或財務上的損失。
其中一個有趣[案例 CVE-2019-8641](https://googleprojectzero.blogspot.com/2020/01/remote-iphone-exploitation-part-1.html)，
就是透過 iMessager 傳送圖片時解析圖片工具時的記憶體安全漏洞（緩衝區溢出），
進一步延伸到能夠控制整台手機，受害者甚至不需要點開圖片就會被攻擊，完全突破 iPhone 的沙盒機制。

這篇將著重在兩個點，解決記憶體安全問題的困境與實務上的解方。

## 重構的困境

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

??? example "成功和失敗的重構範例"
    - [Adobe 產品重構的故事](https://medium.com/adobetech/we-decided-to-rewrite-our-software-you-wont-believe-what-happened-next-dd03574f6654)
    - [Sonos 重構失敗](https://www.theverge.com/2025/1/13/24342282/sonos-app-redesign-controversy-full-story)導致 CEO 下台的案例

除了推進的阻力，也有拉力讓開發者持續在不安全語言中開發。
首先是變強的迷思。
工程師可能會單純的認為只要受過訓練且足夠謹慎聰明就可以避免記憶體安全問題，
然而歷史上生產力或品質的提高，以及錯誤和傷害的減少，都源自於新技術、流程新法規的導入，
例如[車禍傷亡的減少](https://crashstats.nhtsa.dot.gov/Api/Public/Publication/812465)並不是因為駕駛員的技術水平一致的提高了，而是強制繫安全帶的政策實施，
又或者透過[標準化檢查清單](https://pmc.ncbi.nlm.nih.gov/articles/PMC11536331/)[以及在急救車上常備急救用品](https://pmc.ncbi.nlm.nih.gov/articles/PMC10754397/)，減少了院內醫療事故。

再來對強制要求或預期外重構的抵抗。
[部分開發者](https://www.theregister.com/2025/03/02/c_creator_calls_for_action/)認為政府和其他機構提出的記憶體安全建議預示著 C 或 C++ 將被迫走向終結。
然而，事實是沒有任何機構禁止使用預設非記憶體安全的語言。
政府對於記憶體安全方面扮演的角色一直是推廣者而非獨裁者，
無論是 ONCD 的報告「[未來的軟體應該是記憶體安全的](https://bidenwhitehouse.archives.gov/oncd/briefing-room/2024/02/26/press-release-technical-report/)」，
亦或是美國等西方加共同訂定出「[記憶體安全路線圖案例](https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps)」。

而預期外重構的抵抗中知名例子包括
2023 年有人嘗試[用 Rust 對 Linux 的 `iget_locked` 優化](https://www.youtube.com/watch?v=WiPp9YEBV0Q)
和 2025 [針對 DMA 的接口改寫](https://lwn.net/Articles/1006805/)導致社群的動盪。

> The only reason Linux managed to survive so
> long is by not having internal boundaries, and adding another language
> complely breaks this. You might not like my answer, but I will do
> everything I can do to stop this. This is NOT because I hate Rust.
> While not my favourite language it's definitively one of the best new
> ones and I encourage people to use it for new projects where it fits.
> I do not want it anywhere near a huge C code base that I need to
> maintain.
>
> [Re: rust: add dma coherent allocator abstraction](https://lkml.org/lkml/2025/1/31/144)

這些案例最終在 Linus 的仲裁下才平息：

> It was literally just another user of it, in a completely separate
> subdirectory, that didn't change the code you maintain in _any_ way,
> shape, or form.
>
> ...
>
> But maintainers who are taking the "I don't want to deal with Rust"
> option also then basically will obviously not have to bother with the
> Rust bindings - but as a result they also won't have any say on what
> goes on on the Rust side.
>
> [Re: Rust kernel policy](https://lore.kernel.org/rust-for-linux/CAHk-=wgLbz1Bm8QhmJ4dJGSmTuV5w_R0Gwvg5kHrYr4Ko9dUHQ@mail.gmail.com/)

## 實務上的解方

任何策略的目標都是在最大限度地提高記憶體安全性，同時最大限度地降低實現成本。
具體選擇哪種方法取決於服務的現況，包括重要性、目前和欲導入的語言差異、執行團隊的狀況以及時間表。

---

TBD

Chromium 讓團隊進行[二選一的規則](https://chromium.googlesource.com/chromium/src/%2B/master/docs/security/rule-of-2.md)，即所有新程式碼要不用沙盒，要不使用記憶體安全語言編寫。
令團隊驚訝的是，這項新策略惠及了整個程式碼庫——甚至包括那些未被重寫的部分。由於新代碼自帶的安全機制提供了一定的保障，他們可以將安全保障工作集中在如今已保持不變的舊代碼上。透過這種方式，他們不僅降低了程式碼庫中記憶體安全漏洞的整體發生率，也降低了漏洞的整體出現率。

針對關鍵組件進行目標重寫

Mozilla 整合到 Firefox 中的第一個真正的 Rust 程式碼是 MP4 視訊檔案解析器。他們用 Rust 取代了原有的 C++ 解析器。 Firefox 需要解析來自不可信來源的 MP4 文件，如果解析處理出現問題，後果可能不堪設想。對於 Mozilla 來說，這是一個雖小但安全至關重要的漏洞，因此值得重寫。
另一個有用的目標定位工具是 Kelly Shortridge 的 [SUX 規則](https://kellyshortridge.com/blog/posts/the-sux-rule-for-safer-code/)：針對那些沒有沙箱、不安全且外生的程式碼進行重寫。這意味著你應該優先重寫那些處理不受信任（外生）輸入、在沒有沙箱環境下運行且使用記憶體不安全語言編寫的程式碼。

用安全介面封裝不安全程式碼
Rust 標準函式庫中許多常見的容器類型都是這樣寫的。它們底層包含用於以盡可能高效的方式管理緩衝區和指標的不安全程式碼，但提供給使用者的介面不會允許使用者存取任何可能違反記憶體安全保證的資源（緩衝區、指標、長度）。
例如 Rust 的 [Vec 類型](https://doc.rust-lang.org/nomicon/vec/vec.html)，
雖然底層會使用不安全但高效的操作，但對外暴露始終只包含安全的行為。

## final

記憶體安全的優勢在於能夠降低長期產品的安全相關成本。透過從源頭減少記憶體安全漏洞，他們將漏洞成本轉移到了軟體開發生命週期的早期階段
