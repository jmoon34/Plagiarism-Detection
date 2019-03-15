from googlesearch import search

query = "Geeksforgeeks"

for i in search(query, tld='com', lang='en', num=10, stop=2, pause=2):
    print(i)
