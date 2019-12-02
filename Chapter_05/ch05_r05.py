"""Python Cookbook 2nd ed.

Chapter 5, recipe 5
"""

import cmd
import random

red_bins = (1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 28, 30, 32, 34, 36)

# black_bins = (2, 4, 6, 8, 10, 11, 13, 15, 17,
#    19, 20, 22, 24, 26, 29, 31, 33, 35)
#
# assert set(red_bins) | set(black_bins) == set(range(1,37))


def roulette_bin(i):
    return (
        str(i),
        {
            "even" if i % 2 == 0 else "odd",
            "low" if 1 <= i < 19 else "high",
            "red" if i in red_bins else "black",
        },
    )


def zero_bin():
    return "0", set()


def zerozero_bin():
    return "00", set()


def wheel():
    """
    >>> random.seed(1)
    >>> w = wheel()
    >>> spin = random.choice(w)
    >>> spin == ('7', {'odd', 'red', 'low'})
    True
    >>> spin = random.choice(w)
    >>> spin == ('35', {'black', 'high', 'odd'})
    True
    """
    number_bins = [roulette_bin(i) for i in range(1, 37)]
    return [zero_bin(), zerozero_bin()] + number_bins


class Roulette(cmd.Cmd):
    use_rawinput = False  # sys.stdout.write() and sys.stdin.readline() are used
    prompt = "Roulette> "
    bet_names = set(["even", "odd", "high", "low", "red", "black"])

    def preloop(self):
        self.stake = 100
        self.wheel = wheel()
        self.bets = {}
        print(f"Starting with {self.stake}")

    def postloop(self):
        print(f"Ending with {self.stake}")

    bet_names = set(["even", "odd", "high", "low", "red", "black"])

    def do_bet(self, bet):
        """Bet <name> <amount>
        Name is one of even, odd, red, black, high, or low
        """
        try:
            name, text_amount = bet.split()
            name in self.bet_names
            amount = int(text_amount)
        except Exception as ex:
            print(ex)
            return
        self.bets[name] = amount

    def do_spin(self, args):
        if not self.bets:
            print("No bets placed")
            return
        self.spin = random.choice(self.wheel)
        label, winners = self.spin
        print("Spin", label, sorted(winners))
        for b in self.bets:
            if b in winners:
                self.stake += self.bets[b]
                print("Win", b)
            else:
                self.stake -= self.bets[b]
                print("Lose", b)
        self.bets = {}

    def do_stake(self, args):
        print(f"{stake=}")

    def do_done(self, args):
        return True


from unittest.mock import Mock, call


def test_command(capsys):
    mock_input = Mock(readline=Mock(side_effect=["bet black 1", "spin", "done"]))
    mock_output = Mock()
    random.seed(42)
    r = Roulette(stdin=mock_input, stdout=mock_output)
    r.cmdloop()
    assert mock_output.write.mock_calls == [
        call("Roulette> "),
        call("Roulette> "),
        call("Roulette> "),
    ]
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "Starting with 100",
        "Spin 6 ['black', 'even', 'low']",
        "Win black",
        "Ending with 101",
    ]


if __name__ == "__main__":
    r = Roulette()
    r.cmdloop()
