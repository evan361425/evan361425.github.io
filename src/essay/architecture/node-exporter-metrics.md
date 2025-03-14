---
tags: maintenance
title: Node Export Metrics 導讀
description: Node Exporter 輸出很多系統的指標，我該怎麼看這些指標，以及後續動作可以是什麼？
---

本篇目標就是建立多個 Node Exporter Metrics 的 Grafana dashboards，
並在這些儀表板的說明欄位中，放上一些說明和建議 action。

使用版本：v1.9.0。

## NTP

使用 [`timex`](https://github.com/prometheus/node_exporter/blob/v1.9.0/collector/timex) 收集器。
內容來源於 kernel 提供的 [`adjtimex`](https://man7.org/linux/man-pages/man2/adjtimex.2.html)。

對於 NTP 的說明可以參考[這篇](../web/ntp.md)。

| Name | Description | 換句話說 | 越怎樣越好 |
| - | - | - | - |
| `offset_seconds` | Time offset in between local system and reference clock. | NTP server 回過來的時間和本地時間的差距 | 越小 |
| `frequency_adjustment_ratio` | Local clock frequency adjustment. | 當 `offset_seconds` 過高時，開始調整此值讓系統逐步校時，單位是秒，如果值為 1.0001，就代表每秒修正 0.1ms，也就是 100ppm | 越接近 1 |
| `maxerror_seconds` | Maximum error in seconds. | 校時機制算出可能的最大錯誤秒數 | 越小 |
| `estimated_error_seconds` | Estimated error in seconds. | 根據 RFC 5905，此值計算來源於公式中的 `max_error`，而這在 linux kernel 中被 [hard code](https://github.com/systemd/systemd/blob/main/src/timedate/timedated.c#L575) 為 16s，我的經驗是只會拿到 0 或 16s | 越小 |
| `status` | Value of the status array bits. | bitmask 的值，所以在面板中要用 log2 呈現，請參考下方「NTP status 列表」 | 無 |
| `loop_time_constant` | Phase-locked loop time constant. | 同步算法中的常數，通常是 3 秒 | 小可以頻繁調整，大可以抗噪 |
| `tick_seconds` | Seconds between clock ticks. | kernel 中時鐘的最小計時分辨率 | 是固定值 |
| `pps_frequency_hertz` | pps frequency. | | |
| `pps_jitter_seconds` | pps jitter. | | |
| `pps_shift_seconds` | pps interval duration. | | |
| `pps_stability_hertz` | pps stability, average of recent frequency changes. | | |
| `pps_jitter_total` | pps count of jitter limit exceeded events. | | |
| `pps_calibration_total` | pps count of calibration intervals. | | |
| `pps_error_total` | pps count of calibration errors. | | |
| `pps_stability_exceeded_total` | pps count of stability limit exceeded events. | | |
| `tai_offset_seconds` | International Atomic Time (TAI) offset. | 因為閏秒所造成與國際原子時相差的秒數，可以當稱歷來閏秒的總和 | 無所謂 |
| `sync_status` | Is clock synchronized to a reliable server (1 = yes, 0 = no). | 來源於 *time synchronization flag*，但並不是每個 daemon 都會設定此值，相關說明請參考[此篇](https://github.com/prometheus/node_exporter/blob/master/docs/TIME.md#timex-collector) | |

| Bit index | status name | description |
| - | - | - |
| 0 | STA_PLL | 啟用 PLL（相位鎖定環），用於調整系統時鐘的頻率。 |
| 1 | STA_PPSFREQ | 啟用 PPS 頻率調整，利用硬體的 PPS 信號校準時鐘頻率。 |
| 2 | STA_PPSTIME | 啟用 PPS 時間調整，利用硬體的 PPS 信號校準系統時鐘的秒級同步。 |
| 3 | STA_FLL | 啟用 FLL（頻率鎖定環），用於時鐘頻率調整，作為 PLL 的補充或替代。 |
| 4 | STA_INS | 插入閏秒，用於保持 UTC 的正確性。 |
| 5 | STA_DEL | 刪除閏秒，用於保持 UTC 的正確性。 |
| 6 | STA_UNSYNC | 系統時鐘未同步，表示當前無法獲得可靠的時間源。 |
| 7 | STA_FREQHOLD | 暫停頻率更新，可能是因為缺乏可靠的時間同步數據。 |
| 8 | STA_PPSSIGNAL | 正在接收有效的 PPS 信號，表明硬體提供了準確的時間同步信號。 |
| 9 | STA_PPSJITTER | PPS 信號的抖動過大，可能導致時間同步不穩定。 |
| 10 | STA_PPSWANDER | PPS 信號的移過大，超出了內核的接受範圍。 |
| 11 | STA_PPSERROR | PPS 信號發生錯誤，可能是硬體信號丟失或不穩定。 |
| 12 | STA_CLOCKERR | 系統時鐘發生錯誤，例如硬體問題或時間同步異常。 |
| 13 | STA_NANO | Chrony 特有，表示系統內核以 ns 為單位進行時間解析度，而非傳統的 ms。 |
| 16 | STA_RONLY | 只讀模式，系統時鐘被設置為只讀，無法被修改（通常被用於保護或測試模式）。 |

> NTP status 列表

我沒有用 PPS 來做校時，所以這段的指標就不多說什麼，
也因此 NTP status 對我來說真正有解析價值的位元是 4、5、6、12。

*[pps]: Pulse per second，一種精確硬體信號源。

### NTP 注意事項

誠如上面所說，指標來源於 `adjtimex`，
而 Chrony 的日誌通常代表最直接的誤差結果，
所以你很可能看到指標和日誌對不上，或者指標中沒有過大的誤差。
例如，當 Chrony 發現 system time 和 NTP server time 有差距時（也就是 offset 開始拉高），
就會根據 maxupdateskew 逐步修正時間（通常是  0.1 ms/s），並不會真的反應到
這時 kernel 就會不知道 offset 誤差很大，只有 system time 和 physic time 有誤差時才會被感知，
例如有人透過 syscall `CLOCK_SET` 強制調整系統時間或重新初始化 NTP 校時機制。
但是我們可以通過 `frequency_adjustment_ratio` 來得知目前時間是否有異常，
因為 Chrony 會因為和 NTP server 時間對不上，而去調整 kernel 的 `frequency_adjustment_ratio`。

相對而言，如果使用 Linux 原生的 NTP 機制，就會很好地反映在指標中。
