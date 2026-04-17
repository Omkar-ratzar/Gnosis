from app.services.search_service import search_query

while(True):

    query=input("Enter your query, Enter 0 for exit")
    if(query=="0"):
        break
    results = search_query(query=query)
    for r in results:
        print(r)
