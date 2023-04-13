---
title: 11ty 一日架站心得，搭配 Netlify 與 Google Domains 購買網域
description: 11ty 一日架站紀錄，搭配 Netlify 與 Google Domains 購買網域的隨意聊。這次 blog 搬家使用了很多人推薦的 [11ty](https://www.11ty.dev/)，搭配 11ty 官方推薦的 Netlify 簡單架設網站，自己使用的版型是 Yinka 製作的簡單乾淨版面，覺得漂亮很喜歡。
permalink: posts/{{ title | slug }}/index.html
date: '2023-04-13'
tags: [blog]
---

## 11ty

這次 blog 搬家使用了很多人推薦的 [11ty](https://www.11ty.dev/)，搭配 11ty 官方推薦的 Netlify 簡單架設網站，自己使用的版型是 Yinka 製作的簡單乾淨版面，覺得漂亮很喜歡。

在 Yinka 的 [Github](https://github.com/yinkakun/eleventy-duo) 專案裡面 Fork 一份到自己的 Github 再拉到本地端就可以開始修改了， 我自己是新做了一頁 Archive 準備拿來檢視自己到底寫過什麼碗糕( ；´Д ｀)

金魚腦的記憶力，就是會馬上忘記，所以記錄下來學過什麼以後還可以回來複習，特別是面試常被問的題目。

## Google Domains

以前就有用過 google domains 買過網址，這次買也超級快速的，基本上選定網址加入購物車結帳然後就完成了，非常方便，也有附贈 SSL 憑證跟信箱轉址的服務。

用 google domains name servers 才能使用信箱轉寄服務，關於怎麼在 Netlify 加上 DNS 可以參考下方的教學影片。

[[Tutorial] - How to Setup Custom Domain | Netlify & Google Domains | 2022](https://www.youtube.com/watch?v=cDDr-NoI5fo)

## Netlify

第一次使用。我覺得跟 Next.js 的背後金主爸爸 Vercel 很像，只是選單好像比較多，先註冊一個帳號，然後授權自己的 Github 專案，我是選單一專案授權，之後跟著步驟做就會開始自動部署，成功後自己設定一下專屬網址就完成了。

## 調整版型

這個是比較麻煩的部分，要做幾張圖片替換掉原本的預設樣式，還要想一下自己的介紹（寫的很廢 QQ）
之後如果心情不錯的話會再加上分頁功能，Archive 的部分應該會照著日期或是自創標籤排序。

寫了這麼多廢話...好像真的沒有什麼可以做紀錄的耶，可能因為太簡單了，或是有一些步驟教學上網都找得到，好像不需要多寫一篇文章來記錄...

沒關係寫都寫了，要讓未來的自己見證現在有多廢！嗯嗯！

這次 blog 文章搬家最大的好處，應該是寫文章覺得變順手了，因為可以寫在本地端的專案裡面，commit 並 push 上去文章就發布了～增加了寫文章的動力，期待未來自己會有更多產出。
