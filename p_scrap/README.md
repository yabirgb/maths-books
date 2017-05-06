# Info

This python scripts collects the ID of amazon books from the database and calls the Amazon Product Api to collect basic info about books.
Once the info is downloaded the merge scripts combines the multiple files in one single json.

I decided to make a json file for every success request to avoid overuse of memory and as an easy retrieval of the data in case something went wrong.
