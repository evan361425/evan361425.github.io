---
title: 記憶體安全的解方討論
---

ACM 在 [Vol. 23 No.5](https://queue.acm.org/issuedetail.cfm?issue=3775067)
中分享了多篇關於編寫程式時的記憶體安全問題，這邊做了一些簡單心得和整理。

寫好 C++ 來避免記憶體安全問題是困難的，因為它們的**預設行為**並不是記憶體安全。
甚至改進 C++ 來避免安全問題出現這件事[也是困難的](https://github.com/carbon-language/carbon-lang/blob/trunk/docs/project/difficulties_improving_cpp.md)，
所以才會有 Carbon、Cyclone 或 Rust 這類語言或工具，從根本上避免 C 或 C++ 最臭名昭彰記憶體安全問題。
以 Android 專案來說，[逐步導入](https://security.googleblog.com/2024/09/eliminating-memory-safety-vulnerabilities-Android.html)的過程中，五年內錯誤率從 70% 降低到 24%，
且開發指標 [DORA](https://dora.dev/guides/dora-metrics-four-keys/) 並沒有因為採用這些新方法而下降，
甚至是[顯著提升](https://queue.acm.org/detail.cfm?id=3773096#:~:text=A%20key%20metric,accelerating%20software%20delivery.)了相關指標。

??? info "C++ Compile Hardening"
    目前最簡單強化安全的方式是透過 `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST` 編譯，
    其可以在幾乎沒有效能影響下（[0.3%](https://chandlerc.blog/posts/2024/11/story-time-bounds-checking/)），
    檢查越界存取並報錯，提升空間記憶體安全。
    根據[實際運行的專案](https://queue.acm.org/detail.cfm?id=3773097)中，其直接獲得的好處包括：

    - 漏洞檢測。在 100 多個項目中，共發現並修復了 1000 多個漏洞，其中包括潛伏超過十年的漏洞；
    - 可靠性。錯誤基準下降約 30%，最初檢查失敗導致崩潰的數量雖然有增加，但這是預期中的；
    - 安全性。加固措施明顯抵禦了正在進行的內部攻擊演習，並能阻止其他演習；
    - 除錯速度。許多難以發現的細微記憶體問題被轉化為錯誤即可立即被辨識並處理。

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
將資源用於重寫壓縮既有功能或業務目標的交付量，
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
具體選擇哪種方法取決於服務的現況，指標包括服務的重要性、目前和欲導入的語言差異、執行團隊的狀況以及時間表。

根據[研究](https://www.usenix.org/conference/usenixsecurity22/presentation/alexopoulos)，
一個專案的錯誤密度會隨著時間指數型下降，
（不只是該研究納入的專案，包括 Google 的大部分專案也是這個模式，或許這更像是一個軟體工程的基本特性）
但問題是一直有新專案，
所以才會得到不斷發現和修復同類漏洞的無止盡循環。

也就是說，最脆弱的程式碼並非那些古老、看似笨重的舊專案，而是當下正在編寫的程式碼。
這是個好消息！我們不需要急著把一些舊的專案改寫，我們可以先專注在使用記憶體安全的語言來建立新專案。
面對舊專案，有兩個主要方向，一個是有規劃地逐步全面汰換，另一個是共存。

如果是逐步汰換，流程大致如下：

1. 確保上層的支持；
2. 建立專責團隊，負責規劃和建立共用工具等工作；
3. 尋找最可行且可快速導入的產品進行嘗試，並與專責團隊密集的互動，其中過程包括：
   1. 整合：和既有專案的整合；
   2. 互通：和舊語言的協作；
   3. 工具：包括 IDE、CI 等工具；
   4. 套件：依賴套件的建立。
4. 逐步擴張，持續建立溝通管道和學習材料，當工作逐漸變成日常時，就可以往下階段走；
5. 全面可用，不再納管哪些專案有使用，這階段健康的狀況是用既有團隊就可以滿足所有需求；
6. 預設且建議使用新語言，並且幾乎沒有例外狀況。

如果沒有足夠資源可以進行全面汰換，就可能需要採用共存或小團隊內的導入。方式包括：

- 明訂規則，例如 Chromium 讓團隊進行[二選一的規則](https://chromium.googlesource.com/chromium/src/%2B/master/docs/security/rule-of-2.md)，即所有新程式碼要不用沙盒，要不使用記憶體安全語言編寫。
- 針對關鍵組件進行目標重寫，例如 Firefox 中的 MP4 視訊檔案解析器，
  這是一個雖小但影響範圍會很廣的功能，因此決定用 Rust 取代了原有的 C++
- 用安全介面封裝不安全程式碼，Rust 標準函式庫中許多常見的容器類型都是這樣，
  例如 [Vec 類型](https://doc.rust-lang.org/nomicon/vec/vec.html)，
  雖然底層會使用不安全但高效的操作，但對外暴露始終只包含安全的行為。

## 總結

記憶體安全的優勢在於能夠降低長期產品的安全相關成本。透過從源頭減少記憶體安全漏洞，他們將漏洞成本轉移到了軟體開發生命週期的早期階段
