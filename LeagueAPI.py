import requests


class LeagueAPI:
    def __init__(self):
        self.key = "RGAPI-3a55ccd8-b2b0-4820-9f12-7c23e5f54bca"

    def get_summoner(self, summoners):
        """
        :param summoners: The summoner(s) that you are requesting from the api. Can be one or multiple.
        :param key: API key.
        :return:  Dictionary, containing the data of the requested summoner(s)
        """

        url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summoners+"?api_key=" + self.key
        response = requests.get(url)
        return response.json()

    def get_match_history(self, summoner_id):
        url = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(summoner_id)+"?api_key=" + self.key
        response = requests.get(url)
        return response.json()

