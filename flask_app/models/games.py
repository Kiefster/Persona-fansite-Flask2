from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.playerreviews import PlayerReviews

class Game:
    db = "persona"
    def __init__(self,data):
        self.id = data['id']
        self.game_name = data['game_name']
        self.description = data['description']
        self.protagonist = data['protagonist']
        self.color = data['color']
        self.imagelink = data['image_link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reviewed = data['reviewed']
        self.reviews = data['reviews']

    @classmethod
    def get_all(cls, id):
        query = "SELECT * FROM games;"
        results = connectToMySQL(cls.db).query_db(query)
        games = []
        for game in results:
            data = {
                'id': game['id']
                }
            reviewed = False
            reviews = PlayerReviews.get_by_gameid(data)
            for review in reviews:
                if review.author_id == id:
                    reviewed = True
            game['reviewed'] = reviewed
            game['reviews'] = reviews
            games.append( cls(game))
        

        return games

