class Player:
    def __init__(self, name, age, team):
        self.name = name
        self.age = age
        self.team = team

    def __str__(self):
        return f"{self.name} is {self.age} years old and plays for {self.team}"

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def __str__(self):
        return f"{self.name} has {len(self.players)} players"

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)
    
    def compute_average_age(self):
        return sum(player.age for player in self.players) / len(self.players)

def main():
    player1 = Player("John", 20, "Team A")
    player2 = Player("Jane", 21, "Team B")
    team = Team("Team A", [player1, player2])
    print(team)

if __name__ == "__main__":
    main()