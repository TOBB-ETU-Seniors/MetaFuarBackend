from rest_framework import serializers
from MongoDB.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("_id", "mail_address", "login_type", "creation_date")


"""
_id = models.AutoField(primary_key=True)
mail_address = models.EmailField()
login_type = models.CharField(max_length=20)
creation_date = models.DateTimeField()

"""