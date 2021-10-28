import re

# query types
# 1. Search acted movies by actor/actress - දමිතා අබේරත්න රංගනය කල නාට්ය
# 2. Search bio by actor/actress name - දමිතා අබේරත්නගේ විස්තර
# 3. Search career info by actor/actress name - දමිතා අබේරත්නගේ වෘත්තීය දිවිය
# 4. Search awards by player name - දමිතා අබේ රත්නගේ සම්මාන
# 5. Search actors/actresses by movies - මීහරකා චිත්රපටයේ නළුවන්
# 6. Search actors/actresses by awards - හොඳම නිළිය සම්මානලයබාගත්නිළියන්

#   field types
#
# todo: add Search actors/actresses by awards with year


def intent_classifier(query):
    # available fields
    career = "career"
    bio = "bio"
    films = "films"
    awards = "awards"
    name = "sinhala_name"

    selected_fields = []
    actor_bio = [["විස්තර", "ජීවිතය"]]
    actor_awards = [["සම්මාන"]]
    movies_by_actor = [["රංගනය"], ["නාට්ය", "නාට්\u200dය"]]
    actor_career = [["වෘත්තීය"], ["රංගනය", "රංගන"], ["දිවිය", "ජීවිතය"]]
    actors_by_movie = [["නළුවන්", "නලුවන්", "නිලියන්", "නිළියන්"], "චිත්රපටයේ"]
    actors_by_awards = [["සම්මාන"], ["නළුවන්", "නලුවන්", "නිලියන්", "නිළියන්"], ["ලබාගත්", "ලැබූ", "ලැබු"]]

    list_classifier = [actor_bio, actor_awards, movies_by_actor, actor_career, actors_by_movie, actors_by_awards]
    intent_names = ["actor_bio", "actor_awards", "movies_by_actor", "actor_career", "actors_by_movie",
                    "actors_by_awards"]
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
    print('SELECTED INTENT - ', selected_intent)
    if selected_intent == "actor_bio":
        selected_fields = [name, bio]
    elif selected_intent == "actor_awards":
        selected_fields = [name, awards, career]
    elif selected_intent == "movies_by_actor":
        selected_fields = [name, films, awards, career]
    elif selected_intent == "actor_career":
        selected_fields = [name, career]
    elif selected_intent == "actors_by_movie":
        selected_fields = [name, career, films, awards]
    elif selected_intent == "actors_by_awards":
        selected_fields = [name, awards]
    else:
        selected_fields = [name, bio, career, films, awards]

    return selected_intent, selected_fields


# todo: lemmatizer implementation
def lemmatizer(word):
    if re.search(".*යේ$", word):
        print(True)
        return word.removesuffix('යේ')
    elif re.search(".*ගේ$", word):
        print(True)
        return word.removesuffix('ගේ')
    else:
        return word

def query_preprocessor(selected_intent, query):
    actor_bio = ["විස්තර", "ජීවිතය"]
    actor_awards = ["සම්මාන"]
    movies_by_actor = ["රංගනය", "නාට්ය", "නාට්\u200dය"]
    actor_career = ["වෘත්තීය", "රංගනය", "රංගන", "දිවිය", "ජීවිතය"]
    actors_by_movie = ["නළුවන්", "නලුවන්", "නිලියන්", "නිළියන්", "චිත්රපටයේ"]
    actors_by_awards = ["සම්මාන", "නළුවන්", "නලුවන්", "නිලියන්", "නිළියන්", "ලබාගත්", "ලැබූ", "ලැබු"]

    intent_dic = {
        "actor_bio": actor_bio,
        "actor_awards": actor_awards,
        "movies_by_actor": movies_by_actor,
        "actor_career": actor_career,
        "actors_by_movie": actors_by_movie,
        "actors_by_awards": actors_by_awards,
        "":[]
    }
    query_splitted = query.strip().split()
    remaining_words = []

    for word in query_splitted:
        if word not in intent_dic[selected_intent]:
            remaining_words.append(lemmatizer(word.strip()))

    return " ".join(remaining_words)

    # if selected_intent == "actor_bio":
    #
    # elif selected_intent == "actor_awards":
    #     if word not in actor_awards:
    #         remaining_words.append(lemmatizer(word))
    #
    # elif selected_intent == "movies_by_actor":
    #     if word not in movies_by_actor:
    #         remaining_words.append(lemmatizer(word))
    #
    # elif selected_intent == "actor_career":
    #     if word not in actor_career:
    #         remaining_words.append(lemmatizer(word))
    #
    # elif selected_intent == "actors_by_movie":
    #     if word not in actors_by_movie:
    #         remaining_words.append(lemmatizer(word))
    #
    # elif selected_intent == "actors_by_awards":
    #     if word not in actors_by_awards:
    #         remaining_words.append(lemmatizer(word))
    # else:
