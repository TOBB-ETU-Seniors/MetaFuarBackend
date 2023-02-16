from json import dumps, loads
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from bson import json_util
from Models.Lobby import Lobby
from Models.User import User

from MongoDB.utils import connectToMongo
from datetime import datetime
from bson.objectid import ObjectId

# Create your views here.


client = connectToMongo(password="seconduser")
db = client["MetaFuarDB"]
accs = db["Account"]
lobbs = db["Lobby"]

@api_view(["GET","POST"])
def account(request):
    if request.method == "GET":
        # TODO: Implement social login and query login_id
        found_accs = accs.find({})
        return JsonResponse(loads(json_util.dumps(list(found_accs))), safe=False)
    elif request.method == "POST":
        data = request.data
        id = accs.insert_one(User(data).__dict__)
        print(id)
        # Change here verify post 
        return JsonResponse(True, safe=False )


@api_view(["POST"])
def isUsernameAvailable(request):
    print("isUsernameAvailable endpoint has been reachesd")
    data = request.data
    result = accs.find_one({"user_name": str(data["user_name"])})
    # returns None if no document could be found
    # returns whole entry if one matching document has been found
    if result == None:
        return JsonResponse(True, safe =False)
    else:
        return JsonResponse(False, safe =False)


# create lobby
@api_view(["POST"])
def create_lobby(request):
    print("create_lobby endpoint has been reached")
    data = request.data

    """
    request model
     name
     max_user_count
     organization
     creator
    """

    id = lobbs.insert_one(Lobby(data).__dict__)
    print(id)
    # Change here verify post 
    return JsonResponse(id, safe=False )

# create lobby
@api_view(["POST"])
def delete_lobby(request):
    print("create_lobby endpoint has been reached")
    data = request.data

    """
    request model
     lobby_id
    """

    id = lobbs.delete_one({"_id": ObjectId(data["lobby_id"])})
    # Change here verify post 
    return JsonResponse(True, safe=False )



# add user to lobby
@api_view(["POST"])
def join_lobby(request):
    print("create_lobby endpoint has been reached")
    data = request.data

    """
    request model
     user_id,
     lobby_id
    """

    try:
        old_lobby = lobbs.find_one({"_id": ObjectId(data["lobby_id"])})
        # check cur_user_count == max_user_count. if so, do not allow the operation

        if old_lobby["max_user_count"] == old_lobby["cur_user_count"]:
            return JsonResponse(f"This lobby reached its capacity. Total capacity: {old_lobby['max_user_count']}...", safe=False )


    except Exception as e:
        return JsonResponse("An error has occured. Check lobby id please...", safe=False )
    
    try:
        user = accs.find_one({"_id": ObjectId(data["user_id"])})
    except Exception as e:
        return JsonResponse("An error has occured. Check user id please...", safe=False )
    

    lobbs.update_one({"_id": ObjectId(data["lobby_id"])},
                    {
                        "$inc": {"cur_user_count":1},
                        "$push": {"users": ObjectId(data["user_id"])}
                    })
    #TODO: it can take id's as strings. What if they come as ObjectId objects? 
    return JsonResponse(True, safe=False )



# add user to lobby
@api_view(["POST"])
def exit_lobby(request):
    print("exit_lobby endpoint has been reached")
    data = request.data

    """
    request model
     user_id,
     lobby_id
    """

    try:
        old_lobby = lobbs.find_one({"_id": ObjectId(data["lobby_id"])})
    except Exception as e:
        return JsonResponse("An error has occured. Check lobby id please...", safe=False )
    
    try:
        user = accs.find_one({"_id": ObjectId(data["user_id"])})
    except Exception as e:
        return JsonResponse("An error has occured. Check user id please...", safe=False )
    
    lobbs.update_one({"_id": ObjectId(data["lobby_id"])},
                    {
                        "$inc": {"cur_user_count":-1},
                        "$pull": {"users": {"$eq": ObjectId(data["user_id"])}}
                    })
    #TODO: it can take id's as strings. What if they come as ObjectId objects? 
    return JsonResponse(True, safe=False )



    







