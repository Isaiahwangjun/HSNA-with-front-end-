const OCR_ = require('./ocr.js');
const express = require('express');
const multer = require('multer');

const app = express();
const port = 3000;

// 設置 Multer 中間件來處理文件上傳
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// 處理文件上傳路由
app.post('/upload', upload.array('image', Infinity), async (req, res) => {
    try {
        const files = req.files; // 使用 req.files 獲取所有上傳的文件
        const detections = [];
        for (const file of files) {
            if (file.mimetype === "image/png") {
                const imageBuffer = file.buffer;

                // 使用 OCR 函數進行文字識別
                const detection = await OCR_.OCR(imageBuffer);
                detections.push(detection);
            }
            else {
                const pdfBuffer = file.buffer;
                const detection = await OCR_.pdf_OCR(pdfBuffer);
                detections.push(detection);
            }
            // 返回識別結果
            res.json(detections);
        }
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});