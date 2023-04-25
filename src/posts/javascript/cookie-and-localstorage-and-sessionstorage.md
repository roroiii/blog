---
title: cookie, localStorage, sessionStorage 之間的差別？ JWT Token 會存在哪裡？
date: '2023-04-24'
description: 前端經常被問的觀念題目，為了我的金魚腦，特別寫下來以後面試複習。
tags: [javascript, cookie, localStorage, sessionStorage]
---

## 前言

記錄一些前端面試經常被問到的觀念題目，因為每次一緊張就會忘記，為了我的金魚腦特別寫下來以後面試複習。
會忘記就是因為平常寫程式很少用到這些觀念，大部分都是實作比較多，但是這些觀念又很重要所以這裡就當作我的腦內海馬迴 ٩(˃̶͈̀௰˂̶͈́)و

## cookie, localStorage, sessionStorage 之間的差別？ JWT Token 會存在哪裡？

以下分別介紹它們的特性和使用情境

<img src="/images/posts/cookie-and-localstorage-and-sessionstorage01.png" alt="cookie and localStorage and sessionStorage position">
圖為在瀏覽器中工具列的位置

### cookie

- Cookie 是**瀏覽器**提供的機制，通常以文字的形式儲存在客戶端(client)。
- 可以透過 http 在瀏覽器和服務器(Server)之間傳遞，可以在不同網站之間共享。
- Cookie 可以設定到特定域名下，有過期時間，可以透過 JavaScript 設置或刪除。
- 可以用於跨頁面或跨網站維持對話狀態，通常拿來記住使用者的首頁選項、購物車商品、登入訊息與用作網站分析。
- 儲存容量約 4KB。

實作 cookie，使用 document.cookie 設置

```js
document.cookie = 'username=John Doe; expires=Thu, 18 Dec 2023 12:00:00 UTC; path=/'
```

> cookie 名稱為 username，在 2023 年 12 月 18 日 12:00:00 UTC 過期，指定只能在訪問路徑 "/" 時使用。

也可以從後端設置 cookie ，以下使用 Node.js 的 express

```js
app.get('/', function (req, res) {
  res.cookie('username', 'John Doe', { maxAge: 900000, httpOnly: true })
  res.send('Cookie has been set')
})
```

> 使用 `res.cookie()` 設置名稱為 username 的 cookie，並在 900000 毫秒後過期（15 分鐘）。
> 設定 `httpOnly` 禁止 JavaScript 直接存取 cookie，只能透過 http 協議訪問，增加安全性。

### localStorage

localStorage 是 **HTML5** 提供的 web 儲存方式，在瀏覽器中保存一個 key 與對應值（字串）。

- 只要沒被使用者清除或是清除瀏覽器 cashed（clear browsing data），瀏覽器關閉後這些數據都會一直存在（類似永久儲存）。
- 與 cookie 最大的不同是不需要每次在 http 中傳送請求（不用一直打 API 確認）。
- 儲存量約 5MB - 10MB，比 cookie 大一些。
- 需要注意使用者的資料安全性，避免跨站腳本攻擊（XSS）等安全問題。

<img src="/images/posts/cookie-and-localstorage-and-sessionstorage02.png" alt="cookie and localStorage and sessionStorage position">
圖為清除瀏覽器歷史紀錄（清除暫存）

一個簡單的範例：

```js
// 存儲數據
localStorage.setItem('username', 'John Doe')
localStorage.setItem('age', '30')

// 檢索數據
const username = localStorage.getItem('username')
const age = localStorage.getItem('age')

console.log(username) // John Doe
console.log(age) // 30

// 清除數據
localStorage.removeItem('username')
localStorage.clear()
```

存取的時候需要注意轉換資料格式，使用 `JSON.stringify()` 轉為字串，使用 `JSON.parse()` 轉為原始數據。

### sessionStorage

- 與 localStorage 很像，不同的地方是在當前 session 結束時會刪除資料，不是瀏覽器關閉時刪除（但通常關閉瀏覽器整個 session 也會不見，所以關閉瀏覽器 sessionStorage 也會消失喔）。

替換 localStorage 為 sessionStorage 即可，以下是簡單範例：

```js
// 存儲數據
sessionStorage.setItem('username', 'John Doe')
sessionStorage.setItem('age', '30')

// 檢索數據
const username = sessionStorage.getItem('username')
const age = sessionStorage.getItem('age')

console.log(username) // John Doe
console.log(age) // 30
```

## JWT Token

- JWT (JSON Web Token) 是一種網路傳輸安全聲明的開放標準，可以在不同系統中傳輸，通常是 base64 編碼後的 JSON 字符串，常用於身份驗證與授權。
- 通常由 Header、Payload 與 Signature 組成。
  - Header 包含 token 類型與加密演算法，通常是 JSON 格式，例如：`{"alg": "HS256", "typ": "JWT"}`
  - Payload 包含傳輸數據，通常是 JSON 格式，例如：`{"sub": "1234567890", "name": "John Doe", "iat": 1516239022}`
  - Signature 用於驗證 token 加密是否被篡改，使用 Header 中指定的加密演算法對 Header 和 Payload 進行加密（如 HMAC、RSA、HS256 等）。

JWT Token 一般來說都會經過 Algorithm 加密演算法（例如 HS256），但是並不代表他是安全的，隱私資料建議不要放在這裡儲存。
可以到 [JWT](https://jwt.io/) 的網站玩看看。

## 結語

cookie 通常用於在網路上共享數據，localStorage 與 sessionStorage 是在瀏覽器儲存資料。
如何運用這三種儲存資料的技術，可以與後端工程師討論需要怎麼實作，依具體情況而定，沒有一個標準答案。
