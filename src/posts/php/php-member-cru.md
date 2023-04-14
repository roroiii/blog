---
title: PHP 會員管理系統 - 新增 & 修改 & 刪除
tags: [php]
date: '2021-08-25'
---

這是一個偷懶的小孩，時隔一年多才把筆記上傳的系列文 QQ

## 新增資料 INSERT

INSERT INTO VALUES

`$sql = "INSERT INTO Table名稱(欄位1, 欄位2, 欄位3) VALUES('欄位1的值', '欄位2的值', '欄位3的值')";`

```php
<?php
$servername = "localhost";
$username = "member";
$password = "123456";
$dbname = "member";

//建立連線
$conn = mysqli_connect($servername, $username, $password, $dbname);

//判斷連線式成功
if(!$conn){
	die("連線錯誤" . mysqli_connect_error());
}

//寫入資料
$sql = "INSERT INTO usermember(Username, Password, Email)
VALUES('Mary', '123456', 'abc@mail.com')";

//先寫資料連線與執行，之後再寫判斷式。 mysqli_query($conn, $sql);
if(mysqli_query($conn, $sql)){
	echo '新增資料成功';
}else{
	echo '新增資料失敗' . $sql . "<br>" . mysqli_error($conn);
};

mysqli_close($conn);   //$conn->close(); 也可以這樣寫
?>
```

第二步嘗試用變數取代固定的 VALUES 值 ，用 POST 接收資料，製作前後端分離的概念。

```php
<?php
//設定變數來存放要接收的資料
$p_username = $_POST["Username"];
$p_password = $_POST["Password"];
$p_Email = $_POST["Email"];

$servername = "localhost";
$username = "member";
$password = "123456";
$dbname = "member";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if(!$conn){
	die("連線錯誤" . mysqli_connect_error());
}

//VALUES 裡的值代換成自訂變數
$sql = "INSERT INTO usermember(Username, Password, Email)
VALUES('$p_username', '$p_password', '$p_Email')";

if(mysqli_query($conn, $sql)){
	echo '新增資料成功';
}else{
	echo '新增資料失敗' . $sql . "<br>" . mysqli_error($conn);
};

mysqli_close($conn);
?>
```

使用 Postman 測試連線成不成功，這裡要注意的是 Key 名稱要跟資料庫的名稱相同。

![](https://static.coderbridge.com/img/roroiii/e1b545ac39884026956f172c42fd4373.png)

但是上面這樣寫在 PHP 頁面重新整理就會新增一筆空白的資料，所以我們可以加入判斷防止這件事情發生。

```php
//判斷這三個值都不為空值才可以執行，否則就出現警告訊息。
if($p_username != "" && $p_password != "" && $p_Email != ""){
		if(mysqli_query($conn, $sql)){
			echo '新增資料成功';
		}else{
			echo '新增資料失敗' . $sql . "<br>" . mysqli_error($conn);
		}
}else{
		echo "不允許新增空白資料。";
};
```

## 更新資料 UPDATE

UPDATE SET WHERE

`**$sql = "UPDATE [Table名稱] SET [資料表名稱] = '值' WHERE  [Primary key] = 值";**`

```php
<?php
	//建立連線
	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);
	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	};

	//更新資料
	$sql = "UPDATE usermember SET Username = 'TINA' WHERE ID = 1";

	//判斷更新資料有沒有成功
	if(mysqli_query($conn, $sql)){
		echo "更新成功";
	}else{
		echo "更新失敗".mysqli_error($conn);
	}

	mysqli_close($conn);
?>
```

也可以同時修改多筆資料

```php
//更新資料
	$sql = "UPDATE usermember
	SET Username = 'Tina', Password = '999999', Email = 'tina@gmail.com'
	WHERE ID = 1";
```

![](https://static.coderbridge.com/img/roroiii/547ee5c78c5148dca15ef04a3a06b473.png)

第二步同樣我們也可以用變數取代固定的值

```php
<?php
	//設定變數接收值
	$p_id = $_POST["ID"];
	$p_username = $_POST["Username"];
	$p_password = $_POST["Password"];
	$p_email = $_POST["Email"];

	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);
	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	}

	//更新資料使用變數
	$sql = "UPDATE usermember
	SET Username = '$p_username', Password = '$p_password', Email = '$p_email'
	WHERE ID = '$p_id'";

	//判斷如果值有內容才可以更新
	if($p_id != "" && $p_username != "" && $p_password != "" && $p_email != ""){
		//判斷更新資料有沒有成功
		if(mysqli_query($conn, $sql)){
			echo "更新成功";
		}else{
			echo "更新失敗".mysqli_error($conn);
		}
	}else{
		echo "資料更新不能空白。";
	}

	mysqli_close($conn);
?>
```

使用 Postman 測試看看是否成功

![](https://static.coderbridge.com/img/roroiii/dc9868ef04314634a38d2006f0559a1b.png)

## 刪除資料 DELETE

DELETE FROM WHERE

跟上面相同，先設定一個變數置換 ID 的位置，就可以動態的刪除不同的資料囉！

`**$sql = "DELETE FROM  [Table名稱]  WHERE [Primary key]";**`

```php
<?php
	$p_id = $_POST["ID"];

	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);
	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	}

	//刪除資料
	$sql = "DELETE FROM usermember WHERE ID = '$p_id'";

	if(mysqli_query($conn, $sql)){
		echo "刪除成功!";
	}else{
		echo "刪除失敗!" . mysqli_error($conn);
	}

	mysqli_close($conn);
?>
```
