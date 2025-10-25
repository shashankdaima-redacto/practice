import unittest

from main import Player, Team

class TestTeam(unittest.TestCase):
    def test_add_player(self):
        team = Team("Team A", [])
        player = Player("John", 20, "Team A")
        team.add_player(player)
        self.assertEqual(len(team.players), 1)
        self.assertEqual(team.players[0].name, "John")
        self.assertEqual(team.players[0].age, 20)
        self.assertEqual(team.players[0].team, "Team A")
    
    def test_remove_player(self):
        team = Team("Team A", [])
        player = Player("John", 20, "Team A")
        team.add_player(player)
        team.remove_player(player)
        self.assertEqual(len(team.players), 0)
        self.assertEqual(team.players, [])
    
    def test_compute_average_age(self):
        team = Team("Team A", [])
        player1 = Player("John", 20, "Team A")
        player2 = Player("Jane", 21, "Team A")
        player3 = Player("Bob", 22, "Team A")
        player4 = Player("Alice", 23, "Team A")
        player5 = Player("Charlie", 24, "Team A")

        team.add_player(player1)
        team.add_player(player2)
        team.add_player(player3)
        team.add_player(player4)
        team.add_player(player5)

        self.assertEqual(team.compute_average_age(), 22)

if __name__ == "__main__":
    unittest.main()