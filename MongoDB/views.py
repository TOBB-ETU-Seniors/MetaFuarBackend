from json import dumps
from rest_framework.decorators import api_view
from django.http.response import JsonResponse


from MongoDB.utils import connectToMongo
from datetime import datetime

# Create your views here.


client = connectToMongo(password="seconduser")

db = client["metafuar"]
accs = db["Accounts"]

@api_view(["GET", "PUT"])
def accountApi(request):

    found_accs = accs.find({})
    for acc in found_accs:
        print(acc)
    return JsonResponse(dumps(list(found_accs)), safe=False)


@api_view(["POST"])
def accountApi(request):
    id = accs.insert_one({
        "email_address": "alperdeneme@gmail.com",
        "login_type": "google",
        "creation_date": datetime.now()
    })
    # Change here verify post 
    return JsonResponse(True, safe=False )
 