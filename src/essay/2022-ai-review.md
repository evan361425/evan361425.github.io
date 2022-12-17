# 2022 AI 奇蹟年

今天（12/17）回顧 2022 年，發現真是有很多 AI 的突破，讓我備受感動！
以下就來盤點一下幾個我覺得很厲害的產品。

-   [ChatGPT](#ChatGPT)
-   [AI 繪圖 — Stable Diffusion](#stable-diffusion)
-   [AlphaFold2](#alphafold-2)
-   [核融合的溫度維持](#fusion)
-   [戰略遊戲 — CICERO](#cicero)
-   [古希臘歷史文本判讀 — Ithaca](#ithaca)

## ChatGPT

![ChatGPT 能夠理解語意，也能進行「創作」][chat-image]

> Sourced from [Yahoo!][chat-image-src]

今年最後一個月，OpenAI 推出了 [ChatGPT][chat-ui]，這次推出完全顛覆了我對 AI 的想像。
其帶給我的震撼，更甚當初 AlphaGo 下圍棋，而且正是因為它，我才有撰寫這篇文章的動力。

其目的主要是理解前後文的語意，給出適當的回應，而他做到了。

> 我們把各自手上所有的 NLP（自然語言處理）任務都測了一遍，包括自然語言理解、對話狀態追蹤、回覆生成、對話摘要、表格問答、文檔問答、信息抽取、情感分析、詩詞歌曲創造、翻譯...等幾十個任務，效果都非常的好。
> ...
> 不需要 in-context learning，開箱準確率達到 90%+，幾乎達到可以對外產品化販售。
>
> 來自[林廷恩](https://tnlin.github.io/)（自然語言研究者）的臉書

不僅如此，他還可以玩文字版的 RPG，例如讓他扮演密室中的某一個人，給予其選擇和線索，最終讓他成功逃出。
還有人用他整合下面的 AI 繪圖，在短短數小時內，推出了[純 AI 創作的兒童繪本][chat-book]。
當然，網友創意（跟時間）無限，期待未來能讓他有更厲害的應用！

## Stable Diffusion

![AI 繪圖能做的是遠超當初推出時的想像][draw-image]

> Sourced from [metaphysic][draw-image-src]

AI 繪圖無疑在今年大放異彩，不只是 [Stable Diffusion][draw-stablef]，還有 OpenAI 的 [DALL-E][draw-dalle]。

隨著發展，網路也出現越來越多奇耙應用，這裡就不列舉了。
但是其內在的演算法[擴散模式][draw-explain]（Diffusion Model）也不只是在繪圖有所應用。

像是下面提到的蛋白質預測，也[有人使用這個演算法][draw-protein]，達成輕量而又有準確度的模型。

## AlphaFold 2

這個其實不是 2022 年的產品，但隨著發展，今年也看到其實際的應用了。

蛋白質的組成並不複雜，由 21 種已知氨基酸構成，但真正困難的是其組合和建構方式的組合非常複雜。
然而 DeepMind AlphaFold 2 卻做到了[高於 90% 的預測準確度][alphafold-deepmind]（第二名不到 60%）。

![顏色越藍代表準確性越高，換句話說本圖中的蛋白質中心部分準確率較高，由此也看得出蛋白質的長相是非常複雜的][alphafold-i-base]

> 本圖來源於[科技新報發表的文章][alphafold-tecnews]

這裡要注意的是，AlphaFold 做的事情是 *預測*。
換句話說，如果我們要驗證這個預測，方式仍然是使用傳統的 [X 射線、核磁共振或冷凍電鏡等][alphafold-comment]。
但是這個過程是曠時廢日的，通常需要數年的時間。

在 2022 年，AlphaFold 預測出了可能是造成漸凍人的蛋白質 *核孔複合體* 的樣子，而這個問題，科學家已經嘗試了長達數十年。

![科學家和 AlphaFold2 合作建構出的蛋白質繪圖][alphafold-i-app]

> 本圖來源於[科技新報發表的文章][alphafold-cytoplasmic]

## Fusion

[核融合](../feedback/future-of-fusion-energy/index.md)需要極度高溫和高壓才有可觀的機率發生。
要成就這樣的環境不難，但問題是，要怎麼維持這個溫度？

會造成內部系統溫度降低是因為原子之間的碰撞把能量（動能）轉移到外部系統（外部溫度上升）。
為了將低這件事情的發生，我們需要讓原子照著圓圈迴轉（當然還有一些縱軸的力來降低磁力的交錯影響，[詳見](../feedback/future-of-fusion-energy/fusion.md)）。

DeepMind 發展了一種 [AI 演算法][fusion-wired]協助用鐳射維持這個「圓圈」的能量，換句話說，維持熱能。

在 2022/12，美國[國家點火設施發表][fusion-pts]已經達成輸出能量大於輸入能量。
雖說很多媒體宣稱核融合的時代來臨，但其實國家點火設施並不是核融合發電廠。
相較於核融合發電場，他不會處理氚的輻射（核融合是需要氘和氚和一些金屬才能有效達成）。
除此之外所謂的「淨能源」，並不包括鐳射...

## CICERO

Meta 開發的 [CICERO][cicero-github] 在一款鬥智鬥心機的遊戲 [Diplomacy][cicero-game] 中進入前 10% 的排名中。

> Source from [CICERO blog post][cicero-fb]

之前看到這個主題的時候有看到一段簡單的影片說明，現在找不到了！
但是... 我懷疑 ChatGPT 玩得會比他好。

## Ithaca

![歷史文本判度的範例][ithaca-image]

[DeepMind 在三月][ithaca-deepmind]開發了 [Ithaca][ithaca-github]，其用途在判讀古希臘文本的內容。

和人類歷史學家的 25% 預測率，Ithaca 達到了 62% 的準確率。
但是 Ithaca 並不是要取代人類，相反的，他是用來[協助人類][ithaca-tecnews]。
在人類和 Ithaca 一起判讀的情況下，他達到了高達 72% 的準確率。

## 結語

在最後介紹的 Ithaca，我們也可以看到雖然有些人會擔心機器學習取代我們的工作，
但其實機器學習的價值真正是用來協助人類，讓我們能更快速的完成工作。
就像今年英國開始推行的[一週工作四天](https://www.thenewslens.com/article/173604)一樣，
在大家都能在更短的時間中達到相同產能的情況下，對待機器學習更好的心態會是：我將如何（理解和）應用它？

[chat-ui]: http://chat.openai.com
[chat-image]: https://i.imgur.com/c00bejH.png
[chat-image-src]: https://tw.news.yahoo.com/chat-gpt機器人實測-講中文也懂-034423374.html
[chat-book]: https://www.techbang.com/posts/102430-chatgpt-dalle-2-books
[draw-image]: https://i.imgur.com/fck7kM6.png
[draw-image-src]: https://metaphysic.ai/stable-diffusion-is-video-coming-soon/
[draw-stablef]: https://openai.com/dall-e-2/
[draw-dalle]: https://openai.com/dall-e-2/
[draw-explain]: https://www.ycc.idv.tw/diffusion-model.html
[draw-protein]: https://www.techbang.com/posts/102461-aigc-biologists-proteins
[alphafold-tecnews]: https://technews.tw/2022/08/03/deepmind-alphafold/
[alphafold-deepmind]: https://deepmind.com/blog/article/putting-the-power-of-alphafold-into-the-worlds-hands
[alphafold-github]: https://github.com/deepmind/alphafold
[alphafold-cytoplasmic]: https://technews.tw/2022/08/03/deepmind-alphafold/
[alphafold-comment]: https://www.chemistryworld.com/opinion/why-alphafold-wont-revolutionise-drug-discovery/4016051.article
[alphafold-i-base]: https://i.imgur.com/hUh1Yxn.png
[alphafold-i-app]: https://i.imgur.com/gEsBawJ.png
[fusion-wired]: https://www.wired.com/story/deepmind-ai-nuclear-fusion/
[fusion-pts]: https://news.pts.org.tw/article/614363
[ithaca-github]: https://github.com/deepmind/ithaca
[ithaca-deepmind]: https://www.deepmind.com/blog/predicting-the-past-with-ithaca
[ithaca-tecnews]: https://technews.tw/2022/04/11/deepmind-interdisciplinary-ai/
[ithaca-image]: https://i.imgur.com/SPwrwUx.gif
[cicero-fb]: https://ai.facebook.com/research/cicero/
[cicero-ithome]: https://www.ithome.com.tw/news/154365
[cicero-game]: https://webdiplomacy.net
[cicero-github]: https://github.com/facebookresearch/diplomacy_cicero
