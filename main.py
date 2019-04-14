def results_graph(results_file):
    """
    :param results_file: file containing game results seperated by newlines in a very particular format
    :return: a graph represented by a dictionary where the teams are the key, the list of teams they lost to are the values
    """
    with open(results_file, 'r') as games:

        def team_gen():
            for line in games:
                name_delimiter = '  '  # more than one space means the name is over
                winner = line[12:].split(name_delimiter)[0]
                loser = line[41:].split(name_delimiter)[0]
                yield loser, winner

        game_dict = {}
        for (loser, winner) in team_gen():
            if loser not in game_dict:
                game_dict[loser] = [winner]
            else:
                game_dict[loser].append(winner)
            if winner not in game_dict:
                game_dict[winner] = []
        return game_dict


male_game_graph = results_graph('men\'s.txt')
female_game_graph = results_graph('women\'s.txt')


def transitive_winner_search (game_graph, champion):
    """
    :param game_graph: a graph generated by results_graph
    :param champion: the winner of the tournament overall
    :return: the list of teams who either beat the champion (making them transitive champions)
    or beat a transitive champion
    """
    candidates = {champion}
    transitive_winners = set()
    while candidates:
        transitive_winner = candidates.pop()
        transitive_winners.add(transitive_winner)
        candidates |= set(game_graph[transitive_winner]) - transitive_winners

    transitive_winners.remove(champion)  # champs are real winners, not transitive ones
    return transitive_winners


male_transitive_winners = transitive_winner_search(male_game_graph, 'Virginia')
female_transitive_winners = transitive_winner_search(female_game_graph, 'Baylor')

print('There are {0} male team transitive winners out of {1} teams'.format(len(male_transitive_winners), len(male_game_graph)))

print('There are {0} female team transitive winners out of {1} teams'.format(len(female_transitive_winners), len(female_game_graph)))


def transitive_closure(game_graph):
    """
    :param game_graph: a graph generated by results graph
    :return: the transitive closure of game_graph
    """
    return {team:transitive_winner_search(game_graph, team) for team in game_graph}


print(male_transitive_winners == transitive_closure(male_game_graph)['Virginia'])
print(female_transitive_winners == transitive_closure(female_game_graph)['Baylor'])



