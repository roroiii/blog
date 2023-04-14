---
title: JavaScript 進階觀念
description: 前端經常考的JavaScript 進階觀念
permalink: posts/{{ title | slug }}/index.html
date: '2021-08-09'
tags: [javascript]
---

## 這週學了一大堆以前搞不懂的東西，你有變得更懂了嗎？請寫下你的心得。

這週學了很多以前沒有細想的地方，零散地做了筆記，雖然沒有很完整，但這大概是目前的理解程度，就把它拿來當作心得了。
本來 setTimeout 的原理不是很明白，又重看一遍 [What the heck is the event loop anyway?](https://youtu.be/8aGhZQkoFbQ) 突然就明白了，懷疑自己第一遍看的時候都在注意講師很帥ＸＤ

---

## 嚴格執行環境 use strict

讓 JavaScript 在嚴格模式下執行，大部分開發都會用。

```jsx
'use strict'
```

## 七種資料型態

最新的 ECMAScript 標準定義了七種資料型別：

1. Boolean
2. Null
3. Undefined
4. Number
5. BigInt
6. String
7. Symbol （於 ECMAScript 6 新定義）
   另外還有 Object

以上是看 MDN 的 [JavaScript 的資料型別與資料結構](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Data_structures) 的定義。

## 檢查型態

- `typeof` 看資料型態，但不一定只有上面這樣，也可以檢查有沒有這個值

- `null` 是 object ，這是 JavaScript 的著名 bug ，但已經錯很久修改會造成很多錯誤，所以未來可能也不會修。
- 檢測 array 的方法可以用 `Array.isArray([])`
- `Object.prototype.toString.call()`
  是另一種檢查型態的方法，看結果的第二個值就是傳進去的值的型態

```js
console.log(Object.prototype.toString.call(1))

// 結果 [Object Number]
```

> Value 不能被改變，看起來改變其實是回傳一個新的值
> Array 不一定需要改變，但 Array 可以被改變

## 賦值

- 存記憶體位置跟存值
  ![](https://static.coderbridge.com/img/roroiii/127c503e0f9e4a5a8c2be854f711651a.png)
  ↑ 最後 obj 是 10 obj2 是 30

## var、let、const 作用域

- ES5 以前 var 都是以 function 為作用域
- ES6 新增 let 、 const 是以 { } 為作用域

## hoisting（提升）

- 只有宣告的變數會提升，賦值的值不會提升。
- 單純的 function 宣告也會提升
- 如果是把 function 存在變數裡，只有變數會提升， function 是值所以不會提升。

```js
console.log(bbb) // bbb is not defined

console.log(test) // 提升為 var test 結果是 undefined
var test = 123

console.log(a) // 提升為 var a 結果是 undefined
var a = function () {
  console.log(123)
}
```

## hoisting 順序

1. function
2. arguments
3. var
4. let、const 在賦值之前無法存取，不會變成 `undefined` 而是 `is not defined` 或 `ReferenceError: Cannot access 'a' before initialization`，有個名詞叫做 TDZ（Temporal Dead Zone）中文翻譯 暫時性死區

## 理解 Execution Context 與 Variable Object

- Execution Context 執行環境。一個 JavaScript 的 Object
- Variable Object 執行環境裡面的變數物件，存放參數 Arguments

執行順序小筆記：

```jsx
var a = 1
function test() {
  console.log('1.', a) // undefined
  var a = 7
  console.log('2.', a) // 7
  a++
  var a
  inner()
  console.log('4.', a)
  function inner() {
    console.log('3.', a) // 8
    a = 30
    b = 200
  }
}
test()
console.log('5.', a) // 1
a = 70
console.log('6.', a) // 70
console.log('7.', b) // 200
```

```js

inner EC
inner VO {

}

test EC
test VO {
  inner: function,
  a: undefined -> 7 -> 8 -> 30
}

global EC
global VO {
  test: function,
  a: 1 -> 70,
  b: 200
}
```

## Call stack 資料結構

- 像盤子往上堆疊，執行完之後再從最上面一個個把盤子拿起來
- 專有名詞好像是叫 **Last In, First Out** 先進後出。
- 如果盤子有夠多，多到不堪負荷會溢出來變成 **stack overflow**

## Closure 閉包

- 在一個 function return 另一個 function
- 跟 scope chain 很有相關
- 除了在 function 內定義的方法外，無法用其他方法修改 function 內變數的值。

## IIFE 立即呼叫函示

- 用 () 包起來，後面再加一個 () 就可以立刻執行。
- 後面的 () 是用來放參數 arguments 的

```jsx
;(function () {
  console.log('123')
})()
```

## 物件導向

- setter
- getter
- this 從這裡出現，學了物件導向 this 才有意義
- ES5 之前，用 new 就是把 function 當成 construtor 來用， function 第一個字要大寫
- 使用 prototype 創建 method，調用的 function 就會相等 (true)，不會多佔用另一個記憶體空間。

```jsx
class Dog {
  constructor(name) {
    //建構子，用 new Dog 呼叫這個 class 就會自動產生
    this.name = name
  }
  getName() {
    //method -> getter
    return this.name
  }
  sayHello() {
    console.log(this.name)
  }
}

var d = new Dog('abc')
d.satHello() // 使用 method 的方式
```

## 物件導向的繼承：Inheritance

- 會出現 `extends`，第一個字大寫名稱的 function
- `extends` 上層有的東西都可以拿來用
- `super()` 就是上一層的 `constructor`
- `super()` 跟 `constructor` 一定要傳參數，不然會找不到，`super()` 會到上層去設定一些初始化的東西

```jsx
class Dog {
  constructor(name) {
    this.name = name
  }

  sayHello() {
    console.log(this.name)
  }
}

class BlackDog extends Dog {
  constructor(name) {
    // super() 跟 constructor 一定要傳參數
    super(name) // 就是 Dog 的 constructor
  }
  test() {
    console.log('test!', this.name)
  }
}

const d = new BlackDog('hello')
d.sayHello()
```

## This

- 依據環境 `this` 的預設值會有所不同。EX：瀏覽器預設 `this` 的值是 `window`，node.js 預設是 `global`
- 跟程式碼在哪裡無關，跟你在哪呼叫有關
- 在 `'use strict'` 嚴格模式下，瀏覽器跟 node.js 預設值都會變成 `undefined`
- pure function 下跟 `this` 沒什麼關係，幾乎 `this` 都會是預設值
- 例外狀況：使用 `addEventListener` 的時候 `this` 指的是點到的東西
- 箭頭函示的 this 是依據綁定的位置。

## 改變 this 的值用 call() 跟 apply()

- call 內的第一個值就會是 function 內的 this 的值

- 第一個值都是改變 this，call 後面放值，用逗號隔開，apply 後面放陣列。
- call 跟 apply 都是呼叫 function

```jsx
function test(a, b, c) {
  console.log(this) // 結果為 hello
  console.log(a, b, c) // 結果為 1, 2, 3
}

test.call('hello', 1, 2, 3) // hello 為新的 htis 的值，1,2,3 為參數
test.apply('hello', [1, 2, 3]) // 跟上面 call 的用法結果相同，兩個結果會是一樣的
```

## bind 回傳一個新的 function

- 綁定 this 的值，怎麼 call 都不會改變 this 的值
  ![](https://static.coderbridge.com/img/roroiii/43c0a6a8fe4f4cfd8668a469ca26ad16.png)

## arrow function 箭頭函示的 this

- 跟在哪邊定義的有關係
- 跟在哪怎麼呼叫沒關係
- 一般的 `this` 在普通 function 內都會指向預設值（window 或嚴格模式下的 `undefined`），但是在箭頭函式內的 `this` 指的是被定義在程式碼的哪裡

## throttle 閥值 & debounce 去抖動

debounce 像是排隊搭公車，最後一名乘客上車之後，司機才會開車。

debounce 範例

```jsx
function debounce(func, delay = 250) {
  let timer = null
  return () => {
    let context = this
    let args = arguments

    if (timer) {
      clearTimeout(timer)
    }
    timer = setTimeout(() => {
      func.apply(context, args)
    }, delay)
  }
}
```

throttle 跟 debounce 相似，不同的地方是讓使用者觸發相同事件時提供間隔，控制特定時間內事件觸發的次數。

throttle 範例

```jsx
function throttle(func, time = 250) {
  let last
  let timer

  return function () {
    const context = this
    const args = arguments
    const now = +new Date()

    if (last && now < last + timeout) {
      clearTimeout(timer)
      timer = setTimeout(function () {
        last = now
        func.apply(context, args)
      }, timeout)
    } else {
      last = now
      func.apply(context, args)
    }
  }
}
```

```jsx
function handleScroll() {
  console.log(window.scrollY)
}

window.addEventListener('scroll', throttle(handleScroll, 500)). //500ms才允許再執行
```

參考文章：

[Debounce & Throttle -  那些前端開發應該要知道的小事(一)](https://medium.com/@alexian853/debounce-throttle-%E9%82%A3%E4%BA%9B%E5%89%8D%E7%AB%AF%E9%96%8B%E7%99%BC%E6%87%89%E8%A9%B2%E8%A6%81%E7%9F%A5%E9%81%93%E7%9A%84%E5%B0%8F%E4%BA%8B-%E4%B8%80-76a73a8cbc39)

[第十六週練習題 · Issue #16 · Lidemy/mentor-program-4th](https://github.com/Lidemy/mentor-program-4th/issues/16)
