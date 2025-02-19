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
// generateReadme.mjs

/**
 * 生成專案目錄結構的 ProjectStructure.md 文件
 * 使用 node v18.20.4 以上版本執行 (node -v 檢查版本)
 * 使用方法:
 * 1. 將此文件放在專案根目錄
 * 2. 在終端機中執行指令: node generateReadme.mjs
 * 3. 在專案根目錄下生成 ProjectStructure.md 文件
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

function generateFolderStructure(dir, depth = 0) {
  try {
    const items = fs.readdirSync(dir)
    let content = ''

    for (const item of items) {
      try {
        const itemPath = path.join(dir, item)
        const stat = fs.statSync(itemPath)
        const indent = '  '.repeat(depth)

        // 跳過指定的目錄和文件，可自行增減
        const skipList = [
          'node_modules',
          '.git',
          '.DS_Store',
          '.vscode',
          'build',
          'dist',
          'cpp',
          '.husky',
          'coverage',
          'public',
        ]

        if (skipList.includes(item)) {
          continue
        }

        if (stat.isDirectory()) {
          content += `${indent}- 📁 ${item}\n`
          content += generateFolderStructure(itemPath, depth + 1)
        } else {
          content += `${indent}- 📄 ${item}\n`
        }
      } catch (itemError) {
        console.error(`Error processing item ${item}:`, itemError)
      }
    }

    return content
  } catch (error) {
    console.error(`Error reading directory ${dir}:`, error)
    return ''
  }
}

// 正確獲取當前檔案的目錄路徑
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const projectRoot = __dirname // 當前目錄作為根目錄

try {
  const folderStructure = generateFolderStructure(projectRoot)
  const readmeContent = `# Project Folder Structure\n\nGenerated on: ${new Date().toLocaleString()}\n\n${folderStructure}`

  fs.writeFileSync('ProjectStructure.md', readmeContent)
  console.log('✅ ProjectStructure.md generated successfully.')
} catch (error) {
  console.error('❌ Error generating ProjectStructure.md:', error)
}
```

確認電腦有安裝 node ，這邊使用的是 node v18.20.4，然後執行

```bash
node generateReadme.mjs
```

產出來的 README.md 結構會像下面這樣

```
# Project Folder Structure

Generated on: 2/19/2025, 2:49:05 PM

- 📄 generateReadme.mjs
- 📄 index.html
- 📄 package.json
- 📄 ProjectStructure.md
- 📄 README.md
- 📁 src
  - 📁 apis
  - 📄 App.tsx
  - 📁 components
    - 📁 button
      - 📄 init-button.tsx
      - 📄 set-button.tsx
    - 📁 chart

  ...Other files

```

如果想指定專案目錄，也可以直接修改 `projectRoot` 的值

```js
const projectRoot = 'D:\vite-react' // 使用專案實際路徑
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
