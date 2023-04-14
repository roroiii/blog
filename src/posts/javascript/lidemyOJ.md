---
title: LidemyOJ 解題 - 聯誼門票搶起來
date: '2021-11-26'

tags: [javascript]
---

久違的練習解題目，覺得 Huli 出的 Lidemy OJ 題目都滿經典的，而且都是中文題目，很適合訓練邏輯思考。

網址：https://oj.lidemy.com/

我自己報名程式導師實驗計畫，從零基礎開始學程式，剛開始看這些題目真的頭很痛看不太懂，真的很像在寫數學題，認識的數學系同學卻很快就把題目解完了，真的是肉眼可見的程度差距ＸＤ

你要告訴自己其實不是不懂也不是不會，只是沒看過這些題目剛開始被震懾到而已，有一天你也可以靠自己解出這些題目的！多寫題目多看題目都會進步，每天練習一點點，累積起來也會很可觀。

邏輯思考對工程師真的滿重要的，但是這種抽象概念也不是一朝一夕可以練成的，建議大家可以從簡單的題目開始慢慢練習解題，每次解出來都會有種痛快感ＸＤ

解題重點：

1. 先找到要抓取的值
2. 找到要分割的字串長度
3. 把字串拼起來之後用 `split()` 分割
4. 找到要抓取的字的位置，字串拼接起來就是答案

附上我的 ac 方式，不是最好，但是是我自己想出來的解法ＸＤ

```js
var readline = require('readline')

var lines = []
var rl = readline.createInterface({
  input: process.stdin,
})

rl.on('line', function (line) {
  lines.push(line)
})

rl.on('close', function () {
  solve(lines)
})

function solve(lines) {
  // 這裡寫解題方式
  let numLength = Number(lines[0])
  let m = Number(lines[numLength + 1])
  let s = lines[1]

  function sArr() {
    for (let i = 2; i <= numLength; i++) {
      s += lines[i]
    }
    return s.split('')
  }

  const strArr = sArr()
  let str = ''
  function ansStr() {
    for (let i = 1; i <= m; i++) {
      str += strArr[Number(lines[numLength + 1 + i] - 1)]
    }
    return str
  }
  console.log(ansStr())
}
```

前端工程師真的要會滿多技能的，基本的前端三劍客、英文能力、邏輯思考、抽象概念、UIUX、SEO、後端你最好都要懂一點，感覺未來 TypeScript 跟 Docker 可能也會是基本配置，進到公司之後也是無止盡的學，新手菜鳥真的別指望可以像別人下班在家追劇放鬆玩遊戲，要追上公司的程度你自己要花很多下班時間進修。

尤其前端變化真的很快，可能兩年前寫的扣現在看起來已經不太能用了，變成無止盡的學，你是為了薪水還是真心喜歡工程師這份工作呢？

我自己是後者拉，可以讓我持續成長的公司我都很喜歡，太安逸或是技術都沒有想要更新的公司就會待不住，我就常問自己，如果我中了樂透生活無慮我還會想當工程師嗎？答案也是肯定的，因為我就閒不住，就一直想學新的東西，這可能也是自己從行銷轉工程師的原因ＸＤ

覺得很可惜的是為什麼以前學生時代不知道寫程式這麼有趣呢？如果可以早幾年知道該多好

祝大家都可以解出解不開的題目，找到心目中理想的工作。
