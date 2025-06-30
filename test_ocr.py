#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบการใช้งาน EasyOCR สำหรับอ่านข้อความจากรูปภาพ
"""

from read_text import TextReader
import os

def main():
    print("=== ทดสอบ EasyOCR ===")
    
    # สร้าง TextReader instance
    reader = TextReader()
    
    # ตรวจสอบไฟล์รูปภาพที่มีอยู่
    image_folder = "img"
    if os.path.exists(image_folder):
        print(f"\nกำลังตรวจสอบไฟล์ในโฟลเดอร์ {image_folder}...")
        
        # แสดงรายการไฟล์ในโฟลเดอร์
        files = os.listdir(image_folder)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))]
        
        print(f"พบไฟล์รูปภาพ {len(image_files)} ไฟล์:")
        for i, file in enumerate(image_files, 1):
            print(f"  {i}. {file}")
        
        # ทดสอบกับไฟล์แรก
        if image_files:
            test_file = os.path.join(image_folder, image_files[0])
            print(f"\n=== ทดสอบการอ่านข้อความจาก {test_file} ===")
            
            result = reader.read_text_from_image(test_file)
            print("ผลลัพธ์:")
            print(result)
            print("="*50)
        else:
            print("ไม่พบไฟล์รูปภาพในโฟลเดอร์")
    else:
        print(f"ไม่พบโฟลเดอร์ {image_folder}")
    
    # ทดสอบการถ่ายภาพหน้าจอ (สำหรับการทดสอบในอนาคต)
    print("\n=== การใช้งานการถ่ายภาพหน้าจอ ===")
    print("สำหรับการทดสอบการถ่ายภาพหน้าจอ ใช้คำสั่ง:")
    print("reader.read_text_from_screenshot(x=100, y=100, width=400, height=200)")

if __name__ == "__main__":
    main()
