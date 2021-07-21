# from .encrypt import encrypt

# message = "Hello World"
# encrypted_message = encrypt(message=message, padding_scheme="PKCS1")
# print(encrypted_message)
# encrypted_message = encrypt(message=message)
# print(encrypted_message)

from xml.etree import ElementTree as ET

from .input import auth_data

x = ET.fromstring(auth_data)

ET.dump(x)
