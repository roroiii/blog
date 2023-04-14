---
title: React 增進效能，避免重複渲染 Rerender
date: '2021-08-27'
tags: [react]
---

## 渲染機制 Reconciliation

首先先簡單了解 React 的渲染機制 Reconciliation
![](https://i.imgur.com/ApLV4M6.png)

## 認識 Rerender

component state 改變，再呼叫一次 function 的方式就叫 Rerender
component state 改變，V-DOM 找出 DOM diff 這也叫 Render

## 增進效能，避免重複渲染 Rerender

- Memo 與 useCallback 常搭配使用
  Memo 是 component 用的，會檢查 props 有沒有改變，避免重複渲染
  因為 React 的機制會從父元件全部重新渲染，但是子元件沒有改變的情況下，會造成效能上不必要的浪費，這時候 Memo 就派上用場了。

- useCallback 可以把一個 function 記起來，依據 dependency function 內的東西做變動，如果 denpendency function 內的東西沒有改變的話，就算重複 render 一次二次都不會改變。

- useMemo 是給資料用的，在計算量大的時候使用
