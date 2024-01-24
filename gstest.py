from googlesearch import search

query = "What's the weather like in mumbai today?"
search_results = search(query, advanced=True)

for result in search_results:
    print("Title:", result.title)
    print("Description:", result.description)
    print()
