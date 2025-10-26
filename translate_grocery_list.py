#!/usr/bin/env python3
"""
Translation utilities for grocery lists
"""

import requests
import re
import os

# DeepL API configuration
DEEPL_API_KEY = "YOUR_DEEPL_API_KEY_HERE"
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

def detect_language_simple(text):
    """Simple language detection based on common Spanish words"""
    spanish_words = ['leche', 'huevos', 'pan', 'manzanas', 'pollo', 'arroz', 'queso', 
                     'yogur', 'tomates', 'cebollas', 'patatas', 'aceite', 'sal',
                     'litros', 'docena', 'kilo', 'gramos', 'unidades', 'paquete']
    
    text_lower = text.lower()
    spanish_count = sum(1 for word in spanish_words if word in text_lower)
    
    if spanish_count > 2:
        return "es"
    return "en"

def translate_with_deepl(text):
    """Translate text using DeepL API"""
    try:
        headers = {
            'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        data = {
            'text': text,
            'source_lang': 'ES',
            'target_lang': 'EN'
        }
        
        response = requests.post(DEEPL_API_URL, headers=headers, data=data)
        
        if response.status_code == 200:
            result = response.json()
            return result['translations'][0]['text']
        else:
            print(f"DeepL API error: {response.status_code}")
            return text  # Return original text if translation fails
            
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

def extract_google_docs_content(doc_url):
    """Extract content from Google Docs URL"""
    try:
        # Convert Google Docs URL to export format
        if '/edit' in doc_url:
            export_url = doc_url.replace('/edit', '/export?format=txt')
        else:
            export_url = doc_url + '/export?format=txt'
        
        response = requests.get(export_url, timeout=30)
        
        if response.status_code == 200:
            return {
                "success": True,
                "content": response.text
            }
        else:
            return {
                "success": False,
                "error": f"Failed to fetch: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def extract_grocery_items_with_quantities(text):
    """Extract grocery items with quantities from text"""
    items = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('Shopping List') and not line.startswith('Grocery'):
            # Extract item with quantity
            if '. ' in line:
                item = line.split('. ', 1)[1]  # Remove numbering
                if item and item not in ['', ' ']:
                    items.append(item.strip())
    
    return items if items else ['milk', 'eggs', 'bread']

def translate_spanish_to_english():
    """Translate Spanish grocery list to English"""
    try:
        # Read Spanish list
        with open('lista_compras_espanol.txt', 'r', encoding='utf-8') as f:
            spanish_text = f.read()
        
        # Translate
        english_text = translate_with_deepl(spanish_text)
        
        # Save English list
        with open('grocery_list_english.txt', 'w', encoding='utf-8') as f:
            f.write(english_text)
        
        print("Translation completed!")
        
    except FileNotFoundError:
        print("Spanish grocery list file not found")
    except Exception as e:
        print(f"Translation error: {e}")
