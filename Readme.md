# Sinhala Search Engine - Sri Lankan Actors/Actresses
Sri Lankan Actors/Actresses search engine using Sinhala language. The search engine presents following functions.
- Search acted movies by actor/actress - දමිතා අබේරත්න රංගනය කල නාට්ය
- Search bio by actor/actress name - දමිතා අබේරත්නගේ විස්තර
- Search career info by actor/actress name - දමිතා අබේරත්නගේ වෘත්තීය දිවිය
- Search awards by player name - දමිතා අබේරත්නගේ සම්මාන
- Search actresses by movies - මීහරකා චිත්රපටයේ නිළියන්
- Search actresses by awards - හොඳම නිළිය සම්මානය ලබාගත් නිළියන්
- Search actors by awards - හොඳම නළුවා සම්මානය ලබාගත් නළුවන්
- Search actors by movies - සඳ මඩල චිත්රපටයේ නළුවන්
- Search actors/actress by movies - සඳ මඩල චිත්රපටයේ නළුනිළියන්

## Quickstart
- Start an ElasticSearch Instance on the port 9200
- Run data_upload.py file to create index
- Run command flask run to start the application
- App will start on http://127.0.0.1:5000/
- Visit http://127.0.0.1:5000/ and search by entering relevant queries in Sinhala language

## Directory Structure
- /corpus - Contains the scrapped actor data set
- /templates - Contains the User interface templates
- web_scraper.py - Contains the code used to scrape the web
- data_upload.py - Contains code to create the index
- preprocessor.py - Contains the logic of the search engine
- app.py - Contains the code to run flask server

## Corpus
Actor/Actress data along with the metadata was scraped from [Wikipedia](https://en.wikipedia.org/wiki/List_of_Sri_Lankan_actors). The corpus consists of following data fields for each actor/actress.
- Name - Name of the Actor/ Actress
- Career - Career information 
- Bio - Personal life or biography
- Films - Acted films
- Awards - Received awards
- Dob - Date of birth
- Gender - Gender of the person
- Active_years - Years which he or she acted
- Vital_status - Vital status of the person

_Name, Career, Bio, Films and Awards were translated to Sinhala_


## Additional Features
- Intent Classification - Query intention is found by intent classification
- Query Preprocessing - According to the intent queries are pre processed
- Synonyms support for certain words related to cinema industry -  වෘත්තීය දිවිය, සිනමා ජීවිතය
- Simple spelling errors are supported - නිළියන්, නිලියන්





