from .client import Client

c = Client()

auth = c.connect()

print(auth)
