from json import dumps, loads
import random
import string
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from bson import json_util
from Models.Lobby import Lobby
from Models.User import User

from MongoDB.utils import connectToMongo
from datetime import datetime
from bson.objectid import ObjectId

import json
# Create your views here.

def parse_json(data):
    return json.loads(json_util.dumps(data))



client = connectToMongo(password="seconduser")
db = client["MetaFuarDB"]
accs = db["Account"]
lobbs = db["Lobby"]
items = db["Items"]
fair_items = db["FairItems"]
inventories = db["Inventory"]

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@api_view(["POST"])
def account(request):
    data = request.data
    found_acc = accs.find_one({"email_address": data["email"]})
    if bool(found_acc):
        # means that account is previously saved
        # we need to generate new code and then update entry
        login_code = get_random_string(5)
        accs.update_one({"email_address": data["email"]}, {"$set":{"login_code": login_code}})

    else:
        login_code = get_random_string(5)
        id = accs.insert_one(User(data,login_code).__dict__ )
    
    return JsonResponse(login_code, safe=False )

@api_view(["POST"])
def verify_code(request):
    data = request.data
    found_acc = accs.find_one({"login_code": data["login_code"]})
    if bool(found_acc):
        return JsonResponse(found_acc["user_name"], safe=False )
    else:
        return JsonResponse("Hesap bulunamadi. Kodu yanlis girmis olabilir misiniz ?", safe=False )


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
    print(id.inserted_id)
    # Change here verify post 
    return JsonResponse(str(id.inserted_id), safe=False )

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

@api_view(["POST"])
def update_lobby(request):
    print("update_lobby endpoint has been reached")
    data = request.data
    """
    request model
     update_field,
     new_value,
     lobby_id
    
     
    """

    # TODO: verify field values
    if data["update_field"] == "name":
        lobbs.update_one({"_id": ObjectId(data["lobby_id"])}, {"$set":{"name": data["name"]}})
    elif data["update_field"] == "max_user_count":
        lobbs.update_one({"_id": ObjectId(data["lobby_id"])},{ "$set": {"max_user_count": data["max_user_count"]}})
    elif data["update_field"] == "organization":
        lobbs.update_one({"_id": ObjectId(data["lobby_id"])},{"$set": {"organization": data["organization"]}})
    else:
        return JsonResponse("Please give a valid update_field in body...", safe=False)
    
    return JsonResponse(True, safe=False)


# add user to lobby
@api_view(["POST"])
def join_lobby(request):
    print("create_lobby endpoint has been reached")
    data = request.data

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


# get all items
@api_view(["GET"])
def get_fair_items(request):
    fair_items_list_ids = parse_json(fair_items.find({}))
    # we will use this list to get specs of items in items list
    ids = [x["item_id"] for x in fair_items_list_ids]
    fair_items_list = []
    for i in range(len(ids)):
        res = items.find({"_id": ObjectId(ids[i]["$oid"])})
        fair_items_list.extend(parse_json(res))
    
    #here extract oid stuff from object
    for item in fair_items_list:
        item["_id"] = item["_id"]["$oid"]
    return JsonResponse(fair_items_list, safe=False)

# get item details
@api_view(["GET"])
def get_item(request):
    # expects id as string
    id = request.GET["item_id"]
    item = items.find({"_id": ObjectId(id)})
    return JsonResponse(parse_json(item), safe = False)

    
# add to users inventory
@api_view(["POST"])
def add_to_users_inventory(request):
    """
    request model
    user_id,
    item_id (from items table)
    """
    data = request.data
    newobj = {"base_item": ObjectId(data["base_item"]), "eklenme_tarihi": datetime.now()}
    res = inventories.update_one({"user": ObjectId(data["user"])}, {"$push":{"items":newobj}})
    return JsonResponse(True, safe = False)


# add item to inventory
@api_view(["POST"])
def add_to_inventory(request):
    """
    request model
    inventory_id,
    item_id (from items table)
    """
    data = request.data
    newobj = {"base_item": ObjectId(data["base_item"]), "eklenme_tarihi": datetime.now()}
    res = inventories.update_one({"_id": ObjectId(data["_id"])}, {"$push":{"items":newobj}})
    return JsonResponse(True, safe = False)


# remove item from user's inventory
@api_view(["POST"])
def remove_item_users_inventory(request):
    """
    request model
    user_id,
    item_id (from inventory items list)
    """
    data = request.data
    res = inventories.update_one({"user": ObjectId(data["user"])}, {"$pull":{"items":{"base_item": ObjectId(data["base_item"])}}})
    return JsonResponse(True, safe = False)


# remove item from inventory
@api_view(["POST"])
def remove_item_inventory(request):
    """
    request model
    inventory_id,
    item_id (from inventory items list)
    """
    data = request.data
    res = inventories.update_one({"_id": ObjectId(data["_id"])}, {"$pull":{"items":{"base_item": ObjectId(data["base_item"])}}})
    return JsonResponse(True, safe = False)

# update users balance
@api_view(["POST"])
def update_user_balance(request):
    """
    request_model
    user_id
    change_amount (can be -, +)
    """
    data = request.data
    res = inventories.update_one({"user": ObjectId(data["user"])}, {"$inc": {"balance":data["change_amount"]}})
    return JsonResponse(True, safe = False)
