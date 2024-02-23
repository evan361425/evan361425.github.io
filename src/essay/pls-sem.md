---
tags: misc
title: PLS-SEM：量化抽象指標
description: 如何透過數學歸納和多次回歸分析來量化抽象指標，並且擁有哪些好壞處。
image: TODO
---

There are two main approaches to estimating the relationships in a structural equation model (Hair et al., 2011; Hair, Black, et al., 2019). One is CB-SEM, and the other is PLS-SEM, the latter being the focus of this book. Each is appropriate for a different research context, and researchers need to understand the differences in order to apply the correct method (Marcoulides & Chin, 2013; Rigdon, Sarstedt, & Ringle, 2017). Finally, some researchers have argued for using regressions based on sum scores, instead of some type of indicator weighting as is done by PLS-SEM. The sum scores approach offers practically no value compared to the PLS-SEM weighted approach and in fact can produce erroneous results (Hair et al., 2017). For this reason, in the following sections, we only briefly discuss sum scores and instead focus on the PLS-SEM and CB-SEM methods.
有兩種主要方法來估計結構方程模型中的關係。一種是CB-SEM，另一種是PLS-SEM，本書將重點介紹後者。每種方法適用於不同的研究情境，研究人員需要了解差異以應用正確的方法。最後，一些研究人員主張使用基於總分的回歸，而不是像PLS-SEM那樣進行某種形式的指標加權。總分方法與PLS-SEM加權方法相比幾乎沒有價值，實際上可能產生錯誤的結果。因此，在接下來的章節中，我們只簡要討論總分，並專注於PLS-SEM和CB-SEM方法。

A crucial conceptual difference between PLS-SEM and CB-SEM relates to the way each method treats the latent variables included in the model.
PLS-SEM和CB-SEM之間的一個關鍵概念差異涉及每種方法處理模型中包含的潛在變數的方式。

CB-SEM represents a common factor-based SEM method that considers the constructs as common factors that explain the covariation between its associated indicators.
CB-SEM代表了一種基於共同因子的SEM方法，將構造物視為解釋其相關指標之間協變的共同因子。
This approach is consistent with the measurement philosophy underlying reflective measurement, in which the indicators and their covariations are regarded as manifestations of the underlying construct.
這種方法與支持反射性測量的測量理念一致，其中指標及其協變被視為潛在構造的表現形式。
In principle, CB-SEM can also accommodate formative measurement models, even though the method follows a common factor model estimation approach.
原則上，CB-SEM也可以容納形成性測量模型，即使該方法遵循共同因子模型估計方法。
To estimate this model type, however, researchers must follow rules that require specific constraints on the model to ensure model identification (Bollen & Davies, 2009; Diamantopoulos & Riefler, 2011), which means that the method can calculate estimates for all model parameters.
然而，要估計這種模型類型，研究人員必須遵循需要對模型施加特定限制以確保模型識別的規則，這意味著該方法可以計算所有模型參數的估計值。
As Hair, Sarstedt, Ringle, and Mena (2012, p. 420) note, “[t]hese constraints often contradict theoretical considerations, and the question arises whether model design should guide theory or vice versa.”
如Hair等人所指出的，“這些限制通常與理論考量相矛盾，因此問題是模型設計是否應該引導理論，還是反之亦然。”

