from maxflowmincut import *
from dsa1lib.graph import *
from typing import List, Tuple


class BaseballElimination:
    def __init__(self, team_name: List[str], w: List[int], l: List[int], r: List[int], g: List[List[int]]):
        self.team_name = team_name
        self.w = w
        self.l = l
        self.r = r
        self.g = g

        # we start indexing with teams so team_id is preserved, then we have games -
        # flat indexed as g[][] after the end of teams, then at the end we have s and t.
        # For each flow network for each team we have redundant vertices for each team and each match for convenience.
        # This way game indices can be refered to using the teams' ids.
        self.num_teams = len(w)
        self.num_games = self.num_teams ** 2
        self.num_vertices = self.num_teams + self.num_games + 2
        self.s = self.num_vertices - 2
        self.t = self.s + 1

        # contains eliminated teamid, reduced list of certification teams,
        # total wins of those certification teams and the total games among those certification teams
        self.eliminated_teams_with_mincut: List[Tuple[int, List, int, int]] = [
        ]
        self.find_eliminated_teams()

    def game_idx(self, t1: int, t2: int) -> int:
        """Vertex in flow graph for game between t1 and t2. 
        Note: Game index (t1, t2) and (t2, t1) are different. Maintain order so that every time one index is returned for a
        game pair. 

        Args:
            t1 (int): Smaller indexed team.
            t2 (int): Larger indexed team.

        Returns:
            int: Flat index for game between t1 and t2. 
        """
        return self.num_teams + t1 * self.num_teams + t2

    def build_graph_for_team(self, team_id: int) -> WeightedDirectedGraph:
        """Builds flow network for eliminee team. Has reduandant vertices for all teams and matches for convenience.

        Args:
            team_id (int): team_id that is currently being checked for elimination. 

        Returns:
            WeightedDirectedGraph: Flow graph with edge weights for games without team_id, 
            and wins for each team such that it is less than the max win by team_id. 
        """
        graph = WeightedDirectedGraph(self.num_vertices)

        for t1 in range(self.num_teams):
            if t1 == team_id:
                continue

            graph.add_edge(
                t1, self.t, self.w[team_id] + self.r[team_id] - self.w[t1])

            for t2 in range(t1 + 1, self.num_teams):
                if t2 == team_id:
                    continue

                if self.g[t1][t2] == 0:
                    continue

                graph.add_edge(self.s, self.game_idx(t1, t2), self.g[t1][t2])

                graph.add_edge(self.game_idx(t1, t2), t1, self.g[t1][t2])
                graph.add_edge(self.game_idx(t1, t2), t2, self.g[t1][t2])

        return graph

    def is_all_matches_played(self, flow_network: FlowNetwork) -> bool:
        for edge_from_s in flow_network.adj(self.s):
            edge_from_s = cast(FlowEdge, edge_from_s)
            if edge_from_s.flow != edge_from_s.capacity:
                return False
        else:
            return True

    def _get_certificate_of_elim(self, edmondskarp: EdmondsKarp, team_id: int) -> Tuple[List[int], int, int]:
        """Mincut with reduced number of teams required to get a higher average win than the total possible wins for
        team_id.

        Args:
            edmondskarp (EdmondsKarp): Edmonds-Karl max flow instance. 
            team_id (int): team whose elimination is to be certified. 

        Returns:
            Tuple[List[int], int, int]: Tuple containing - 
                Teams that have a higher average win than the max possible wins of team_id,
                total win of teams in the eliminitor list,
                games among eachother of the eliminator list.
        """

        mincut_teams = list(
            filter(lambda v: v < self.num_teams, edmondskarp.mincut))

        # so teams with highest wins are likely to be enough first
        mincut_teams.sort(key=(lambda t: self.w[t]), reverse=True)

        reduced_list = []
        total_win = 0
        games_among = 0

        for mincut_team in mincut_teams:
            reduced_list.append(mincut_team)
            total_win += self.w[mincut_team]

            for included_team in reduced_list:
                games_among += self.g[mincut_team][included_team]

            if (total_win + games_among) / len(reduced_list) > self.w[team_id] + self.r[team_id]:
                break

        return reduced_list, total_win, games_among

    def trivial_elimination(self, team_id: int) -> int:
        """Checks if any team already has more win that the max possible win of team_id.

        Args:
            team_id (int): team_id whose elimination to check. 

        Returns:
            int: Eliminator team. 
        """
        eliminator = -1
        for team in range(num_teams):
            if team == team_id:
                continue

            if self.w[team] > self.w[team_id] + self.r[team_id]:
                eliminator = team
                break

        return eliminator

    def find_eliminated_teams(self):
        for team_id in range(self.num_teams):
            trivial_eliminator = self.trivial_elimination(team_id)
            if trivial_eliminator >= 0:
                self.eliminated_teams_with_mincut.append(
                    (team_id, [trivial_eliminator], self.w[trivial_eliminator], 0))
            else:
                eliminee_graph = self.build_graph_for_team(team_id)
                edmondskarp = EdmondsKarp(eliminee_graph, self.s, self.t)

                if not self.is_all_matches_played(edmondskarp.flow_network):
                    self.eliminated_teams_with_mincut.append(
                        (team_id, *self._get_certificate_of_elim(edmondskarp, team_id)))


def print_elim_info(baseball: BaseballElimination):
    for elim_team_id, mincut_teams, total_win, games_among in baseball.eliminated_teams_with_mincut:
        print()
        print(f"{baseball.team_name[elim_team_id]} is eliminated.")
        print(
            f"They can win at most {baseball.w[elim_team_id]} + {baseball.r[elim_team_id]} = {baseball.w[elim_team_id] + baseball.r[elim_team_id]} games")
        print(
            f"{' and '.join([baseball.team_name[team] for team in mincut_teams])} have won a total of {total_win} games.")
        print(f"They play each other {games_among} times.")
        avg_win = (total_win + games_among) / len(mincut_teams)
        print(
            f"So on average, each of the teams wins {(total_win + games_among)}/{len(mincut_teams)} = {avg_win} games")
        print()


if __name__ == '__main__':
    num_teams = int(input())
    team_name = [""] * num_teams
    w = [0] * num_teams
    l = [0] * num_teams
    r = [0] * num_teams
    g = [[0] * num_teams for _ in range(num_teams)]

    for team_id in range(num_teams):
        inputs = input().split()
        team_name[team_id] = inputs[0]
        w[team_id] = int(inputs[1])
        l[team_id] = int(inputs[2])
        r[team_id] = int(inputs[3])
        g[team_id] = [int(i) for i in inputs[4:]]

    baseball_elim = BaseballElimination(team_name, w, l, r, g)

    print_elim_info(baseball_elim)
