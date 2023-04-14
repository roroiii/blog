---
title: React 的 controller component 與 uncontrolled
date: '2021-08-17'
tags: [react]
---

此為 React 學習筆記，純粹用自己好記憶的方式所寫喔～

常見表單的控制方法，分為
**controller component (有被 React 控制著)**  
**uncontrolled (沒有被 React 控制)**

---

## controller component

使用 `value={value} onChange={handleInputClick}` 做 controller

`setTodos([value,...todos])` 這個方法會新增一個新的陣列，產生新的 todo。
這邊要注意的是不能用 `push` 對陣列做改變，因為 `push` 是改變原來的陣列
React 每次重新呼叫 function 會認為值沒有改變，所以畫面就不會變。

` setValue(e.target.value)` 會拿到輸入的值

App.js

```js
import styled from 'styled-components'
import TodoItem from './TodoItem'
import { useState } from 'react'

function App() {
  const [todos, setTodos] = useState([1])

  const [value, setValue] = useState('')

  const handleButtonClick = () => {
    setTodos([value, ...todos]) // 產生新的 todo
    setValue('')
  }

  const handleInputClick = (e) => {
    setValue(e.target.value) // 拿到 input 輸入的值
  }

  return (
    <div className="App">
      <input type="text" value={value} onChange={handleInputClick} />
      <button onClick={handleButtonClick}>Add todo</button>
      {todos.map((todo, index) => (
        <TodoItem key={index} content={todo} />
      ))}
    </div>
  )
}

export default App
```

---

## uncontrolled

有二種方法，一種是常見的 `ducument.querySelector` 抓取 className 名稱
一種是用 `useRef` 的方式。

`ducument.querySelector` 抓取 className 名稱

```js
function App() {
   const handleButtonClick = () => {
    document.querySelector('.input-todo').value()
  }

  return (
      ...
       <input className="input-todo" type="text"  />
      ...
  )
}

```

用 `useRef` 的方式
首先 import `useRef` 來用。
設定變數 `const inputRef = useRef()`
input 加上 `ref={inputRef}` 。

`useRef` 可以像 state 一樣操作，但是在重新 Render 的時候不會改變。

`console.log(inputRef.current.value)` 可以查看取到的值
在這裡 `inputRef` 是物件，物件裡面會有 `current` ，可以拿到所選的物件(`<input type="text">`)，是 React 提供的一種方法。
不太懂的話可以自己 console.log 幾次就知道了

```js
import { useState, useRef } from 'react'

function App() {
  const [todos, setTodos] = useState([1])

  const [value, setValue] = useState('')
  const inputRef = useRef()

  const handleButtonClick = () => {
    console.log(inputRef.current.value)
    setTodos([value, ...todos])
    setValue('')
  }

  const handleInputClick = (e) => {
    setValue(e.target.value)
  }

  return (
    <div className="App">
      <input ref={inputRef} type="text" onChange={handleInputClick} />
      <button onClick={handleButtonClick}>Add todo</button>
      {todos.map((todo, index) => (
        <TodoItem key={index} content={todo} />
      ))}
    </div>
  )
}
```

上面的範例都是用 `index` 當作 key 的值，但是這樣寫比較不好，應該讓每個 todo 都有獨特的 id ，所以可以改成這樣：

App.js

```js
import TodoItem from './TodoItem'
import { useState } from 'react'

let id = 2 // 因為 function 每次都會重新被呼叫，所以 id 要放在 function 外面
function App() {
  const [todos, setTodos] = useState([{ id: 1, content: 'abc' }])

  const [value, setValue] = useState('')

  const handleButtonClick = () => {
    setTodos([
      {
        id,
        content: value,
      },
      ...todos,
    ])
    setValue('')
    id++ // 由 setTodos 操作 state 讓 id + 1
  }

  const handleInputClick = (e) => {
    setValue(e.target.value)
  }

  // key 的值改成 todo.id
  return (
    <div className="App">
      <input type="text" value={value} onChange={handleInputClick} />
      <button onClick={handleButtonClick}>Add todo</button>
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  )
}

export default App
```

TodoItem.js
增加一個 `data-todo-id={todo.id}` 確認 id 是不是有正確

```js
import './App.css'
import styled from 'styled-components'
import { ThemeProvider } from 'styled-components'
import { MEDIA_QUERY_M, MEDIA_QUERY_L } from './constants/breakpoint'

const theme = {
  colors: {
    primary_300: '#ff0000',
    primary_600: '#dd0000',
    primary_900: '#yy0000',
  },
}

const Title = styled.h1`
  font-size: 36px;

  ${(props) =>
    props.size === 'XL' &&
    `
    font-size: 20px;
  `}
`

const TodoContent = styled.div`
  color: ${(props) => props.theme.colors.primary_300};
  font-size: ${(props) => (props.size === 'XL' ? '20px' : '16px')};
`

const BlackTodoItem = styled(TodoItem)`
  background: #000000;
`

const TodoItemWrapper = styled.div`
  padding: 20px;
  border: solid 1px #000000;
  display: flex;
  align-items: center;
  justify-content: space-between;

  ${MEDIA_QUERY_M} {
    border: solid 2px red;
  }
`

const Button = styled.button`
  padding: 4px;
  background-color: blue;
  color: #ffffff;
`

const ReButton = styled(Button)`
  background-color: #ff0000;
`

function Counter() {
  alert(1)
}

function TodoItem({ className, size, todo, title }) {
  return (
    <ThemeProvider theme={theme}>
      <Title>{title}</Title>
      <TodoItemWrapper className={className} data-todo-id={todo.id}>
        <TodoContent size={size}>{todo.content}</TodoContent>
        <div>
          <Button>已完成</Button>
          <ReButton>刪除</ReButton>
        </div>
      </TodoItemWrapper>
    </ThemeProvider>
  )
}

export default TodoItem
```

這樣就有 id 的值囉～

![](https://static.coderbridge.com/img/roroiii/44f0c00ca015482e9a5d2c6d4f12ac16.png)
