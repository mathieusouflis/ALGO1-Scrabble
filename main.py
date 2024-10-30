import json
from rich import box
from rich.console import Console
from rich.table import Table

# def words_file_to_array(file_path):
#   # Fonction pour ouvrir des fichiers (liste de mots) et renvoyer la liste des mots
#   file = open(file_path, "r")
#   return json.load(file)["words"]

# print("Hello [bold magenta]World[/bold magenta]!", ":vampire:")

from rich.prompt import Prompt
import random

console = Console()

class Game:
    def __init__(self, words: list) -> None:
        self.level = 0
        self.words = words
        self.words_found = 0
        self.letters_usable = []
        words = "".join(words)
        for i in range(len(words)):
            if  words[i] not in self.letters_usable:
                self.letters_usable.append(words[i])
        random.shuffle(self.letters_usable)

    def change_words(self, new_list_of_words: list) -> None:
        self.words = new_list_of_words

    def change_level(self, level: int) -> None:
        self.level = level

    def print_level(self) -> None:
        console.print(f"Level: {self.level}")

    def print_char_to_use(self) -> None:
        letter_usable_in_color = "[bold]"
        for i in range(len(self.letters_usable)):
            if i % 2:
                letter_usable_in_color += "[yellow]" + self.letters_usable[i] + " "
            else:
                letter_usable_in_color += "[blue]" + self.letters_usable[i] + " "

        console.print(f"Letters avalable : {letter_usable_in_color}")

    def print_board(self) -> None:
        table = Table(show_edge=False, box=False)
        for i in range(len(self.words)):
            table.add_column(f"Word {i+1}", justify="center")
        words_length = [len(word) * "_" for word in self.words]
        table.add_row(*words_length)

        self.print_level()
        console.print("\n", table, "\n")

        self.print_char_to_use()
    def end(self) -> None:
        print("END OF THE GAME")

game = Game(["COUCOU", "LA", "TCHEAM"])

game.print_board()


def is_choice_legit(choice):
    for letter in choice:
        if letter not in game.letters_usable:
            return False

    return True


validity = False
while validity == False:
    choice = input("\n\nYou can write 'Quit' to pass the level.\nWrite a word: ")

    if choice.lower() == "quit":
        game.end()
    elif is_choice_legit(choice) != True:
        # ECRIRE QUE L'UTILISATEUR A MIS LES MAUVAISES LETTRES
        pass
    else:
        # Ajouter 1 au nombre de mots trouvés
        pass




# liste_char ="coucou j'aime les pates et les chiens aussi"
# char_sans_doublons = ""
# for i in range(len(liste_char)):
#     valable = True
#     for b in range(len(char_sans_doublons)):
#         if liste_char[i] == char_sans_doublons[b]:
#             valable = False
#             break
#     if valable:
#         char_sans_doublons += liste_char[i]

# i = 0
# while i < len(liste_char):
#     valable = True
#     b = 0
#     while b < len(char_sans_doublons)):
#         if liste_char[i] == char_sans_doublons[b]:
#             valable = False
#             b = 0
#             break
#         b += 1
#     if valable:
#         char_sans_doublons += liste_char[i]
#     i += 1

# for i in range(len(liste_char)):
#     if liste_char[i] not in char_sans_doublons:
#         char_sans_doublons += liste_char[i]


# print(char_sans_doublons)
