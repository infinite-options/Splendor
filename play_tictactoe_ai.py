import pickle
import random

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.winner = None

    def reset(self):
        self.board = [" " for _ in range(9)]
        self.winner = None

    def make_move(self, position, player):
        if self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                self.winner = self.board[combo[0]]
                return self.winner

        if " " not in self.board:
            self.winner = "Tie"
            return "Tie"

        return None

    def is_valid_move(self, position):
        return self.board[position] == " "

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == " "]

    def render(self):
        for row in [self.board[i:i + 3] for i in range(0, 9, 3)]:
            print("|".join(row))
        print()

class QLearningAgent:
    def __init__(self, symbol):
        self.symbol = symbol
        self.q_table = {}

    def get_state(self, board):
        return tuple(board)

    def choose_action(self, board):
        state = self.get_state(board)

        q_values = self.q_table.get(state, [0] * 9)
        valid_moves = [i for i in range(9) if board[i] == " "]
        max_q_value = max(q_values[i] for i in valid_moves)
        best_moves = [i for i in valid_moves if q_values[i] == max_q_value]

        return random.choice(best_moves)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.q_table = pickle.load(file)

if __name__ == "__main__":
    agents = {}

    print("Welcome to Tic Tac Toe!")
    print("Load your AI agent pickle files.")
    
    while True:
        filename = input("Enter the filename of an AI agent pickle file (or type 'done' to finish): ").strip()
        if filename.lower() == "done":
            break

        try:
            symbol = input("Enter the symbol for this agent (X or O): ").strip().upper()
            if symbol not in ["X", "O"]:
                print("Invalid symbol. Please choose either X or O.")
                continue

            agent = QLearningAgent(symbol=symbol)
            agent.load(filename)
            agents[filename] = agent
            print(f"Loaded agent from {filename} with symbol {symbol}.")
        except Exception as e:
            print(f"Error loading agent: {e}")

    if not agents:
        print("No agents loaded. Exiting.")
        exit()

    while True:
        print("\nChoose a game mode:")
        print("1. AI vs. AI")
        print("2. Human vs. AI")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            print("\nAvailable AI agents:")
            for idx, filename in enumerate(agents.keys()):
                print(f"{idx + 1}. {filename}")

            try:
                agent1_idx = int(input("Select the first agent (by number): ")) - 1
                agent2_idx = int(input("Select the second agent (by number): ")) - 1

                if agent1_idx == agent2_idx:
                    print("You must choose two different agents.")
                    continue

                agent1 = list(agents.values())[agent1_idx]
                agent2 = list(agents.values())[agent2_idx]

                game = TicTacToe()

                play_again = "y"
                while play_again.lower() == "y":
                    game.reset()
                    print("Starting a new AI vs. AI game!")

                    current_player = agent1

                    while not game.winner:
                        move = current_player.choose_action(game.board)
                        game.make_move(move, current_player.symbol)
                        game.render()

                        winner = game.check_winner()
                        if winner:
                            if winner == "Tie":
                                print("It's a tie!")
                            else:
                                print(f"Agent {winner} wins!")
                            break

                        current_player = agent2 if current_player == agent1 else agent1

                    play_again = input("Do you want to play another AI vs. AI game? (y/n): ")

            except (ValueError, IndexError):
                print("Invalid selection. Please try again.")

        elif choice == "2":
            print("\nAvailable AI agents:")
            for idx, filename in enumerate(agents.keys()):
                print(f"{idx + 1}. {filename}")

            try:
                agent_idx = int(input("Select an AI agent to play against (by number): ")) - 1
                agent = list(agents.values())[agent_idx]

                human_symbol = "O" if agent.symbol == "X" else "X"

                game = TicTacToe()

                play_again = "y"
                while play_again.lower() == "y":
                    game.reset()
                    print("Starting a new Human vs. AI game!")
                    game.render()

                    current_player = "X"

                    while not game.winner:
                        if current_player == human_symbol:
                            move = -1
                            while move not in game.available_moves():
                                try:
                                    move = int(input(f"Your turn ({human_symbol}). Enter a position (0-8): "))
                                except ValueError:
                                    print("Invalid input. Please enter a number between 0 and 8.")

                            game.make_move(move, human_symbol)
                        else:
                            print(f"Agent's turn ({agent.symbol}).")
                            move = agent.choose_action(game.board)
                            game.make_move(move, agent.symbol)

                        game.render()
                        winner = game.check_winner()

                        if winner:
                            if winner == "Tie":
                                print("It's a tie!")
                            elif winner == human_symbol:
                                print("Congratulations! You win!")
                            else:
                                print("Agent wins. Better luck next time!")
                            break

                        current_player = human_symbol if current_player != human_symbol else agent.symbol

                    play_again = input("Do you want to play another Human vs. AI game? (y/n): ")

            except (ValueError, IndexError):
                print("Invalid selection. Please try again.")

        elif choice == "3":
            print("Thanks for playing! Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")
