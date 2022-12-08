import random
import json
from urllib.request import urlopen

url = "http://localhost:4000/bike"
response = urlopen(url)
bikes = json.load(response)[0]

for n in range(0,9000):
    print(bikes[n])
