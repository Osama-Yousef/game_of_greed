""""
Create a Game of Greed Player Bots
ONLY use public methods
- Game class constructor and play method
- DO NOT INJECT CUSTOM ROLL FUNCTION
- GameLogic, all methods available
"""
import builtins
import re

# from gameofgreed.game import Game
from game import Game
# from gameofgreed.game_logic import GameLogic
from game_logic import GameLogic



class BasePlayer:
    def __init__(self):
        self.old_print = print
        self.old_input = input
        builtins.print = self._mock_print
        builtins.input = self._mock_input
        self.total_score = 0

    def reset(self):
        builtins.print = self.old_print
        builtins.input = self.old_input

    # The default behaviour
    def _mock_print(self, *args, **kwargs):
        self.old_print(*args, **kwargs)

    def _mock_input(self, *args, **kwargs):
        return self.old_input(*args, **kwargs)

    @classmethod
    def play(cls, num_games=1):

        mega_total = 0

        for i in range(num_games):
            player = cls()
            game = Game() # doesn't pass a mock roller
            try:
                game.play()
            except SystemExit:
                # in game system exit is fine
                # because that's how they quit.
                pass

            mega_total += player.total_score
            player.reset()

        print(
            f"{num_games} games (maybe) played with average score of {mega_total // num_games}"
        )


class Ali(BasePlayer):
    def _mock_input(self, *args, **kwargs):
        return "n"


class NervousNellie(BasePlayer):
    def __init__(self):
        super().__init__()
        self.roll = None

    def _mock_print(self, *args, **kwargs):
        first_arg = args[0]
        first_char = first_arg[0]
        if first_char.isdigit():
            self.roll = tuple(int(char) for char in first_arg.split(","))
        elif first_arg.startswith("Thanks for playing."):
            self.total_score = int(re.findall(r"\d+", first_arg)[0])
        self.old_print(first_arg)
    def _mock_input(self, *args, **kwargs):
        prompt = args[0]
        if prompt.startswith("Wanna play?"):
            # self.old_print(prompt, 'y')
            return "y"
        elif prompt.startswith("Enter dice to keep (no spaces), or (q)uit:"):
            scorers = GameLogic.get_scorers(self.roll)
            keepers = "".join([str(ch) for ch in scorers])
            # self.old_print(prompt, keepers)
            return keepers
        elif prompt.startswith("(r)oll again, (b)ank your points or (q)uit "):
# _________________________________________________________
    # our average score 9175
            x=GameLogic.get_scorers(self.roll)
            y=GameLogic.calculate_score(x)
            # print(type(x))
            # print("x"*50)
            # print(x)
            # print("x"*50)
            if y < 200:
            # scorers = GameLogic.get_scorers(self.roll)
            # if  keepers < 200:
                return ("r")
            else:
                    return "b"
# _________________________________________________________
            # return "b"
        else:
            raise ValueError(f"Unrecognized prompt {prompt}")



if __name__ == "__main__":
    # Ali.play(20)
    NervousNellie.play(100)