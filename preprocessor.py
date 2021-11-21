import re

# supported query types

# 1. Search acted movies by actor/actress - දමිතා අබේරත්න රංගනය කල නාට්ය
# 2. Search bio by actor/actress name - දමිතා අබේරත්නගේ විස්තර
# 3. Search career info by actor/actress name - දමිතා අබේරත්නගේ වෘත්තීය දිවිය
# 4. Search awards by player name - දමිතා අබේ රත්නගේ සම්මාන
# 5. Search actresses by movies - මීහරකා චිත්රපටයේ නිළියන්
# 6. Search actresses by awards - හොඳම නිළිය සම්මානය ලබාගත් නිළියන්
# 7. Search actors by awards - හොඳම නළුවා සම්මානය ලබාගත් නළුවන්
# 8. Search actors by movies - සඳ මඩල චිත්රපටයේ නළුවන්
# 9. Search actors/actress by movies - සඳ මඩල චිත්රපටයේ නළුනිළියන්


'''classifies the intent of the query
   Identifies best intent using similar words and misspelled words to a certain extent'''


def intent_classifier(query):
    # available fields
    name = "name"
    career = "career"
    bio = "bio"
    films = "films.name"
    awards = "awards.name"
    dob = "dob"
    gender = "gender"
    vital_status = "vital_status"
    active_years = "active_years"

    selected_fields = []

    # 1. Search acted movies by actor/actress - දමිතා අබේරත්න රංගනය කල නාට්ය
    movies_by_actor = [["රංගනය"], ["නාට්ය", "නාට්\u200dය", "චිත්රපට"]]
    # 2. Search bio by actor/actress name - දමිතා අබේරත්නගේ විස්තර
    actor_bio = [["විස්තර", "ජීවිතය"]]
    # 3. Search career info by actor/actress name - දමිතා අබේරත්නගේ වෘත්තීය දිවිය
    actor_career = [["වෘත්තීය"], ["රංගනය", "රංගන", "සිනමා"], ["දිවිය", "ජීවිතය"]]
    # 4. Search awards by player name - දමිතා අබේරත්නගේ සම්මාන
    actor_awards = [["සම්මාන"]]
    # 5. Search actresses by movie - මීහරකා චිත්රපටයේ නිළියන්
    actresses_by_movie = [["නිලියන්", "නිළියන්"], "චිත්රපටයේ"]
    # 6. Search actresses by awards - හොඳම නිළිය සම්මානය ලබාගත් නිළියන්
    actresses_by_awards = [["සම්මාන", "සම්මානය"], ["නිලියන්", "නිළියන්"], ["ලබාගත්", "ලැබූ", "ලැබු"]]
    # 7. Search actors by awards - හොඳම නළුවා සම්මානය ලබාගත් නළුවන්
    actors_by_awards = [["සම්මාන", "සම්මානය"], ["නළුවන්", "නලුවන්"], ["ලබාගත්", "ලැබූ", "ලැබු"]]
    # 8. Search actors by movie - සඳ මඩල චිත්රපටයේ නළුවන්
    actors_by_movie = [["නළුවන්", "නලුවන්"], "චිත්රපටයේ"]
    # 9. Search actors/actresses by movie - සඳ මඩල චිත්රපටයේ නළුනිළියන්
    both_by_movie = [["නළු නිළියන්", "නළුනිළියන්"], "චිත්රපටයේ"]

    list_classifier = [actor_bio, actor_awards, movies_by_actor, actor_career, actors_by_movie, actors_by_awards,
                       actresses_by_movie, actresses_by_awards, both_by_movie]
    intent_names = ["actor_bio", "actor_awards", "movies_by_actor", "actor_career", "actors_by_movie",
                    "actors_by_awards", "actresses_by_movie", "actresses_by_awards", "both_by_movie"]

    # calculate intent scores
    score_list = []
    for index, classifier in enumerate(list_classifier):
        score = 0
        for word_list in classifier:
            for word in word_list:
                if word in query.strip().split():
                    score += 1
                    break
        score_list.append(score)

    print('SCORE LIST', score_list)
    selected_intent = intent_names[score_list.index(max(score_list))]
    if len(set(score_list)) == 1 and (0 in set(score_list)):
        selected_intent = ""
    print(query, ' SELECTED INTENT - ', selected_intent)
    if selected_intent == "actor_bio":
        selected_fields = [name, bio]
    elif selected_intent == "actor_awards":
        selected_fields = [name, awards, career]
    elif selected_intent == "movies_by_actor":
        selected_fields = [name, films, awards, career]
    elif selected_intent == "actor_career":
        selected_fields = [name, career]
    elif selected_intent == "actors_by_movie":
        selected_fields = [films, awards, gender]
    elif selected_intent == "actors_by_awards":
        selected_fields = [awards, gender]
    elif selected_intent == "actresses_by_movie":
        selected_fields = [films, awards, gender]
    elif selected_intent == "actresses_by_awards":
        selected_fields = [awards, gender]
    elif selected_intent == "both_by_movie":
        selected_fields = [films, awards]
    #     fill remaining selected intents
    else:
        selected_fields = [name, bio, career, films, awards, dob, gender, vital_status, active_years]

    gender_based_query = False
    gender_query = ""

    intent_dic = {
        "actors_by_movie": "පිරිමි",
        "actors_by_awards": "පිරිමි",
        "actresses_by_movie": "ගැහැණු",
        "actresses_by_awards": "ගැහැණු"
    }

    if selected_intent in intent_dic.keys():
        gender_based_query = True
        gender_query = intent_dic[selected_intent]

    return selected_intent, selected_fields, gender_based_query, gender_query


'''lemmatize single words'''


def lemmatizer(word):
    if re.search(".*යේ$", word):
        return word.removesuffix('යේ')
    elif re.search(".*ගේ$", word):
        return word.removesuffix('ගේ')
    elif re.search(".*න්$", word):
        return word.removesuffix('න්')
    else:
        return word


'''Process queries'''


def query_preprocessor(selected_intent, query):
    # words to remove - කල ලබාගත් ලැබූ ලැබු
    drop_list = ["කල", "ලබාගත්", "ලැබූ", "ලැබු", "චිත්රපටයේ"]

    query_splitted = query.strip().split()
    remaining_words = []

    for word in query_splitted:
        if word not in drop_list:
            # lemmatize the word
            remaining_words.append(lemmatizer(word.strip()))


    return " ".join(remaining_words)

# queries = ["දමිතා අබේරත්න රංගනය කල නාට්ය", "දමිතා අබේරත්නගේ විස්තර", "දමිතා අබේරත්නගේ වෘත්තීය දිවිය",
#            "දමිතා අබේරත්නගේ සම්මාන", "මීහරකා චිත්රපටයේ නිළියන්", "හොඳම නිළිය සම්මානය ලබාගත් නිළියන්",
#            "හොඳම නළුවා සම්මානය ලබාගත් නළුවන්", "සඳ මඩල චිත්රපටයේ නළුවන්", "සඳ මඩල චිත්රපටයේ නළුනිළියන්"]
#
