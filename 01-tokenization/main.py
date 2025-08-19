import tiktoken

enc =tiktoken.encoding_for_model("gpt-4o")

text ="Hey I am Akash Malhotra"
token = enc.encode(text)
print("Tokens:",token)

decoded =enc.decode(token)
print("Decoded token:",decoded)
