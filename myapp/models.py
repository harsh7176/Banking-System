from django.db import models



class Cust(models.Model):
 cust_id=models.IntegerField(primary_key=True)
 passwd=models.CharField(max_length=20)
 name=models.CharField(max_length=20)
 balance=models.FloatField(default=0)
 open_date=models.DateField(default=0)
 status=models.SmallIntegerField(default=0)

class Trans(models.Model):
 trans_id=models.AutoField(primary_key=True) 
 sendr=models.ForeignKey(Cust,on_delete=models.RESTRICT)
 recevr=models.IntegerField(default=0)
 val=models.FloatField(default=0)
 status=models.SmallIntegerField(default=0) 
 dat=models.DateField(default=0)

