
from LeagueAPI import LeagueAPI
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


class Summoner:
    def __init__(self, name, id=None):
        self.name = name
        if id is None:
            self.id = LeagueAPI().get_summoner(summoners=name)['accountId']
            self.match_history = None
        else:
            self.id = id

    def get_match_history(self):
        return LeagueAPI().get_match_history(self.id)

    def get_worst_champions_to_play_against(self, lane):
        return LeagueAPI().get_worst_champs_to_play_against(account_id=self.id, lane=lane)

    def get_timeline_differentials(self, lane):
        return LeagueAPI().get_timeline_differentials(account_id=self.id, lane=lane)


@app.route("/")
def get_worst_champions_to_play_against():
    try:
        # Get the summoner_id and lane from the browser request.
        summoner_name = request.args.get('summoner_id')
        lane = request.args.get('lane')
        if lane == 'No Lane':
            lane = None
        else:
            # Make the lane all uppercase to make sure it works in other methods.
            lane = str.upper(lane)
    except Exception as e:
        return str(e)

    # Returns the data, back to the browser in a Json format.
    return jsonify(Summoner(summoner_name).get_worst_champions_to_play_against(lane=lane))


@app.route("/page2.html")
def get_timeline_differentials():
    try:
        # Get the summoner_id and lane from the browser request.
        summoner_name = request.args.get('summoner_id')
        lane = request.args.get('lane')

        # Make the lane all uppercase to make sure it works in other methods.
        lane = str.upper(lane)
    except Exception as e:
        return str(e)
    # Returns the data, back to the browser in a Json format.
    return jsonify(Summoner(summoner_name).get_timeline_differentials(lane=lane))

if __name__ == "__main__":
    summoner_1 = Summoner('2B Father Servo')
    test = summoner_1.get_timeline_differentials(lane='MIDDLE')
    print(test)




