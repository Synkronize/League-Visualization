from LeagueAPI import LeagueAPI


class Summoner:
    def __init__(self, name, id=None):
        self.name = name
        if id is None:
            self.id = LeagueAPI().get_summoner(summoners=name)['accountId']
            self.match_history = None

    def get_match_history(self):
        return LeagueAPI().get_match_history(self.id)


if __name__ == "__main__":
    summoner_1 = Summoner('2B Father Servo')
    summoner_list = [Summoner('2B Father Servo'), Summoner('Itona Horibe'), Summoner('Asagiri Aya'), Summoner('Rinka Hayami'), Summoner('Yuma Isogai')]
    match_history = []
    for summoner in summoner_list:
        match_history.append(summoner.get_match_history())
    print()





