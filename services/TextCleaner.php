<?php

class TextCleaner {
    # Нормализация текста: нижний регистр, замена 'ё'->'е',
    # удаление/замена разделителей и лишних пробелов с помощью регулярных выражений.
    public static function normalize(string $text): string {
        $text = mb_strtolower($text, 'UTF-8');
        $text = str_replace('ё', 'е', $text);
        $separators = [
            '/', '\\', '.', ',', '-', '(', ')', ':', ';', '!', '"', "'", '[', ']', '{', '}',
            '<', '>', '@', '#', '$', '%', '^', '&', '*', '+', '=', '|', '~', '`'
        ];
        $escaped = array_map(function($char) {
            return preg_quote($char, '/');
        }, $separators);
        $pattern = '/[' . implode('', $escaped) . ']/u';
        $text = preg_replace($pattern, ' ', $text);
        $text = preg_replace('/\s+/', ' ', $text);
        return trim($text);
    }
}
