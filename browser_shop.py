import asyncio
import os
import requests
import json
from typing import List, Dict, Any

from pydantic import BaseModel, Field

from browser_use import Agent, Browser, ChatBrowserUse

# Set environment variable to handle Unicode properly
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = '1'

# Configure logging to avoid Unicode issues
import logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')

# Dedalus API configuration
DEDALUS_API_KEY = "YOUR_DEDALUS_API_KEY_HERE"
DEDALUS_BASE_URL = "https://api.dedalus.ai/v1"


class GroceryItem(BaseModel):
	"""A single grocery item"""

	name: str = Field(..., description='Item name')
	price: float = Field(..., description='Price as number')
	brand: str | None = Field(None, description='Brand name')
	size: str | None = Field(None, description='Size or quantity')
	url: str = Field(..., description='Full URL to item')


class GroceryCart(BaseModel):
	"""Grocery cart results"""

	items: list[GroceryItem] = Field(default_factory=list, description='All grocery items found')


def connect_to_dedalus_api():
	"""Test connection to Dedalus API"""
	try:
		headers = {
			"Authorization": f"Bearer {DEDALUS_API_KEY}",
			"Content-Type": "application/json"
		}
		
		# Test API connection
		response = requests.get(f"{DEDALUS_BASE_URL}/models", headers=headers, timeout=10)
		
		if response.status_code == 200:
			print("✅ Successfully connected to Dedalus API")
			return True
		else:
			print(f"❌ Dedalus API connection failed: {response.status_code}")
			return False
			
	except Exception as e:
		print(f"❌ Error connecting to Dedalus API: {e}")
		return False


def get_dedalus_shopping_plan(items: List[str]) -> Dict[str, Any]:
	"""Get shopping plan from Dedalus AI"""
	try:
		headers = {
			"Authorization": f"Bearer {DEDALUS_API_KEY}",
			"Content-Type": "application/json"
		}
		
		# Create shopping prompt for Dedalus
		prompt = f"""
		Create an optimized shopping plan for Instacart with these items: {', '.join(items)}
		
		Provide:
		1. Search strategy for each item
		2. Price optimization tips
		3. Cart management strategy
		4. Checkout optimization
		
		Format as JSON with sections: search_strategy, price_tips, cart_management, checkout_flow
		"""
		
		payload = {
			"model": "gpt-4",
			"messages": [
				{"role": "system", "content": "You are a shopping optimization expert for Instacart"},
				{"role": "user", "content": prompt}
			],
			"max_tokens": 1000,
			"temperature": 0.7
		}
		
		response = requests.post(
			f"{DEDALUS_BASE_URL}/chat/completions",
			headers=headers,
			json=payload,
			timeout=30
		)
		
		if response.status_code == 200:
			result = response.json()
			return {
				"success": True,
				"plan": result["choices"][0]["message"]["content"],
				"usage": result.get("usage", {})
			}
		else:
			return {
				"success": False,
				"error": f"API request failed: {response.status_code}",
				"response": response.text
			}
			
	except Exception as e:
		return {
			"success": False,
			"error": f"Exception: {str(e)}"
		}


def load_grocery_items():
	"""Load grocery items from the translated shopping list"""
	try:
		with open('grocery_list_english.txt', 'r', encoding='utf-8') as file:
			lines = file.readlines()
		
		items = []
		for line in lines:
			line = line.strip()
			if line and not line.startswith('Shopping List') and not line.startswith('Grocery'):
				# Extract item name (remove numbers and quantities)
				if '. ' in line:
					item = line.split('. ', 1)[1]  # Remove numbering
					if ' - ' in item:
						item = item.split(' - ')[0]  # Remove quantity
					if item and item not in ['', ' ']:
						items.append(item.strip())
		
		return items if items else ['milk', 'eggs', 'bread']
	except FileNotFoundError:
		print("grocery_list_english.txt not found. Using default items.")
		return ['milk', 'eggs', 'bread']

async def add_to_cart(items: list[str] = None):
	# Test Dedalus API connection first
	print("🔗 Testing Dedalus API connection...")
	if not connect_to_dedalus_api():
		print("⚠️  Dedalus API not available, proceeding with browser automation only")
	else:
		print("🤖 Getting AI shopping plan from Dedalus...")
		dedalus_plan = get_dedalus_shopping_plan(items)
		if dedalus_plan["success"]:
			print("✅ Dedalus AI shopping plan received:")
			print(dedalus_plan["plan"])
		else:
			print(f"❌ Dedalus plan failed: {dedalus_plan['error']}")

	browser = Browser()

	llm = ChatBrowserUse(api_key="YOUR_BROWSER_USE_API_KEY_HERE")

	# Task prompt
	task = f"""
    Search for "{items}" on Instacart, add to cart, and proceed to checkout with payment.

    Steps:
    1. Go to https://www.instacart.com/
    2. search for each item and add to cart:
       - Search for the item
       - Find the best match (closest name, lowest price)
       - Click on the product to view details
       - Click the "Add to cart" button
       - Clear search box/field
       - Continue to next item
    3. After adding all items, proceed to checkout:
       - Click on the cart icon
       - Review items in cart
       - Click "Checkout" or "Proceed to checkout"
    4. Go through checkout process:
       - Select delivery/pickup option
       - Proceed to payment section
       - Click "Add payment method" or "Add card"
       - Fill in card details (use test card: 4111 1111 1111 1111)
       - Add card to account

    IMPORTANT: 
    - You MUST login first before shopping
    - You MUST click the "Add to cart" button for each item
    - Complete the entire checkout process up to adding a payment card
    - Do not stop after adding items - continue to payment
    - Look for "Add to cart", "Checkout", "Add payment method" buttons
    - Clear the search box/field after adding each item

    Site:
    - Instacart: https://www.instacart.com/
    """

	# Create agent with structured output
	agent = Agent(
		browser=browser,
		llm=llm,
		task=task,
		output_model_schema=GroceryCart,
		instructions="You are a helpful shopping assistant for Instacart. You MUST: 1) Login first with the provided credentials, 2) Add each item to cart, 3) Clear the search after each item, 4) Proceed to checkout, 5) Go through payment setup, 6) Add a payment card. IMPORTANT: Login first, then clear the search box/field after adding each item to cart before searching for the next item. Do not stop until you reach the payment card addition step.",
	)

	# Run the agent with better error handling
	try:
		result = await agent.run()
		return result
	except Exception as e:
		print(f"Browser automation error: {e}")
		# Try to return a basic result structure
		from pydantic import BaseModel
		class ErrorResult(BaseModel):
			structured_output = None
			error = str(e)
		return ErrorResult()


if __name__ == '__main__':
	# Load grocery items from translated list
	items = load_grocery_items()
	print(f'Loaded {len(items)} items from shopping list:')
	for i, item in enumerate(items, 1):
		print(f'{i}. {item}')
	print()

	result = asyncio.run(add_to_cart(items))

	# Access structured output
	if result and result.structured_output:
		cart = result.structured_output

		print(f'\n{"=" * 60}')
		print('Items Added to Cart')
		print(f'{"=" * 60}\n')

		for item in cart.items:
			print(f'Name: {item.name}')
			print(f'Price: ${item.price}')
			if item.brand:
				print(f'Brand: {item.brand}')
			if item.size:
				print(f'Size: {item.size}')
			print(f'URL: {item.url}')
			print(f'{"-" * 60}')
