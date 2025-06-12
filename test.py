import csv
import requests
import time
import json
import os
import math
import re

INPUT_FILE = 'result.csv'
OUTPUT_FILE = 'result_updated_new.csv'
CACHE_FILE = 'cache.json'
URL = "http://192.168.1.7:8002/weight"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def clean_product_name(name: str) -> str:
    name = re.sub(r"\b[A-Z0-9\-]{2,}\b", "", name, flags=re.IGNORECASE)
    name = re.sub(r"[^\w\sА-Яа-яЁё]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip().upper()

def query_weight(product_name):
    try:
        response = requests.post(URL, data={"product_name": product_name})
        response.raise_for_status()
        data = response.json()
        weight = data.get("weight")
        if isinstance(weight, (int, float)):
            return math.ceil(weight), data
        return None, data
    except Exception as e:
        print(f"Error processing '{product_name}': {e}")
        return None, None

def process_file():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Начало обработки файла: {start_time}")

    cache = load_cache()

    with open(INPUT_FILE, encoding='utf-8') as f:
        total = sum(1 for _ in f)

    with open(INPUT_FILE, newline='', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for i, row in enumerate(reader, 1):
            if len(row) < 5:
                writer.writerow(row)
                continue

            original_name = row[4]
            cleaned_name = clean_product_name(original_name)

            if not cleaned_name:
                weight = 200
            elif cleaned_name in cache:
                weight = cache[cleaned_name]
            else:
                weight, data = query_weight(cleaned_name)
                if weight and weight > 0:
                    cache[cleaned_name] = weight
                    save_cache(cache)
                else:
                    print(f"Warning: {cleaned_name}': {data}")
                    weight = 200

            new_row = row[:]
            new_row[0] = str(weight)

            writer.writerow(new_row)
            outfile.flush()

            percent = (i / total) * 100
            print(f"Обработано {i}/{total} ({percent:.2f}%)", end='\r')

    end_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nОбработка завершена: {end_time}")
    print(f"Результат записан в {OUTPUT_FILE}")

if __name__ == "__main__":
    process_file()
