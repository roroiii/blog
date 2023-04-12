---
title: Debounce 與 Memoize
description: 介紹 Debounce 與 Memoize 在前端的用法。
permalink: posts/{{ title | slug }}/index.html
date: '2023-04-11'
tags: [javascript]
---

## Debounce

#### 概念

類似搭公車，人都上車了公車才發動～要是發現還有人要上車，公車就會再等一下直到大家都上車。

#### 應用

在搜尋時，等待使用者打完所有要搜尋的字之後，才去打 API 拿資料，減少效能耗損優化效率～

詳細介紹可參考：[Debounce – How to Delay a Function in JavaScript (JS ES6 Example)](https://www.freecodecamp.org/news/javascript-debounce-example/)

```js
寫法一
function debounce(fn, delay) {
  let timer = null
  return function (...args) {
    if (timer) {
      clearTimeout(timer)
    }
    timer = setTimeout(() => fn(...args), delay)
  }
}

寫法二
function debounce(fn, delay = 300) {
  let timer
  return (...args) => {
    clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}
```

---

## Memoize

#### 概念

把複雜的計算記起來，下次就不用再算一次～
類似 React 的 useMemo 跟 Memo 的功能

#### 應用

直接看下面程式碼～
利用一個 Object 儲存運算後的值，如果 Object 內沒有這個值就把它存起來～
有值的話就直接回傳計算後的結果

```js
function memoize(fn) {
  let cached = {}
  return function (n) {
    if (!cached[n]) {
      cached[n] = fn(n)
    }
    return cached[n]
  }
}
```

參考：[第十六週練習題](https://github.com/Lidemy/mentor-program-4th/issues/16)
