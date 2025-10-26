import unittest

from main import Player, Team

class TestTeam(unittest.TestCase):
    
    def setUp(self):
        print("Setting up test...")
        self.team = Team("Team A", [])
        self.player = Player("John", 20, "Team A")
        self.player1 = Player("John", 20, "Team A")
        self.player2 = Player("Jane", 21, "Team A")
        self.player3 = Player("Bob", 22, "Team A")
        self.player4 = Player("Alice", 23, "Team A")
        self.player5 = Player("Charlie", 24, "Team A")

    def tearDown(self):
        print("Test completed")

    def test_add_player(self):
        self.team.add_player(self.player)
        self.assertEqual(len(self.team.players), 1)
        self.assertEqual(self.team.players[0].name, "John")
        self.assertEqual(self.team.players[0].age, 20)
        self.assertEqual(self.team.players[0].team, "Team A")
    
    def test_remove_player(self):
        self.team.add_player(self.player)
        self.team.remove_player(self.player)
        self.assertEqual(len(self.team.players), 0)
        self.assertEqual(self.team.players, [])
    
    def test_compute_average_age(self):
        self.team.add_player(self.player1)
        self.team.add_player(self.player2)
        self.team.add_player(self.player3)
        self.team.add_player(self.player4)
        self.team.add_player(self.player5)

        self.assertEqual(self.team.compute_average_age(), 22)

if __name__ == "__main__":
    unittest.main()