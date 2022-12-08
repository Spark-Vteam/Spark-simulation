"""
The Data class fetches data from the database through the API
"""
import json
from urllib.request import urlopen

class DataFetcher:
    """
    
    """
    def __init__(self, url):
        """
        
        """
        self.url = url

    def fetch(self, endpoint):
        """
        Fetch users, return dictionary
        """
        response = urlopen(self.url + endpoint)

        return json.load(response)[0]

    
