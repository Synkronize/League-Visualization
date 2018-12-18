# League-Visualization
League Visualization,  uses the League of Legends API along with all the tools
mentioned above  to pull some data from the game, and visualize it on the browser. Currently it
lists the frequency of times that a user loses to various champions, by looking at their past
hundred games. Alternatively, the user can also examine their most recent game, and view
graphs of the differentials between them and their counterpart in the game. I say counterpart,
because each of the five players in a League match has a role in the game, and likewise the
enemy team’s roles mirror those roles so the user usually always has a counterpart on the enemy
team. The differentials range from how much of a gold difference there is between the user and
their counterpart, to the difference in damage taken between the two players.

To run the program
Python code was written with Python3
The only library installed should be Flask and pip and maybe flask_cors.
Install flask using: pip install Flask
More help here: http://flask.pocoo.org/docs/1.0/installation/

Install flask_cors using: pip install -U flask-cors

To get the web-server running all you should really have to do is type into the terminal:
set FLASK_APP=Summoner.py
flask run
Change set to export if using Linux/Mac
Example video here: https://www.youtube.com/watch?v=MwZwr5Tvyxo&ab_channel=CoreySchafer

Once the Flask web server is running, the only thing that should be left to do is to, to open up
either page.html or page2.html enter in the user data and click the submit button on the page.

# Note: You must put in an API key in LeagueAPI.py to be able to get information.