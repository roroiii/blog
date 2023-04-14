---
title: React 只會更新畫面中有變化的部分
date: '2021-08-17'
tags: [react]
---

React 只會更新畫面中有變化的部分
useStatus

```js
const [count, setCount] = useState(<資料預設值>);
```

count 是透過 `useState()` 產生的變數，這是我們希望監控的變數
setCount 則是 `useState()` 產生用來修改 count 這個資料的方法
`useState()` 這個方法的參數中可以帶入資料的預設值

下面這些例子都是合法的：

```js
const [price, setPrice] = useState(1000)
const [description, setDescription] = useState('This is description')
const [product, setProduct] = useState({
  name: 'iPhone 11',
  price: 24900,
  os: 'iOS',
})
```
