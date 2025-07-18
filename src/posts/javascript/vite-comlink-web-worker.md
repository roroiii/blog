---
title: Web Worker 上身，我的前端變成神了(?
description: 用生活化方式理解 Web Worker、WebAssembly、Comlink 等效能相關技術，帶你從基礎到進階，一步步打造前端性能怪獸。
date: '2025-05-13'
tags: [javascript, worker]
---

前端效能的極致展現(?
有神快拜(X)敗(O)
PS.很難供養，請神回家要小心。

這篇文章帶你從 Web Worker 搬磚小弟，一路進階到 WebAssembly 黑道大哥，還有 Comlink 魔法棒，讓你瞬間擁有多執行緒威能。後面也會搭配 Vite 的 plugin 實作，以及一些踩雷警告和實戰技巧。來吧！進香團出發～

---

### 🧱 Web Worker 搬磚大哥

> **Web Worker（網頁工作執行緒）** 是一種可以幫 JavaScript 分擔重活的技術，它會在主執行緒（main thread）之外開一條背景執行緒來跑程式，讓畫面不會因為重運算而卡住。

用白話講：就是有個「搬磚工人」可以幫你處理沉重任務，像是：大量計算、資料處理、影像轉換等等。主角（UI）就可以繼續做他的表演，不會 lag。

✅ 適合做的事：

- 資料解析（例如 CSV、JSON 巨量資料）
- 圖像處理（ImageData）
- 長時間計算（例如密碼加解密）

❌ 不適合的事：

- DOM 操作（Worker 裡面碰不到畫面元素）
- 要即時互動的事件處理

---

### 🕶️ WebAssembly 黑道老大

> **WebAssembly（Wasm）** 是一種可以讓 C/C++ 或 Rust 寫的原生程式碼在網頁中跑的格式。效能幾乎可以媲美原生 App。

簡單說，就是你請一位黑道大哥（C++），幫你處理數學運算、音訊處理、或遊戲引擎等超硬核的事。他不多話，但動作快狠準。

跟 Web Worker 合作就像：搬磚大哥拿著黑道老大給的指令，搬磚時飛快效率 max！

---

### 🪄 Comlink 魔法棒簡單實作

> **Comlink** 是 Google 推出的一個小工具，可以讓你用「超簡單的方式」呼叫 Web Worker 裡的函式，像在用普通物件一樣。

通常我們跟 Worker 溝通，要用 `postMessage()` 傳訊息、然後 `onmessage` 接收回應，非常麻煩。Comlink 就是幫你「自動打電話＋翻譯＋記錄」的好工具。

原本的 worker 應該要這樣寫:

```js
// worker.js
self.onmessage = function (event) {
  const { a, b } = event.data
  const result = a + b
  self.postMessage(result)
}
```

```js
// main.js
const worker = new Worker(new URL('./worker.js', import.meta.url))

worker.postMessage({ a: 2, b: 3 })

worker.onmessage = function (event) {
  console.log(event.data) // 👉 5
}
```

要手動管理 `postMessage()` 和 `onmessage`。

但 Comlink 只要這樣寫:

```js
// worker.js
import * as Comlink from 'comlink'

const add = (a, b) => a + b

// 用 Comlink 暴露函式
Comlink.expose({ add })
```

```js
// main.js
import * as Comlink from 'comlink'

const worker = new Worker(new URL('./worker.js', import.meta.url), {
  type: 'module',
})

// 用 Comlink wrap 起來
const api = Comlink.wrap(worker)

// 呼叫就像平常函式一樣簡單
const result = await api.add(2, 3)
console.log(result) // 👉 5
```

Comlink 就像把 worker.js 包裝成一個「遠端物件」，你可以像平常呼叫函式一樣去用它，超級方便！

### vite-plugin-comlink 讓你直接晉升效能魔法大師

覺得上面的 Comlink 還不夠簡單嗎？ [vite-plugin-comlink](https://classic.yarnpkg.com/en/package/vite-plugin-comlink) 讓你就用 ES Module 直接寫 worker，什麼都不需要處理，只要 import 跟 export 就搞定！

使用方法非常簡單：

1. 安裝 plugin

```bash
npm install vite-plugin-comlink
```

2. 加到 vite.config.ts 裡，注意 `comlink()` 一定要放在第一個。

```ts
export default {
  plugins: [comlink(), react()],
  worker: {
    format: 'es',
    plugins: [comlink()],
  },
}
```

3. 然後就可以像上面那樣 new ComlinkWorker() 開始用了！

官方範例:
Usage

```js
// worker.js
export const add = (a: number, b: number) => a + b

// main.ts

// Create Worker
const instance = new ComlinkWorker(new URL('./worker.js', import.meta.url), {
  /* normal Worker options*/
})
const result = await instance.add(2, 3)

result === 5

// Create SharedWorker
const instance = new ComlinkSharedWorker(new URL('./worker.js', import.meta.url), {
  /* normal Worker options*/
})
const result = await instance.add(2, 3)

result === 5
```

範例寫得很簡單，但要注意 `new ComlinkWorker` 這個實例要放在 Vite React component 外面，也不可以放在 hook 內，不然會產生超~~~級多 requests 直到你網頁掛掉為止唷(>.^)/

> 💥 注意 ⚠️：ComlinkWorker 不可以寫在 React component 裡，也不能放在 hook 裡！
> 會產生大量 Worker 實例（超爆炸），導致 memory 滿到掛網！

### 進階傳遞 ArrayBuffer

如果你要在主執行緒與 Worker 間傳送大量資料（例如：影像、音訊、浮點數陣列），建議使用 ArrayBuffer。

更進階一點，可以使用 Transferable Object 技術，把資料記憶體「搬移」過去，而不是複製（效能差超多）。

```js
worker.postMessage(arrayBuffer, [arrayBuffer])
```

✅ 用 Transferable 會快非常多，因為不用複製記憶體！

### 🤝 好東西一起分享，SharedArrayBuffer 共享記憶體

> SharedArrayBuffer 讓你可以在多個執行緒（Worker）之間共享一塊記憶體區塊。

這就像大家共用一塊白板，可以同時讀寫，不用一直 message 傳來傳去。

但小心：需要啟用 Cross-Origin Isolation（跨來源隔離），否則會報錯。

設定方式（Vite dev server）：

```js
// vite.config.ts
server: {
  headers: {
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Embedder-Policy': 'require-corp'
  }
}

```

### 🛞 避免山道猴子追逐車禍：Atoms API

前面提到的共享記憶體會帶來 競爭條件（Race Condition） 問題。

你可能需要一些「原子操作 (Atomic Operations)」確保資料一致，例如用 Atomics.add, Atomics.wait, Atomics.notify 這些 API。

簡單說：大家輪流寫，不要打架。

### 🕹️ 實戰運作，加上 WebSocket 傳遞

當你要處理遊戲、聊天系統、直播彈幕等等即時功能時，WebSocket + Worker 是夢幻組合：

主線程負責畫面和互動

Worker 處理邏輯與計算

WebSocket 傳遞訊息給伺服器／接收他人訊息

可以搭配 SharedWorker 共用同一條連線

最後附上一張 Claude AI 產生的圖
<img src="/images/posts/sharedArrayBuffer_webSocket_webAssembly.png" alt="sharedArrayBuffer with webSocket and webAssembly">

以上就是今天的神明介紹～
前端也能很兇，讓我們拿起工具開始請神上身，打造你的效能怪物吧 🧙‍♂️⚡

如果喜歡這篇，可以幫我分享給更多信徒（前端同好）🙏
讓更多人把神請回家^^

---

與 小花(ChatGPT) 還有 Claude 共同編輯^^
