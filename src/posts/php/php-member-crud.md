---
title: PHP 會員管理系統 - CRUD概念 & 前後端分離介面
tags: [php]
date: '2021-08-25'
---

以下預設你已經裝好了 XAMPP ，也會使用這套軟體。

這篇文章會使用的語言：

- PHP & MySQL
- HTML ( Bootstrap )
- JavaScript ( jQuery )

使用到的 函數：

PHP & MySQL

---

- mysqli_connect() ; mysqli_connect_error()
- mysqli_query()
- mysqli_num_rows()
- mysqli_fetch_assoc()
- json_encode()
- mysqli_close()

JavaScript ( jQuery )

---

- alert()
- append()
- $.ajax()

## 1.先建立資料庫 member

---

![](https://static.coderbridge.com/img/roroiii/8de0a04477bb4168a7ea11c4513cea8b.png)

## 2.創建一個管理 member 的管理帳號

---

不建議用最高權限管理，有可能手誤或程式寫錯就把系統整個砍掉！

![](https://static.coderbridge.com/img/roroiii/44110768ae9d4e33a872e8689ab2c778.png)

![](https://static.coderbridge.com/img/roroiii/c61fe492bd534ca2a7a0e9f4117a5a75.png)

指定資料庫的 管理權限不要勾選

資料表 給只管理 member 的權限

再重新登入之後就會看到只有 menber 這個資料庫。

使用者帳號這是練習使用 'member@localhost' 比較好記憶，但是在實務上帳號不可以用一樣的唷，危險危險。

![](https://static.coderbridge.com/img/roroiii/b90e6fad9f1049d4b27da2ce29c4e467.png)

如果不能重新登入，就是要到 phpMyAdmin 資料夾裡的 config.inc.php 檔案修改成使用 http

以下僅供練習，真正實務上要設計再強\強度高的密碼。

![](https://static.coderbridge.com/img/roroiii/9f4053de47f844269b9228a80cf5554b.png)

```php
/* Authentication type and info */
$cfg['Servers'][$i]['auth_type'] = 'http';  //選擇使用 http 網域登入
$cfg['Servers'][$i]['user'] = 'root';       //這裡輸入你的帳號
$cfg['Servers'][$i]['password'] = '';       //這裡輸入密碼
$cfg['Servers'][$i]['extension'] = 'mysqli';  //選擇是哪個資料庫
$cfg['Servers'][$i]['AllowNoPassword'] = true;  //要不要開啟密碼登入資料庫
$cfg['Lang'] = '';
```

資料庫的地方也會顯示沒有建立新資料庫的權限

![](https://static.coderbridge.com/img/roroiii/1e35aa61970c4039ad767f209669878f.png)

## 3.建立 PHP 連線

---

這裡可以參考 W3School 的 [**PHP Connect to MySQL**](https://www.w3schools.com/php/php_mysql_connect.asp) 練習寫一遍，以下是用 Example (MySQLi Procedural) 的範例練習。

```php
<?php
	$servername = "localhost";
	$username = "member";
	$password = "123456";

	//建立連線
	$conn = mysqli_connect($servername, $username, $password);

	//測試連線有沒失敗
	if(!$conn){
		die('連線失敗' . mysqli_connect_error());
	}

	echo '連線成功';
?>
```

加上 `mysqli_connect_error()` 連線失敗會有錯誤訊息，就可以判斷是哪裡有 Bug

![](https://static.coderbridge.com/img/roroiii/7f155f5d724a4245898a904761b625f3.png)

連線失敗 Access denied for user 'member'@'localhost' (using password: YES)

> 小知識：**CRUD**
> Create Read Update Delete
> 常用在資料庫連線的說法，再回去看 W3School 的 MySQL 列表是不是比較清楚明白了呢？

## 4.建立資料庫裡的資料表連線

---

因為一步驟一步驟學，所以把 PHP 連線跟資料表連線分開紀錄。有部分程式碼是一樣的。

參考 W3School 的 [PHP MySQL Select Data](https://www.w3schools.com/php/php_mysql_select.asp)

```php
<?php
	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";    //資料庫 member

	//連線資料庫
	$conn = mysqli_connect($servername, $username, $password, $dbname);

	//判斷連線是否失敗
	if(!$conn){
		die('連線失敗' . mysqli_connect_error());
	}

	//選擇要撈取的資料， * 表示全部。
	$sql = 'SELECT * FROM usermember';

	//找出 result 的語法
	$result = mysqli_query($conn, $sql);

	//判斷資料表有沒有內容，如果是空的就不執行查詢
	if(mysqli_num_rows($result) > 0){
		while($row = mysqli_fetch_assoc($result)){   //因為不知道資料有多少筆，所以用 While 迴圈
			echo $row['Username'];
		}
	}else{
		echo '沒有資料內容';
	}
	//每次連線完都要寫關閉，才不會讓伺服器負載過大
	mysqli_close($conn);
?>
```

這裡畫一個流程圖

## 5.讓 PHP 的 MySQL 資料轉成 JSON 格式

---

修改上一步驟的 if...else 程式碼。

```php
//新增一個 PHP 陣列，用來轉成 Json 格式
	$myarray = array();

	//判斷資料表有沒有內容，如果是空的就不執行查詢
	if(mysqli_num_rows($result) > 0){
		while($row = mysqli_fetch_assoc($result)){
			// echo $row['Username'];
			$myarray[] = $row;
		}
		//轉成 json 語法
		echo json_encode($myarray);
	}else{
		echo '沒有資料內容';
	}
```

解釋一下 `$myarray = array()` 是新增一個 PHP 陣列，目的是要把這個陣列轉換成 JSON 格式。由於 PHP 內建把陣列轉換成 JSON 的函數 `json_encode()` ，所以最後用 echo 就好。

還有 While 迴圈的地方，我們要把輸出結果用陣列取代，所以改寫成 `$myarray[] = $row` 。

如果只有寫 `$myarray = $row` ，就只會顯示第一筆資料。

把它想像成是抽屜一樣，多了 **[ ]** 就可以打開每個抽屜放入你要的資料，讓每筆資料都正常顯示了。

![](https://static.coderbridge.com/img/roroiii/190cdb0af046414892d9ffe2abd68759.jpg)

![](https://static.coderbridge.com/img/roroiii/a1a3dfc9f0244bac959cf0070dc1b08d.jpg)

他們之間的關係圖應該是長這樣，有空再整理畫一張。

## 6.開始寫個前端介面，接收資料庫的 data 囉

---

使用的是 Bootstrap 簡單做一個表格，用 jQuery 的 Ajax 函數串接資料顯示出來。

```html
這是完整的程式碼，以下會一一說明解釋。
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />

    <!-- Bootstrap CSS -->
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
      integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
      crossorigin="anonymous"
    />

    <title>會員資料系統</title>
  </head>
  <body>
    <div class="container">
      <div class="row">
        <div class="col-md-8 offset-2">
          <table class="table">
            <thead>
              <tr>
                <th>標號</th>
                <th>姓名</th>
                <th>註冊時間</th>
                <th>信箱</th>
              </tr>
            </thead>
            <tbody id="member_list">
              <tr>
                <td>001</td>
                <td>TT</td>
                <td>465656</td>
                <td>d@mail</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script
      src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
      integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"
      integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6"
      crossorigin="anonymous"
    ></script>
    <script>
      $(function () {
        $.ajax({
          type: 'GET',
          url: 'http://www/mobileweb/20200515_php_Server_dataconn_to_json.php',
          dataType: 'json',
          success: show,
          error: function () {
            alert('error!')
          },
        })
      })
      function show(data) {
        console.log(data)
        for (i = 0; i < data.length; i++) {
          str =
            '<tr><td>' +
            data[i].ID +
            '</td><td>' +
            data[i].Username +
            '</td><td>' +
            data[i].Created_at +
            '</td><td>' +
            data[i].Email +
            '</td></tr>'

          $('#member_list').append(str)
        }
      }
    </script>
  </body>
</html>
```

特別要注意的是直接使用 Bootstrap 的檔案時，**使用的 jQuery 檔案不能是 slim 檔**，因為這個檔案不包含 Ajax 的語法，所以我們要修改 Bootstrap 預設引入的檔案。

```html
<!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
  </body>
```

然後把要串接的資料程式寫在引入檔的下面，或是另外建一個 JavaScript 檔寫也可以。

```jsx
<script>
    	$(function(){
    		$.ajax({
    			type: "GET",
    			url: "http://www/mobileweb/20200515_php_Server_dataconn_to_json.php",
    			dataType: "json",
    			success: show,   //創立一個名字叫"show"的function，拉出去括號寫
    			error: function(){
    				alert("error!");
    			}
    		});
		});
		//定義名叫"show" 的 function 要做什麼內容
		function show(data){
			console.log(data);  //測試一下資料有沒有跑出來

			//因為要顯示很多筆資料，所以我們寫一個迴圈讓它重複做這件事情
			for(i=0; i<data.length; i++){

				//str 存放要顯示的資料跟HTML格式
				str = '<tr><td>'+data[i].ID+'</td><td>'+data[i].Username+'</td><td>'+data[i].Created_at+'</td><td>'+data[i].Email+'</td></tr>';

				//寫一個監聽做這件事情，使用append()函數，把資料覆蓋上去的用法。
				$("#member_list").append(str);
			};
		};
    </script>
```

如果跑出來的資料都是 undefined 表示 Ajax 裡面的 dataType 寫錯囉！ **T** 要記得大寫。

![](https://static.coderbridge.com/img/roroiii/72ef0e79fb594cdeb62f99618c84cd53.png)

str 存放要顯示的 HTML 應該有更好閱讀與維護的寫法，但是目前只學到這種，之後會再研究這部分的內容。

## 結語

以上就做完一個前後端分離的會員系統，非常簡單的做法，但是能利用自己實作理解前後端的概念，並互相串連起來。
