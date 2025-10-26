#!/usr/bin/env python3
"""
Google Docs Shopping System - Final Version
Works with Google Docs URLs and provides fallback to sample data
"""

import asyncio
import os
import sys

# Set environment variable to handle Unicode properly
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = '1'

# Configure logging to reduce Unicode issues
import logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')

async def run_google_docs_shopping_final():
    """Run the final Google Docs shopping system"""
    
    print("=" * 60)
    print("GOOGLE DOCS SHOPPING SYSTEM")
    print("=" * 60)
    print("Fetches grocery lists from Google Docs + Target shopping")
    print("=" * 60)
    
    # Step 1: Process Google Docs or use sample data
    print("\n1. GOOGLE DOCS PROCESSING")
    print("-" * 30)
    
    try:
        from translate_grocery_list import detect_language_simple, extract_google_docs_content
        
        # Your Google Docs URL
        doc_url = "YOUR_GOOGLE_DOCS_URL_HERE"
        
        print(f"Fetching content from Google Docs: {doc_url}")
        
        # Fetch content from Google Docs
        content_result = extract_google_docs_content(doc_url)
        
        if not content_result["success"]:
            print(f"ERROR: Failed to fetch from Google Docs: {content_result['error']}")
            print("Falling back to sample data...")
            
            # Fallback to sample content
            sample_content = """Lista de Compras - Supermercado

1. Leche - 2 litros
2. Huevos - 1 docena
3. Pan - 2 barras
4. Manzanas - 1 kilo
5. Pollo - 1 kilo
6. Arroz - 1 paquete
7. Queso - 200 gramos"""
            content = sample_content
        else:
            content = content_result["content"]
            print(f"SUCCESS: Fetched {len(content)} characters from Google Docs")
        
        # Detect language and translate
        language = detect_language_simple(content)
        print(f"Detected language: {language}")
        
        if language != "en":
            print("Translating using DeepL API...")
            from translate_grocery_list import translate_with_deepl
            translated_content = translate_with_deepl(content)
            print("Translated to English using DeepL")
        else:
            translated_content = content
            print("Already in English")
        
        # Extract items with quantities
        from translate_grocery_list import extract_grocery_items_with_quantities
        items = extract_grocery_items_with_quantities(translated_content)
        print(f"Extracted {len(items)} items with quantities: {items}")
        
        # Save files
        with open('grocery_list_english.txt', 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        with open('shopping_items.txt', 'w', encoding='utf-8') as f:
            for item in items:
                f.write(item + '\n')
        
        print("SUCCESS: Google Docs processing completed!")
        
    except Exception as e:
        print(f"ERROR: Google Docs processing failed: {e}")
        # Fallback to existing system
        print("Using fallback translation system...")
        from translate_grocery_list import translate_spanish_to_english
        translate_spanish_to_english()
        from browser_shop import load_grocery_items
        items = load_grocery_items()
    
    # Step 2: Load Items
    print("\n2. ITEM LOADING")
    print("-" * 30)
    try:
        if 'items' not in locals():
            from browser_shop import load_grocery_items
            items = load_grocery_items()
        
        print(f"SUCCESS: Loaded {len(items)} items")
        print(f"Items: {items}")
    except Exception as e:
        print(f"ERROR: Item loading failed: {e}")
        return
    
    # Step 3: Browser Automation
    print("\n3. BROWSER AUTOMATION")
    print("-" * 30)
    print("This will open a browser window for Instacart shopping")
    print("The system will:")
    print("- Navigate to Instacart.com")
    print("- Login with credentials")
    print("- Search for each item")
    print("- Add items to cart")
    print("- Proceed to checkout")
    
    print("\nStarting browser automation...")
    
    print("\n" + "=" * 60)
    print("SHOPPING LIST READY FOR MANUAL SHOPPING")
    print("=" * 60)
    print("Your translated grocery list with quantities:")
    print("-" * 40)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    print("-" * 40)
    print(f"Total items: {len(items)}")
    print("=" * 60)
    print("You can now manually shop on Instacart with this list!")
    print("=" * 60)
    
    # Optional: Try browser automation (but don't fail if it doesn't work)
    try:
        print("\nAttempting browser automation...")
        from browser_shop import add_to_cart
        result = await add_to_cart(items)
        
        if result and result.structured_output:
            cart = result.structured_output
            print(f"\nSUCCESS: Browser automation completed!")
            print("=" * 60)
            print("SHOPPING RESULTS")
            print("=" * 60)
            
            total_price = 0
            for item in cart.items:
                print(f"Item: {item.name}")
                print(f"Price: ${item.price}")
                if item.brand:
                    print(f"Brand: {item.brand}")
                if item.size:
                    print(f"Size: {item.size}")
                print(f"URL: {item.url}")
                print("-" * 40)
                total_price += item.price
            
            print(f"TOTAL: ${total_price:.2f}")
            print("=" * 60)
        else:
            print("Browser automation had issues, but your shopping list is ready!")
            
    except Exception as e:
        print(f"Browser automation encountered issues: {e}")
        print("Your shopping list is still ready for manual use!")
    
    print("\n" + "=" * 60)
    print("GOOGLE DOCS SHOPPING SYSTEM COMPLETE")
    print("=" * 60)

def main():
    """Main function"""
    try:
        asyncio.run(run_google_docs_shopping_final())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"\nSystem error: {e}")

if __name__ == "__main__":
    main()
