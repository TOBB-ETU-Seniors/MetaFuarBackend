from json import dumps, loads
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from bson import json_util
from Models.User import User

from MongoDB.utils import connectToMongo
from datetime import datetime

# Create your views here.


client = connectToMongo(password="seconduser")
db = client["MetaFuarDB"]
accs = db["Account"]

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


