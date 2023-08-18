---
title: 升級你的專案 Node
description: 升級你的專案 Node 套件，跟上最新 Node.js 的版本吧！
permalink: posts/{{ title | slug }}/index.html
date: '2023-08-18'
tags: [javascript, node]
---

這次嘗試升級 blog 的 Node 版本，從 16 升級到 18，搭配使用 chatGPT 可以幫助我們減少找文件的時間唷。

### 小花，要怎麼把專案 npm 的版本從 node 16 升級到 node 18 ？確保套件沒有問題？

要將你的專案從 Node.js 16 升級到 Node.js 18，並確保相依的 npm 套件沒有問題，你可以按照以下步驟操作：

1. 升級 Node.js：

   - 首先，安裝新版的 Node.js。訪問 Node.js 官方網站 下載並安裝 Node.js 18 的版本。

2. 驗證 Node.js 和 npm 版本：

   - 安裝新版後，在終端檢查 Node.js 和 npm 的版本以確保安裝成功：
     ```bash
     node -v
     npm -v
     ```

3. 更新專案依賴：

   - 在你的專案資料夾中運行以下命令，更新專案的 npm 套件：

     ```bash
     npm update
     or
     yarn upgrade
     ```

4. 檢查過時的依賴：

   - 使用以下命令查看哪些套件已經過時，這可以幫助你確定哪些套件可能需要手動升級：

     ```bash
     npm outdated
     or
     yarn outdated
     ```

5. 升級過時的依賴：

   - 對於 npm outdated 列出的過時套件，你可以手動更新它們到新的版本。修改 package.json 文件中的對應版本號，然後執行：

     ```bash
     npm install
     or
     yarn install
     ```

6. 解決依賴衝突：

   - 升級後，可能會出現一些依賴衝突或者不兼容的情況。這時需要你手動檢查和解決這些問題。這可能涉及更新套件，或者回退到某個與新版 Node.js 兼容的版本。

7. 運行測試：

   - 如果你的專案中包含自動測試，此時運行它們以確保升級後一切仍然運作正常：

     ```bash
     npm test
     or
     yarn test
     ```

8. 手動測試：

   - 除了自動測試，也應該手動運行你的應用並進行測試，以確保一切都按照預期工作。

9. 查看更新日誌和變更日誌：

   - 查看你依賴的每個套件的更新日誌或變更日誌，這些文檔會列出新版本中的更改，並指出任何重大變更或潛在的破壞性更改。

10. 備份你的專案：
    - 在升級重要依賴之前，確保你已經備份了整個專案，以便於需要時能夠回滾到之前的狀態。
      請記住，在升級 Node.js 和 npm 套件版本時，一定要謹慎。始終確保你的專案有適當的備份，並且充分測試以確保一切都在正常工作。

### 小花，如果我是使用 yarn 上面的指令要如何更正？

與 npm 流程相同，我有把指令貼在 npm 下面了。

---

這邊要注意的是手動替換 `package.json` 的版本不要眼殘貼錯了 XD
<img src="/images/posts/upgrade-the-node-version.png" alt="upgrade the node version">

專案大套件變多的話，可能會更麻煩，但如果 yarn build 也沒問題，就可以放心的 commit 並部署囉！沒有遇到錯誤是不是很快就解決了ＸＤ
