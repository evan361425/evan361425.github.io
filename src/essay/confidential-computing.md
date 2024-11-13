---
tags: security
title: 機密運算
description: 如何避免內存和計算被 root 權限的使用者竊取？
image: https://i.imgur.com/btENriw.png
---

自從我知道可以透過一些 Linux 工具，把執行中的記憶體整個複製出來分析後，
我就在想，**如果某個程序取得了 root 權限，是不是代表它可以對所有應用程式做所有事？**
即使應用程式有 TLS 做點對點的加密，但是在記憶體複製大法下仍然變成赤裸的羔羊，
直接把解密後的傳輸內容取出來，根本不用考慮 TLS 內的金鑰。

帶著這樣的想法搜尋了下，發現有個叫機密運算（Confidential Computing）的東西，
就是以硬體的方式，避免計算和記憶體被窺視，本篇將透過 Intel SGX 闡述其作法。

## 抽象概念

在 2015 Intel 推中 Software Guard Extensions (SGX) 之後，
這種保護機制開始被推廣，
最終促成 [Confidential Computing Consortium](https://confidentialcomputing.io/)（CCC）的成立，
共同推動開放標準及跨平台的 *可信執行環境*（Trusted Execution Environment, TEE）。

> Securing data in use and accelerating the adoption of confidential computing
> through open collaboration.
>
> Confidential Computing Consortium

### Encryption in use

## Intel SGX

### Enclave

### Sealing

### Attestation

## 其他機密運算的架構
