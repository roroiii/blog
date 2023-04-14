---
title: PHP CodeIgniter 資料庫字詞替換
tags: [php]
date: '2021-08-25'
---

大量替換字詞，針對文章只取一部份資料替換再塞回去資料庫
資料撈出來->替換字詞->更新回去
遇到 / 可以直接替換
" 會有點問題，要做跳脫字元的處理

```php
<?php
  echo '\''; // 會印 '
  echo '\\'; // 會印 \
  echo '\"'; // 會印 "
?>
```

```php
    //替換字詞
    public function replace($database) {
      $this->db = $this->load->database($database, TRUE);
      $this->db->select('news_id, news_content_cn');
      $query = $this->db->get('news');

      foreach($query->result_array() as $row){
        $str = 'http://www.web.tw';
        $result = str_replace("$str", "", $row['news_content_cn'], $count);

        $data = array(
          'news_content_cn' => $result,
        );

        $this->db->where('news_id',$row['news_id']);
        $this->db->update('news', $data);
      }
    }
```

嘗試了公司的資料庫，發現只要遇到 雙引號就無法替換 QQ
但其他字詞都沒問題，
用了簡短的 Array 去測試也都沒問題
我推測的原因是文章的資料表格格式太多種，可能有遇到什麼狀況造成無法順利取代。
