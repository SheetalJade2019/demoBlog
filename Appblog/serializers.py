from rest_framework import serializers
from .models import User

class User_Serializers(serializers.ModelSerializer):
   
    class Meta:
        model =  User
        # fields = ['contract_type_id','contract_type','contract_group']
        fields = "__all__"