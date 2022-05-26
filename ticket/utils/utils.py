import random


def generate_good_luck():
    phrases = ["Good luck",
               "Have fun",
               "Best of luck",
               "Fingers crossed",
               "You'll do great",
               "Break a leg",
               "May the force be with you",
               "May the odds ever be in your favor",
               "You got this",
               "Fight on",
               "Rock on",
               "Veel geluk",
               "Buena suerte",
               "Powodzenia"]
    return random.choice(phrases)


def generate_good_job():
    phrases = ["Good job",
               "Nice work",
               "You are a hero",
               "Congratulations",
               "Fantastic",
               "Excellent",
               "Perfect",
               "Wonderful",
               "Marvelous",
               "Outstanding",
               "Dobra robota",
               "Buen trabajo",
               "Goed gedaan"]
    return random.choice(phrases)
