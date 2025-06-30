import os
from typing import Optional, Dict, List
import json

class MultiTranslator:
    def __init__(self):
        """
        เริ่มต้นคลาสสำหรับแปลภาษาด้วยหลาย engine
        """
        self.available_engines = []
        self._init_engines()
    
    def _init_engines(self):
        """เริ่มต้น translation engines ที่มีอยู่"""
        
        # ลอง import googletrans
        try:
            from googletrans import Translator as GoogleTranslator
            self.google_translator = GoogleTranslator()
            self.available_engines.append('google')
            print("✅ Google Translator พร้อมใช้งาน")
        except ImportError:
            print("❌ Google Translator ไม่พร้อม (ติดตั้ง: pip install googletrans==4.0.0rc1)")
        
        # ลอง import deep-translator
        try:
            from deep_translator import GoogleTranslator as DeepGoogleTranslator
            self.deep_translator = DeepGoogleTranslator
            self.available_engines.append('deep')
            print("✅ Deep Translator พร้อมใช้งาน")
        except ImportError:
            print("❌ Deep Translator ไม่พร้อม (ติดตั้ง: pip install deep-translator)")
    
    def translate_with_google(self, text: str, dest_lang: str = 'en', src_lang: str = 'auto') -> Optional[str]:
        """
        แปลด้วย Google Translator (googletrans)
        
        Args:
            text: ข้อความที่ต้องการแปล
            dest_lang: ภาษาปลายทาง (en, th, ja, ko, zh, etc.)
            src_lang: ภาษาต้นทาง (auto = ตรวจจับอัตโนมัติ)
        """
        if 'google' not in self.available_engines:
            return None
        
        try:
            result = self.google_translator.translate(text, dest=dest_lang, src=src_lang)
            return result.text
        except Exception as e:
            print(f"Google Translator Error: {e}")
            return None
    
    def translate_with_deep(self, text: str, dest_lang: str = 'en', src_lang: str = 'auto') -> Optional[str]:
        """
        แปลด้วย Deep Translator
        
        Args:
            text: ข้อความที่ต้องการแปล
            dest_lang: ภาษาปลายทาง
            src_lang: ภาษาต้นทาง
        """
        if 'deep' not in self.available_engines:
            return None
        
        try:
            translator = self.deep_translator(source=src_lang, target=dest_lang)
            result = translator.translate(text)
            return result
        except Exception as e:
            print(f"Deep Translator Error: {e}")
            return None
    
    def translate(self, text: str, dest_lang: str = 'en', src_lang: str = 'auto', engine: str = 'auto') -> Dict:
        """
        แปลภาษาด้วย engine ที่เลือก
        
        Args:
            text: ข้อความที่ต้องการแปล
            dest_lang: ภาษาปลายทาง
            src_lang: ภาษาต้นทาง
            engine: เลือก engine ('google', 'deep', 'auto')
        
        Returns:
            Dict: ผลลัพธ์การแปล
        """
        if not text.strip():
            return {"error": "ข้อความว่าง"}
        
        results = {
            "original": text,
            "dest_lang": dest_lang,
            "src_lang": src_lang,
            "translations": {},
            "best_result": None
        }
        
        # ถ้าเลือก auto ให้ลองทุก engine
        if engine == 'auto':
            engines_to_try = self.available_engines
        else:
            engines_to_try = [engine] if engine in self.available_engines else []
        
        # ลองแปลด้วยแต่ละ engine
        for eng in engines_to_try:
            if eng == 'google':
                result = self.translate_with_google(text, dest_lang, src_lang)
            elif eng == 'deep':
                result = self.translate_with_deep(text, dest_lang, src_lang)
            else:
                continue
            
            if result:
                results["translations"][eng] = result
                if not results["best_result"]:
                    results["best_result"] = result
        
        return results
    
    def batch_translate(self, texts: List[str], dest_lang: str = 'en', src_lang: str = 'auto') -> List[Dict]:
        """
        แปลข้อความหลาย ๆ ข้อพร้อมกัน
        
        Args:
            texts: รายการข้อความที่ต้องการแปล
            dest_lang: ภาษาปลายทาง
            src_lang: ภาษาต้นทาง
        
        Returns:
            List[Dict]: ผลลัพธ์การแปลทั้งหมด
        """
        results = []
        for i, text in enumerate(texts):
            print(f"กำลังแปลข้อความที่ {i+1}/{len(texts)}")
            result = self.translate(text, dest_lang, src_lang)
            results.append(result)
        return results
    
    def get_supported_languages(self) -> Dict[str, List[str]]:
        """
        ดูภาษาที่รองรับ
        """
        common_languages = {
            "Popular": ["en", "th", "ja", "ko", "zh", "fr", "de", "es", "it", "ru"],
            "Asian": ["th", "ja", "ko", "zh-cn", "zh-tw", "vi", "id", "ms", "tl"],
            "European": ["en", "fr", "de", "es", "it", "pt", "ru", "pl", "nl", "sv"]
        }
        return common_languages
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        ตรวจจับภาษาของข้อความ
        """
        if 'google' in self.available_engines:
            try:
                result = self.google_translator.detect(text)
                return result.lang
            except:
                pass
        return None

def install_translators():
    """
    ติดตั้ง translation packages
    """
    packages = [
        "googletrans==4.0.0rc1",
        "deep-translator"
    ]
    
    import subprocess
    import sys
    
    for package in packages:
        try:
            print(f"กำลังติดตั้ง {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ ติดตั้ง {package} สำเร็จ!")
        except Exception as e:
            print(f"❌ ไม่สามารถติดตั้ง {package}: {e}")

def test_translator():
    """
    ทดสอบการใช้งาน translator
    """
    translator = MultiTranslator()
    
    if not translator.available_engines:
        print("ไม่มี translation engine ใช้งานได้")
        print("รันคำสั่ง: install_translators() เพื่อติดตั้ง")
        return
    
    # ทดสอบแปลภาษา
    test_texts = [
        "สวัสดีครับ วันนี้อากาศดีมาก",
        "Hello, how are you today?",
        "こんにちは、元気ですか？",
        "안녕하세요, 오늘 날씨가 좋네요"
    ]
    
    print("\n=== ทดสอบการแปลภาษา ===")
    
    for text in test_texts:
        print(f"\nต้นฉบับ: {text}")
        
        # ตรวจจับภาษา
        detected = translator.detect_language(text)
        if detected:
            print(f"ภาษาที่ตรวจพบ: {detected}")
        
        # แปลเป็นภาษาอังกฤษ
        result = translator.translate(text, dest_lang='en')
        if result['best_result']:
            print(f"แปลเป็นอังกฤษ: {result['best_result']}")
        
        # แปลเป็นภาษาไทย
        result = translator.translate(text, dest_lang='th')
        if result['best_result']:
            print(f"แปลเป็นไทย: {result['best_result']}")

# ฟังก์ชันทำงานง่าย ๆ
def quick_translate(text: str, to_lang: str = 'en', from_lang: str = 'auto') -> str:
    """
    ฟังก์ชันแปลภาษาแบบง่าย
    
    Args:
        text: ข้อความที่ต้องการแปล
        to_lang: ภาษาปลายทาง
        from_lang: ภาษาต้นทาง
    
    Returns:
        str: ข้อความที่แปลแล้ว
    """
    translator = MultiTranslator()
    result = translator.translate(text, to_lang, from_lang)
    return result.get('best_result', text)

if __name__ == "__main__":
    # ถ้ายังไม่ได้ติดตั้ง packages
    # install_translators()
    
    # ทดสอบการใช้งาน
    test_translator()