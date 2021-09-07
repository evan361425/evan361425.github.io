# OWASP API Top 10

## Broken Object Level Authorization

```
GET /api/v2/shops/{shop_name}/revenue_data.json HTTP/1.1
...
```

攻擊者只要更改 `shop_name` 就可以存取他人的資料。

---

## Broken Authentication

如果 API 在處理身份認證時，沒有適當保護，如：`CAPTCHA`、`速度限制`、`鎖 IP` 等。

攻擊者可以運用使用者帳號、密碼組合列表反覆嘗試來取得權限， 就可以得到正確的組合。

---

## Excessive Data Exposure

新進`保全`只能存取限制的`監控`。

```
GET /api/v2/camera/ids HTTP/1.1
...
```

回傳的卻是全部的`監控`，然後再在 APP 作過濾和限制。

---

## Lack of Resources & Rate Limiting

阻斷服務攻擊 (DoS)

```
GET /api/v2/users?page=1&size=100 HTTP/1.1
...
```

`size` 從 `100` 調整成 `2,000,000`。

---

## Broken Function Level Authorization

可以存取未經授權的功能

```
POST /api/admin/v2/invites HTTP/1.1

...

{"email"："hugo@malicious.com"}
```

注意和 [Object](#Broken-Object-Level-Authorization) 之間的差異

---

## Mass Assignment

比較下列兩段程式碼的差異。

```javascript=
const user = new User(req.body);
user.update();
```

```javascript=
const data = req.body;
const user = new User({ name: data.name, age: data.age });
user.update();
```

---

若使用者打入以下 API 尚無影響。

```
PUT /api/v2/user/data HTTP/1.1

...

{"name"："john","age"：24}
```

但改成以下資訊，則會給予錯誤權限。

```
PUT /api/v2/user/data HTTP/1.1

...

{"name"："john","age"：24,"money"：999999}
```

---

## Security Misconfiguration

如果資料庫管理系統使用的是預設配置

而其在默認情況下會解除身份認證...

---

## Injection

```
POST /api/v2/auth/login HTTP/1.1

...

{"account"："some-account' OR 1 --", "password": "dont-care"}
```

在資料庫中會如以下執行：

```sql=
SELECT * FROM user
WHERE account='some-account' OR 1 --' AND password='dont-care'
LIMIT 1
```

---

## Improper Assets Management

`v2` 把 [Lack of Resources & Rate Limiting](#Lack-of-Resources-amp-Rate-Limiting) 的問題修好了

```
GET /api/v2/users?page=1&size=100 HTTP/1.1
...
```

但是 `v1` 呢？有正確修正或重新導入（redirect）到 `v2` 嗎

測試環境的 DB 有沒有和正式環境互相影響？

---

## Insufficient Logging & Monitoring

好的 Log 和警告系統，會讓管理員有能力當下對攻擊做處理。
