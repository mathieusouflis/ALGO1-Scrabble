import json
import time
from random import *
from rich.console import Console
from rich.table import Table

console = Console()

class Game:
    def __init__(self) -> None:
        """
        Initialisation du jeu
        Level = Le niveau actuel
        Words = Les mots a trouver + leurs états + le nombre total de mots trouvés
        Tries = Le nombre d'essais effectués
        Score = Le score du joueur
        Letters usable = Les lettres utilisables pour trouver les mots
        Words File Path = Le fichier contenant tous les mots
        Number of words to find = Le nombre de mots a trouver
        Initialise Game : Assigne des valeurs a words, tries et letters_usable
        """
        self.level = 1
        self.words = None
        self.tries = None
        self.score = 0
        self.letters_usable = None
        self.word_file_path = "./french.json"
        self.number_of_words_to_find = 3
        self.initialise_game()

    def generate_letters_usable(self, words: list) -> str:
        liste_sans_doublons = []
        word_list = "".join(words)
        for lettres in word_list:
         if lettres not in liste_sans_doublons:
          liste_sans_doublons.append(lettres)
        shuffle(liste_sans_doublons)
        liste_sans_doublons = "".join(liste_sans_doublons)

        return liste_sans_doublons

    def initialise_game(self) -> None:
        """
        Cette fonction assigne des valeurs a :
            self.words : ex - {"words", [["mot1", 0], ["mot2", 0]], "found": 0} le second élément de la liste ["mot1", 0] nous dis si le mot a été trouvé ou non.
            self.letters_usable : prend toutes les lettres des mots choisis, retire les doublons et les mélanges
        """
        file = open(self.word_file_path, "r")
        all_words = json.load(file)["words"]

        # Choisir les mots à trouver à partir de la liste de mots
        list_words_to_find = []
        i = 0
        while i < self.number_of_words_to_find:
            list_words_to_find.append([all_words[randint(0,len(all_words)-1)], 0])
            i = i + 1
        print(list_words_to_find) # A SUPP
        self.words = {
            "words": list_words_to_find,
            "found": 0
        }
        self.letters_usable = self.generate_letters_usable([word[0] for word in list_words_to_find])

    def start(self) -> None:
        """
        Cette fonction lance le jeu
        """
        while self.level <= 3:
            self.play_level()
            console.clear()
            input(f'Pour passer au niveau {self.level + 1} appuyez sur "ENTRER": ')
            self.initialise_game()
        self.end()

    def play_level(self) -> None:
        """
        Cette fonction lance un niveau
        """
        error = False
        self.tries = 0
        while self.words["found"] < self.number_of_words_to_find and (self.level == 1 or self.tries < 10):
            console.clear()
            self.print_board(helps=self.level != 2, error=error)
            word_try = self.get_user_input()
            if word_try is None:
                self.level += 1
                return
            self.tries += 1
            is_valid, word_index = self.check_word_validity(word_try)
            if is_valid:
                self.words["words"][word_index][1] = 1
                self.words["found"] += 1
                error = False
            else:
                error = True
        self.tries = 0
        self.level += 1

    def get_user_input(self) -> str | None:
        word_try = input("\n\nYou can write 'Quit' to pass the level.\nWrite a word: ")
        if word_try.lower() == "quit":
            console.clear()
            console.print(f"Arf, tu as abandonné...\nLes mots à trouver étaient : [blue]{self.words['words'][0][0]} [yellow]{self.words['words'][1][0]} [blue]{self.words['words'][2][0]}")
            input("Appuie sur 'ENTER' pour passer au niveau suivant: ")
            return None
        return word_try

    def check_word_validity(self, word: str) -> tuple:
        """
        Cette fonction regarde si le mot choisis est bien dans la liste des mots a trouver :
            words : Le mot choisis par l'utilisateur
        """
        for i in range(len(self.words["words"])):
            word_to_find = self.words["words"][i][0]
            found = self.words["words"][i][1]

            if word.lower() == word_to_find.lower() and not found:
                return (True, i)
            elif word.lower() == word_to_find.lower() and found:
                break

        return (False, None)

    def print_board(self, helps: bool = True, error: bool = False) -> None:
        """
        Cette fonction affiche le jeu dans la console:
            helps : Si True - Affiche une aide sur la longueur des mots -- Si False - Affiche des "..."
            error : Si True (quand le mot choisis est mauvais) - Affiche un message d'erreur
        """
        table = Table(show_edge=False, box=False)
        for i in range(len(self.words["words"])):
            table.add_column(f"Word {i+1}", justify="center")
        words_display = [("_" * len(word[0]) if word[1] == 0 else word[0]) for word in self.words["words"]] if helps else ["..."  if word[1] == 0 else word[0] for word in self.words["words"]]
        table.add_row(*words_display)

        console.print(f"Level: {self.level}\nTries: {self.tries}\n",table,"\n")

        if error:
            console.print("[red]Word incorrect, retry...")
        letters_display = "[bold]" + " ".join(f"[blue]{letter}" for letter in self.letters_usable)
        console.print(f"Letters available: {letters_display}")

    def print_score(self):
        console.print()
    def end(self) -> None:
        """
        Fin du jeu :D
        """
        console.print("END OF THE GAME")


game = Game()
game.start()
