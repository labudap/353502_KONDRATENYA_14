import requests
from random import choice

def get_cat_fact():
    """
    Get a random cat fact from Cat Facts API
    """
    try:
        response = requests.get('https://catfact.ninja/fact')
        if response.status_code == 200:
            data = response.json()
            return data.get('fact')
    except Exception as e:
        print(f"Error fetching cat fact: {e}")
    return "Did you know that cats are amazing pharmacy assistants? They always know when it's time to take medicine!"

def get_activity():
    """
    Get a random dog image from Dog API
    """
    # List of backup activities in case API is not available
    backup_activities = [
        {
            'image_url': 'https://images.dog.ceo/breeds/retriever-golden/n02099601_1024.jpg',
            'type': 'Golden Retriever',
            'description': 'A friendly pharmacy assistant dog'
        },
        {
            'image_url': 'https://images.dog.ceo/breeds/husky/n02110185_1511.jpg',
            'type': 'Husky',
            'description': 'A loyal companion for health walks'
        }
    ]
    
    try:
        # Try the Dog API endpoint
        response = requests.get('https://dog.ceo/api/breeds/image/random', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                image_url = data.get('message', '')
                # Extract breed from URL
                breed = image_url.split('/breeds/')[1].split('/')[0].replace('-', ' ').title()
                return {
                    'image_url': image_url,
                    'type': breed,
                    'description': f'A lovely {breed} to brighten your day'
                }
            
    except Exception as e:
        print(f"Error fetching dog image: {e}")
    
    # Return a random backup activity if API fails
    return choice(backup_activities) 