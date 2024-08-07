---
tags: SRE-workbook
---

# 務實大型系統設計

務實大型系統設計的目的在於讓開發者設計系統架構時，有個依據建立穩健而又高擴充的系統。

本文先透過定義問題，收集需求並透過迭代的方式循序改善設計，最終得到一個可靠的系統設計解方。
目標是讓開發者能設計出一個在初期便擁有高穩健性且同時擁有未來調整的環境，
而這個過程，就是把抽象的需求，降成實際可被估量的實踐。
這些實踐包括：

- 容量（capacity）預估
- 功能獨立性（類似艙壁原則，bulkheads），避免單一功能的損壞影響全部的服務。
- 允許服務降能（degradation）

這些實踐讓 SRE 有能力在面對系統設計時，
思考他擴充性和可能的瓶頸，並專注在這些點上。
在接下來的練習中，每一次迭代的設計，都可以問問自己這四個問題：

- 這個設計可能嗎？
- 有沒有更好的方法？
- 這方法可以在有限的時間和金錢內達成嗎？
- 如果專案有了其他干擾或插件，這方法仍能成功嗎？
