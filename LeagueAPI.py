import requests
from collections import defaultdict


class LeagueAPI:
    def __init__(self):
        self.key = "xxxxxxxxxxxxxxxxxxxx" #Riot games api key here.

    def get_summoner(self, summoners):
        """
        :param summoners: The summoner(s) that you are requesting from the api. Can be one or multiple.
        :param key: API key.
        :return:  Dictionary, containing the data of the requested summoner(s)
        """
        url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summoners+"?api_key=" + self.key
        response = requests.get(url)
        return response.json()

    @staticmethod
    def get_participant_id(match, account_id):
        """

        :param match: A Match object, that contains various data about a single match
        :param account_id: Summoner's whose participant_id your looking for's account Id
        :return: Returns an int, which represents the participant_id
        """
        participant_id = None
        for index in range(0, match['participantIdentities'].__len__()):  # Finding summoners participant ID
            if match['participantIdentities'][index]['player']['accountId'] == account_id:
                participant_id = match['participantIdentities'][index]['participantId']
                break

        return participant_id

    @staticmethod
    def get_team_id_of_participant(match, participant_id):
        """
        :param match: Match object to bee parsed.
        :param participant_id: Participant_id whose team_id is being searched for
        :return: The team_id of the participant_id
        """
        team_id = None
        for index in range(0, match['participants'].__len__()):  # finding which team the summoner is on.
            if match['participants'][index]['participantId'] == participant_id:
                team_id = match['participants'][index]['teamId']
                break
        return team_id

    def get_match_history(self, summoner_id, lane=None):
        """
        :param summoner_id: accountId of the summoner, whose match_history you want
        :param lane: If specified, will filter the match history list to only contain games with the specified lane.
        Possible lane values are, MIDDLE, BOTTOM, JUNGLE, and TOP
        :return: returns a list of gameIds
        """
        url = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(summoner_id)+"?api_key=" + \
              self.key
        response = requests.get(url)
        # Handles an inconsistency in Riots API. MID is a legacy value and must be used here. MIDDLE is used elsewhere.
        if lane == 'MIDDLE':
            lane = 'MID'

        # Grabbing the gameId of every match in the response, if lane is None, then there is no filtering applied.
        if lane is not None:
            matches = []
            for match in response.json()['matches']:
                if match['lane'] == lane:
                    matches.append(match['gameId'])
            return matches

        return response.json()['matches']

    def get_match(self, match_id):
        """
        :param match_id: match_id of the match that is being obtained.
        :return: returns a match object
        """
        url = "https://na1.api.riotgames.com/lol/match/v3/matches/"+str(match_id)+"?api_key=" + self.key
        response = requests.get(url)
        return response.json()

    @staticmethod
    def get_counterpart(match, team_id, lane):
        """
        :param match: Match object that to be parsed
        :param team_id: Team id of the counterpart, which is the opposite of the counterpart's counterpart.
        :param lane: The lane, the counterpart is playing, should be the same as the counterpart's counterpart.
        :return: Returns a smaller match object, focused on the counterpart, this could be called a Player object.
        """
        if team_id == 200:
            # Find the counter part of said summoner.
            for index in range(5, match['participants'].__len__()):
                if match['participants'][index]['teamId'] != team_id:
                    continue
                if lane is not None:
                    if match['participants'][index]['timeline']['lane'] == lane:
                        return match['participants'][index]

        else:
            # Find the counter part of said summoner.
            for index in range(0, 6):
                if match['participants'][index]['teamId'] != team_id:
                    continue
                if lane is not None:
                    if match['participants'][index]['timeline']['lane'] == lane:
                        return match['participants'][index]

    def get_worst_champs_to_play_against(self, account_id, lane):
        """
        :param account_id: account_id of the summoner that is being examined.
        :param lane: Lane specifies the lane that is being examined when it comes to games that were loss. For example,
        MIDDLE games will not be paid attention to, if lane is JUNGLE.
        :return: A frequency dictionary, where each key is a champion Id, and the value is the amount of games lost to
        said champion.
        """
        # Get match history
        matches = self.get_match_history(summoner_id=account_id, lane=lane)

        # Start up the frequency list.
        frequency_list = defaultdict(int)

        # Go through every match in the matches list. If lane is None,
        # then the match object in the loop will have a  different structure
        for match in matches:
            if lane is None:
                match = self.get_match(match_id=match['gameId'])
            else:
                match = self.get_match(match_id=match)

            # If 'status' is a key in the match object, then we have reached the max amount of requests,
            # just return the frequency_list as is.
            if 'status' in match:
                    return frequency_list

            # Get the participant_id of the specified account_id, and team_id of the participant_id
            participant_id = self.get_participant_id(match=match, account_id=account_id)
            team_id = self.get_team_id_of_participant(match=match, participant_id=participant_id)
            # TODO: Get the following section working, using get_counterpart as this section is get_counterpart's job.
            if team_id is 100:
                team_id = 200

                # Find the counter part of said summoner.
                for index in range(5, match['participants'].__len__()):
                    if match['participants'][index]['teamId'] != team_id:
                        continue
                    # If Lane is None then we do not care about counterparts, we wil just go through the enemy team and
                    # look for the championId's that we lost to.
                    if lane is not None:
                        if match['participants'][index]['timeline']['lane'] == lane:
                            # If we've found the counterpart, then check if they won, if they did then
                            # increment the championId in the frequencyList
                            if match['participants'][index]['stats']['win']:
                                frequency_list[str(match['participants'][index]['championId'])] += 1
                    else:
                        for index in range(5, match['participants'].__len__()):
                            if match['participants'][index]['stats']['win']:
                                frequency_list[str(match['participants'][index]['championId'])] += 1
            else:
                # Same stuff as above, but this is if the counterpart is on team 100.
                team_id = 100
                for index in range(0, 6):
                    if match['participants'][index]['teamId'] != team_id:
                        continue
                    if lane is not None:
                        if match['participants'][index]['timeline']['lane'] == lane:
                            if match['participants'][index]['stats']['win']:
                                frequency_list[str(match['participants'][index]['championId'])] += 1
                    elif match['participants'][index]['stats']['win']:
                        frequency_list[str(match['participants'][index]['championId'])] += 1
        return frequency_list

    def get_most_recent_match(self, account_id, lane=None):
        """
        :param account_id: the account_id that whose last recent match is being searched for.
        :param lane: If lane is specified the match that is returned will tbe the most recent match, in which the user
        with an account id of account_id played this lane.
        :return: returns a match object.
        """
        # Get the match history
        matches = self.get_match_history(summoner_id=account_id, lane=lane)
        #  Return the match which is the first gameId in the matches list. If Lane is None the matches list structure
        # is a bit different.
        if lane is None:
            return self.get_match(match_id=matches[0]['gameId'])

        return self.get_match(match_id=matches[0])

    def get_timeline_differentials(self, account_id, lane):
        """
        :param account_id: account_id, whose timeline differential in it's most recent game is being retrieved.
        :param lane: The lane to be examined, which must be specifed differentials only exist when there is a
        counterpart
        :return: A list of dictionaries containing the differentials.
        """
        # Get the match, get the participant id, and get the team Id. Also set up the list that will hold the
        # differentials
        match = self.get_most_recent_match(account_id=account_id, lane=lane)
        participant_id = self.get_participant_id(match=match, account_id=account_id)
        team_id = self.get_team_id_of_participant(match=match, participant_id=participant_id)
        differentials = []

        # Getting the enemy's team id.
        if team_id is 100:
            enemy_team_id = 200
        else:
            enemy_team_id = 100

        # Parse through the match object specific subsection related to the participant_id, this is where the
        # differential dictionaries are located But some other dictionaries and values are in this section to,
        # these things we do not care about, so we skip over them.
        for key, value in match['participants'][participant_id-1]['timeline'].items():
            # If the value for this key, is the participant_id then this is not a key we are interested in, next.
            if value == participant_id:
                continue

            # If the current key that we are at is 'role' then we've read all the differentials.
            if key == 'role':
                break

            # If we reach here, then we are at a Key and value we are interested in, append it to the differentials
            # list.
            differentials.append({key: value})

        # Finally get the champion Id's, that the two players were playing and append them at the end of the
        # differentials list as this information may prove useful.
        counterpart = self.get_counterpart(match=match, team_id=enemy_team_id, lane=lane)
        differentials.append({'champion': match['participants'][participant_id-1]['championId'],
                              'enemychampion': counterpart['championId']})
        return differentials




