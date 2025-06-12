import re

# Нормализация текста: нижний регистр, замена 'ё'->'е',
# удаление/замена разделителей и лишних пробелов с помощью регулярных выражений.
def normalize_text(text):
    text = text.lower()
    text = text.replace('ё', 'е')
    separators_list = [
        '/', '\\', '.', ',', '-', '(', ')', ':', ';', '!', '"', "'", '[', ']', '{', '}', '<', '>',
        '@', '#', '$', '%', '^', '&', '*', '+', '=', '|', '~', '`'
    ]
    escaped = [re.escape(char) for char in separators_list]
    separators_pattern = f"[{''.join(escaped)}]"
    text = re.sub(separators_pattern, ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text