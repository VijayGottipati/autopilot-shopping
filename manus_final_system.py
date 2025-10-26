#!/usr/bin/env python3
"""
Manus Final System - Ready for Production
Creates a task in Manus to fetch data from Notion, then polls for completion
"""

import requests
import json
import time
import os

# Set environment variable to handle Unicode properly
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Manus API configuration
# IMPORTANT: Replace with your actual valid Manus API key
MANUS_API_KEY = "YOUR_MANUS_API_KEY_HERE"
MANUS_BASE_URL = "https://api.manus.ai/v1"

def create_manus_task():
    """Create a task in Manus to fetch data from Notion"""
    
    headers = {
        "Authorization": f"Bearer {MANUS_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Task payload for fetching from Notion
    task_payload = {
        "name": "Fetch Notion Grocery List",
        "description": "Fetch grocery list data from Notion database",
        "type": "data_fetch",
        "source": "notion",
        "parameters": {
            "database_id": "your_notion_database_id",  # Replace with your actual Notion database ID
            "notion_token": "your_notion_integration_token",  # Replace with your Notion token
            "fields": ["Item", "Quantity", "Category", "Notes"],
            "filter": {
                "property": "Status",
                "select": {
                    "equals": "Active"
                }
            }
        },
        "priority": "high",
        "timeout": 300
    }
    
    try:
        print("Creating Manus task for Notion data fetch...")
        
        response = requests.post(
            f"{MANUS_BASE_URL}/tasks",
            headers=headers,
            json=task_payload,
            timeout=30
        )
        
        if response.status_code == 201:
            task_data = response.json()
            task_id = task_data.get('id')
            print(f"SUCCESS: Task created! Task ID: {task_id}")
            return task_id
        else:
            print(f"ERROR: Failed to create task: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"ERROR: Error creating Manus task: {e}")
        return None

def check_task_status(task_id):
    """Check if the Manus task is finished"""
    
    headers = {
        "Authorization": f"Bearer {MANUS_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{MANUS_BASE_URL}/tasks/{task_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            task_data = response.json()
            status = task_data.get('status')
            print(f"Task status: {status}")
            return status, task_data
        else:
            print(f"ERROR: Failed to check task status: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"ERROR: Error checking task status: {e}")
        return None, None

def fetch_task_result(task_id):
    """Fetch the result data from the completed Manus task"""
    
    headers = {
        "Authorization": f"Bearer {MANUS_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{MANUS_BASE_URL}/tasks/{task_id}/result",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result_data = response.json()
            print("SUCCESS: Successfully fetched task result!")
            return result_data
        else:
            print(f"ERROR: Failed to fetch task result: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"ERROR: Error fetching task result: {e}")
        return None

def poll_task_completion(task_id, max_attempts=30, poll_interval=10):
    """Poll the task until completion"""
    
    print(f"Polling task {task_id} for completion...")
    print(f"Max attempts: {max_attempts}, Poll interval: {poll_interval}s")
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n--- Attempt {attempt}/{max_attempts} ---")
        
        status, task_data = check_task_status(task_id)
        
        if status is None:
            print("ERROR: Failed to get task status")
            return None
        
        if status == "completed":
            print("SUCCESS: Task completed successfully!")
            return task_data
        elif status == "failed":
            print("ERROR: Task failed")
            return None
        elif status in ["pending", "running", "processing"]:
            print(f"WAITING: Task is {status}, waiting...")
            if attempt < max_attempts:
                print(f"Waiting {poll_interval} seconds before next check...")
                time.sleep(poll_interval)
        else:
            print(f"WARNING: Unknown status: {status}")
            if attempt < max_attempts:
                print(f"Waiting {poll_interval} seconds before next check...")
                time.sleep(poll_interval)
    
    print(f"TIMEOUT: Task did not complete within {max_attempts * poll_interval} seconds")
    return None

def process_notion_data(notion_data):
    """Process the fetched Notion data into a shopping list"""
    
    if not notion_data:
        print("ERROR: No data to process")
        return []
    
    print("Processing Notion data...")
    
    # Extract items from Notion data
    items = []
    
    # Handle different possible data structures from Notion
    if 'results' in notion_data:
        # Standard Notion API response
        for item in notion_data['results']:
            properties = item.get('properties', {})
            
            # Extract item name
            item_name = ""
            if 'Item' in properties:
                item_name = properties['Item'].get('title', [{}])[0].get('text', {}).get('content', '')
            elif 'Name' in properties:
                item_name = properties['Name'].get('title', [{}])[0].get('text', {}).get('content', '')
            
            # Extract quantity
            quantity = ""
            if 'Quantity' in properties:
                quantity = properties['Quantity'].get('rich_text', [{}])[0].get('text', {}).get('content', '')
            elif 'Amount' in properties:
                quantity = properties['Amount'].get('rich_text', [{}])[0].get('text', {}).get('content', '')
            
            if item_name:
                if quantity:
                    items.append(f"{item_name} - {quantity}")
                else:
                    items.append(item_name)
    
    elif isinstance(notion_data, list):
        # Direct list of items
        items = notion_data
    
    else:
        # Try to extract items from other formats
        print("WARNING: Unknown data format, attempting to extract items...")
        # Add custom extraction logic here based on your Notion structure
    
    print(f"Extracted {len(items)} items from Notion:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    
    return items

def save_shopping_list(items):
    """Save the processed shopping list to files"""
    
    if not items:
        print("ERROR: No items to save")
        return
    
    # Save to grocery list file
    with open('grocery_list_english.txt', 'w', encoding='utf-8') as f:
        f.write("Shopping List - Notion\n\n")
        for i, item in enumerate(items, 1):
            f.write(f"{i}. {item}\n")
    
    # Save to shopping items file
    with open('shopping_items.txt', 'w', encoding='utf-8') as f:
        for item in items:
            f.write(item + '\n')
    
    print("SUCCESS: Shopping list saved to files:")
    print("  - grocery_list_english.txt")
    print("  - shopping_items.txt")

def main():
    """Main function to run the Manus Notion fetcher"""
    
    print("=" * 60)
    print("MANUS NOTION DATA FETCHER")
    print("=" * 60)
    print("This will create a Manus task to fetch data from Notion")
    print("and poll for completion.")
    print("=" * 60)
    print("IMPORTANT: Make sure you have:")
    print("1. A valid Manus API key")
    print("2. A Notion database ID")
    print("3. A Notion integration token")
    print("=" * 60)
    
    # Step 1: Create Manus task
    print("\n1. CREATING MANUS TASK")
    print("-" * 30)
    task_id = create_manus_task()
    
    if not task_id:
        print("ERROR: Failed to create Manus task. Exiting.")
        print("Please check your Manus API key and try again.")
        return
    
    # Step 2: Poll for completion
    print("\n2. POLLING FOR COMPLETION")
    print("-" * 30)
    completed_task = poll_task_completion(task_id)
    
    if not completed_task:
        print("ERROR: Task did not complete successfully. Exiting.")
        return
    
    # Step 3: Fetch result data
    print("\n3. FETCHING RESULT DATA")
    print("-" * 30)
    result_data = fetch_task_result(task_id)
    
    if not result_data:
        print("ERROR: Failed to fetch result data. Exiting.")
        return
    
    # Step 4: Process the data
    print("\n4. PROCESSING NOTION DATA")
    print("-" * 30)
    items = process_notion_data(result_data)
    
    # Step 5: Save shopping list
    print("\n5. SAVING SHOPPING LIST")
    print("-" * 30)
    save_shopping_list(items)
    
    print("\n" + "=" * 60)
    print("MANUS NOTION FETCHER COMPLETE")
    print("=" * 60)
    print(f"Successfully processed {len(items)} items from Notion!")
    print("=" * 60)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("Now you can run the shopping system with the fetched data:")
    print("python google_docs_shopping_final.py")
    print("=" * 60)

if __name__ == "__main__":
    main()

