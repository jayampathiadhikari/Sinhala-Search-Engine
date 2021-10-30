import re


# query types

# 1. Search acted movies by actor/actress - දමිතා අබේරත්න රංගනය කල නාට්ය
# 2. Search bio by actor/actress name - දමිතා අබේරත්නගේ විස්තර
# 3. Search career info by actor/actress name - දමිතා අබේරත්නගේ වෘත්තීය දිවිය
# 4. Search awards by player name - දමිතා අබේ රත්නගේ සම්මාන
# 5. Search actresses by movies - මීහරකා චිත්රපටයේ නිළියන්
# 6. Search actresses by awards - හොඳම නිළිය සම්මානය ලබාගත් නිළියන්
# 7. Search actors by awards - හොඳම නළුවා සම්මානය ලබාගත් නළුවන්
# 8. Search actors by movies - සඳ මඩල චිත්රපටයේ නළුවන්
# 9. Search by actors of decade - 90 දශකයේ නළුවන්
# 10. Search by actress of decade - 90 දශකයේ නිළියන්
# 11. Search by actress of decade - 90 දශකයේ නළුනිළියන්

# todo: add Search actors/actresses by awards with year
# todo: add gender neutral queries

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
    # key words for each query
    # words to remove - කල ලබාගත් ලැබූ ලැබු
    # 1. Search acted movies by actor/actress - දමිතා අබේරත්න රංගනය කල නාට්ය
    movies_by_actor = [["රංගනය"], ["නාට්ය", "නාට්\u200dය"]]
    # 2. Search bio by actor/actress name - දමිතා අබේරත්නගේ විස්තර
    actor_bio = [["විස්තර", "ජීවිතය"]]
    # 3. Search career info by actor/actress name - දමිතා අබේරත්නගේ වෘත්තීය දිවිය
    actor_career = [["වෘත්තීය"], ["රංගනය", "රංගන"], ["දිවිය", "ජීවිතය"]]
    # 4. Search awards by player name - දමිතා අබේ රත්නගේ සම්මාන
    actor_awards = [["සම්මාන"]]
    # 5. Search actresses by movies - මීහරකා චිත්රපටයේ නිළියන්
    actresses_by_movie = [["නිලියන්", "නිළියන්"], "චිත්රපටයේ"]
    # 6. Search actresses by awards - හොඳම නිළිය සම්මානය ලබාගත් නිළියන්
    actresses_by_awards = [["සම්මාන"], ["නිලියන්", "නිළියන්"], ["ලබාගත්", "ලැබූ", "ලැබු"]]
    # 7. Search actors by awards - හොඳම නළුවා සම්මානය ලබාගත් නළුවන්
    actors_by_awards = [["සම්මාන"], ["නළුවන්", "නලුවන්"], ["ලබාගත්", "ලැබූ", "ලැබු"]]
    # 8. Search actors by movies - සඳ මඩල චිත්රපටයේ නළුවන්
    actors_by_movie = [["නළුවන්", "නලුවන්"], "චිත්රපටයේ"]

    list_classifier = [actor_bio, actor_awards, movies_by_actor, actor_career, actors_by_movie, actors_by_awards,
                       actresses_by_movie, actresses_by_awards]
    intent_names = ["actor_bio", "actor_awards", "movies_by_actor", "actor_career", "actors_by_movie",
                    "actors_by_awards", "actresses_by_movie", "actresses_by_awards"]
    score_list = []
    for index, classifier in enumerate(list_classifier):
        score = 0
        for word_list in classifier:
            for word in word_list:
                if word in query:
                    score += 1
                    break
        score_list.append(score)

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
    #     fill remaining selected intents
    else:
        selected_fields = [name, bio, career, films, awards, dob, gender, vital_status, active_years]

    return selected_intent, selected_fields


# todo: lemmatizer implementation
def lemmatizer(word):
    if re.search(".*යේ$", word):
        return word.removesuffix('යේ')
    elif re.search(".*ගේ$", word):
        return word.removesuffix('ගේ')
    elif re.search(".*න්$", word):
        return word.removesuffix('න්')
    else:
        return word


def query_preprocessor(selected_intent, query):
    drop_list = ["කල", "ලබාගත්", "ලැබූ", "ලැබු"]

    intent_dic = {
        "actors_by_movie": "පිරිමි",
        "actors_by_awards": "පිරිමි",
        "actresses_by_movie": "ගැහැණු",
        "actresses_by_awards": "ගැහැණු"
    }

    query_splitted = query.strip().split()
    remaining_words = []

    for word in query_splitted:
        remaining_words.append(lemmatizer(word.strip()))

    if selected_intent in intent_dic.keys():
        remaining_words.append(intent_dic[selected_intent])

    return " ".join(remaining_words)


# test

# 10. Search by actress of decade - 90 දශකයේ නිළියන්
# 11. Search by actress of decade - 90 දශකයේ නළුනිළියන්

queries = ["දමිතා අබේරත්න රංගනය කල නාට්ය", "දමිතා අබේරත්නගේ විස්තර", "දමිතා අබේරත්නගේ වෘත්තීය දිවිය",
           "දමිතා අබේරත්නගේ සම්මාන", "මීහරකා චිත්රපටයේ නිළියන්", "හොඳම නිළිය සම්මානය ලබාගත් නිළියන්",
           "හොඳම නළුවා සම්මානය ලබාගත් නළුවන්", "සඳ මඩල චිත්රපටයේ නළුවන්"]


# def query_preprocessor(selected_intent, query):
#     actor_bio = ["විස්තර", "ජීවිතය"]
#     actor_awards = ["සම්මාන"]
#     movies_by_actor = ["රංගනය", "නාට්ය", "නාට්\u200dය"]
#     actor_career = ["වෘත්තීය", "රංගනය", "රංගන", "දිවිය", "ජීවිතය"]
#     actors_by_movie = ["නළුවන්", "නලුවන්", "නිලියන්", "නිළියන්", "චිත්රපටයේ"]
#     actors_by_awards = ["සම්මාන", "නළුවන්", "නලුවන්", "නිලියන්", "නිළියන්", "ලබාගත්", "ලැබූ", "ලැබු"]
#
#     intent_dic = {
#         "actor_bio": actor_bio,
#         "actor_awards": actor_awards,
#         "movies_by_actor": movies_by_actor,
#         "actor_career": actor_career,
#         "actors_by_movie": actors_by_movie,
#         "actors_by_awards": actors_by_awards,
#         "": []
#     }
#     query_splitted = query.strip().split()
#     remaining_words = []
#
#     for word in query_splitted:
#         if word not in intent_dic[selected_intent]:
#             remaining_words.append(lemmatizer(word.strip()))
#
#     return " ".join(remaining_words)
