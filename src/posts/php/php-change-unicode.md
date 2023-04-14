---
title: PHP 翻譯 繁轉簡 轉換編碼
date: '2021-08-25'
tags: [php]
---

利用 php 內建編碼，轉換編碼即可。

```php
先把要轉換的資料從資料庫撈出來
之後對資料執行下面的程式

 $value[$trans_source] = iconv('UTF-8', 'BIG5', $value[$trans_source]);
$value[$trans_source] = iconv('BIG5', 'GB2312', $value[$trans_source]);
$out = iconv('GB2312', 'UTF-8', $value[$trans_source]);

$data = array(
    $trans_column => $out,
);

最後再更新到資料表就可以囉
```

ci 版本

可以寫成獨立 function 之後調用

```php
class Trans
{
	public function trans($data)
	{

		$table_name1 = $data['table_name1'];
		$trans_source = $data['trans_source'];
		$trans_column = $data['trans_column'];
		$column_name = $data['column_name'];
		$column_id_name = $data['column_id_name'];


		$CI = &get_instance();   // 處理 ci 底層的運作
		$CI->db2 = $CI->load->database('db3', TRUE);
        $a = $CI->db2->get($table_name1)->result_array();



        foreach($a as $value)
        {

            $value[$trans_source] = iconv('UTF-8', 'BIG5', $value[$trans_source]);
            $value[$trans_source] = iconv('BIG5', 'GB2312', $value[$trans_source]);
            $out = iconv('GB2312', 'UTF-8', $value[$trans_source]);

            $data = array(
                $trans_column => $out,
            );
            $CI->db2->where($column_id_name,$value[$column_id_name]);
            $CI->db2->update($table_name1,$data);

        }
	}
}

```

使用

```php
public function index()
    {
        // news_title_tw
         $news_title = array(
             'table_name1' => 'news', //資料表
             'trans_source' => 'news_title_tw', //轉換來源
             'trans_column' => 'news_title_cn', //被轉換欄位
             'column_id_name' => 'news_id' //轉換主鍵
        );
        $this->load->library('Trans',$news_title);
        $this->Trans->trans();
    }
```

但是遇到文章那種比較複雜的內容，就不建議用這個方法，因為會有滿多錯誤的 QQ
文章推薦用 繁化姬 或 OpenCC API 的方式做轉換
