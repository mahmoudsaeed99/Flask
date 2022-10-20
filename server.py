# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 18:32:37 2022

@author: Mahmoud Saeed
"""
from flask import Flask, redirect, url_for, request , Response

import pymongo
import json
from bson.objectid import ObjectId


app = Flask(__name__)

try:
    mongo = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mongo['company']
    mongo.server_info()
except:
    print("Error in connection to mongoDB")
    
#############################
@app.route("/users" , methods=['GET'])
def get_users():
    
    try:
        data = list(mydb.users.find({}))
        for user in data:
            user["_id"] = str(user["_id"])

        return Response(
            response = json.dumps(data)
            )
    
    except Exception as ax:
        return Response(
            response = json.dumps({"message":"can not read users"}) )    



############################# 
@app.route("/users", methods = ["POST"])
def create_user():
    try:
        user = {"firstname":request.form['firstname'],
                "lastname":request.form['lastname'] ,
                "age":request.form['age']}
        dbResponse = mydb.users.insert_one(user)
        l = []
        for attr in dir(dbResponse):
            l.append(attr)
        return Response(
            response= json.dumps({"message":"user created" ,
                                  "id":f"{dbResponse.inserted_id}" })
            )   
    except Exception as ax:
        return (ax)


#############################
@app.route("/users/<id>" , methods = ['PATCH'])
def update_user(id):
    try:
        dbResponse = mydb.users.update_one({"_id":ObjectId(id)},
                                    {"$set":{"age":request.form['age']}})
        for attr in dir(dbResponse):
            print(f"******{attr}*******")
            
        return Response(
            response = json.dumps({"message":"user updated"})
            )

    
    except Exception as ex:
        print("**********")
        print(ex)
        print("**********")
        return Response(
            response = json.dumps({"message":"Sorry can not update user"})
            )

#############################

@app.route("/users/<id>" , methods = ['DELETE'])
def delete_user(id):
    try:
        dbResponse = mydb.users.delete_one({"_id":ObjectId(id)})
        for attr in dir(dbResponse):
            print(f"******{attr}*******")
        
        return Response(
            response = json.dumps({"message":"user deleted"})
            )  
    
    except Exception as ex:
        return Response(
            response = json.dumps({"message":"user can not be deleted"})
            )

#############################
@app.route("/")
def hey():
    return "hello users"
    


if __name__ == "__main__":
    app.run(port = 80, debug = True)
    
    
    