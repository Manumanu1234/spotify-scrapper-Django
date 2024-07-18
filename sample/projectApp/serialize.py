from rest_framework import serializers
from projectApp.models import Room

class RoomSerialize(serializers.ModelSerializer):
   class Meta:
        model=Room
        fields ='__all__'
        
class createRoomSerailizer(serializers.ModelSerializer):
   class Meta:
      model=Room
      fields=('vote_to_skip','gust_can_pause')
      
class UpdateRoomSerailzer(serializers.ModelSerializer):
   code = serializers.CharField()
   class Meta:
      model=Room
      fields=('vote_to_skip','gust_can_pause','code')
      
      
      