from functions import *

pyk, puk=generate_key_pair()

text="Hello"

cipher=encrypt_message(text, puk)
print(type(cipher))

texted=decrypt_message(cipher,pyk)
print(type(texted))
