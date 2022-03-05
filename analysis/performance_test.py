from src.game import ConnectFour
from src.agent import AlphaBeta, MiniMax, Reflex, IterativeDeepening

record = {-1: 0, 1: 0, 3: 0}


def simulate_game(n=0):
    agent_1 = AlphaBeta(player=1, depth_limit=3)
    agent_2 = AlphaBeta(player=-1, depth_limit=3)
    game = ConnectFour()

    while True:
        if game.get_turn() % game.get_player_count() == 0:
            action = agent_1.get_action(game)
        else:
            action = agent_2.get_action(game)

        game.perform_action(action)
        print(".", end="")

        if game.is_terminal_state():
            status = game.get_status()
            record[status] += 1
            print(f"\nFinished game={n + 1}\tstatus={status}")
            return


if __name__ == '__main__':
    for i in range(10):
        simulate_game(i)
    print(record)
    print("Done")
