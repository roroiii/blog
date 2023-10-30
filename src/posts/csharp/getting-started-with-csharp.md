---
title: 跨足 C#：以前端為出發點的學習策略，Mac 上的 C# 學習計畫
date: '2023-10-26'
tags: [csharp, asp.net, blazor]
description: ''
---

> 標題真難想 QQ

## 學習起因

雖然有一些後端的概念，也使用過 PHP 或 Node.js 之類的語言，但還是想學習有比較完整概念的後端語言，剛好公司後端目前都使用 C# ，就趁這個機會挑戰看看。

學習一門程式語言要了解基礎語法、慣用程式語言、基礎架構還有一些語法糖 ⋯⋯ 總之從零開始學的話，要熟悉這些語言都要花上一段時間（就跟學英文法文德文之類的語言一樣）睡覺睡得夠多(?)才會記在腦袋裡。本篇學習心得是建立在「已經會一門前端框架程式」的基礎上，你已經會使用前端框架開發網站的角度來學習 C#。

因為我的電腦是 Mac ，雖然公司有派發 win 系統的電腦但因為想虐待自己(?)挑戰用 Mac 系統可不可以從頭學會 C#，所以寫了這個心得過程筆記。

---

## 學習基礎

- 作業系統： masOS Ventura 13.3.1
- IDE： VS Code (Visual Studio Code) ，搭配使用 Copilot Chat 學習
- 前端技能：JavaScript、TypeScript、React，會使用 npm，了解 package.json 是什麼
- 筆記軟體：UpNote

VS Code prettier settings 參考：

```json
  "[csharp]": {
    "editor.defaultFormatter": "ms-dotnettools.csharp",
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "editor.suggest.showWords": true
  },
  "[aspnetcorerazor]": {
    "editor.defaultFormatter": "ms-dotnettools.blazorwasm-companion",
    "editor.tabSize": 4,
    "editor.insertSpaces": true
  },
```

X: 不推薦使用 Visual Studio For Mac，功能太閹割了，且微軟已經宣布將在 2024 年 8 月 31 日淘汰這個產品。

---

## 入門 C#

因為 C# 是一門歷史悠久的程式語言，所以內容包山包海，要從哪個角度切入開始理解慨念真的滿重要的，我是用 FreeCodeCamp 的 [Foundational C# with Microsoft](https://www.freecodecamp.org/learn/foundational-c-sharp-with-microsoft/) 開始入門，他是搭配微軟的教學系統 [Write your first C# code](https://learn.microsoft.com/en-us/training/modules/csharp-write-first/) 一步一步開始教起。

選擇理由是這個真的最基礎，也會很詳細的講到一些程式慣用語跟概念，課綱 FreeCodeCamp 也都幫你排好了，照著學就對！
微軟也很貼心的有 Mac 作業系統搭配 VS Code 的教學，圖文詳細的教你如何使用 VS Code Debug 工具，也會帶著你做小作品。

小缺點大概就是微軟寫的教學介紹真的滿長的，常常看到想睡覺 QQ<br>
懶得全看的話，已經會的概念可以快速跳過。

學習重點就是不要複製貼上，不可以一直按 tab tab 補完程式，請自己一行行碼字，使用肌肉記憶。
期間搭配使用 Google 與 Copilot Chat，例如各種函數的用途，VS Code 的功能藏在哪裡之類的蠢問題，學習完成時間大概一至二週。

最後課程結束會有個考試，考完就會給你一張證書。
![](/images/posts/freecodecamp-certifications-csharp.png)

這個課程學完的話就會知道怎麼使用 function 寫一隻程式<br>
是的，他沒教你 interface、class 之類的東西，真的是給你學基礎概念 XD

---

## 學習 C# 的前端框架 Blazor

是的，因為我們是從前端往後端 C# 學，不急著一開始就全學會 C# 武功秘笈全集，我們要從擅長的角度切入，所以從 Blazor 開始。

學習搭配教學文章：

