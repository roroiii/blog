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

其他部分目前尚在學習中 ⋯⋯
