from json import dumps, loads
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from bson import json_util

from MongoDB.utils import connectToMongo
from datetime import datetime

# Create your views here.


client = connectToMongo(password="seconduser")

db = client["metafuar"]
accs = db["Accounts"]

@api_view(["GET","POST"])
def accountApi(request):
    if request.method == "GET":
        found_accs = accs.find({})
        return JsonResponse(loads(json_util.dumps(list(found_accs))), safe=False)
    elif request.method == "POST":
        # id = accs.insert_one({
        # "email_address": "alperdeneme@gmail.com",
        # "login_type": "google",
        # "creation_date": datetime.now()
        # })

        print(json_util.dumps(request.data))
        # Change here verify post 
        return JsonResponse(True, safe=False )
