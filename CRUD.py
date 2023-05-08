# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 14:01:54 2022

@author: Mahmoud Saeed
"""

from flask import Flask ,jsonify , request ,Response
import json
import pandas

import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


app = Flask(__name__)

mydb = myclient['CRUD']
###########################################
# add new user
###########################################
@app.route("/users/add" , methods = ['POST'])
def add_user():
    try:
        mycol = mydb['Users']
        dbResponse = mycol.insert_one({"firstname":request.form['firstname'],
                                       "secondname":request.form['secondname'],
                                       "age":int(request.form["age"]),
                                       "email":request.form["email"],
                                       "job":request.form["job"],
                                       "address":{"street":request.form["street"],
                                                  "city":request.form["city"],
                                                  "country":request.form["country"],
                                                  "postalcode":request.form["postalcode"]},
                                       "phone":{"code":request.form["code"],
                                                "number":request.form["number"]
                                           }})
        
        return Response(
            response = json.dumps({"message":request.form['firstname']+" added successfully"})
            )
    
    except Exception as ex:
        return Response(
            response = jsonify({"message":"ex"})
            )

###########################################
# get all users 
##http://127.0.0.1:5000/users
###########################################
@app.route("/users" , methods = ['GET'])
def get_all_users():
    mycol = mydb['Users']
    dbResponse = list(mycol.find({}))
    for user in dbResponse:
        user['_id'] = str(user['_id'])
    # re = dbResponse[0]['address']['street']
    re = dbResponse
    return Response(
        response = json.dumps(re)
        )
    
###########################################
# get all users by address
###########################################
@app.route("/users/address/<add>" , methods = ['PATCH'])
def get_user_by_address(add):
    
    mycol = mydb['Users']
    
    if add == "postalcode":
        dbResponse = list(mycol.find({"address.postalcode":request.form['postalcode']}))
    elif add == "country":
        dbResponse = list(mycol.find({"address.country":request.form['country']}))
    elif add == "city":
        dbResponse = list(mycol.find({"address.city":request.form['city']}))
        # return request.form['city']
    else:
        dbResponse = list(mycol.find({"address.street":request.form['street']}))
        
    for user in dbResponse:
        user['_id'] = str(user['_id'])
    # re = dbResponse[0]['firstname']+" "+dbResponse[0]['secondname']
    re = dbResponse
    return Response(
        response = json.dumps(re)
        )


###########################################
# get all users  by phone number
###########################################
@app.route("/users/phone" , methods = ['POST'])
def get_user_by_phone():
    mycol = mydb['Users']
    dbResponse = list(mycol.find({"phone":{"code":request.form['code'] ,
                                  "number":request.form['number']}}))
    for user in dbResponse:
        user['_id'] = str(user['_id'])
    re = dbResponse[0]['firstname']+" "+dbResponse[0]['secondname']
    # re = dbResponse
    return Response(
        response = json.dumps(re)
        )
    return 


###########################################
# get all users by define the search key
#--------------
#http://127.0.0.1:5000/users/firstname  --send in body -- find = "mahmoud"
#http://127.0.0.1:5000/users/secondname  --send in body -- find = "saeed"
#http://127.0.0.1:5000/users/age  --send in body -- find = "23"
###########################################
@app.route("/users/<t>" , methods=["PATCH"])
def get_user(t):
    
    if t == "age":
        searchKey = int(request.form['find'])
    else:
        searchKey = str(request.form['find'])
    mycol = mydb['Users']
    
    dbResponse = list(mycol.find({str(t):searchKey}))
    for user in dbResponse:
        user['_id'] = str(user['_id'])
    # re = dbResponse[0]['address']['street']
    re = dbResponse
    return Response(
        response = json.dumps(re)
        )

###########################################
# get user by id 
#--------------
#http://127.0.0.1:5000/users/delete
###########################################
@app.route("/users/delete" , methods = ['POST'])
def delete_user():
    mycol = mydb['Users']
    dbResponse = list(mycol.delete_one({"_id":ObjectId(request.form['id'])}))
    return json.dumps({"message":"user deleted"})


###########################################
# Filter all users by age and select a comparison key
#--------------
#http://127.0.0.1:5000/users/filter/age/==/23
#http://127.0.0.1:5000/users/filter/age/</23
#http://127.0.0.1:5000/users/filter/age/<=/23
#http://127.0.0.1:5000/users/filter/age/>/23
#http://127.0.0.1:5000/users/filter/age/>=/23
###########################################
@app.route("/users/filter/age/<filter_type>/<age>" , methods = ['GET'])
def filter_age(filter_type , age):
    fil_type = ""
    age = int(age)
    if filter_type == ">":
        fil_type = "$gt"
    elif   filter_type == ">="  :
        fil_type = "$gte"
    elif   filter_type == "<"  :
        fil_type = "$lt"    
        
    elif   filter_type == "<="  :
        fil_type = "$lte"
        
    elif   filter_type == "=="  :
        fil_type = ""    
    else:
        return json.dumps({"message":"error in filter by"})
    mycol = mydb['Users']
    if fil_type == "":
        dbResponse = list(mycol.find({"age":age}))
    else:
        dbResponse = list(mycol.find({"age":{str(fil_type):age}}))
    
    for user in dbResponse:
        user['_id'] = str(user['_id'])
        
    return json.dumps(dbResponse)

###########################################
# group all users and get the min and max and avg age in each country
#----------------
#http://127.0.0.1:5000/users/group/address.city
#http://127.0.0.1:5000/users/group/address.country
#http://127.0.0.1:5000/users/group/job
#http://127.0.0.1:5000/users/group/firstname
#http://127.0.0.1:5000/users/group/secondname
#http://127.0.0.1:5000/users/group/phone.code
###########################################
@app.route("/users/group/<key>" , methods = ['GET'])
def aggregate_users_country(key):
    mycol = mydb['Users']
    dbResponse = list(mycol.aggregate([{"$group":{"_id":{str(key):"$"+str(key)},
                                             "max":{"$max":"$age"},
                                             "min":{"$min":"$age"},
                                             "avg":{"$avg":"$age"}}
                                        }]))
    return json.dumps(dbResponse)


@app.route("/test" , methods = ['GET'])
def test():
    mycol = mydb['Users']
    #.sort("age",-1)
    # dbResponse = list(mycol.find({},{"firstname":1,"age":1 , "_id" :0}).sort(
    #     [("age" , -1) , ("firstname" , 1)]))
    dbResponse = list(mycol.find({"firstname":{"$regex":"^a"}}))
    for user in dbResponse:
        user['_id'] = str(user['_id'])
    return json.dumps(dbResponse)

if __name__ == "__main__":
    app.run(debug = True )


   