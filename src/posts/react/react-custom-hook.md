---
title: Custom Hook 來自己寫一個  hook 吧!
date: '2021-08-25'
tags: [react]
---

## 首先， 自訂的 Hook 一定要用 use 作為開頭

會用到的 hook 記得要 import 進來。
把變數 return 回去就可以在 app.js 中使用。

新增一個檔案叫做 useInput.js 把 App.js 裡面的邏輯抽出來

### useInput.js

```jsx
import { useState } from 'react'

export default function useInput() {
  const [value, setValue] = useState('')
  const handleChange = (e) => {
    setValue(e.target.value)
  }

  return {
    value,
    setValue,
    handleChange,
  }
}
```

再做一個把 todos 會用到的東西抽出來

### useTodos.js

```jsx
import { useState, useEffect, useRef } from 'react'
import useInput from './useInput'

function writeTodosToLocalStorage(todos) {
  window.localStorage.setItem('todos', JSON.stringify(todos))
}

export default function useTodos() {
  const id = useRef(1)
  const { value, setValue, handleChange } = useInput()
  const [todos, setTodos] = useState(() => {
    let todoData = window.localStorage.getItem('todos') || ''
    if (todoData) {
      todoData = JSON.parse(todoData)
      id.current = todoData[0].id + 1
    } else {
      todoData = []
    }
    return todoData
  })

  useEffect(() => {
    writeTodosToLocalStorage(todos)
  }, [todos])

  const handleButtonClick = () => {
    setTodos([
      {
        id: id.current,
        content: value,
        size: 'XL',
      },
      ...todos,
    ])
    setValue('')
    id.current++
  }

  const handleToggleIsDone = (id) => {
    setTodos(
      todos.map((todo) => {
        if (todo.id !== id) return todo // 不等於要修改的 id 直接回傳
        return {
          ...todo,
          isDone: !todo.isDone,
        } // 是要修改的 id 就把原本的 todo 加上要修改的屬性
      })
    )
  }

  const handleDeleteTodo = (id) => {
    setTodos(todos.filter((todo) => todo.id !== id))
  }

  return {
    todos,
    setTodos,
    id,
    handleButtonClick,
    handleToggleIsDone,
    handleDeleteTodo,
    value,
    setValue,
    handleChange,
  }
}
```

如果要用同一個 hook 在新的 input 裡面使用，這樣寫就可以調用了
變成 ES6 object 的寫法

```jsx
// 假如有第二個 input 也需要這個方法，就可以用：
const { value: todoName, setValue: setTodoName, handleChange: handleTodoName } = useInput()
```

最後 App.js 檔案就變得很乾淨了
`import { useState, useRef, useEffect } from "react";`
也都不用寫在 App.js 裡面

### App.js

```jsx
import TodoItem from './TodoItem'
import useTodos from './useTodos'

function App() {
  const {
    todos,
    setTodos,
    id,
    handleButtonClick,
    handleToggleIsDone,
    handleDeleteTodo,
    value,
    setValue,
    handleChange,
  } = useTodos()

  return (
    <div className="App">
      <input type="text" value={value} onChange={handleChange} />
      <button onClick={handleButtonClick}>Add todo</button>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          title={todo.title}
          size={todo.size}
          handleDeleteTodo={handleDeleteTodo}
          handleToggleIsDone={handleToggleIsDone}
        />
      ))}
    </div>
  )
}

export default App
```

這樣拆開來寫的好處是，介面跟邏輯分開，把共同的邏輯抽出來另外寫，這樣以後只要在套用一樣的邏輯，就可以產出不一樣的 UI 畫面了，是不是很棒呢～^^
