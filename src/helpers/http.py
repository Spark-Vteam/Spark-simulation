"""
The Data class fetches data from the database through the API
"""
import json
import requests
from urllib.request import urlopen

class Http:
    """
    
    """
    def __init__(self, url):
        """
        
        """
        self.url = url

    def get(self, endpoint):
        """
        Fetch users, return dictionary
        """
        response = urlopen(self.url + endpoint, headers={'key': '18c364b7-641e-440e-849a-20a3c67036a1'})

        return json.load(response)["data"]

    def create_rent(self, user, bike):
        """
        Create a rent through the API
        """
        #
        requests.post(f"{self.url}/rent/create/{user}", data={"bikeId": bike}, headers={'key': '18c364b7-641e-440e-849a-20a3c67036a1'})

    def get_rent(self, user):
        """
        Get a rent id based on user id 
        """
        response = requests.get(f"{self.url}/rent/active/{user}", headers={'key': '18c364b7-641e-440e-849a-20a3c67036a1'})
        return response.json()["data"][0]["id"]

    def end_rent(self, user):
        """
        End a rent through the API
        """
        requests.put(f"{self.url}/rent/{self.get_rent(user)}", headers={'key': '18c364b7-641e-440e-849a-20a3c67036a1'})
        

    
