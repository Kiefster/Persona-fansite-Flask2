from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import datetime

date_format = '%m-%d-%Y'

class games:
    db = "persona"
    def __init__(self,data):
        self.id = data['id']
        self.posted_by = data['posted_by']
        self.name = data['first_name'] + ' ' + data['last_name']
        self.location = data['location']
        self.description = data['description']
        self.sighted_at = data['sighted_at']
        self.sasquatch_count = data['comment']
        

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = """SELECT sightings.id, sightings.posted_by, users.first_name, users.last_name, sightings.description, sightings.sighted_at, sightings.sasquatch_count, sightings.location
                FROM sightings
                INNER JOIN users ON users.id = sightings.posted_by"""
        results = connectToMySQL(cls.db).query_db(query)
        sightings = []
        for row in results:
            sightings.append(cls(row))
        return sightings
    
    @classmethod
    def get_sighting(cls, data):
        query = """SELECT sightings.id, sightings.posted_by, users.first_name, users.last_name, sightings.description, sightings.sighted_at, sightings.sasquatch_count, sightings.location
                FROM Sightings
                INNER JOIN Users ON Users.id = Sightings.posted_by
                WHERE Sightings.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print("results")
        print(results)
        if (len(results) < 1):
            flash("Sighting doesn't exist","sighting")
            return None
        else:
            sighting = cls(results[0])
            return sighting
       
    
    @classmethod
    def save_sighting(cls, data):
        query = """INSERT INTO sightings (posted_by, location, description, sighted_at, sasquatch_count) 
                VALUES(%(posted_by)s, %(location)s,%(description)s,%(sighted_at)s,%(sasquatch_count)s);"""

        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_sighting(cls, data):
        query = """UPDATE sightings 
                SET posted_by = %(posted_by)s, location = %(location)s, description = %(description)s, sighted_at = %(sighted_at)s, sasquatch_count = %(sasquatch_count)s
                WHERE id = %(id)s AND posted_by = %(posted_by)s"""
        
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_sighting(cls, data):
        query = """DELETE FROM sightings 
                WHERE id = %(id)s AND posted_by = %(posted_by)s"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate_sighting(sighting):
        is_valid = True

        if len(sighting['location']) < 3:
            flash("Location name must be atleast 3 characters","sighting")
            is_valid= False
        if len(sighting['description']) < 3:
            flash("What happened must be atleast 3 characters","sighting")
            is_valid= False
        if not sighting['sasquatch_count'] or int(sighting['sasquatch_count']) < 1:
            flash("Sasquatch count must be atleast 1","sighting")
            is_valid= False

        try:
            datetime.datetime.strptime(sighting['sighted_at'], '%Y-%m-%d')
        except ValueError:
            flash("Date must be included in the form MM/DD/YYYY", "sighting")
            is_valid= False
            
        return is_valid