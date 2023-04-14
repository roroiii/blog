---
title: 在 React 刪除 todo 的方法
date: '2021-08-25'
tags: [react]
---

觀念：在 parent 處理 function -> 當作 props 傳下去給 child -> child 再呼叫這個 function

parent(App.js) 傳給 child(TodoItem.js)

---

`todos.filter(todo => todo.id !== id)` true 的東西會留下來

可以用下面這了例子來思考
`[1, 2, 3].filter(i => i > 1)` 大於 1 的會留下來

**App.js**

```js
function App() {

  ...

  const handleDeleteTodo = id => {  // 接收 id 當作參數
    setTodos(todos.filter(todo => todo.id !== id))
  }

  return (
    <div className="App">

      ...

      // 把 handleDeleteTodo 傳下去給 child
      {
        todos.map(todo => <TodoItem key={todo.id} todo={todo} handleDeleteTodo={handleDeleteTodo}/>)
      }
    </div>
  );
}
```

**TodoItem.js**

```js
// 接收 handleDeleteTodo 就可以使用了
function TodoItem({ className, size, todo, handleDeleteTodo }) {
  return (
    <>
      ...
      <ReButton
        onClick={() => {
          handleDeleteTodo(todo.id)
        }}
      >
        刪除
      </ReButton>
      ...
    </>
  )
}
```
