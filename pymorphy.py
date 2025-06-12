import json
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def extract_nouns(text):
    parts = text.split(' и ')
    nouns = []
    for part in parts:
        words = part.split()
        for word in words:
            parses = morph.parse(word)
            nomn_parses = [p for p in parses if p.tag.POS == 'NOUN' and 'nomn' in p.tag and p.is_known]
            if nomn_parses:
                best = nomn_parses[0]
                noun = best.normal_form.lower().replace('ё', 'е') # нормализация словаря к условному Е вместо Ё
                nouns.append(noun)
                break
    return nouns

with open('cache.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = {}

for phrase, value in data.items():
    nouns = extract_nouns(phrase)
    for noun in nouns:
        new_data[noun] = value

with open('cache.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)
