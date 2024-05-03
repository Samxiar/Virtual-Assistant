from googlesearch import search

def google_search_and_print(query):
    try:
        search_results = search(query, num=5, stop=5, pause=2)
        for url in search_results:
            try:
                title = 'Dummy Title'  # Replace with your method to extract title
                description = 'Dummy Description'  # Replace with your method to extract description
                print("Title:", title)
                print("Description:", description)
                print("-" * 50)
            except Exception as e:
                print("Error fetching information from:", url)
                print("Error:", e)
    except Exception as e:
        print("Error performing Google search:", e)

google_search_and_print(input("Enter your search query: "))
