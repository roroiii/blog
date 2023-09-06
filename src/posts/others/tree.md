---
title: 使用 JavaScript 腳本或是 tree 自動產出目錄結構吧！
date: '2023-09-06'
tags: [others]
---

如果專案越來越龐大，是不是很難了解整個專案結構呢？<br/>
如果有可以自動產出結構的東西，就不用自己一層一層慢慢找了，真的非常方便，減少了手動寫文件出錯的機率，就跟 Swagger 一樣是懶人的福音^^

接下來簡單介紹兩種方法～

## 自己寫 JavaScript 腳本產出

使用 node 18 版本

```js
// generateReadme.js

import fs from 'fs'
import path from 'path'

function generateFolderStructure(dir, depth = 0) {
  const items = fs.readdirSync(dir)

  let content = ''

  for (const item of items) {
    const itemPath = path.join(dir, item)
    const isDirectory = fs.statSync(itemPath).isDirectory()
    const indent = '  '.repeat(depth)

    if (isDirectory) {
      content += `${indent}- ${item}\n`
      content += generateFolderStructure(itemPath, depth + 1)
    } else {
      content += `${indent}- ${item}\n`
    }
  }

  return content
}

const projectRoot = '/path/to/your/project' // 這裡替換成自己電腦專案的絕對路徑

const folderStructure = generateFolderStructure(projectRoot)
const readmeContent = `# Project Folder Structure\n\n${folderStructure}`

fs.writeFileSync('README.md', readmeContent)
console.log('README.md generated successfully.')
```

確認電腦有安裝 node，然後執行

```bash
node generateReadme.js
```

產出來的 README.md 結構會像下面這樣

```
- apis
  - commonAPI.ts
- components
  - .DS_Store   // 會不小心混入記得刪除唷
  - button
    - CalcButton.tsx
    - SubmitButton.tsx
  - loading
    - LoadingBox.tsx
- hooks
  - types.ts
  - utils
    - useOpen.ts
  - utilsQuery
    - useAddData.ts
    - useDeleteData.ts
    - useGetData.ts
    - useUpdateData.ts
- main.tsx
- pages
  - error-page.tsx
  - home-page.tsx
  - signIn-page.tsx
- redux
  - hooks.ts
  - reducers
    - alertBoxReducer.ts
    - loadingReducer.ts
    - userReducer.ts
  - store.ts
- vite-env.d.ts

```

---

## tree

Mac 系統直接安裝：

```bash
brew install tree
```

使用就是在專案直接

```bash
tree
```

如果只想要拿到 src 的結構

```bash
$ cd src  // 切換到 src 的路徑
$ tree
```

其他指令可以看[tree 文檔](https://mama.indstate.edu/users/ice/tree/)或是

```bash
tree --help
```

產出來的 README.md 結構會像下面這樣，有著酷酷的線條，是不是比較好閱讀 ^^

```
.
├── git
│   ├── command-line.md
│   ├── git-and-vim.md
│   └── server-ansyc-gitlab.md
├── javascript
│   ├── cookie-and-localstorage-and-sessionstorage.md
│   ├── debounce-and-memoize.md
│   ├── javascript-note.md
│   ├── lidemyOJ.md
│   ├── q1.md
│   └── upgrade-the-node-version-of-your-project.md
├── lidemy
│   ├── 2020-06-11.md
│   ├── 2020-06-12.md
│   ├── 2020-06-15.md
│   ├── 2020-06-16.md
├── others
│   ├── 11ty-blog.md
│   ├── 2022-work.md
│   ├── 2023-changed-your-name.md
│   └── tree.md
├── php
│   ├── php-change-unicode.md
│   ├── php-member-api.md
│   ├── php-member-cru.md
│   ├── php-member-crud.md
│   ├── php-member-list.md
│   ├── php-member-register.md
│   └── php-replace-str.md
├── posts.json
└── react
    ├── react-change-state.md
    ├── react-controller-component-and-uncontrolled.md
    ├── react-custom-hook.md
    ├── react-delete-todo.md
    ├── react-nextjs-mui.md
    ├── react-render.md
    └── redux-toolkit-query.md
```

以後如果遇到交接或是需要解釋檔案位置的時候，就試試看使用這種方式吧^^

---

參考資料：<br/>
小花<br/>
[Homebrew tree](https://formulae.brew.sh/formula/tree) <br/>
[[Mac] Homebrew 安裝 tree(樹狀資料夾目錄結構)](https://quietbo.com/2021/11/10/mac-homebrew%E5%AE%89%E8%A3%9Dtree%E6%A8%B9%E7%8B%80%E8%B3%87%E6%96%99%E5%A4%BE%E7%9B%AE%E9%8C%84%E7%B5%90%E6%A7%8B/)<br/>
[[Tools]使用 tree 自動生成目錄結構](https://tiffrrr.medium.com/to-o-l-s-%E4%BD%BF%E7%94%A8tree%E8%87%AA%E5%8B%95%E7%94%9F%E6%88%90%E7%9B%AE%E9%8C%84%E7%B5%90%E6%A7%8B-ca421a81b009)
