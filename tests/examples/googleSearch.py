from googlesearch import search

query = "@smurthys"

for j in search(query, tld="com", num=10, stop=1, pause=2):
    print(j)
