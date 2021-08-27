As an application developer, if you’re armed with this knowledge about the internals of storage engines, you are in a much better position to know which tool is best suited for your particular application. If you need to adjust a database’s tuning parameters, this understanding allows you to imagine what effect a higher or a lower value may have.
Although this chapter couldn’t make you an expert in tuning any one particular storage engine, it has hopefully equipped you with enough vocabulary and ideas that you can make sense of the documentation for the database of your choice.

一個應用程式需要滿足許多需求才能提供特定服務。

- 功能性需求，例如：允許存取資料、搜尋等等。
- 非功能性需求，例如：
  - 安全性（security）
  - 可靠性（reliability）
  - 順從性（compliance）
  - 可延展性（compatibility）
  - 相容性（scalability）
  - 可維護性（maintainability）

## 可靠性

當服務發生狀況時，仍然能正確運行。狀況可能為

- 硬體，通常是無相關性且隨機的
- 軟體，通常是性統性的且難以解決
- 人為

容錯能力（Fault-tolerance）代表他能接受特定狀況的發生，並讓使用者不會受此影響。

## 可延展性

可延展性代表即使流量增加，表現仍是正常的。在討論延展性前，需定義流量（load）和表現能力（performance quantitatively）。以 Twitter 的個人首頁為例，利用回應時間的百分位數（percentiles）代表表現能力。即使流量增加，回應時間的百分位數仍低於特定水平。

在一個可擴充的系統，我們可以增加機器的量（processing capacity）來維持可靠的表現能力。

## 可維護性

可維護性有很多面向，基本上來說，就是為了讓工程師和運維工程師準時。讓系統保持抽象化（把維度提高）可以降低系統的複雜性，並且讓其更容易修改和適應新的功能。

好的操作性（operability）代表能觀察到系統內部運作狀態和健康檢查，並且擁有高效的方式去管理。

## 結論

通常來說不會有一個辦法可以簡單且完整的讓應用程式可靠、好延展和維護。然而，都會有某種模式或工具幫助我們一個一個解決這些問題。

以下這張圖代表一般應用程式的框架：

![](https://i.imgur.com/4uYcSaB.png)