PLS-SEM, on the other hand, assumes the concepts of interest can be measured as composites (Jöreskog & Wold, 1982), which is why PLS is considered a composite-based SEM method (Hwang et al., 2020).
另一方面，PLS-SEM假設感興趣的概念可以作為組合進行測量，這就是為什麼PLS被認為是一種基於組合的SEM方法。
Model estimation in PLS-SEM involves linearly combining the indicators of a measurement model to form composite variables.
在PLS-SEM中，模型估計涉及將測量模型的指標線性組合以形成組合變數。
The composite variables are assumed to be comprehensive representations of the constructs, and, therefore, valid proxies of the conceptual variables being examined (e.g., Hair & Sarstedt, 2019).
假設組合變數是對構造的全面代表，因此是所檢驗的概念變數的有效代理。
The composite-based approach is consistent with the measurement philosophy underlying formative measurement, but this does not imply that PLS-SEM is only capable of estimating formatively specified constructs.
基於組合的方法與支持形成性測量的測量理念一致，但這並不意味著 PLS-SEM 僅能夠估計形成性指定的構造。
The reason is that the estimation perspective (i.e., forming composites to represent conceptual variables) should not be confused with the measurement theory perspective (i.e., specifying measurement models as reflective or formative).
原因在於估計觀點（即形成組合以代表概念變數）不應與測量理論觀點（即指定測量模型為反映性或形成性）混淆。
The way a method like PLS-SEM estimates the model parameters needs to be clearly distinguished from any measurement theoretical considerations on how to operationalize constructs (Sarstedt et al., 2016).
像 PLS-SEM 這樣的方法如何估計模型參數的方式需要清楚地區分出來，與如何操作化構造的測量理論考量有所不同。
Researchers can include reflectively and formatively specified measurement models that PLS-SEM can straight-forwardly estimate.
研究人員可以包含 PLS-SEM 可以直接估計的反映性和形成性指定的測量模型。

In following a composite-based approach to SEM, PLS relaxes the strong assumption of CB-SEM that all of the covariation between the sets of indicators is explained by a common factor (Henseler et al., 2014; Rigdon, 2012; Rigdon et al., 2014).
在遵循基於組合的SEM方法時，PLS放寬了CB-SEM的強假設，即所有指標集之間的協變由一個共同因子解釋。
At the same time, using weighted composites of indicator variables facilitates accounting for measurement error, thus making PLS-SEM superior compared to multiple regression using sum scores, where each indicator is weighted equally.
同時，使用指標變數的加權組合有助於考慮測量誤差，因此使得PLS-SEM比使用總分的多元回歸更優越，其中每個指標都被等同加權。

It is important to note that the composites produced by PLS-SEM are not assumed to be identical to the theoretical concepts, which they represent.
值得注意的是，PLS-SEM 產生的組合並不被假定為與它們所代表的理論概念相同。
They are explicitly recognized as approximations (Rigdon, 2012).
它們被明確地認識為近似值。
As a consequence, some scholars view CB-SEM as a more direct and precise method to empirically measure theoretical concepts (e.g., Rönkkö, McIntosh, & Antonakis, 2015), while PLS-SEM provides approximations.
因此，一些學者認為CB-SEM是一種更直接和精確的方法來實證測量理論概念，而PLS-SEM則提供了近似值。
Other scholars contend, however, that such a view is quite shortsighted, since common factors derived in CB-SEM are also not necessarily equivalent to the theoretical concepts that are the focus of the research (Rigdon, 2012; Rigdon et al., 2017; Rossiter, 2011; Sarstedt et al., 2016).
然而，其他學者則認為這種觀點相當短視，因為在CB-SEM中衍生的共同因子也不一定等同於研究焦點的理論概念。
Rigdon, Becker, and Sarstedt (2019a) show that common factor models can be subject to considerable degrees of metrological uncertainty.
Rigdon、Becker和Sarstedt（2019a）表明，共同因子模型可能存在相當大的計量不確定性。
Metrological uncertainty refers to the dispersion of the measurement values that can be attributed to the object or concept being measured (JCGM/WG1, 2008).
計量不確定性是指可以歸因於被測量的對象或概念的測量值的分散程度。
Numerous sources contribute to metrological uncertainty such as definitional uncertainty or limitations related to the measurement scale design, which go well beyond the simple standard errors produced by CB-SEM analyses (Hair & Sarstedt, 2019).
許多來源都會導致計量不確定性，如定義性的不確定或與測量尺度設計相關的限制，這遠遠超出了CB-SEM分析所產生的簡單標準誤差。
As such, uncertainty is a validity threat to measurement and has adverse consequences for the replicability of study findings (Rigdon, Sarstedt, & Becker, 2020).
因此，不確定性是測量的有效性威脅，對研究結果的可重複性產生不良影響。
While uncertainty also applies to composite-based SEM, the way researchers treat models in CB-SEM analyses typically leads to a pronounced increase in uncertainty (Rigdon & Sarstedt, 2021).
雖然不確定性也適用於基於組合的SEM，但研究人員在CB-SEM分析中處理模型的方式通常會導致不確定性明顯增加。
More precisely, in an effort to improve model fit, researchers typically reduce the number of indicators per construct, which in turn increases uncertainty (Hair, Matthews, Matthews, & Sarstedt, 2017; Rigdon et al., 2019a).
更確切地說，為了改善模型適配度，研究人員通常會減少每個構造的指標數量，這反過來會增加不確定性。
These issues do not necessarily imply that composite models are superior, but they cast considerable doubt on the assumption of some researchers that CB-SEM constitutes the gold standard when measuring unobservable concepts.
這些問題不一定意味著組合模型更優越，但它們對於某些研究人員認為CB-SEM在衡量不可觀察概念時構成黃金標準的假設提出了相當大的質疑。
In fact, researchers in various fields of science show increasing appreciation that common factors may not always be the right approach to measure concepts (e.g., Rhemtulla, van Bork, & Borsboom, 2020; Rigdon, 2016).
事實上，各個科學領域的研究人員逐漸意識到，共同因子可能並不總是衡量概念的正確方法。
Similarly, Rigdon, Becker, and Sarstedt (2019b) show that using sum scores can significantly increase the degree of metrological uncertainty, which questions this measurement practice.
同樣地，Rigdon、Becker和Sarstedt（2019b）表明，使用總分可以顯著增加計量不確定度，這對這種測量方法提出了質疑。

