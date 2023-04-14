---
title: PHP 會員管理系統 - 超入門版登入串接
tags: [php]
date: '2021-08-25'
---

開始製作登入畫面的連線，這裡用到 `mysqli_num_rows($result) == 1` 來判斷資料庫裡有沒有重複的資料。

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

	$sql = "SELECT * FROM usermember WHERE Username = 'Tina' AND Password = '999999'";

	$result = mysqli_query($conn, $sql);

	if(mysqli_num_rows($result) == 1){
		echo '登入成功';
	}else{
		echo '登入失敗';
	}

?>
```

上面測試成功後，把登入的帳號跟密碼用變數取代，再用 Postman 測試有沒有成功。

`mysqli_num_rows($result) == 1` 這裡的判斷值也改成 `true` 跟 `false` ，讓前端去處理要顯示什麼東西。

```php
<?php
	$p_username = $_POST["Username"];
	$p_password = $_POST["Password"];

	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);
	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	}

	$sql = "SELECT * FROM usermember WHERE Username = '$p_username' AND Password = '$p_password'";

	$result = mysqli_query($conn, $sql);

	if(mysqli_num_rows($result) == 1){
		echo true;
	}else{
		echo false;
	}
?>
```

成功之後就開始用 Ajax 寫串接啦~ `password: $("#Password").val()` 是取得前端畫面輸入框的值跟資料庫做對比，`if(data)` 是判斷登入成功之後執行什麼事情。

```jsx
<script>
    	$(function(){
    		$("#btn_login").bind("click", login);

    		function login(){
    			$.ajax({
    				url: '20200526-login.php',
    				type: 'POST',
    				dataType: 'json',
    				data: {username:$("#username").val(), password: $("#Password").val()},
    				success: show,
    				error: function(){
    					alert('連線錯誤');
    				}

    			})
    		}
    	});

    	function show(data){
    		if(data){
    			alert('登入成功');
    			location.href = "20200526-member-list.html";
    		}else{
    			alert('登入失敗');
    		};
    	};
    </script>
```

在開始新增或是測試帳號有沒有重複，要先記得把資料庫重複的資料清空，判斷才會正確喔!
`$_POST["Username"]` 的值要跟資料庫的名稱相同。
