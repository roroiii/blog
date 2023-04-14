---
title: PHP 會員管理系統 - 註冊表單判斷
tags: [php]
date: '2021-08-25'
---

在開始新增或是測試帳號有沒有重複，要先記得把資料庫重複的資料清空，判斷才會正確喔!
`$_POST["Username"]` 的值要跟資料庫的名稱相同。

用 JavaScript 監聽帳號有沒有跟資料庫的帳號重複

```php
<script>
		var flag_username = false;
		var flag_password = false;
		var flag_re_password = false;
		var flag_email = false;
		var flag_check_uni = false;

    	$(function(){
    		$("#btn_register").bind("click",reg);

    		//監聽帳號
    		$("#username").bind("input propertychange", function(){
    			if($(this).val().length < 6){
    				$("#err_username").text('帳號不得小於 6 個字');
    				$("#err_username").css("color","#ff0000");
    				flag_username = false;
    			}else{
    				$("#err_username").text('');
    				flag_username = true;

    				//到資料庫去判斷帳號是否有重複
    				$.ajax({
                        type: "POST",
                        url: "20200526-register-api-uni.php",
                        data: {Username: $("#username").val()},   //Username的值要跟資料庫的名稱一樣
                        success: function(data){
                            if(data){
                                $("#err_username").html("此帳號已存在!");
                                $("#err_username").css("color", "red");
                                flag_check_uni = false;
                            }else{
                                $("#err_username").html("此帳號可以使用");
                                $("#err_username").css("color", "#0BF844");
                                flag_check_uni = true;
                            }
                        },
                        error: function(){
                            alert("check uni api error");
                        }
                    });
    			}
    		});
    		$("#password").bind("input propertychange", function(){
    			if($(this).val().length < 8){
    				$("#err_password").text('密碼不得小於 8 個字');
    				$("#err_password").css("color","#ff0000");
    				flag_password = false;
    			}else{
    				$("#err_password").text('');
    				flag_password = true;
    			}
    		});
    		$("#re_password").bind("input propertychange", function(){
    			if($(this).val() != $("#password").val() ){
    				$("#err_re_password").text('確認密碼不相同');
    				$("#err_re_password").css("color","#ff0000");
    				flag_re_password = false;
    			}else{
    				$("#err_re_password").text('');
    				flag_re_password = true;
    			}
    		});
    		$("#email").bind("input propertychange", function(){
    			if($(this).val().length < 10){
    				$("#err_email").text('Email不得小於 10 個字');
    				$("#err_email").css("color","#ff0000");
    				flag_email = false;
    			}else{
    				$("#err_email").text('');
    				flag_email = true;
    			}
    		});
    	});
		function reg(){
			if(flag_username && flag_password && flag_re_password && flag_email && flag_check_uni){
				//測試用
				console.log($("#username").val());
				console.log($("#password").val());
				console.log($("#re_password").val());
				console.log($("#email").val());

				/*實際串接資料庫 20200519-php-Insert-data.php*/
				$.ajax({
					type: "POST",
					url: "20200519-php-Insert-data.php",
					data: {Username: $("#username").val(), Password: $("#password").val(), Email: $("#email").val()},
					success: show,
					error: function(){
						alert('連接 20200519-php-Insert-data.php 有錯誤');
					}
				});
	    	}else{
	    		alert('欄位有錯誤!');
	    	}
		};
		function show(data){
			alert(data);
			location.href="20200519-login.html";
		};
    </script>
```

php 後端

```php
<?php
	$p_username = $_POST["Username"];

	$servername = "localhost";
	$username = "member";
	$password = "123456";
	$dbname = "member";

	$conn = mysqli_connect($servername, $username, $password, $dbname);
	if(!$conn){
		die('連線失敗'.mysqli_connect_error($conn));
	}

	$sql = "SELECT * FROM usermember WHERE Username = '$p_username'";

	$result = mysqli_query($conn, $sql);

	if(mysqli_num_rows($result) == 1){   //判斷重複
		echo true;
	}else{
		echo false;
	}
	mysqli_close($conn);
?>
```
