import random
import csv
from players import Roll, Player
import logbook
import sys

header = "--------------------------------------------"
intro = "    Welcome to Rock, Paper, Scissors"
footer = "--------------------------------------------"
Rolls = [
        Roll("rock", "scissors", "paper"),
        Roll("paper", "rock", "scissors"),
        Roll("scissors", "paper", "rock"),
    ]

program_log = logbook.Logger("Program")


def main():
    values = createRollObjects()
    #print(values)
    #game_loop()
    game_loop2(values)


def createRollObjects():
    with open('battle-table.csv') as fin:
        reader = csv.DictReader(fin)
        rolls = []
        for row in reader:
            name = row['Attacker'].lower()
            #print(row)
            defeats = []
            loses = []
            for key, value in row.items():
                if value == 'win':
                    defeats.append(key.lower())
                elif value == 'lose':
                    loses.append(key.lower())
            roll_type = Roll(name, defeats, loses)
            rolls.append(roll_type)
        return rolls


def game_loop2(rolls):
    computer_score = 0
    user_score = 0
    #for val in rolls:
    #    print(str(val.name) + str(val.defeats) + str(val.loses))

    print(header)
    print(intro)
    print(footer)

    value = input("What is your name? ")
    program_log.trace("Username is {}".format(value))
    player = Player(value)
    print(f'Welcome {value}!\n')

    rounds = int(input("How many rounds would you like to play? "))
    program_log.trace("The user chose {} rounds".format(rounds))
    i = 0

    while i < rounds:
        chosen_roll = input("\nPlease play Rock, Gun, Lightning, Devil, Dragon, Water, Air, Paper, Sponge, Wolf, Tree, Human, Snake, Scissors or Fire ")
        chosen_roll = chosen_roll.lower()

        if any(x.name == chosen_roll for x in rolls):
            program_log.trace("Roll number {} the player chose {}".format(i + 1, chosen_roll))
            print("")
        else:
            program_log.warn("The User did not choose a valid value: {}".format(chosen_roll))
            chosen_roll = process_roll(chosen_roll, rolls)

        computer_roll = random.choice(rolls)

        if chosen_roll in computer_roll.loses:
            print("Your {} beat their {}".format(chosen_roll, computer_roll.name))
            user_score += 1
            i += 1
        elif computer_roll.name == chosen_roll:
            print("Your {} tied their {}".format(chosen_roll, computer_roll.name))
            i += 1
            rounds += 1
        elif chosen_roll in computer_roll.defeats:
            print("Your {} lost to their {}".format(chosen_roll, computer_roll.name))
            i += 1
            computer_score += 1
        print("\nUser Score: " + str(user_score))
        print("Computer Score: " + str(computer_score))

    if user_score > computer_score:
        print("\nYou won :)")
    elif computer_score > user_score:
        print("\nYou lost :(")
    else:
        print("\nYou tied the computer")


def game_loop():
    computer_score = 0
    user_score = 0

    print(header)
    print(intro)
    print(footer)

    value = input("What is your name? ")
    player = Player(value)
    print(f'Welcome {value}!\n')

    rounds = int(input("How many rounds would you like to play? "))
    i = 0

    while i < rounds:
        chosen_roll = input("\nPlease play Rock, Gun, Lightning, Devil, Dragon, Water, Air, Paper, Sponge, Wolf, Tree, Human, Snake, Scissors or Fire ")
        chosen_roll = chosen_roll.lower()

        if chosen_roll == Rolls[0].name or chosen_roll == Rolls[1].name or chosen_roll == Rolls[2].name:
             print("")
        else:
            chosen_roll = process_roll(chosen_roll)

        computer_roll = random.choice(Rolls)

        if computer_roll.loses == chosen_roll:
            print("Your {} beat their {}".format(chosen_roll, computer_roll.name))
            user_score += 1
            i += 1
        elif computer_roll.name == chosen_roll:
            print("Your {} tied their {}".format(chosen_roll, computer_roll.name))
            i += 1
            rounds += 1
        elif computer_roll.defeats == chosen_roll:
            print("Your {} lost to their {}".format(chosen_roll, computer_roll.name))
            i += 1
            computer_score += 1
        print("\nUser Score: " + str(user_score))
        print("Computer Score: " + str(computer_score))

    if user_score > computer_score:
        print("\nYou won :)")
    elif computer_score > user_score:
        print("\nYou lost :(")
    else:
        print("\nYou tied the computer")


def process_roll(chosen_roll, rolls):
    if any(x.name == chosen_roll for x in rolls):
        program_log.trace("The player chose {}".format(chosen_roll))
        return chosen_roll
    else:
        program_log.warn("The User did not choose a valid value: {}".format(chosen_roll))
        chosen_roll = input("Please only choose from Rock, Gun, Lightning, Devil, Dragon, Water, Air, Paper, Sponge, Wolf, Tree, Human, Snake, Scissors or Fire ")
        chosen_roll = chosen_roll.lower()
        chosen_roll = process_roll(chosen_roll, rolls)
        return chosen_roll


def init_logging(filename: str = None):
    level = logbook.TRACE
    log_filename = "logbook"

    if not log_filename:
        logbook.StreamHandler(sys.stdout, level=level).push_application()
    else:
        logbook.TimedRotatingFileHandler(log_filename, level=level).push_application()


if __name__ == '__main__':
    init_logging()
    main()