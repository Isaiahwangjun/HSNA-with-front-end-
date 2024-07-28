from google.cloud import vision
from google.oauth2 import service_account
import io
import fitz


def OCR(file):
    credentials = service_account.Credentials.from_service_account_file(
        filename='app/vision-ocr-311508-2df5a99e811b.json')
    client = vision.ImageAnnotatorClient(credentials=credentials)
    # with io.open(file, 'rb') as image_file:
    #     content = image_file.read()
    image = vision.Image(content=file)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description


##### pdf 切成一頁一頁，每頁可以有 text 和 image，先 scan text, then image
def pdf_OCR(path):
    ans = ''
    doc = fitz.open(path)
    for page in doc:
        text = page.get_text()
        ans += text + '\n'

        # 提取图像
        images = page.get_images()
        print(images)
        for img_num, img in enumerate(images):
            xref = img[0]  # 图像的对象引用
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]  # 图像的字节数据
            image_path = f"page_{page.number}_image_{img_num}.png"
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
                text = OCR(image_bytes)
                ans += text + '\n'

    return ans


##### pdf 切成一頁一頁，每頁不是 text 就是 image
def pdf_OCR(path):
    ans = ''
    doc = fitz.open(path)
    for page in doc:
        text = page.get_text()
        if text.strip():  #如果有字，當作是 pdf_text
            ans += text + '\n'
        else:  #如果沒有，當作是 pdf_image
            pix = page.get_pixmap()  #page 目前是 <class 'fitz.fitz.Page'>，先轉為圖片
            pix = pix.tobytes(
            )  #'Pixmap' type --> bytes type (以符合 google ocr input)
            text = OCR(pix)
            ans += text + '\n'
    return ans


# ans = pdf_OCR("C:\\Users\\wang\\Downloads\\1810.09136-5-6.pdf")
# test = pdf_OCR("C:\\Users\\wang\\Downloads\\1_merged.pdf")
# print(ans)
