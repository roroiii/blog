---
title: Redux Toolkit Query 管理共用的 API 狀態
date: '2023-08-22'
tags: [react, redux]
---

使用 Redux Toolkit Query 來管理共用的 API 狀態吧！

說明：

- `import.meta.env.VITE_API_URL` 這是 vite 獲取環境變數的語法
- 使用 Redux Toolkit Query 的 `createApi`, `fetchBaseQuery`

<!--

用 Redux Toolkit Query 做一個範例專案
寫下步驟與要注意的地方
做一個 GitHub 開源小專案可以 build 起來的那種
 -->

```ts
// auth.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const authApi = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: `${import.meta.env.VITE_API_URL}` }), // 這邊替換成自己的API網址
  endpoints: (builder) => ({
    login: builder.mutation({
      query: (credentials) => ({
        url: '/login',
        method: 'POST',
        body: credentials,
      }),
    }),
  }),
})

export const { useLoginMutation } = authApi
```

設定 store

```ts
// store.ts
import { configureStore } from '@reduxjs/toolkit'
import { authApi } from './api/auth'

export const store = configureStore({
  reducer: {
    [authApi.reducerPath]: authApi.reducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(authApi.middleware),
})
```

```tsx
// main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { store } from './store.ts'
import { Provider } from 'react-redux'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
)
```

使用方式跟 [TanStack Query](https://tanstack.com) 類似

```tsx
// App.tsx
import { useLoginMutation } from './api/auth'
import { useState } from 'react'
import './App.css'

function App() {
  const [user, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const [login] = useLoginMutation()

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value)
  }

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value)
  }

  const handleLogin = () => {
    login({ user, password })
      .unwrap()
      .then((response) => {
        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  return (
    <>
      <div>
        <h1>Login</h1>
        <input type="text" placeholder="Username" value={user} onChange={handleUsernameChange} />
        <input type="password" placeholder="Password" value={password} onChange={handlePasswordChange} />
        <button onClick={handleLogin}>Login</button>
      </div>
    </>
  )
}

export default App
```

參考資料：[[Redux] Redux Toolkit Query](https://pjchender.dev/react/redux-rtk-query/)
