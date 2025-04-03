
from quiz_brain import QuizBrain

question_bank = [{'index': 1, 'text': 'In the 1992 film "Army of Darkness", what name does Ash give to his double-barreled shotgun?', 'answers': ['Blastbranch', 'Boomstick', 'Bloomstick', '2-Pump Chump'], 'correct': 'Boomstick'},
                 {'index': 2, 'text': 'In the movie "Spaceballs", what are the Spaceballs attempting to steal from Planet Druidia?', 'answers': ['Meatballs', 'Princess Lonestar', 'Air', 'The Schwartz'], 'correct': 'Air'},
                 {'index': 3, 'text': 'What is the name of the fictional retro-mod band starring Austin Powers as the lead vocalist?', 'answers': ['Cough Fi', 'Ming Tea', 'Spear Mint', 'Mister E'], 'correct': 'Ming Tea'},
                 {'index': 4, 'text': 'In the movie Gremlins, after what time of day should you not feed Mogwai?', 'answers': ['Afternoon', 'Morning', 'Midnight', 'Evening'], 'correct': 'Midnight'},
                 {'index': 5, 'text': 'In the Super Mario Bros. Movie (2023), who plays Toad?', 'answers': ['Keegan-Michael Key', 'Seth Rogan', 'Charlie Day', 'Jack Black'], 'correct': 'Keegan-Michael Key'},
                 {'index': 6, 'text': "Which actress danced the twist with John Travolta in 'Pulp Fiction'?", 'answers': ['Uma Thurman', 'Pam Grier', 'Kathy Griffin', 'Bridget Fonda'], 'correct': 'Uma Thurman'},
                 {'index': 7, 'text': 'Who directed the movies "Pulp Fiction", "Reservoir Dogs" and "Django Unchained"?', 'answers': ['James Cameron', 'Quentin Tarantino', 'Martin Scorcese', 'Steven Spielberg'], 'correct': 'Quentin Tarantino'},
                 {'index': 8, 'text': 'Which animated movie was first to feature a celebrity as a voice actor?', 'answers': ['James and the Giant Peach', 'The Hunchback of Notre Dame', 'Aladdin', 'Toy Story'], 'correct': 'Aladdin'},
                 {'index': 9, 'text': 'At the end of the 2001 film "Rat Race", whose concert do the contestants crash?', 'answers': ['Bowling for Soup', 'Linkin Park', 'Sum 41', 'Smash Mouth'], 'correct': 'Smash Mouth'},
                 {'index': 10, 'text': 'In "Jurassic World", what is the name of the dinosaur that is a genetic hybrid?', 'answers': ['Tyrannosaurus Rex ', 'Pteranodon', 'Indominus Rex', 'Mosasaurus'], 'correct': 'Indominus Rex'}]

quiz = QuizBrain(question_bank)
while quiz.still_has_questions():
    quiz.get_next_question()
    answer = input()
    quiz.check_answer(answer)
quiz.get_next_question()


# # Initialize BeautifulSoup on the html
# soup = BeautifulSoup(site_html, "html.parser")
#
# select_tag = soup.find('select', {'name': 'trivia_category'})
#
# # Extract values and categories
# categories = []
# for option in select_tag.find_all('option'):
#     value = option.get('value')
#     category = option.text
#     categories.append((value, category))
#
# # Print the result
# categories = {category:value for value, category in categories}
# print(categories)

