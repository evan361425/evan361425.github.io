---
description: 本篇介紹一些天文學上的基本知識，如何觀測黑洞、星體的噴發，什麼是星雲、紅巨星等等。
image: https://i.imgur.com/a1dPXXQ.jpg
---

# 天文學

目前觀測到的宇宙中有數千億顆星星，且我們猜想整個宇宙可能已有一百多億年的壽命。
單單在太陽系中，就有數百萬顆漂流巨石足以毀滅地球。
這些發現，都是天文學家、宇航員、物理學家等等眾多領域的人們一起搭建出來的。
問題是，我們怎麼知道這些東西的？

??? question "天文學有什麼用？"

    這是有一次在家看電視時，我媽問我的問題，我想這也是很多人心中都有的問題。
    其實科學突破和日常科技息息相關，例如：

    -   微波，最初透過微波觀測宇宙，進而讓我們對這個波段更了解，從而延伸到生活工具，最後再從生活應用延伸更多面向，例如 Wi-Fi。
    -   CCD，透過在天文學上的應用，最後普及到每個人手上都有的手機相機。

> 聲明：本篇是以心得形式撰寫，受惠於成功大學的[天文學實驗室](http://sprite.phys.ncku.edu.tw/astrolab/)和愛丁堡大學的課程 [AstroTech](https://www.coursera.org/learn/astronomy-technology/)。

## 演進

我們總是能從歷史中學到一些東西，因此在開始談一些新東西之前，先來簡單回顧一下整個天文學的六個重要演進：

-   *望遠鏡*（telescope），越大的感光範圍，能看到的東西就會越清晰，
    例如：我們眼睛有 5 mm 的寬度接收光線，並從中釐清物體的輪廓。
    目前正在（2017-）智利興建一個世上最大的望遠鏡，[歐洲極大望遠鏡](https://en.wikipedia.org/wiki/Extremely_Large_Telescope)，其將擁有 40 m 大的直徑來接收光線。
-   *光譜*（spectroscopy），從牛頓開始研究光的散射後，我們發現了日光是由不同顏色的光組成的。
    如今，我們會透過觀察天文物體的光譜，推測該物體的溫度、組成、移動速度。
    ![光譜和其對應於望遠鏡的使用](https://i.imgur.com/nzX6xT0.png)
-   *影像*，有了影像，我們可以客觀的紀錄這些物體，不再是透過觀察家的口述、書寫或手繪。
    除此之外，我們也可以利用一些影像技術，獲得以前不知道的訊息，
    例如曝光，CCD 可以長期置於星空下，並累積那些發光微弱的星體所散發出的光線。
-   *多波段天文學*，光線是電磁波的一種表現形式，
    透過觀察不同頻率的電磁波，我們獲得除了顏色外，以往不知道的一些訊息。
    事實上，每次我們發明不同波長（例如2008 年 NASA 發射的費米伽馬射線太空望遠鏡）的觀測手法，
    都會得到一些全新的發現（例如中子星噴流和[費米氣泡](https://technews.tw/2023/01/10/fermi-bubble-milky-way/)等等）。
    ![不同波段的電磁波呈現的太空一角樣貌](https://i.imgur.com/MMdvgOm.png)
-   *太空探測*，自從 1960 年代後，人類有能力在除了地球之外的地方進行觀測。
    在外太空觀測可以避免大氣層的干擾，例如 *X射線* 就無法穿透大氣層，必須用太空望遠鏡。
    ![不同波段的電磁波被大氣層干擾的程度](https://i.imgur.com/ZxEzJnu.png)
-   *電子計算*，透過前述幾項的成果，轉換成電腦的資料後，就可以進行任何複雜的計算。
    最後利用計算結果重新回來調整觀測方式和設定，反覆透過這些正向回饋，達成越來越精準的結果。

在觀測天文學上，我們也有很多困難需要面對：

-   *距離*，我們觀察到的物體光線強度會[隨著距離**平方**成反比](https://en.wikipedia.org/wiki/Inverse-square_law)。
    舉例來說，距離我們最近的恆星 [*比鄰星*](https://zh.m.wikipedia.org/zh-tw/%E6%AF%94%E9%82%BB%E6%98%9F)，它和我們的距離是 270k AU。
    換算下來，我們從那收到的光線會比太陽還弱上 $10^{11}$ 倍。
-   *大小*，物體在觀察者看到的大小跟實際大小會和距離成反比（注意不是平方），
    我們通常用角直徑來表示物體的距離和大小關係。
    一個 DVD 大小的物體，在 400 公尺遠的距離約為 1 弧分（arch minute），
    在 27 公里外則約為 1 弧秒。
    天文學裡很常使用這個單位，以韋伯望遠鏡為例，
    他的畫質清晰度可以拍攝 0.1 弧秒的物體。
-   *多變的波長*，不同溫度釋放的波長不同（機率分佈上的高峰），
    溫度越高波長越短、頻率越高（但不是線性的）。
    這就代表我們需要設計很多不同儀器，用來觀測不同波長的電磁波。
-   *數量*，天體數量太多了，如果我們要把它存進資料庫中，這代表我們需要為其設計一些特殊的資料庫。
    除此之外，在做任何統計和計算時，也會面臨計算能力的問題。
-   *時間*，天體變異的速度通常很慢，我們如何在短短數年間就暸解並驗證天體在各個階段的變異？
    例如：太陽燃燒殆盡需要數十億年。
    也有一些天文現象是快速的，例如超新星的能量釋放可能只要數月甚至數天、
    一個巨石在砸向地球前，可能只需要數小時的時間就可以發生劇烈的移動變化。

## 望遠鏡

在 [Milky Way 開放的地圖](https://djer.roe.ac.uk/vsa/vvv/mosaic/lb.html)中我們可以看到它如何透過多張照片，整合成一個大的圖片。
主畫面的圖像只是 *右上角大地圖* 中的其中一塊，
而這個大地圖又只是天空中的一小塊而已，如下圖所示。

![夜晚中抬頭望向天空時的一小塊區域](https://i.imgur.com/a1dPXXQ.jpg)

而這一張張清晰的影像可能是從地球也可能是從宇宙中拍攝出來的照片，為了得到好的照片，我們至少要有這些要求：

-   *亮度*，要能偵測並整合最微小的光源。
-   *銳利度*，每個星體要和其他星體區分開來。
-   *多個波段*，不只是可見光，也希望有其他波段的電磁波被收集。

### 亮度

為了收集更多光線，我們會把望遠鏡做得更大，其中又分成兩種望遠鏡反射和折射：

![反射和折射式的望遠鏡](https://i.imgur.com/vELAsmt.png)

一般來說，在大型的望遠鏡中我們都使用反射的方式。
因為如果用折射，為了讓成像結果變更大，
我們需要讓焦距更長（所以你在中世紀看到的望遠鏡中都會很長），
進而導致中間的透鏡變得很厚。

然而反射望遠鏡造價不菲，兩倍大的望遠鏡其成本會因為工程等等因素上升到約八倍左右（三次方成長）。

總而言之，要收集微弱的光體時，需要更大的（反射）望遠鏡。

### 銳利度

會降低銳利度的原因大致有三個：

-   [繞射](#_6)
-   [大氣干擾](#_7)
-   [望眼鏡的不完美](#_8)

#### 繞射

繞射是光線天生的特性，各個角度進來的光線會干擾最終的成像。

![單一光源的繞射成像](https://i.imgur.com/Yo4u9BI.png)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Single_Slit_Diffraction_First_Minimum.svg) under the CCA license.

根據物理特性，焦距越短的望遠鏡，這種效應對成像的影響會越嚴重。
以人的眼睛為例，繞射的干擾會讓人眼觀察天體的極限達到約 25 弧秒。

#### 大氣干擾

光線在進入地表前就會因為大氣的干擾而晃動：

![受到大氣干擾的成像](https://upload.wikimedia.org/wikipedia/commons/e/ed/Eps_aql_movie_not_2000.gif)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Eps_aql_movie_not_2000.gif) under the CCA license.

這效果在越靠近地表越嚴重，通常高山上的干擾程度約為 1 弧秒。有兩種方式解決：

-   在外太空建置望遠鏡，詳見[太空望遠鏡](#_10)。
-   追蹤這些晃動然後透過計算校正這個誤差。
    例如歐洲極大望遠鏡利用打出去的雷射來計算大氣晃動程度，詳見[電腦](#_28_)。

#### 望眼鏡的不完美

每個望遠鏡設計時，會為了各種因素去妥協銳利度。
例如人的眼睛就會受到[球面相差](https://zh.wikipedia.org/wiki/球面像差)的影響。

又例如哈伯望眼鏡發射到太空之初，他的鏡子和理論上有大約 1 毫米的差距，進而造成成像的誤差，
詳見太空任務編號 [STS-61](https://en.wikipedia.org/wiki/STS-61) 的行動。

![因 SMM1 任務而改善的哈伯望遠鏡成像](https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Improvement_in_Hubble_images_after_SMM1.jpg/512px-Improvement_in_Hubble_images_after_SMM1.jpg)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Improvement_in_Hubble_images_after_SMM1.jpg) under the CCA license.

最近（2022），[韋伯望遠鏡就受到軟體的障礙](https://technews.tw/2022/12/25/webb-telescope-nasa-safe-mode/)，無法正常運作。

### 波長

透過 *赫羅圖*（H-R diagram）我們可以透過亮度和顏色區分不同星體。
X 軸由左至右為藍至紅；Y 軸由下至上為暗至亮，
其中太陽位於中間偏左的位置（Luminosity = 1, Temperature = 5778K）。

![以觀測所得的依巴谷星表中 22,000 顆的恆星，和葛利澤近星星表的 1,000 顆所繪製的赫羅圖。此圖顯示恆星只出現在圖的某些區域。最顯著的是稱為主序帶，為從左上（熱且亮）到右下角（冷且暗）的對角線。在左下區域是已經發現的白矮星，主序帶上方是次巨星、巨星和超巨星。可以在主序帶上找到我們的太陽：光度為1（絕對星等 4.8），B-V的色指數為 0.66（溫度 5,780K，光譜類型 G2V）。](https://upload.wikimedia.org/wikipedia/commons/6/6b/HRDiagram.png)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:HRDiagram.png#/media/File:HRDiagram.png) under the CCA license.

但問題是我們怎麼取得該星體的顏色呢？
在成像前，我們在 CCD 前面裝上濾波器（類似透明色紙），
只讓特定顏色的光可以打進感測器，這樣就可以收集到特定顏色的成像（例如藍色）。

反覆這種過程，就能取得該星體不同顏色的光亮程度。
最後整合並比較這個星體的不同顏色（通常是藍、紅、黃）的比例，
來得知該星體的顏色、溫度等物理性質，詳見[光譜圖](#_33)。

### 太空望遠鏡

如果我們想要了解星體的更多細節，我們就只能上太空建立望遠鏡。
很多工作如果在地上做，會很簡單，可是一旦到了太空，就需要處理一些棘手問題：

-   發射 *太空梭* 的設施
-   望遠鏡所需的 *能量*
-   讓望遠鏡保持 *穩定*
-   體認到自己的 *位置*
-   特定位置避免 *輻射和溫度差*
-   能破壞設施的 *碎石*
-   確保 *資料傳輸* 的穩定

#### 太空梭

我們需要[很多設施](https://blogs.esa.int/luca-parmitano/)才能發射太空船：
控制中心、測試機構、軟硬體等等。
最重要的是，這些東西由於維運建設成本極高，都會需要政府支持，
換句話說，你會受到**嚴格的預算監督**。

#### 能量

在外太空你沒有電源線可以接，你需要自產能源。
通常是使用很大的太陽能板來捕捉太陽能，很大的太陽能板代表將面臨到不同的工程技術和知識。

![大片太陽能板需要可以摺疊，這樣才能裝在太空船並送出去；同時你還需要能夠自動展開和配合光源（太陽）轉向](https://i.imgur.com/ezZNu5H.png)

#### 穩定

若需要太空望遠鏡精準探測某個星體，勢必需要穩定地對準目標，有幾種方式：

-   氣體微控，就像電影演的那樣。
-   三個不同方向的輪圈，透過賦予三個輪圈不同的轉動速度來控制方向。
-   利用望遠鏡內的線圈，製造出磁力，並試著和地磁交錯（或平行）來產生磁力矩並控制方向。

#### 位置

為了對準某個目標，我們需要讓望遠鏡知道自己在哪裡，並找出該目標的方向：

-   地平線觀測器，觀看地球位置來得知自己的位置
-   太陽感測器，觀看太陽位置來得知自己的位置
-   陀螺儀
-   星體追蹤器，額外一個相機去確認和辨識目標的位置。
    這相對於其他方法會比較精準但比較貴。

#### 輻射和溫度差

地磁會把太陽磁暴匯集在[*范艾倫輻射帶*](https://zh.wikipedia.org/zh-tw/范艾伦辐射带)（Van Allen radiation belt）上，
所以需要讓太空船移動到該輻射帶之外的地方。

在外太空有無照射到太陽，會讓溫度差距很大。
為了維持望遠鏡的穩定，我們會需要遮陽板，
例如[韋伯望遠鏡用了一個網球場大小的遮陽板](https://webb.nasa.gov/content/observatory/sunshield.html)

![每一個器材都需要大量時間和金錢來研發和測試](https://i.imgur.com/gx3PK06.png)

這裡有一個要注意的小知識：[*拉格朗日點*](https://zh.wikipedia.org/zh-tw/拉格朗日点)。
很多太空設備都會躲在地球對應太陽的正後方，並利用地球來遮陽，
這個位置稱為拉格朗日點
（事實上有四個不同功能的點，例如在地球和太陽的中間的點，能讓設施處於兩種重力的平衡點）。

#### 碎石

太空中的物體幾乎沒有空氣阻力，所以可能會以每秒數十公里的速度朝望遠鏡撞擊。

![被一個小小碎石擊中就可能對望遠鏡造成極大的影響](https://upload.wikimedia.org/wikipedia/commons/1/12/Space_debris_impact_on_Space_Shuttle_window.jpg)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Space_debris_impact_on_Space_Shuttle_window.jpg#/media/File:Space_debris_impact_on_Space_Shuttle_window.jpg) under the CCA license.

這類新聞很多，例如：

-   [MS22 聯盟號飛船被微流星打出破洞](https://technews.tw/2023/01/13/russia-capsule-space-station-roscosmos-ms-22-soyuz/)

#### 資料傳輸

太空望遠鏡沒辦法使用 Wi-Fi，但可以透過電磁束打出二進位資料。
為了維持傳輸的穩定性，會讓望遠鏡待在離地球遠一點的地方，這樣繞地週期才會長，
換句話說，才能待在同一個地方久一點，讓資料傳輸穩定一點。

我們也可以把望遠鏡運行到 *地球靜止軌道*（Geostationary orbit），在那裡和地球自轉同步，
就可以待在相對於地表不會移動的位置達到穩定的資料傳輸。

#### 太空望遠鏡的優缺點

總而言之，為了解決上述問題，做一個太空望遠鏡會需要很多很多很多很多的錢。

這還不算上那些昂貴又耗時的維修任務。

![著名的哈伯望遠鏡維修任務——SMM1](https://upload.wikimedia.org/wikipedia/commons/0/0c/Upgrading_Hubble_during_SM1.jpg)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Upgrading_Hubble_during_SM1.jpg#/media/File:Upgrading_Hubble_during_SM1.jpg) under the CCA license.

雖然太空望遠鏡昂貴，卻可以避免以下的影響：

-   大氣層會阻擋特定射線。
    ![有了太空望遠鏡，我們可以觀察到很多之前沒發現的物體](https://i.imgur.com/1L2X5zN.png)
-   干擾（distort）光線，因為大氣層的密度不同，就像光從空氣進入水會折射一樣，所以光會在大氣層中抖動。
-   地表光源，例如月光、燈光。
    就算到了朔夜，仍然會因為在地球另一邊太陽透過大氣層折射的微弱光源。

??? info "地球各種輻射帶、特殊點的比例圖"
    ![右邊的圖是左邊的局部放大](https://i.imgur.com/8klCa1K.png)

    右邊的圖可以看到：

    1. 最靠近中心（地球）的圓圈稱為 *低軌道*，通常運行對地衛星。約為 1.05~1.1 個 $R_e$（地球半徑）
    2. *質子幅射帶*（proton radiation orbit），約為 1.5 個 $R_e$
    3. *電子輻射帶*（electron radiation orbit），約為 4 個 $R_e$
    4. *地球靜止軌道*（Geostationary orbit），約為 6.54 個 $R_e$
    5. *磁層*（magnetosphere），在這臨界點太空中帶電的粒子子受到地球磁力影響的程度會大於太空之外，
       約為 10 個 $R_e$

    接著看左邊的圖：

    7. *月球繞行* 約為 61 個 $R_e$
    8. *拉格朗日點* （L2）約為 236 個 $R_e$
    9. 太陽約為 23,000 個 $R_e$

## 星體

在上一段中，介紹了 *赫羅圖* 中星體的分佈，
你會注意到其有一個主要分佈帶從右下至左上，我們稱其為 *主序帶*（Major sequence）。
這代表大部分星星在越接近藍色（越熱）它的發光程度會越高，為什麼？

因為越亮的星星，它會燃燒越多的燃料（核融合中的氫原子），其能造成的溫度也就越高。
但是為什麼燃燒中的星星不會爆炸呢？

這是因為星體不只在承受燃燒所造成的向外壓力，同時也面對著重力的壓縮。
在這兩個力量的平衡下，星星的大小就能夠維持著，例如現在我們看到的太陽。

> 我們透過觀察[核融合的產品](../future-of-fusion-energy/index.md)：*微中子*，來驗證我們的猜想。

在 *主序帶* 之上，也有一群分布較為密集的區域，
我們稱其為巨星分支（Giant branch），就是常聽到的紅巨星的所在位置。

紅巨星的成因是星星的燃燒原料（核融合中的氫原子）用盡後，重力會打贏這場拉鋸戰，
並開始收縮星體內部。
當收縮到一定程度後，由於其極高溫高壓，帶動周圍的物質進行新一波的核融合反應
（若星體過於龐大，收縮速度快到不足以產生足夠的力對抗，就會形成[黑洞](#_20)）。
這個反應會加速星體的燃燒，最後開始突破重力的平衡向外擴張，
形成紅巨星，這也是五十億年後，我們的太陽可能會面臨的狀態。

![紅巨星的生成是由於星體在死亡前燃燒旺盛導致體積擴張。](https://i.imgur.com/CHS1IDo.gif)

紅巨星在爆炸前後，會因為極度的高溫和高壓，生成許多重的元素，包括碳、氧和金屬。
最後噴射出的氣體和物質，又會因為重力和電磁力吸引，最終重新生成一個新的星體。

![紅巨星的噴發](https://i.imgur.com/Je3mYRV.png)

> [哈伯望遠鏡](https://hubblesite.org/resource-gallery/images)拍的 [Crab Nebula](https://hubblesite.org/contents/media/images/2020/03/4601-Image)。

![紅巨星噴發後形成的星雲](https://i.imgur.com/hMmRQNE.png)

> [哈伯望遠鏡](https://hubblesite.org/resource-gallery/images)拍的 [Hourglass Nebula](https://hubblesite.org/contents/media/images/2019/15/4487-Image)。

![著名的創生之柱，也是來源於紅巨星噴發，凝聚成星球前的模樣](https://i.imgur.com/oVmi8jT.png)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Eagle_nebula_pillars.jpg#/media/File:Eagle_nebula_pillars.jpg) under the CCA license.

### 黑洞

有了星體的知識和太空望遠鏡的建造，我們終於可以說明如何計算黑洞的基本資料了。

當星體過於龐大，其因為重力而收縮的力大到沒有任何力能有效對抗其存在時，就會形成黑洞。
黑洞形成時，它的重力會大到影響任何靠近他的物體，
當星體經過黑洞並被吸引時（有個臨界點），該星體會開始被撕扯破壞（潮汐破壞事件，tidal disruption event，TDE）。
被撕扯出來的物質會開始繞著黑洞轉，越繞越快，溫度也跟著越來越高，
這時，其釋放的高能電磁波（例如 *X射線*）就可以被捕捉，進而觀察出黑洞的存在。

![以下天文學家畫出黑洞可能的樣貌，可以看到物體繞著黑洞旋轉](https://i.imgur.com/QU7PflM.png)

我們就來試著推算一下 [*天鵝座X-1*](https://en.wikipedia.org/wiki/Cygnus_X-1) 這個最先被認為是黑洞的星體的重量和大小吧！

![天鵝座X-1 的 X射線 圖](https://i.imgur.com/ZC2f2e8.png)

首先我們看一下它的質量。

我們可以透過繞行黑洞的[一個藍巨星](https://astronomy.com/news/2021/03/cygnus-x-1-the-black-hole-that-started-it-all)來簡單計算牛頓力學並取得黑洞的質量。

假設黑洞（質量 $M$）和藍巨星（質量 $m$）會因為重力而彼此吸引，其力會用來當作繞行的角速度（v）：

\begin{align*}
F &= \frac{GMm}{r^2} \\
 &= \frac{mv^2}{r}
\end{align*}

另外我們也知道角速度的計算公式為：

\begin{align*}
v = \frac{2\pi r}{t}
\end{align*}

整合上述兩個式子，就可以得到該黑洞的質量公式：

\begin{align*}
M = \frac{v^3t}{2\pi G}
\end{align*}

把常數帶進去算後，黑洞質量約為 16 倍的太陽質量。
接著我們來推算一下它的體積上限。

由於我們觀察到那些被黑洞撕扯出來的物質所發射出的 *X射線* 的強度每秒會變動約一百次
（一下變強一下變弱，每秒重複著這個規律一百次），
這就代表周圍的物體繞行時間約為百分之一秒。

假設周圍物體繞行速度約為光速（$3x10^8m$），可得繞行周長為：

\begin{align*}
r &= vt \\
 &= 3\times 10^{8} \times \frac{1}{100} \\
 &= 3\times 10^{6}m \\
 &= 3\times 10^{3}km
\end{align*}

換句話說，天鵝座X-1 在僅僅的 3000 公里內就裝著 16 顆太陽的質量。

> 當物體太大，且速度太快時，我們就需要狹義和廣義相對論來計算更精準的結果，但這邊忽略。
> 同樣的，雙星運行的計算也會比上述的還要複雜很多，這邊也忽略。

之所以有辦法得到這個結果，都是因為我們成功在外太空裝設了望遠鏡，並觀察 *X射線* 的變化。

## 感測器

感測器替我們做四件事：

-   客觀地紀錄物體。
-   把紀錄結果數位化。
-   整合結果，例如曝光。
-   可以感測除了可見光之外的電磁波。

??? example "整合結果的例子"

    以[哈伯超深空視場](https://en.wikipedia.org/wiki/Hubble_Ultra-Deep_Field#Hubble_eXtreme_Deep_Field)（Hubble eXtreme Deep Field, HXDF）為例，
    它之所以能感測宇宙中（對我們來說）最暗最遠的星系，就是[站在原地](#_13)曝光了 23 天。

    ![XDF 和月亮的比較，可以看到這張照片的目標是非常暗的星系](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/XDF-scale.jpg/1200px-XDF-scale.jpg)

    > [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:XDF-scale.jpg#/media/File:XDF-scale.jpg) under the CCA license.

!!! info "時光機器"
    由於光線傳遞速度的限制，我們看到那些最遠的星體，其實是該星體早年的樣子。

    例如目前（2022）可觀測最遠的星體是 [GN-z11](https://en.wikipedia.org/wiki/GN-z11)，
    它距離地球 134 億光年，
    換句話說，觀察它就可以觀察出大爆炸四億年後星體的樣子。

    我們利用這種特性來釐清宇宙初期的模樣。

### CCD

1980 年發明的 CCD 和傳統的感光儀器最主要的不同在於數位化。
除此之外，它亦有強大的感光能力。
例如，
傳統的[感光幹板](https://en.wikipedia.org/wiki/Photographic_plate)能處理約 1% 接收到的光線，
但 CCD 卻可以處理到 80%。

#### 他怎麼運作的？

光線的能量和其頻率（波長）有關，越高頻的光，能量越強。
當光線擁有足夠高的能量時，就可能讓原子裡的電子進行能量躍遷。
電子進行能量躍遷後，就有可能在其他靠近的原子進行遷移，如下圖所示。

![原子在固態中緊密排列並讓電子進行遷移](https://i.imgur.com/2bXA69D.png)

能讓特定物質的電子躍遷到可以傳導的程度時
（該臨界點稱為[導帶](https://en.wikipedia.org/wiki/Valence_and_conduction_bands)），
就可以依此來**判斷該光線的頻率**。
當持續照射電磁波，並累積足夠的電子時，
就可以把這些電子收集並計算數量，最終依此來**判斷光線的強弱**。

這種物質稱其為半導體，首選就是矽，因為它很便宜又很好印刷出電路。
也因為它的便利性，所以擁有很多方面的應用，也進一步讓更多人（非天文學上）進行不同的實驗與嘗試。
越多的關注就又進一步的提升該物質的良率和功能，也就重新回饋給天文學的進展。
這也回到最一開始的問題：*天文學有什麼用？*

#### 要怎麼收集電子？

CCD 是用 [MOS](https://en.wikipedia.org/wiki/MOSFET) （Metal–Oxide–Semiconductor）來收集電子。
利用外部電壓（Metal）讓半導體（Semiconductor）中的電子朝著特定方向前進，
最終會有個絕緣體（Oxide）擋住電子，並困住他。

![MOS 的架構圖](https://i.imgur.com/SVAgcIt.png)

CCD 中的每一個位元都是一組 MOS，而一個位元約為 $15\mu m$，
所以 6x6 $cm$ 的 CCD 就有 4000x4000 個位元（$6cm / 15\mu m = 4000$）。

#### 要怎麼計算電子？

CCD 有兩種主流方式來計算電子，一種稱為 CMOS 或 Active Pixel Sensors 的方法。
快速但會有雜訊，適合用在一般相機。

另一種則是適合用在望遠鏡上，稱為 Charge Coupling 的方法。
透過循序（以 6 $cm$ 的 CCD 來說，會有四千層）釋放電壓，
把電子慢慢累積並統計，這方法慢（6x6 $cm$ 的 CCD 需要約三十秒來判讀）但是精準。

### 紅外線感測

任何東西只要有溫度就會發射紅外線，例如冰塊、被微塵包裹的物體、宇宙邊緣紅移的物體。
然而紅外線因為太低頻，所以其攜帶的能量不足以讓矽進入[導帶](#_22)，
所以我們需要其他物質，例如，
[CMT](https://en.wikipedia.org/wiki/Mercury_cadmium_telluride)，來捕捉近紅外線。

每種不一樣頻率的電磁波，很可能就會需要用不一樣的材質來感測，
而這些材質不會像矽這麼通用，這麼便宜。
所以通常這種感測器都會又昂貴又精密且可能全球就只有數個團隊在做研究而已。

#### 要怎麼知道星體是暗還是遠？

![紅移效應會讓被觀察的星體呈現更低頻的電磁波](https://i.imgur.com/kCAOpVW.png)

> [Sky at Night Magazine](https://www.skyatnightmagazine.com/space-science/redshift/)

因為 *都卜勒效應* 和 *大爆炸理論*，我們可以知道越接近宇宙邊緣的星體，遠離我們的速度越快。
也因此，透過紅移的現象，我們可以知道這個星體和我們的距離。

![我們只能透過紅外線去感測那些最遠的星體](https://i.imgur.com/9PHoXXY.png)

> [Early star-forming galaxies and the re-ionization of the Universe](https://arxiv.org/pdf/1011.0727v1.pdf)

以上圖哈伯超深空視場中的其中一個星系為例，我們只能透過紅外線去感測那些遙遠的星系。
上圖觀測的星系是目前已知最遠最古老的星系之一，距離地球約 130 億光年，
透過觀測它，能夠幫助我們理解宇宙成形之初的樣子。

### 感測器的其他議題

感測器需要注意溫度，我們可以把感測器放在冷卻液，例如液態氦中。

這是因為物體只要有溫度就會發射電磁波（遠紅外線），
所以需要讓感測對象（目標星體）之外的環境盡量冷卻，否則會影響成像，即所謂的熱干擾。

除此之外，溫度代表電子本身就帶有一定的能量（動能加上內能），
而每次電子和物體的碰撞或晃動都可能讓它突破導帶，並影響成像。

除了 CCD，近期也有研究其他類型的感測器，例如 KIDS（Kinetic Inductance Detection System）。

還有從投影機技術延伸的數位光處理（Digital Micro Mirrors）技術。

## 電腦

隨著人們可以觀測的星體越來越多，
我們需要的是一個可以 *儲存* 大量紀錄的機制且可以進行繁雜且精密的 *計算*。
電腦在 1950 年代之後，逐漸在天文學中佔有非常重要的一塊，其優勢有：

-   可以直接儲存、運算數位化的感測結果。
-   可以控制望遠鏡，進行校準。
-   可以進行複雜且精密的計算。
    例如我們可以「製造」出數十億個假的星體，並模擬其碰撞、互動等等的機制，來驗證各種假說。
-   可以透過網路快速和他人互動。世界各地都有天文學家把自己的研究結果存下來，
    透過網路，我們可以快速把自己的結果（例如 *X射線* 的曝光結果）和別人的結果（例如紅外線的曝光結果）進行比對。

!!! info "望遠鏡的校準"

    我們在[大氣干擾](#_7)有提到天體的光線進入地球前會晃動。

    ![利用雷射取得目前大氣對光干擾的程度](https://i.imgur.com/adOHd50.png)

    > [CANARY's Laser Launch](https://www.ing.iac.es//PR/press/canary_photo.html)

    透過打出的雷射，計算當前大氣對光線的影響程度，
    再反推回星體的觀測，並進行望遠鏡的移動和成像的修正。

### 儲存和計算能力

我們來看看一般天文學常見的應用下，需要多少儲存和計算的能力。

#### 儲存能力

CCD 中每個位元（MOS）可以儲存 2 bytes（16 bits）的資訊，如果以一排有 [4000 個位元](#_23)來計算，
每張 CCD 出來的影像就會有 32 MB 的大小。

我們再以一個望遠鏡有多個 CCD 來考慮，所以一張天文照片約需要數 GB 來儲存。

這樣要照出一個完整的宇宙（$360^{\circ}$）需要多少張照片？
如果以一張照片大約會照到 $0.3^{\circ}$ 的太空為例，我們需要約 10 TB 的空間儲存一夜的太空。

隨著紀錄的天數增加（例如[計算出隕石](#_32)）儲存的空間將會越來越大。

#### 計算能力

有了電腦，我們就可以模擬宇宙成形之初，各種物體交互影響下的發展。

假設我們有一百萬個物體（$10^6$），就會需要 $(10^6)^2 = 10^{12}$ 次計算，
當數量達到數億個，將讓電腦計算時間拉長到失去意義。
而且這還只是一瞬間的互動，如果要紀錄一百步甚至數億步，這個時間將會拉得更長。

所以我們只能取大約的結果，也就是只計算較有影響力的互動。
通常會讓計算時間變成 $n\log n$ 這種等級的成長。

總的來說，[大量的儲存](http://www.sdss3.org/index.php)和[高速的運算](http://www.ncsa.illinois.edu/enabling/bluewaters)的需求，
讓天文學家通常會使用資料中心來滿足需求。

透過遠端去檢視、計算需要的資訊和結果，就可以避免資料被無意義的傳輸。
而相關的協定（如何使用、儲存等等）也已經在製作中，例如 [IVOA](https://www.ivoa.net)。

### 計算出隕石

![透過每天的觀測並記錄，我們可以找出那些正在移動的隕石](https://i.imgur.com/gVAEDX9.png)

> NASA [Approaching Asteroid](https://www.nasa.gov/mission_pages/asteroids/multimedia/asteroid2012da14i.html)

每天我們使用望遠鏡觀測太空，並把結果數位化存進電腦里。
在這些海量的資料裡，我們要怎麼找出那些正在朝著我們前進的星體，並預測其撞上地球的可能性呢？

我們每晚會紀錄各個星體的位置，並確認其移動週期和移動方向，例如它是繞著太陽轉還是朝著地球走。
而這些資料就是透過計算該星體的移動速度和距離遠近所得之。

\begin{align}
v &= d/t \nonumber \\
&= 2\pi r/t \label{vr}
\end{align}

萬有引力當作運轉的向心力的話，可以得到：

\begin{align*}
GMm /r^{2} =  mv^2/ r \\
\Rightarrow v^2 = GM /r
\end{align*}

最後就可以整合前面的公式得到繞行半徑：

\begin{align*}
v^2 = GM/r = (2\pi r/t)^2
\end{align*}

\begin{align*}
r^3 = \frac{GMt^2}{4\pi ^2}
\end{align*}

最後再得出繞行速度（$v$）。

## 光譜圖

透過光譜圖我們可以得到得到很多資訊，
除次之外本章也會討論怎麼獲得光譜圖和利用其推估宇宙的暗物質、暗能量的組成比例。

### 用途

可以利用光譜圖獲得：

-   溫度，該星體的溫度是多少？
-   組成，該星體透過哪些成分組成？
-   速度，移動的速度和方向。

#### 溫度

感測的電磁波頻率越高，溫度越高。
換句話說，呈現藍色的星體的的溫度會比紅色高，然後統計各個星體的溫度後就可以畫出 *赫羅圖*。

顏色的光譜圖獲得方法在前面的[波長](#_9)有提到（在 CCD 前面擺上色紙）。

#### 組成

因為不同物質會吸收不同頻率的光（做為電子的能階跳躍），
所以光譜遺漏的地方就是組成的物質（但也可能被大氣層的物質吸收，需要篩選一下）。

![暗的地方就是特定波長的電磁波被特定物質吸收](https://i.imgur.com/Pxw4UJk.png)

> [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Fraunhofer_lines.svg) under the CCA license.

反過來説，也有可能是透過特定物質釋放的電磁波，來組成光譜圖。
例如星雲，他的光譜就是透過原子釋放能階

![不同物質釋放的電磁波，特定頻率出現的機率高峰會不同](https://i.imgur.com/3x39yc3.png)

> [HIFI Cht3. HIFI Scientific Capabilities and Performance](http://herschel.esac.esa.int/Docs/HIFI/html/ch3.html)

#### 速度

![透過不同地方的頻率高低，可以知道其旋轉的速度和方向](https://i.imgur.com/w2qAZzp.png)

> [Nitrogen II emission line measured galaxy M87](http://pages.astronomy.ua.edu/keel/agn/m87core.html).

上圖我們可以看到，左邊是高頻（透過 *都卜勒效應*，可以知道這側正靠近我們）右邊是低頻（遠離）所以知道該星系正在以逆時針的方向旋轉，
然後再透過前述[測量黑洞質量的手法](#_20)，
結果發現整個星系的質量大於星系中星星總和的質量和，所以估計中間有個質量很大的黑洞。

### 觀測方法

早期牛頓使用三角稜鏡（prism）觀測光的可見光光譜，但在現代天文學中是使用繞射光柵（Diffraction grating）。

![每毫米數千個光柵，並把特定波長的電磁波匯聚在特定位置。](https://i.imgur.com/T75cmqp.png)

> [Diffraction Grating](http://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/grating.html)

透過多個光柵（grating）把特定波長的電磁波聚合在某處（想像一下 CD 盤上不同角度就會看到不同顏色），
我們就可以在特定位置中放置 CCD，並擷取想要的電磁波。

完整的 *攝譜儀* 就會是：

-   一個從 *反射鏡* 匯聚而成的光源。
-   *準直儀* 把光線變成平行的。
-   *光柵* 把光線打散，讓特定波長的電磁波聚焦於某處。
-   CCD 來儲存這些電磁波。

![位於 William Herschel Telescope 的大型攝譜儀](https://i.imgur.com/1SF48sZ.png)

#### 其他要解決的困難

望遠鏡是會移動的，每次移動要對準特定電磁波的聚合處是有工程困難的，
解法大致是透過光纖（optical fibres）讓光源的來源處維持一致。

需要讓望遠鏡的周圍足夠冷，避免紅外線的干擾。

收集到的光，因為被打散了，所以他的強度會更低，需要花更長的時間（數十倍）來曝光。

因為耗時長，所以會在一個時間，同時觀察多個物體的光譜。
要做到這樣，就需利用光纖把各個星體的光源都移至相同的陣列中，並同時觀察他們。

![多個光纖（optical fibres）把各個光源整合進同個光盤（focal plane）](https://i.imgur.com/haoSB06.png)

> [Andy Lawrence](https://www.coursera.org/instructor/andyxl) 組合多張 [AAT](https://www.mq.edu.au/faculty-of-science-and-engineering/departments-and-schools/australian-astronomical-optics-macquarie) 的照片而成。

### 暗能量

如同前面提到的紅巨星，重力會把星體向內壓縮，核融合的能量再把星體向外撐起，形成穩定的星體形狀。

整個宇宙事實上就是如此，只是向外的力量（暗能量，約佔 70%）大於向內壓縮（暗物質，約佔 25%），
所以我們才觀察到宇宙正在擴張的現象。

!!! warning "假說"

    上述的只是一種普遍的說法，當你可以提出一個理論，並滿足觀察到的現象，這時這個理論就可能被大家接受。

    但是，被接受不代表它就是事實，過了三十年，我們可能就會建構出一個完全不一樣的宇宙觀。

問題是，怎麼觀察出宇宙正在擴張的？

透過 *都卜勒效應*，我們只要知道物體發出的頻率漸漸提高，就可以知道它正在遠離，
問題是我們不可能觀察數十萬年來證明它的變化。
所以我們需要一種星體，不管是在哪邊生成，他的亮度都要一樣（standard candle），
*1a 類超新星* 就是這樣一種星體。

![1a 類超新星的爆炸是白矮星吸收恆星釋放的物質，並突破臨界點後引發的爆炸](https://i.imgur.com/lSv4oWt.png)

> [The Gobbling Dwarf that Exploded](https://www.eso.org/public/news/eso0731/)

因為白矮星吸收旁邊恆星釋放的物質後引發的 *1a 類超新星*爆炸，
其爆炸時的質量都差不多是 1.4 倍的太陽質量，所以他們釋放的能量和亮度也都差不多。

由此觀察不同的 *1a 類超新星*，就可以知道越暗（遠）的 *1a 類超新星* 其頻率越低，
代表宇宙的邊緣正更快速地遠離我們。

#### 比例的推估

![超新星的紅移程度（z）和距離的比例](https://i.imgur.com/vhA5sFO.png)

> [Improved cosmological constraints from a joint analysis of the SDSS-II and SNLS supernova samples](https://arxiv.org/pdf/1401.4064v2.pdf)

透過上述觀察到的事實（宇宙正在擴張），
論文中就指出宇宙組成的比例為 70% 的暗能量、25% 的暗物質和 5% 的已知物質。

## 總結

有了這些知識，
當你在欣賞[韋伯望遠鏡所拍攝的照片](https://www.bbc.com/zhongwen/trad/science-64101354)和理解其運作原理時，
是不是更有感呢！

其他有趣連結：

-   [探索木星溫度變化的週期性](https://technews.tw/2022/12/31/decades-of-data-shows-strange-temperature-swings-pulsing-through-jupiters-clouds/)
-   [費米氣泡的可能成因](https://technews.tw/2023/01/10/fermi-bubble-milky-way/)
-   [重力波](https://en.m.wikipedia.org/wiki/Gravitational-wave_observatory)
-   [黑洞的重複潮汐破壞事件](https://technews.tw/2023/01/17/tde-tidal-disruption-event-at2018fyk/)
-   [類地行星和相似衛星的行程原因推測](https://technews.tw/2023/01/15/rocky-planet-exoplanet/)
-   [特殊超新星 Pa 30](https://www.nature.com/articles/d41586-023-00202-1)
    （你可以在本篇看到很多[本文](#_19)提到關於超新星的內容）
-   [能形成千新星的雙星系統](https://technews.tw/2023/02/02/sgr-0755-2933-kilonova-be-type-star-cpd-29-2176/)
-   前面都是利用牛頓力學測得星體質量，[你也可以使用重力微透鏡](https://technews.tw/2023/02/04/hubble-telescope-white-dwarf-lawd-37/)得到精準質量。

*[弧秒]: Arch second；計算物體遠近和大小程度的單位，通常用於天文學。
*[CCD]: Charge-Coupled Device； 感光耦合元件，能感應光線，並將影像轉變成數字信號。
*[AU]: Astronomical Unit； 天文單位，為地球到太陽的距離。
*[赫羅圖]: H-R Diagram； 天文學中常見的圖，用來表示星體的顏色和亮度的分佈。
*[主序帶]: Major Sequence； 在赫羅圖中主序帶是星體常見的顏色—亮度比例範圍。
*[天鵝座X-1]: 人類最早期推測為黑洞的星體。
*[都卜勒效應]: 靠近我們的物體，其頻率會漸漸提高，遠離我的們的物體，則是會降低頻率（可以想像呼嘯而過的汽車）。