Apart from differences in the philosophy of measurement, the differing treatment of latent variables and, more specifically, the availability of construct scores also have consequences for the methods’ areas of application.
除了在測量哲學上的差異之外，潛在變數的不同處理，更具體地說，構造分數的可用性也對方法的應用範圍產生了後果。
Specifically, while it is possible to estimate latent variable scores within a CB-SEM framework, these estimated scores are not unique.
具體而言，在CB-SEM框架內估計潛在變數分數是可能的，但這些估計分數並不是唯一的。
That is, an infinite number of different sets of latent variable scores that will fit the model equally well are possible.
也就是說，可能有無限多種不同的潛在變數分數集合，它們同樣適用於模型。
A crucial consequence of this factor (score) indeterminacy is that the correlations between a common factor and any variable outside the factor model are themselves indeterminate (Guttman, 1955).
這種因素（分數）的不確定性的一個關鍵結果是，在因子模型之外的任何變量與公共因子之間的相關性本身就是不確定的。
That is, they may be high or low, depending on which set of factor scores one chooses.
也就是說，它們可能高也可能低，這取決於選擇哪個因子分數集合。
As a result, this limitation makes CB-SEM grossly unsuitable for prediction (e.g., Dijkstra, 2014; Hair & Sarstedt, 2021).
因此，這種限制使得CB-SEM非常不適合於預測。
In contrast, a major advantage of PLS-SEM is that it always produces a single specific (i.e., determinate) score for each composite of each observation, once the indicator weights/loadings are established.
相反，PLS-SEM的一個主要優勢是，一旦建立了指標權重/加載，它總是為每個觀察的每個組合生成單一特定的（即確定的）分數。
These determinate scores are proxies of the theoretical concepts being measured, just as factors are proxies for the conceptual variables in CB-SEM (Rigdon et al., 2017; Sarstedt et al., 2016).
這些確定的分數是被測量的理論概念的代理，就像因子是CB-SEM中概念變量的代理一樣。

