---
title: Server  同步 gitLab
date: '2020-06-19'
tags: [git]
---

cPanel 自動同步 GitLab 檔案

## php 的方式

Cron job 指令

```php
php -q /home/.../public_html/git.php >/dev/null 2>&1
```

檔案 git.php

```php
<?php
    shell_exec( 'git pull origin master' );
    echo '同步完成！';
?>
```

## git.sh 的方式

Cron job 指令

```php
/home/.../git.sh >/dev/null 2>&1
```

檔案 git.sh

```
cd /home/.../public_html/資料夾名稱

git checkout -b branch-name
git remote update

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git pull origin branch-name
fi
```
