---
title: PHP 會員管理系統 - 會員列表
tags: [php]
date: '2021-08-25'
---

HTML

```html
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

    <title>會員列表</title>
  </head>
  <body>
    <div class="container">
      <div class="row">
        <div class="col-md-8 offset-2">
          <div class="card mt-5">
            <div class="card-header">
              <h1>會員列表</h1>
            </div>
            <div class="card-body">
              <table class="table">
                <thead>
                  <tr>
                    <th>編碼</th>
                    <th>帳號</th>
                    <th>密碼</th>
                    <th>信箱</th>
                    <th>註冊時間</th>
                  </tr>
                </thead>
                <tbody id="member_list">
                  <tr>
                    <th>1</th>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                </tbody>
              </table>
              <div class="card-footer"></div>
            </div>
          </div>
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
      Ajax 串接寫在這裡
    </script>
  </body>
</html>
```

JavaScript

```jsx
//Ajax串接內容
$(function () {
  $.ajax({
    type: 'GET',
    url: 'http://192.168.10.14/mobileweb/member/20200526-list-api.php',
    dataType: 'json',
    success: show,
    error: function () {
      alert('20200526-list-api error')
    },
  })
})
function show(data) {
  // console.log(data);
  // console.log(data[0].ID);
  // strHTML = '<tr><th>1</th><td>Mark</td><td>Otto</td><td>@mdo</td></tr>';

  //ES6寫法 **`** 代替 **'** 就有排版可讀性
  str =
    `<tr>
                  <th>` +
    data[0].ID +
    `</th>
                  <td>` +
    data[0].Username +
    `</td>
                  <td>` +
    data[0].Password +
    `</td>
                  <td>` +
    data[0].Email +
    `</td>
                  <td>` +
    data[0].Created_at +
    `</td>
                </tr>`

  $('#member_list').append(str)
}
```

php 把資料撈出來

```php
<?php
	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);

	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	}

	$sql = "SELECT * FROM usermember ORDER BY ID DESC";  // ORDER BY ID DESC 排序最新在上面

	$result = mysqli_query($conn, $sql);

	// $row = mysqli_fetch_assoc($result);  //挖掘機，挖資料，一次挖一筆
	// echo $row["Username"];

	$myArray = array();

	while ($row = mysqli_fetch_assoc($result)) {   //加上while迴圈讓挖掘機一直挖資料出來
		//echo $row["Username"]."<br>";
		$myArray[] = $row;
	}

	//轉成 json 格式
	echo json_encode($myArray);

	mysqli_close($conn);
?>
```

![](https://static.coderbridge.com/img/roroiii/8938d66d262b47deae36935552a7412f.png)

在 HTML 裡可以藏 `data-id` ，可以用 JavaScript 監聽
EX: HTML:`<data-* = "123">` JavaScript: `data(*)`

## 刪除資料

```php
<?php
	$p_ID = $_POST['ID'];

	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);
	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	}

	$sql = "DELETE FROM usermember WHERE ID = '$p_ID'";

	//mysqli_affected_rows($conn) == 1 表示刪除的資料要有1筆才會是成功刪除
	if(mysqli_query($conn, $sql) && mysqli_affected_rows($conn) == 1){
		echo true;
	}else{
		echo false;
	}
	mysqli_close($conn);
?>
```

確認 Postman 測試沒問題之後再開始寫 Ajax 串接刪除資料。

`confirm()` 是有點像 `alert` 的彈出視窗，常拿來用為防止不小心刪除的雙重確認。

```jsx
<script>
      $(function(){
        $.ajax({
          type: "GET",
          url: "20200526-list-api.php",
          dataType: "json",
          async: false,    //把Ajax的非同步關掉。因為Ajax的優點是非同步、最後才執行，這裡關掉刪除按鈕才能監聽到資料。
          success: show,
          error: function(){
            alert('20200526-list-api error');
          }
        });

        //監聽刪除按鈕
        $("table #btn-del").bind("click", function(){  //因為監聽的位置巢狀很多層，加讓table可以讓瀏覽器順利找到資料。
          //alert($(this).data("id"));
          $del_id = $(this).data("id"); //設定一個變數儲存data-id的資料，以防使用者亂按位置跑掉。

          //防手滑刪除首選 confirm
          if(confirm("你確定要刪除"+ $del_id)){
            //Ajax執行刪除資料
            $.ajax({
              type: "POST",
              url: "20200526-member-del.php",
              data:{ID: $del_id},  //ID大小寫要跟Postman測試使用的一樣
              success: function(data){
                if(data){
                  alert('刪除成功');
                  location.href="20200526-member-list.html";
                }else{
                  alert('刪除失敗!')
                }
              },
              error: function(){
                alert('del api error');
              }
            });
          }


        });
      });
      function show(data){
        // console.log(data);
        // console.log(data[0].ID);
        // strHTML = '<tr><th>1</th><td>Mark</td><td>Otto</td><td>@mdo</td></tr>';
        for(i = 0; i<data.length; i++){
            str = `<tr>
            <th>`+data[i].ID+`</th>
            <td>`+data[i].Username+`</td>
            <td>`+data[i].Password+`</td>
            <td>`+data[i].Email+`</td>
            <td>`+data[i].Created_at+`</td>
            <td>
              <a href="#" class="btn btn-danger" id="btn-del" data-id="`+data[i].ID+`">刪除</a>
              <a href="#" class="btn btn-primary">更新</a>
            </td>

          </tr>`;

          $("#member_list").append(str);
        }

      }
    </script>
```

## 更新資料

PHP 語法

`mysqli_affected_rows($conn) == 1` 是確定資料庫的筆數為一筆才動作，才不會資料庫沒有那筆資料卻顯示 true。可以練習用刪除的語法改寫。

```php
<?php
	$p_id = $_POST['ID'];
	$p_username = $_POST['Username'];
	$p_password = $_POST['Password'];
	$p_email = $_POST['Email'];

	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);
	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	}

	//更新資料庫語法
	$sql = "UPDATE usermember SET Username='$p_username', Password='$p_password', Email='$p_email' WHERE id='$p_id'";

	//mysqli_affected_rows($conn) == 1 是確定資料庫的筆數為一筆才動作
	if(mysqli_query($conn, $sql) && mysqli_affected_rows($conn) == 1){
		echo true;
	}else{
		echo false;
	}

	mysqli_close($conn);
?>
```
