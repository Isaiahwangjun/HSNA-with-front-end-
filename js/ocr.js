// class ImageSizeError extends Error {
//     constructor(message) {
//         super(message);
//         this.name = this.constructor.name;
//         Error.captureStackTrace(this, this.constructor);
//     }
// }

// class NoTextFoundError extends Error {
//     constructor(message) {
//         super(message);
//         this.name = this.constructor.name;
//         Error.captureStackTrace(this, this.constructor);
//     }
// }

const vision = require("@google-cloud/vision");
const client = new vision.ImageAnnotatorClient({ keyFilename: "vision-ocr-311508-2df5a99e811b.json" })

async function OCR(file) {
    console.log('正在執行 OCR 函數...');
    const image_size = file.length / (1024 * 1024);
    if (image_size > 20) {
        throw new Error("圖片大小超過 20 MB，無法處理。");
    }

    const image = { content: file.toString('base64') };
    const [result] = await client.textDetection({ image });
    const texts = result.textAnnotations;

    if (!texts || !texts[0].description.trim()) {
        throw new Error("沒有掃描到文字在圖片中");
    }

    return texts[0].description;
}

const pdfImage = require('pdf-image').PDFImage;
const fs = require('fs').promises;
const os = require('os');
const path = require('path');

async function pdf_OCR(pdfBuffer) {
    let result = '';
    console.log('正在執行 pdf OCR 函數...');
    try {
        // 将缓冲区写入临时文件
        const tempPdfPath = path.join(os.tmpdir(), 'temp.pdf');
        await fs.writeFile(tempPdfPath, pdfBuffer);

        // 使用临时文件路径转换为PNG
        const pdfImageConverter = new pdfImage(tempPdfPath);
        const imagePaths = await pdfImageConverter.convertFile()
        console.log("to png workkk")
        for (let i = 0; i < imagePaths.length; i++) {
            const imagePath = imagePaths[i];
            try {
                const imageBuffer = fs.readFileSync(imagePath);
                const base64String = imageBuffer.toString('base64');
                const [result] = await client.textDetection({ base64String });
                const texts = result.textAnnotations;
                if (!texts || !texts[0].description.trim()) {
                    throw new Error("沒有掃描到文字在圖片中");
                }
                result += texts[0].description + '\n';
            } catch (error) {
                console.error('Error reading image file:', error);
            }
        }
        return result;
    } catch (error) {
        console.error('执行 PDF OCR 函数时出错:', error);
        throw error;
    }
}

module.exports = { OCR, pdf_OCR }
