---
tags: security
title: 機密運算
description: 如何避免內存和計算被 root 權限的使用者竊取？
image: https://i.imgur.com/btENriw.png
---

自從我知道可以透過一些 Linux 工具，把執行中的記憶體整個複製出來分析後，
我就在想著，**如果我有 root 權限，是不是代表我可以對 application 做所有事？**
即使我有 TLS 做點對點的加密，但是把記憶體直接複製後，
就可以把解密後的傳輸內容直接複製出來，根本不用考慮解密。

帶著這樣的想法搜尋了下，發現有個叫機密運算（Confidential Computing）的東西，
就是以硬體的方式，避免計算和記憶體被窺視，本篇將透過 Intel SGX 闡述其作法。

## 抽象概念

## Intel SGX

### Enclave

### Sealing

### Attestation

## 其他機密運算的架構
