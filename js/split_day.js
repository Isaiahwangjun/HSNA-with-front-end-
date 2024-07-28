const fs = require('fs');

function splitDiary(text) {
    const lines = text.split('\n');
    let fileName = '';
    let content = '';

    for (let line of lines) {
        // 檢查是否包含日期
        const match = line.match(/(\d{1,2}|[\u4E00-\u9FFF]{1,3})月(\d{1,2}|[\u4E00-\u9FFF]{1,3})日/g);
        if (match) {
            fileName = match
            fs.appendFileSync(`${fileName}.txt`, line);
        } else {
            // 如果不是日期，將該行內容添加到內容中
            fs.appendFileSync(`${fileName}.txt`, line);
        }
    }

    // 寫入最後一個檔案
    if (content) {
        fs.writeFileSync(`${fileName}.txt`, content);
    }
}

splitDiary(`一月十六日晚上九點多,江東〔施江東〕君來中央書局找我,兩人相偕去大正
軒喝紅茶。一月十七日
肇嘉兄今夜從臺中回故鄉清水,預定由該地直接上京。`)