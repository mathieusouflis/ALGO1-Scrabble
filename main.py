    # Décommenter l.59 si les mots sont trop durs à trouver.

import json
from time import sleep
from random import *
from rich.console import Console
from rich.table import Table

console = Console()

class Game:
    def __init__(self) -> None:
        """
        Initialisation du jeu
        Level = Le niveau actuel
        Words = Les mots à trouver + leurs états + le nombre total de mots trouvés
        Tries = Le nombre d'essais effectués
        Score = Le score du joueur
        Letters usable = Les lettres utilisables pour trouver les mots
        Words File Path = Le fichier contenant tous les mots
        Number of words to find = Le nombre de mots à trouver
        Initialise Game : Assigne des valeurs à words, tries et letters_usable
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
        list_without_doubles = []
        word_list = "".join(words)
        for letters in word_list:
         if letters not in list_without_doubles:
             list_without_doubles.append(letters)
        shuffle(list_without_doubles)
        list_without_doubles = "".join(list_without_doubles)

        return list_without_doubles

    def initialise_game(self) -> None:
        """
        Cette fonction assigne des valeurs à :
            self.words : ex - {"words", [["mot1", 0], ["mot2", 0]], "found": 0} le second élément de la liste ["mot1", 0] nous dit si le mot a été trouvé ou non.
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
        # print(list_words_to_find)
        self.words = {
            "words": list_words_to_find,
            "found": 0
        }
        self.letters_usable = self.generate_letters_usable([word[0] for word in list_words_to_find])

    def start(self) -> None:
        """
        Cette fonction lance le jeu
        """
        # Message de bienvenue
        console.print("Bievenue sur un morpion fait par [red]Nermine [white]et [yellow]Mathieu[white] ! Pour commencer, appuie sur 'ENTRER'", end="")
        input()

        while self.level <= 3:
            console.clear()
            # Message lors du commencement d'un nouveau niveau
            input(f"Bienvenue dans le niveau {self.level}\n\tNombre d'essais : {"Infini" if self.level == 1 else "10"}\n\tAides : {"Oui (le nombre de _ correspond au nombre de lettres que contient le mot" if self.level <=2 else "Non"}\n\nPour continuer appuie sur 'ENTRER'")

            level_status = self.play_level()

            self.level += 1

            console.clear()

            if self.level <= 3:
                # Met sous format texte et coloré les mots qu'il fallait trouver
                word_text = "".join([f"[blue]{self.words["words"][i][0]} " if i % 2 == 0 else f"[yellow]{self.words["words"][i][0]} " for i in range(len(self.words["words"]))])

                self.print_score()
                console.print(f"{"Bien joué ! Tu as complété le niveau" if level_status else "Arf, tu as abandonné..."}\nLes mots à trouver étaient : {word_text}")
                input(f'Pour passer au niveau {self.level} appuyez sur "ENTRER": ')
                self.initialise_game()
        self.end()

    def play_level(self) -> bool:
        """
        Cette fonction lance un niveau
        """
        error = False
        self.tries = 0
        while self.words["found"] < self.number_of_words_to_find and (self.level == 1 or self.tries < 10):
            console.clear()
                # Affiche le jeu dans la console
            self.print_board(helps=self.level < 3, error=error)

            word_try = input("\n\nVous pouvez ecrire 'Quit' pour passer le niveau.\nEcrivez un mot: ")

            if word_try.lower() == "quit":
                return False # Retourne False pour afficher le bon message (l.90)

            self.tries += 1
            is_valid, word_index = self.check_word_validity(word_try)

            if is_valid:
                self.words["words"][word_index][1] = 1 # Met à jour le statut du mot en question
                self.words["found"] += 1

                self.score += self.level

                error = False
            else:
                error = True
        self.tries = 0
        return True # Retourne False pour afficher le bon message (l.90)


    def check_word_validity(self, word: str) -> tuple:
        """
        Cette fonction regarde si le mot choisi est bien dans la liste des mots à trouver :
            words : Le mot choisi par l'utilisateur
        """
        for i in range(len(self.words["words"])):
            word_to_find = self.words["words"][i][0]
            found = self.words["words"][i][1]

            if word.lower() == word_to_find.lower() and not found:
                return (True, i)
            elif word.lower() == word_to_find.lower() and found:
                break # Stop la boucle pour ne pas boucler dans des mots inutilement (tous les mots sont uniques)

        return (False, None)

    def print_board(self, helps: bool = True, error: bool = False) -> None:
        """
        Cette fonction affiche le jeu dans la console:
            helps : Si True - Affiche une aide sur la longueur des mots -- Si False - Affiche des "..."
            error : Si True (quand le mot choisi est mauvais) - Affiche un message d'erreur
        """
        table = Table(show_edge=False, box=False)
        for i in range(len(self.words["words"])):
            table.add_column(f"Word {i+1}", justify="center")
        words_display = [("_" * len(word[0]) if word[1] == 0 else word[0]) for word in self.words["words"]] if helps else ["..."  if word[1] == 0 else word[0] for word in self.words["words"]]
        table.add_row(*words_display)

        console.print(f"Niveau: {self.level}")
        self.print_score()
        console.print(f"Essais: {self.tries}\n",table,"\n")

        if error:
            console.print("[red]Mot incorrect, réessayez...")
        letters_display = "[bold]" + " ".join(f"[blue]{letter}" for letter in self.letters_usable)
        console.print(f"Lertres valables: {letters_display}")

    def print_score(self) -> None:
        console.print(f"Score: {self.score}")

    def end(self) -> None:
        """
        Fin du jeu :D
        """
        while True:
            console.clear()
            self.print_score()
            console.print("".join([f"[color({randint(9, 14)})]{letter}" for letter in "BIEN JOUÉ, TU AS FINI LE JEU !"]))
            sleep(0.5)


game = Game()
game.start()
