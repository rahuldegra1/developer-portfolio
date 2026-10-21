board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]


def print_board(b):
    print(f"\n {b[0]} | {b[1]} | {b[2]} ")
    print("-----------")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("-----------")
    print(f" {b[6]} | {b[7]} | {b[8]} \n")


def check_win(b, player):
    win_combos = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # rows
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # columns
        [0, 4, 8],
        [2, 4, 6],  # diagonals
    ]
    for combo in win_combos:
        if b[combo[0]] == player and b[combo[1]] == player and b[combo[2]] == player:
            return True
    return False


current_player = "X"

while True:
    print_board(board)

    move = input(f"Player {current_player}, enter your move (1-9): ")
    try:
        move = int(move) - 1
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 9.")
        continue
    if move < 0 or move > 8:
        print("Invalid input. Please enter a number between 1 and 9.")
        continue

    if board[move] == " ":
        board[move] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins!")
            break

        if " " not in board:
            print_board(board)
            print("It's a draw!")
            break

        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"
    else:
        print("Invalid move. Try again.")
