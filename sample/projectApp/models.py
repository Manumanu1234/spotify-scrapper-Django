from django.db import models
import random
import string
def genearate_unique_code():
    lenght=6
    while True:
        code=''.join(random.choices(string.ascii_uppercase,k=lenght))
        if Room.objects.filter(code=code).count()==0:
            break
    return code;    


class Room(models.Model):
    code=models.CharField(max_length=8,default=genearate_unique_code,unique=True)
    host=models.CharField(max_length=50,unique=True)
    vote_to_skip=models.IntegerField(null=False,default=1)
    gust_can_pause=models.BooleanField(null=False,default=False)
    createdAt=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.host

  



      