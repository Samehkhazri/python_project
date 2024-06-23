from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Rent:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.rent = data['rent']
        self.location = data['location']
        self.beds = data['beds']
        self.bathroom = data['bathroom']
        self.surface = data['surface']
        self.pic = data['pic']
        self.created_at = data['created_at']
        self.updated_at= data['updated_at']

    #CRUD
    #CREATE
    @classmethod
    def add_rent_house(cls,data):
        query="""INSERT INTO houses_to_rent 
                (user_id, rent, location, beds, bathroom, surface, pic)
                    VALUES 
                (%(user_id)s, %(rent)s, %(location)s, %(beds)s, %(bathroom)s, %(surface)s, %(pic)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #READ
    #Get all houses for rent
    @classmethod
    def get_houses_for_rent(cls):
        query="""SELECT * FROM houses_to_rent;"""
        result=  connectToMySQL(DATABASE).query_db(query)
        houses=[]
        for row in result:
            houses.append(cls(row))
        return houses
    
    #Get all houses by id
    @classmethod
    def get_houses_by_id(cls,data):
        query="""SELECT * FROM houses_to_rent WHERE id=%(id)s;"""
        resultat=connectToMySQL(DATABASE).query_db(query,data)
        r_id=[]
        for row in resultat:
            r_id.append(cls(row))
        return r_id

    #Get all houses by rent
    @classmethod
    def get_houses_by_rent(cls,data):
        query="""SELECT * FROM houses_to_rent WHERE rent<=%(max_rent)s AND rent>=%(min_rent)s ;"""
        results=connectToMySQL(DATABASE).query_db(query,data)
        rents=[]
        for row in results:
            rents.append(cls(row))
        return rents
    
    #Get all houses by location
    @classmethod
    def get_houses_by_location(cls,data):
        query="""SELECT * FROM houses_to_rent WHERE location<=%(max_location)s AND location>=%(min_location)s ;"""
        resultats=connectToMySQL(DATABASE).query_db(query,data)
        loc=[]
        for row in resultats:
            loc.append(cls(row))
        return loc
    
    #Get all houses by beds
    @classmethod
    def get_houses_by_beds(cls,data):
        query="""SELECT * FROM houses_to_rent WHERE beds<=%(max_beds)s AND beds>=%(min_beds)s ;"""
        resu=connectToMySQL(DATABASE).query_db(query,data)
        bed=[]
        for row in resu:
            bed.append(cls(row))
        return bed
    
    #Get all houses by bathroom
    @classmethod
    def get_houses_by_bathroom(cls,data):
        query="""SELECT * FROM houses_to_rent WHERE bathroom<=%(max_bathroom)s AND bathroom>=%(min_bathroom)s ;"""
        res=connectToMySQL(DATABASE).query_db(query,data)
        bath=[]
        for row in res:
            bath.append(cls(row))
        return bath
    
    #Get all houses by surface
    @classmethod
    def get_houses_by_surface(cls,data):
        query="""SELECT * FROM houses_to_rent WHERE surface<=%(max_surface)s AND surface>=%(min_surface)s ;"""
        re=connectToMySQL(DATABASE).query_db(query,data)
        surfaces=[]
        for row in re:
            surfaces.append(cls(row))
        return surfaces
    
    #UPDATE
    @classmethod
    def update_houses_to_rent(cls,data):
        query="""UPDATE houses_to_rent 
                SET rent=%(rent)s, location=%(location)s, beds=%(beds)s, bathroom=%(bathroom)s, surface=%(surface)s, pic=(pic)s
                    WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #DELETE
    @classmethod
    def delete(cls,data):
        query="""DELETE FROM houses_to_rent WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #VALIDATION 
    @staticmethod
    def validate(data):
        is_valid=True

        if not data['rent']:
            flash(" Rent must be fixed!!!")
            is_valid = False
        if not data['location']:
            flash(" Location must be selected!!!")
            is_valid = False
        if not data['beds']:
            flash("Number of beds must be fixed!!!")
            is_valid = False
        if not data['bathroom']:
            flash("Number of bathrooms must be fixed!!!")
            is_valid = False
        if not data['surface']:
            flash(" Surface must be fixed!!!")
            is_valid = False
        if (data['pic'])=="":
            flash(" Picture must be selected!!!")
            is_valid = False
        
        return is_valid
        












