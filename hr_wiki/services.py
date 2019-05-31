def get_books(year, author):
    url = 'http://api.example.com/books' 
    params = {'year': year, 'author': author}
    r = requests.get(url, params=params)
    books = r.json()
    books_list = {'books':books['results']}
    return books_list