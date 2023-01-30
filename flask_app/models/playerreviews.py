from flask_app.config.mysqlconnection import connectToMySQL


class PlayerReviews:
    db = "persona"
    def __init__(self,data):
        self.id = data['id']
        self.review = data['review']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author_id = data['author_id']
        self.game_id = data['game_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO player_reviews (review, rating, author_id, game_id) VALUES(%(review)s,%(rating)s,%(author_id)s,%(game_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM player_reviews;"
        results = connectToMySQL(cls.db).query_db(query)
        reviews = []
        for row in results:
            reviews.append( cls(row))
        return reviews
    
    @classmethod
    def get_by_gameid(cls, data):
        query = "SELECT * FROM player_reviews WHERE game_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        reviews = []
        if results == 0:
            return reviews
        for row in results:
            reviews.append( cls(row))
        return reviews
    @classmethod
    def update_review(cls, data):
        query = """UPDATE player_reviews
                SET review = %(review)s, rating = %(rating)s
                WHERE id = %(id)s """
        
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_review(cls, data):
        query = """DELETE FROM player_reviews
                WHERE id = %(id)s """
        return connectToMySQL(cls.db).query_db(query, data)
    # @classmethod
    # def get_all_with_games(cls):
    #     games = Game.get_all();
    #     for game in games:
    #         for field in game:
    #             print(field)
    
    #     return 0

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM player_reviews WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        playerReview = cls(results[0])
        return playerReview

#@app.route('/delete/<int:games_id>')
#def delete_sighting(games_id):
    #if 'user_id' not in session:
        #return redirect('/logout')
    #data = { 
        #"id": games_id,
        #"posted_by": session['user_id']
    #}
    #games = games.delete_comment(data)
   # return redirect('/dashboard')  

# [game1[review1, review2,.....], game2, game3, ...]