- [.NET Blazor 筆記：簡介](https://www.huanlintalk.com/2022/12/net-blazor-introduction.html)
- [Blazor 修仙之旅 - 初尝](https://www.cnblogs.com/stulzq/p/12984971.html)
- [Blazor - app building workshop](https://github.com/dotnet-presentations/blazor-workshop/tree/main)

Blazor 跟 React 還有 Vue 很像，有類似 npm、yarn 跟 package.json 的東西，只差在指令不同改成 `dotnet` 開頭，
套件改成使用 NuGet 安裝， Component 的副檔名變成 `.razor`。

### Blazor Server

- 程式跑在後端，對伺服器需求量大，不支持 PWA。
- 需要可執行 C# 的環境。

### Blazor WebAssembly

- 靜態可部署在 GitHub Pages ，支持 PWA
- 在 Blazor WebAssembly 中，您可以使用 HttpClient 類別或 IHttpService 服務來發送 HTTP 請求。
- 不需要 C# 執行環境。

Component 簡單說明：
`@page` 就是路由， `@Code` 的地方寫邏輯，操作 DOM 的地方都改成 `@` 開頭。

```csharp
@page "/myorders"
@inject HttpClient HttpClient

<PageTitle>Blazing Pizza - My Orders</PageTitle>

<div class="main">
    @if (ordersWithStatus == null)
    {
        <text>Loading...</text>
    }
    else if (!ordersWithStatus.Any())
    {
        <h2>No orders placed</h2>
        <a class="btn btn-success" href="">Order some pizza</a>
    }
    else
    {
        <div class="list-group orders-list">
            @foreach (var item in ordersWithStatus)
            {
                <div class="list-group-item">
                    <div class="col">
                        <h5>@item.Order.CreatedTime.ToLongDateString()</h5>
                        Items:
                        <strong>@item.Order.Pizzas.Count()</strong>;
                        Total price:
                        <strong>£@item.Order.GetFormattedTotalPrice()</strong>
                    </div>
                    <div class="col">
                        Status: <strong>@item.StatusText</strong>
                    </div>
                    <div class="col flex-grow-0">
                        <a href="myorders/@item.Order.OrderId" class="btn btn-success">
                            Track &gt;
                        </a>
                    </div>
                </div>
            }
        </div>
    }
</div>

@code {
    IEnumerable<OrderWithStatus> ordersWithStatus;

   protected override async Task OnParametersSetAsync()
    {
        ordersWithStatus = await HttpClient.GetFromJsonAsync<List<OrderWithStatus>>("orders");
    }
}
```

但是目前 Blazor 在 VS Code 上編輯真的太難 Debug 了，例如錯字會不提示，變數名稱錯誤找不到，語法 highlight 錯誤之類都是家常便飯，所以肌肉學習打字練習就好，接下來就往 ASP.NET Core webAPI 前進吧！

至於 .NET 家族之間的愛恨情仇可以參考這一篇文章：
[ASP.NET Core MVC 入門教學 - ASP.NET 之開發網站各技術架構簡介](https://blog.talllkai.com/ASPNETCoreMVC/2023/02/24/environment)

---

### 學習 ASP.NET Core WEB API

這部分嘗試開始找網路影片教學，但是會卡在作業系統跟 IDE 的問題，大部分教學都使用 Visual Studio for Windows ，這樣在第一步環境建置專案就會有入門困難，所以還是繞回來從微軟的教學開始 [Build web apps with ASP.NET Core for beginners](https://learn.microsoft.com/en-us/training/paths/aspnet-core-web-app/)

---

接下來是痛苦的開始～俗話說沒有痛苦沒有成長

### 學習 C# 物件導向概念

雖然我是有點概念但是很難用自己的話講出一套說法，簡而言之就是還不熟 QQ
這裡講解的文章五花八門，我推薦看 伊果的沒人看筆記本的菜雞新訓記 ，講得算清楚也描述的很有趣。

[菜雞新訓記 (5): 使用 三層式架構 來切分服務的關注點和職責吧](https://igouist.github.io/post/2021/10/newbie-5-3-layer-architecture/)

---

其他看影片的部分就使用時間軸 ⋯⋯

---

#### Oct 18, 2023, 5:23 PM

ASP .Net Core WebAPI

Teddy 教學影片
[https://youtu.be/\_8nLSsK5NDo?si=NZMaATIbY2lj1HU2  
](https://youtu.be/_8nLSsK5NDo?si=NZMaATIbY2lj1HU2)

學到一半學了 SQL Server for Mac 的安裝與設定

FreeCodeCamp
[Learn ASP.NET Core MVC (.NET 6) - Full Course - YouTube](https://www.youtube.com/watch?v=hZ1DASYd9rk)

---

#### Oct 19, 2023, 9:40 AM

觀念學習
[菜雞新訓記 (5): 使用 三層式架構 來切分服務的關注點和職責吧](https://igouist.github.io/post/2021/10/newbie-5-3-layer-architecture/ 'https://igouist.github.io/post/2021/10/newbie-5-3-layer-architecture/')

---

#### Oct 22, 2023, 5:20 PM

系列影片，看到一半有跟著做。後面有點看不下去，所以先去看別的影片。

[ASP.NET Core Web API - 6. GET & Read Methods [PART 1]](https://youtu.be/K4WuxwkXrIY?si=cZpIW4SvY8kezZhx&t=1648 'https://youtu.be/K4WuxwkXrIY?si=cZpIW4SvY8kezZhx&t=1648')

---

#### Oct 24, 2023, 5:16 PM

這個影片講滿快的，但是講解得滿清楚，理解 .net core 整體架構有跟著做到一半，後面之後再找時間做。

還有講者用 vim 開發真的很快，也促使我開始好好學 vim

[Industry Level REST API using .NET 6 – Tutorial for Beginners](https://youtu.be/PmDJIooZjBE?si=MsD9BF208hO3ZaEk 'https://youtu.be/PmDJIooZjBE?si=MsD9BF208hO3ZaEk')

---

#### Oct 24, 2023, 5:14 PM

因為用因為英文畢竟不是母語，有一些專有名詞用英文還是不太能理解，所以接下來用母語來補足一些不懂的概念。

著重在後半部，用母語補足一些基本觀念，這個講者真的解釋得很清楚 👍

但是真的講得太基礎了，所以其實沒有再往下學的感覺。

[【C#】3 小時初學者教學 ｜ Csharp ｜ C# 教學 ｜ C# 入門 | C++++ - YouTube](https://www.youtube.com/watch?v=T9BeejD3i0g 'https://www.youtube.com/watch?v=T9BeejD3i0g')

---

#### Oct 24, 2023, 5:18 PM

凱哥寫程式，影片真的太多了，只看了前面三分之一 QQ

看前面講解 .net 之間的可以了解這個框架之間的愛恨情仇（？

[ASP.NET Core Web API 入門教學](https://youtu.be/dXUfZuf1Wp4?si=hE4kx001czuAJnFH 'https://youtu.be/dXUfZuf1Wp4?si=hE4kx001czuAJnFH')

---

#### Oct 25, 2023, 3:40 PM

LINQ

查詢資料庫的語法，第一次知道這個東西ＱＱ

[https://learn.microsoft.com/zh-tw/dotnet/csharp/linq/](https://learn.microsoft.com/zh-tw/dotnet/csharp/linq/)

[LINQ 深入淺出（一）：觀念篇](https://jscinin.medium.com/linq-%E6%B7%B1%E5%85%A5%E6%B7%BA%E5%87%BA-%E4%B8%80-%E8%A7%80%E5%BF%B5%E7%AF%87-f43881fa4e5a 'https://jscinin.medium.com/linq-%E6%B7%B1%E5%85%A5%E6%B7%BA%E5%87%BA-%E4%B8%80-%E8%A7%80%E5%BF%B5%E7%AF%87-f43881fa4e5a')

---

#### Oct 26, 2023, 8:57 AM

本來打算之後找時間跟著做，但是其實官方就有提供範例拉～
[使用 Web API 慣例](https://learn.microsoft.com/zh-tw/aspnet/core/web-api/advanced/conventions?view=aspnetcore-6.0)

[【SP】ASP.NET Core Web API 示範 - CRUD Database First,GET,POST,PUT,DELETE](https://www.youtube.com/watch?v=d9WZoH3vYAY&list=PLneJIGUTIItsqHp_8AbKWb7gyWDZ6pQyz&index=14)

---

#### Oct 26, 2023, 10:33 AM

從這裡開始看

[【3.事前必備知識】ASP.NET Core Web API 入門教學(3_6) - 回應正確的 HTTP 狀態碼？](https://youtu.be/GUjnwK0BsN4?si=gfdlbVikc4HHvKtp 'https://youtu.be/GUjnwK0BsN4?si=gfdlbVikc4HHvKtp')

---

#### Oct 27, 2023, 15:57 AM

借了電子書 [C#最強入門邁向頂尖高手之路王者歸來](https://taichunggov.ebook.hyread.com.tw/bookDetail.jsp?id=325084) ，這本是今年 2 月出版的，我覺得很適合用來入門 .net6.0，觀念也講得滿清楚的，但是只能借 14 天所以我打算跳著看。

#### Oct 30, 2023, 2:49 PM

跟著影片完成教學專案，有放到我的 [Github](<[https://github.com/roroiii/dotnet-webapi-net7.0](https://github.com/roroiii/dotnet-webapi-net7.0)>)，這個教學講解很清楚，跟著做也沒問題。
然後因為我是用 Mac 系統，所以最後面連線資料庫我是換成 SQLite。

[.NET 7 Beginner Course 🚀 Web API, Entity Framework 7 & SQL Server](https://youtu.be/9zJn3a7L1uE?si=PEdvH9HXQV3ehDH4&t=1648 'https://youtu.be/9zJn3a7L1uE?si=PEdvH9HXQV3ehDH4&t=1648')

---

暫時的結語（？

目前這樣學下來，應該是可以寫簡單的 Web API 了，還要花時間在熟一下語法的部分，還不敢自居已經會使用 C#，筆記總共寫了 28 篇。

其實中間因為作業系統的問題踩了一些坑但都被我順手解決掉了，感覺是工程師的職業生涯裡，已經讓我培養出解決問題的能力，而且現在還有 Copilot 可以問問題，真的縮短滿多踩坑卡住的時間。

大概用了一個月的時間 (09/26 - 10/30) 主管放手讓我自學，是也很希望公司有提供教育訓練啦～但這樣應該會更久才學會怎麼用 C#，我覺得我自學也學得還算滿不錯的嘿嘿 (´･ω･`)

希望之後寫 C# 專案順利～