Using these proxies as input, PLS-SEM applies ordinary least squares regression with the objective of minimizing the error terms (i.e., the residual variance) of the endogenous constructs.
利用這些代理作為輸入，PLS-SEM應用最小二乘回歸的方法，目標是最小化內生構造的誤差項（即殘差方差）。
In short, PLS-SEM estimates coefficients (i.e., path model relationships) with the goal of maximizing the R2 values of the endogenous (target) constructs.
簡而言之，PLS-SEM通過估計係數（即路徑模型關係）的方法，旨在最大化內生（目標）構造的R2值。
This feature achieves the (in-sample) prediction objective of PLS-SEM (Hair & Sarstedt, 2021), which is therefore the preferred method when the research objective is theory development and explanation of variance (prediction of the constructs).
這個特性實現了PLS-SEM的（樣本內）預測目標，因此當研究目標是理論發展和解釋變異（構造的預測）時，PLS-SEM是首選方法。
For this reason, PLS-SEM is also regarded a variance-based SEM approach.
因此，PLS-SEM也被認為是一種基於變異的SEM方法。
Specifically, the logic of the PLS-SEM approach is that all of the indicators’ variance should be used to estimate the model relationships, with particular focus on prediction of the dependent variables (e.g., McDonald, 1996).
具體而言，PLS-SEM方法的邏輯是應該使用所有指標的變異來估計模型關係，特別注重對依賴變量（例如McDonald，1996）的預測。
In contrast, CB-SEM divides the total variance into three types – common, unique, and error variance – but utilizes only common variance (i.e., the variance shared with other indicators in the same measurement model) for the model estimation (Hair, Black, et al., 2019).
相比之下，CB-SEM將總變異劃分為三種類型——共同、唯一和誤差變異——但僅利用共同變異（即與同一測量模型中其他指標共享的變異）進行模型估計。
That is, CB-SEM only explains the covariation between measurement and structural model indicators (Jöreskog, 1973) and does not focus on predicting dependent variables (Hair, Matthews, et al., 2017).
也就是說，CB-SEM僅解釋測量和結構模型指標之間的協變，並不專注於預測依賴變量。

PLS-SEM is similar but not equivalent to PLS regression, another popular multi-variate data analysis technique (Abdi, 2010; Wold, Sjöström, & Eriksson, 2001).
PLS-SEM與另一種流行的多變量數據分析技術PLS回歸相似但並不相等。
PLS regression is a regression-based approach that explores the linear relationships between multiple independent variables and a single or multiple dependent variable(s).
PLS回歸是一種基於回歸的方法，它探索多個自變量與單個或多個因變量之間的線性關係。
PLS regression differs from regular regression, however, because, in developing the regression model, the method derives composite factors from the multiple independent variables by means of principal component analysis.
然而，PLS回歸與常規回歸有所不同，因為在開發回歸模型時，該方法通過主成分分析從多個自變量中推導出組合因子。
PLS-SEM, on the other hand, relies on prespecified networks of relationships between constructs as well as between constructs and their measures (see Mateos-Aparicio, 2011, for a more detailed comparison between PLS-SEM and PLS regression).
另一方面，PLS-SEM依賴於預先指定的構造之間以及構造與其測量之間的關係網絡。

下表比較了 PLS-SEM 和 CB-SEM 之間的主要差異：

| 特徵 | PLS-SEM | CB-SEM |
|-|-|-|
| 哲學 | 基於組合 | 基於共同因子 |
| 測量模型 | 構造分數被視為近似值 | 構造被視為共同因子|
| 模型估計 | 最小二乘回歸 | 最大概似估計 |
| 分析方法 | 變異量分析 | 共變量分析 |
| 理論發展 | 對變異的解釋和預測 | 對於潛在概念的精確測量 |
| 理論方向 | 應用於預測和理論發展 | 主要用於測量模型的驗證和精確測量 |
| 變異解釋 | 重視對內生構造的變異的解釋 | 較少關注解釋變異，更多關注模型的適配和結構方程式模型 |
| 模型複雜度 | 對於複雜模型提供較強的適用性 | 在複雜模型中可能會導致計算上的挑戰 |
