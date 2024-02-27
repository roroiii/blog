---
title: 輕鬆上手：使用 ExcelJS 在前端產出 Excel 文件
# description:
permalink: posts/{{ title | slug }}/index.html
date: '2024-02-27'
tags: [javascript]
---

## 寫個 ExcelJS 的小筆記

ExcelJS 是 JavaScript 的一個 Library，有許多非常方便的功能，可以讓你順利產出漂漂亮亮的 Excel 的版面。

以下是官方的介紹：

> Read, manipulate and write spreadsheet data and styles to XLSX and JSON.
> Reverse engineered from Excel spreadsheet files as a project.

### 安裝

```bash
npm install exceljs
```

### 使用

```js
import ExcelJS from 'exceljs'

const workbook = new ExcelJS.Workbook()
const worksheet = workbook.addWorksheet('My Sheet') // 這是 Excel 表的名字
```

其實[ExcelJS 官方文件](https://github.com/exceljs/exceljs)都寫得相當清楚，下面就舉幾個我自己延伸用過的小範例。

### 文字格式設定

設定文字位置

```js
worksheet.getCell('F55').value = 'Apple'
worksheet.getCell('F55').alignment = { vertical: 'bottom', horizontal: 'right' }

worksheet.addRow(['第一格', '', '', '第四格']).alignment = { horizontal: 'left' }
```

使用 richText 的方式設定粗體、顏色等。

```js
worksheet.getCell('A17').value = {
  richText: [
    {
      font: {
        size: 9,
        bold: true,
      },
      text: 'Apple',
    },
  ],
}
```

### 設定數字格式

使用 numFmt 這個函數設定

```js
worksheet.getCell('K46').value = 54106
worksheet.getCell('K46').numFmt = '"$" #,##0.00'
```

### 從瀏覽器中讀取圖片放入 Excel

搭配 axios 從瀏覽器中讀取圖片，放入 Excel 檔案的指定位置。

```js
const imageBufferCompany = await axios.get(`/img/company.png`, {
  responseType: 'arraybuffer',
})

const imageId = workbook.addImage({
  buffer: imageBufferCompany.data,
  extension: 'png',
})

worksheet.addImage(imageId, {
  tl: { col: 9, row: 57 }, // 指定位置
  ext: { width: 174, height: 118 }, // 指定大小
})
```

### 底色填色

寫一個共用的 function ， 之後就可以直接拿來使用。

```js
function setCellFill(worksheet: ExcelJS.Worksheet, cellAddress: string, fillColor: string) {
  worksheet.getCell(cellAddress).fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: fillColor },
  }
}

const columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

// 使用
setCellFill(worksheet, 'I47', 'fffe35')
setCellFill(worksheet, 'I48', 'fffe35')

columns.forEach((column, index) => {
  if (index <= 6) setCellFill(worksheet, `${column}3`, 'b8b8b8')
})
```

### 文字租體 Bold

這滿常使用的，也是寫成一個共用的 function

```js
function setRichText(
  worksheet: any,
  cellAddress: string,
  text: string,
  vertical = 'middle',
  horizontal = 'center',
  fontSize = 9,
  isBold = true
) {
  const cell = worksheet.getCell(cellAddress)
  cell.value = {
    richText: [
      {
        font: { size: fontSize, bold: isBold },
        text: text,
      },
    ],
  }
  cell.alignment = { vertical: vertical, horizontal: horizontal }
}

// 使用
setRichText(worksheet, 'A47', 'Country of Origin:', 'middle', 'left')
setRichText(worksheet, 'J46', 'Sub Total', 'middle', 'right')
```

### 邊框 Borders

寫好共用的 border 設定，直接拿來使用。

```js
export const borderAll: Partial<ExcelJS.Borders> = {
  top: { style: 'thin' },
  left: { style: 'thin' },
  bottom: { style: 'thin' },
  right: { style: 'thin' },
}

export const borderTopLeft: Partial<ExcelJS.Borders> = {
  left: { style: 'thin' },
  top: { style: 'thin' },
}

export const borderTopRight: Partial<ExcelJS.Borders> = {
  right: { style: 'thin' },
  top: { style: 'thin' },
}

export const borderLeftBottom: Partial<ExcelJS.Borders> = {
  left: { style: 'thin' },
  bottom: { style: 'thin' },
}

export const borderRightBottom: Partial<ExcelJS.Borders> = {
  right: { style: 'thin' },
  bottom: { style: 'thin' },
}

// 使用
worksheet.getCell(`A1`).border = borderAll
worksheet.getCell(`A3`).border = borderTopLeft
worksheet.getCell(`G3`).border = borderTopRight
worksheet.getCell(`A10`).border = borderLeftBottom
worksheet.getCell(`G10`).border = borderRightBottom
```

如果要做邊線也可以用 `for` 迴圈

```js
export const borderLeft: Partial<ExcelJS.Borders> = {
  left: { style: 'thin' },
}

export const borderRight: Partial<ExcelJS.Borders> = {
  right: { style: 'thin' },
}

// 使用
for (let i = 3; i <= 52; i++) {
  worksheet.getCell(`A${i}`).border = borderLeft
  worksheet.getCell(`G${i}`).border = borderRight
}
```

### 產出 Excel 文件

最後，將做好的資料保存產出為一個文件

```js
workbook.xlsx.writeBuffer().then((content) => {
  const link = document.createElement('a')
  const blobData = new Blob([content], {
    type: 'application/octet-stream;charset=utf-8;',
  })
  link.download = `${dayjs().format('YYYYMMDDHHmmss')}.xlsx`
  link.href = URL.createObjectURL(blobData)
  link.click()
})
```
