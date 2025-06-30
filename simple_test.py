import easyocr
import os

# ทดสอบ EasyOCR
print("กำลังโหลด EasyOCR...")
reader = easyocr.Reader(['th', 'en'])
print("โหลดสำเร็จ!")

# ตรวจสอบไฟล์ในโฟลเดอร์ img
img_folder = "img"
if os.path.exists(img_folder):
    files = os.listdir(img_folder)
    print(f"ไฟล์ในโฟลเดอร์ {img_folder}: {files}")
    
    # ทดสอบกับไฟล์แรกที่เป็นรูปภาพ
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    if image_files:
        test_file = os.path.join(img_folder, image_files[0])
        print(f"ทดสอบกับไฟล์: {test_file}")
        
        try:
            results = reader.readtext(test_file)
            print("ผลลัพธ์:")
            for (bbox, text, confidence) in results:
                if confidence > 0.5:
                    print(f"ข้อความ: {text} (ความมั่นใจ: {confidence:.2f})")
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
    else:
        print("ไม่พบไฟล์รูปภาพ")
else:
    print("ไม่พบโฟลเดอร์ img")
