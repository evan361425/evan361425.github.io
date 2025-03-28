---
description: 舊有系統對許多開發者來說是場惡夢，有什麼好方法處理它嗎？
image: https://i.imgur.com/ahOz6F6.png
---

# 處理舊有系統

舊有系統（Legacy system）對許多開發者來說，是場惡夢。
它通常有幾個特點：

- 這個系統從早期便存在；
- 和很多既有的系統有隱晦的聯繫；
- 是個在商務邏輯中不重要的系統；
- 長期穩定的運行，沒有發生過什麼會導致多系統崩潰的情況。

由於他的穩定，導致沒必要去改，由於他的盤根錯節，導致要去改很困難。
進而引起它變成舊有系統：使用舊的運行系統、舊的語言版本、舊的相依套件等等。

在處理舊有系統時，這裡列出五個工法：

- [擱置](#擱置)；
- [包裝](#包裝)；
- [擴充](#擴充)；
- [替換、撤除](#替換撤除)；
- [託管](#託管)。

和五個心法：

- [定義基準](#定義基準)；
- [建立計畫](#建立計畫)；
- [尋找領導](#尋找領導)；
- [確保溝通](#確保溝通)；
- [迭代更新](#迭代更新)。

## 工法

這些工法並不僅僅只是獨立的方法，更有甚者，它們可能是[一系列處理舊有系統的步驟](#工法的整合)：

### 擱置

一個最省力的方法，擱置。

你評估過改變帶來的成本和風險，於是發現維持現狀就是最好的辦法。
通常**討論過程中會伴隨著未來可能可行的方向**，只是當下欠缺某些條件或環境。

### 包裝

透過應用程式設計介面（Application Programming Interface, API）
你可以把舊有系統包裝起來。

透過新的語言、套件、服務包裝舊有系統，這種手法稱為
[Strangler Pattern – Martin Fowler](https://martinfowler.com/bliki/StranglerFigApplication.html) 或
[Encasement Strategy – Dr. Robert L. Read](https://18f.gsa.gov/2014/09/08/the-encasement-strategy-on-legacy-systems-and-the/)。
在這過程中，你既能確保服務不會有相容性問題，也能增加一點可以控制的面積。

### 擴充

既然要改變很難，那就僅僅擴充（augmentation）他的功能，盡可能**去優化而不是異動**商務邏輯。

這種手法通常會和[包裝](#包裝)併行使用。

### 替換、撤除

這種手法很直觀，替換（replacement）部分功能或者直接撤除（retirement）舊有系統。

先從簡單或急迫的功能慢慢改，做一些部分的替換。
或者直接從頭重寫，並把線上的輸入輸出都保留下來，然後驗證新的系統並不會有任何破壞。

### 託管

舊有系統之所以難以改動，有很大一部份的原因在於它和其他系統的隱晦關係。

當你調整完舊有系統或直接撤除，卻突然有一個團隊告訴你：「抱歉我的系統因為你的改動壞了。」
既然改動舊有系統是共識，並且已經開始執行了，在其他團隊因為時程或其他專案關係無法配合改動時
（即使你已經盡可能滿足並相容大部分情境了），
你可以把舊有系統的管理權（ownership）託管（custodian）給另一個需要它的團隊。

## 工法的整合

上面提到的這些方法其實也可以整合成一整套的改動步驟：

- 我們意識到舊有系統的改動要付出大量精力，於是 *擱置*，但同時也討論出一些未來可能的解法；
- 後來決議是時候開始改動了，於是先把舊有系統 *包裝* 起來；
- 並且配合一些新的規範或要求來 *擴增*，例如增加追蹤（tracing）；
- 逐漸 *替換* 部分功能，例如使用新版的套件來解決 [CVE](https://www.cvedetails.com/)，
  並使用線上資料確保正確性；
- 最後全部改寫，*撤除* 舊的實作；
- 當舊有系統對某個團隊仍是必要的，就把保管權 *託管* 於它。

## 心法

學了工法漏了心法，就好像得其形而不得其神。

### 定義基準

替舊有系統增加觀測性（observability），並且建立舊有系統的基準，例如 HTTP 5xx 狀態的回應比例。
每次改善時，確保這個基準沒有被突破。

### 建立計畫

建立未來可能的發展路徑，並持續追蹤進度是否達標。
準繩定出來，將會幫助你走得更遠更久。

定義出最終推出的時限，通常當你訂出一個日期，大家就會把他釘在日曆上。

### 尋找領導

當線上出現問題時，這個人會是對外的窗口，並且擁有整個專案的視角。
同時，他會確保工時的優先程度被滿足，專注在當下應該被解決的事情。

### 確保溝通

外部單位很可能會無法理解為什麼好好地要去改舊有系統，
確保和其他人的溝通，並且讓他人理解改動舊有系統的必要性。

最重要的是讓他們知道，當出現問題時，該去找誰，怎麼解決？

### 迭代更新

先針對小範圍的異動去修改、優化。
當整個上線流程是暢通且熟悉的，再來逐步一段一段的調整。

## 總結

舊有系統是需要跨單位之間的努力，在處理的過程很有可能是曠日費時的。
對他抱有耐心並尋求心理上的認同和支持。最後，祝你好運！
