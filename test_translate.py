from translate import MultiTranslator, quick_translate

# วิธีง่าย
result = quick_translate("สวัสดีครับ", "en")
print(result)  # Hello

# วิธีละเอียด
translator = MultiTranslator()
result = translator.translate("Hello World", dest_lang="th")
print(result['best_result'])  # สวัสดีโลก