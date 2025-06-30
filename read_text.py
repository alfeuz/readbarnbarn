import cv2
import numpy as np
from PIL import Image
import os
import easyocr

class TextReader:
    def __init__(self):
        """
        เริ่มต้นคลาสสำหรับอ่านข้อความด้วย EasyOCR
        """
        print("กำลังโหลด EasyOCR model...")
        try:
            # สร้าง EasyOCR reader สำหรับภาษาไทยและอังกฤษ
            self.ocr = easyocr.Reader(['th', 'en'])
            print("โหลด model สำเร็จ!")
        except Exception as e:
            print(f"ไม่สามารถโหลด model ได้: {e}")
            self.ocr = None
    
    def read_text_from_image(self, image_path):
        """
        อ่านข้อความจากไฟล์รูปภาพ
        
        Args:
            image_path (str): path ของไฟล์รูปภาพ
            
        Returns:
            str: ข้อความที่อ่านได้
        """
        if not self.ocr:
            return "Model ไม่พร้อมใช้งาน"
            
        try:
            # ตรวจสอบว่าไฟล์มีอยู่จริง
            if not os.path.exists(image_path):
                return f"ไม่พบไฟล์: {image_path}"
            
            # ใช้ EasyOCR อ่านข้อความ
            results = self.ocr.readtext(image_path)
            
            # รวมข้อความทั้งหมด
            text_list = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # ใช้เฉพาะข้อความที่มีความมั่นใจสูง
                    text_list.append(text)
            
            return '\n'.join(text_list) if text_list else "ไม่พบข้อความในรูปภาพ"
            
        except Exception as e:
            return f"เกิดข้อผิดพลาด: {str(e)}"
    
    def read_text_from_screenshot(self, x, y, width, height):
        """
        ถ่ายภาพหน้าจอแล้วอ่านข้อความ
        
        Args:
            x, y (int): ตำแหน่งเริ่มต้น
            width, height (int): ขนาดพื้นที่ที่ต้องการ
            
        Returns:
            str: ข้อความที่อ่านได้
        """
        if not self.ocr:
            return "Model ไม่พร้อมใช้งาน"
            
        try:
            import pyautogui
            
            # ถ่ายภาพหน้าจอ
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # แปลงเป็น numpy array
            screenshot_np = np.array(screenshot)
            
            # ใช้ EasyOCR อ่านข้อความ
            results = self.ocr.readtext(screenshot_np)
            
            # รวมข้อความทั้งหมด
            text_list = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # ใช้เฉพาะข้อความที่มีความมั่นใจสูง
                    text_list.append(text)
            
            return '\n'.join(text_list) if text_list else "ไม่พบข้อความในภาพ"
            
        except Exception as e:
            return f"เกิดข้อผิดพลาด: {str(e)}"
    
    def preprocess_image(self, image_path, output_path=None):
        """
        ปรับปรุงคุณภาพรูปภาพก่อนอ่านข้อความ
        
        Args:
            image_path (str): path ของไฟล์รูปภาพต้นฉบับ
            output_path (str): path สำหรับบันทึกรูปที่ปรับปรุงแล้ว
            
        Returns:
            str: path ของรูปที่ปรับปรุงแล้ว
        """
        try:
            # อ่านรูปภาพ
            image = cv2.imread(image_path)
            
            # แปลงเป็นสีเทา
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # ปรับความคมชัด
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # ลดสัญญาณรบกวน
            denoised = cv2.medianBlur(enhanced, 3)
            
            # เพิ่มความคมชัด
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            # กำหนด path สำหรับบันทึก
            if not output_path:
                name, ext = os.path.splitext(image_path)
                output_path = f"{name}_processed{ext}"
            
            # บันทึกรูปที่ปรับปรุงแล้ว
            cv2.imwrite(output_path, sharpened)
            
            return output_path
            
        except Exception as e:
            print(f"ไม่สามารถปรับปรุงรูปภาพได้: {e}")
            return image_path

def test_ocr():
    """
    ทดสอบการใช้งาน OCR
    """
    reader = TextReader()
    
    # ทดสอบกับรูปภาพในโฟลเดอร์ img
    test_images = ["img/test.jpg", "img/main.jpg", "img/temp.jpg"]
    
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\n=== ทดสอบกับ {image_path} ===")
            
            # อ่านข้อความจากรูปต้นฉบับ
            text = reader.read_text_from_image(image_path)
            print(f"ข้อความจากรูปต้นฉบับ:\n{text}")
            
            # ปรับปรุงรูปภาพแล้วอ่านใหม่
            processed_path = reader.preprocess_image(image_path)
            processed_text = reader.read_text_from_image(processed_path)
            print(f"\nข้อความจากรูปที่ปรับปรุงแล้ว:\n{processed_text}")
        else:
            print(f"ไม่พบไฟล์: {image_path}")

if __name__ == "__main__":
    test_ocr()