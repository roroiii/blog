---
title: Git 版本控制指令 與 vim 編輯器
date: '2020-06-19'

tags: [git, vim, terminal]
---

## Git 的好處

- 比較容易看到版本之間的差異
- 有版本控制與分支的概念
  ![](https://static.coderbridge.com/img/roroiii/127d51a8ec204af4bf620e0161b66e63.png)

最近在學習 Git，發現 Terminal 上 Git 命令提示顯示中文，希望改成英文。
`echo "alias git='LANG=en_GB git'" >> ~/.zshrc`
![](https://static.coderbridge.com/img/roroiii/78747c6a728642919821984e2bef29d6.png)

如果你在 git commit 的時候出現錯誤，跳出了一個要你設定帳號跟姓名的畫面，請輸入以下指令

（記得把名字跟 email 換成你自己的）

1. `git config --global user.name "your name"`
2. `git config --global user.email "youremail"`

> 在 Mac “command + shift + . （dot）”可以顯示隱藏檔案/檔案夾。
> ![](https://static.coderbridge.com/img/roroiii/f12843e31c414d19823645aef8e0db90.png)

## Git 的使用方式

1. 先 `cd` 到要版控的資料夾
2. `git init`
3. `git add .`
4. `git commit -m "hello"` 或 `git commit -am "hello"`
   ![](https://static.coderbridge.com/img/roroiii/34a6cee965c74e12bc8829b91dd338e9.png)
   ![](https://static.coderbridge.com/img/roroiii/807b0bde185743eaa4376e9cd08622fe.png)

> 如果是 WIN 系統要另外下載 Git (使用的是 Git Bash)

## 常用 Git 指令

![](https://static.coderbridge.com/img/roroiii/253512209c6a417084de061dd6434ff7.jpg)

## Git branch 分支

![](https://static.coderbridge.com/img/roroiii/59e2cdf5753848ed9b41f7f964e322b4.png)
兩個不同的 Branch ，好處是大家可以互相分工。

### Branch 開發流程

1. `git branch b名稱` 開發新功能，先用 Branch 新建一個是好習慣
2. `git checkout b名稱` 切換到 b 名稱 分支做開發
3. `git checkout master` 開發完成切回主幹
4. `git merge b名稱` 把 b 名稱 的分支合併進 Master
5. `git commit -am "c名稱"` commit 修改的內容，結束

### Branch 衝突 COUFLICT

如果合併之後有衝突，要手動修改衝突的部分， Git 會提示哪裡需要修改。

1. 自己決定要留什麼內容（手動解決）
2. 儲存檔案
3. commit
   ![](https://static.coderbridge.com/img/roroiii/c4e9a1b9c4774fecb94910fd9812fe61.jpg)

## Vim 編輯器使用

![](https://static.coderbridge.com/img/roroiii/f12605ec59e9456b911aafb6177c2fe0.jpg)

## Git 狀況劇

### 什麼時候適合 commit ?

自己決定時機，通常都是完成一個小進度的時候。

### 打錯字了，想改 commit message

`git commit —amend` 可以修改指令名稱。

### 已經 commit 可是後悔了

`git reset HEAD^`  
上一個 commit 不要，但改的檔案還是要，預設 `git reset HEAD^ --soft` 的簡寫。
`git reset HEAD^ --hard`  
上一個 commit 改的東西全部不要了(當作 commit 沒發生過)

### 還沒 commit 但改的東西我不想要了

`git checkout --<flie>` 回復上一個 commit 狀態
`git checkout --.` 還沒 commit 的檔案都回到上一個 commit 的狀態
如果指令忘記了， `git status` 都有提示。

### 想修改 branch 名稱

1. `git checkout b名稱` 先切換到該 branch
2. `git branch -m b新名稱` 重新命名該 branch

### 想修改或使用遠端的 branch

直接用 `git checkout b名稱` 切換過去該分支， Git 就會自動抓下來了

### Git Hook 發生某件事情時通知我

可以用來檢查 push 的狀態，或是錯漏的地方，有時間再研究一下。
