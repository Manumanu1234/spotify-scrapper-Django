from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from projectApp.models import Room
from projectApp.serialize import RoomSerialize,createRoomSerailizer,UpdateRoomSerailzer
from datetime import datetime
from django.contrib.sessions.models import Session
class RoomView(generics.CreateAPIView):
    queryset=Room.objects.all()
    serializer_class=RoomSerialize
    
class createRoomByUser(APIView):
    
    serializer_class=createRoomSerailizer
    def post(self,request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serialzed=self.serializer_class(data=request.data)
        if serialzed.is_valid():
            gust_can_pause=serialzed.data.get('gust_can_pause')
            vote_to_skip=serialzed.data.get('vote_to_skip')
            host=self.request.session.session_key
            queyset=Room.objects.filter(host=host)
            if queyset.exists():
                room=queyset[0]
                room.gust_can_pause=gust_can_pause
                room.vote_to_skip=vote_to_skip
                room.createdAt=datetime.now()
                self.request.session['room-code']=room.code
                room.save(update_fields=['gust_can_pause','vote_to_skip'])
            else:
                room=Room(host=host,gust_can_pause=gust_can_pause,vote_to_skip=vote_to_skip)
                room.save()
                self.request.session['room-code']=room.code
            return Response(RoomSerialize(room).data)
        return Response("not vlid")                       

class GetRoom(APIView):
    serailize_class=RoomSerialize
    def get(self,request):
        code=request.GET.get('code')
        if code!=None:
            room=Room.objects.filter(code=code)
            if len(room)>0:
                data=RoomSerialize(room[0]).data
                data['is_host']=self.request.session.session_key==room[0].host
                if (self.request.session.session_key==room[0].host):
                    print("yes this is the host")
                
                return Response(data)
            return Response('no room is found')
        return Response('no code is exist')    
class JoinRoom(APIView):
    serialze_class=RoomSerialize
    def post(self,request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code=request.data.get('code')
        if code!=None:
            room=Room.objects.filter(code=code)
            if len(room)>0:
                room=room[0]
                self.request.session['room-code']=code
                return Response({'status':True,'data':code})
            return Response({'status':False})
        return({'not code found'})
class Roomexist(APIView):
    serialize_class=RoomSerialize
    def get(self,request):
        valid=self.request.session.get('room-code')
        if valid!=None:
            dataoftheroom=Room.objects.filter(code=valid)
           # print(RoomSerialize(dataoftheroom).data)
            if len(dataoftheroom)>0:
               return Response({"status":True,"datas":RoomSerialize(dataoftheroom[0]).data})
            else:
               return Response({"status":False})
        else:
            return Response({"status":False})
class Leaving(APIView):
    def get(self,request):
        valid=self.request.session.get('room-code')
        hostid=self.request.session.session_key
        #print(valid,hostid)
        room_result=Room.objects.filter(host=hostid)
        if valid!=None:
            print(room_result)
            self.request.session.pop('room-code')
            if len(room_result)>0:
                print("in")
                room=room_result[0]
                room.delete()
            else:
                print("not")
        return Response({'status':True})        
class UpdateRoom(APIView):
    serialize_class=UpdateRoomSerailzer
    def post(self,request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serialized=self.serialize_class(data=request.data)
        if serialized.is_valid():
            gust_can_pause=serialized.data.get('gust_can_pause')
            vote_to_skip=serialized.data.get('vote_to_skip')
            code=serialized.data.get('code')
            quryset=Room.objects.filter(code=code)
            if quryset.exists():
                room=quryset[0]
                hostid=self.request.session.session_key
                if hostid!=room.host:
                    return Response({"msg":"you are not the hosted person"})
                else:
                    print("yes qury set us exist")
                    room.gust_can_pause=gust_can_pause
                    room.vote_to_skip=vote_to_skip
                    room.save(update_fields=['vote_to_skip','gust_can_pause'])
                    return Response({"msg":"sucess","data":code})        
            else:
                return Response({"msg":'This room is not available',"data":False})
        else:
            return Response({'msg':'field not valid',"data":False})      
            
            
            
                
            
            
            
                    
                
                
            
                


       

        
           
                     
        


    
    
 
# Create your views here.
