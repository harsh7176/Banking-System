from django.shortcuts import render

from datetime import date

from .models import Cust,Trans

from django.http import HttpResponse


def home(req):
 return render(req,'home.html',{})


def display(req):
#  print(req.POST)
 if 'adlog' in req.POST:
  id=req.POST['id']
  passwd=req.POST['passwd']
  if id!=str(100) or passwd!='harsh':
   return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px;"><center><form action="/"><button>Back to Home</button></form><h3>Wrong credentials..</h3></center></body>')
  else:
   return render(req,'admin.html',{})
 elif 'login' in req.POST:
  try:
   o=Cust.objects.get(cust_id=req.POST['id'])
   if o.cust_id==100 or o.passwd=='harsh' or o.passwd!=req.POST['passwd']:
    return HttpResponse('<center><form action="/"><button>Back to Home</button></form>Wrong credentials..</center>')
   else:
    return render(req,'det.html',{'id':o.cust_id,'name':o.name,'passwd':o.passwd,'login':'Login','bal':o.balance,'date':o.open_date,'status':o.status})
  except:
   return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px;"><center><form action="/"><button>Back to Home</button></form><h3>Wrong credentials..</h3></center></body>')
  



def admin(req):
 print(req.GET)
 if 'newac' in req.GET:
  return render(req,'newacc.html',{})
 elif 'delete' in req.GET:
  return render(req,'delete.html',{})
 elif 'block' in req.GET:
  return render(req,'block.html',{}) 
 elif 'update' in req.GET:
  return render(req,'update.html',{})  
 elif 'changepass' in req.GET:
  return render(req,'change.html',{})  
 elif 'update' in req.GET:
  return render(req,'update.html',{})
 elif 'revert' in req.GET:
  return render(req,'revert.html',{})



def new(req):
 try: 
  o=Cust.objects.get(cust_id=req.POST['id'])
  return HttpResponse('Customer Id already exists..')
 except: 
  o=Cust.objects.create(cust_id=req.POST['id'],passwd=req.POST['passwd'],name=req.POST['name'],balance=req.POST['bal'],open_date=req.POST['dat'],status=1)
  o.save()
  return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px;"><center><form action="/"><button>Back to Home</button></form><h2>Account created Successfully....</h2></center></body>')



def dele(req):
 try:
  n=req.POST['id']
  o=Cust.objects.get(cust_id=req.POST['id'])
  if o.passwd!=req.POST['passwd']:
   return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px;"><center><form action="/"><button>Back to Home</button></form>Customer Id does not exists..</center></body>')
  else:
   o.status=0
   o.save()
   return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px;"><center><form action="/"><button>Back to Home</button></form>Customer deleted...</center></body>')
 except:
  return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px;"><center><form action="/"><button>Back to Home</button></form>Customer Id does not exists..</center></body>')  
  

def block(req):
 try:
  o=Cust.objects.get(cust_id=req.POST['id'])
  if o.passwd!=req.POST['passwd'] or o.status==0:
   return HttpResponse('Customer Id does not exists  or  is blocked already ..')
  else:
   o.status=0
   o.save()
   return HttpResponse('Customer Blocked...')
 except:
  return HttpResponse('Customer Id does not exists..')  

def change(req):
 try:
  o=Cust.objects.get(cust_id=req.POST['id'])
  if o.passwd!=req.POST['passwd'] or o.status==0:
   return HttpResponse('Customer Id does not exists  or  is blocked /deleted ..')
  else:
   return render(req,'newpass.html',{'id':o.cust_id})
 except:
  return HttpResponse('Customer Id does not exists..') 

def newpass(req):
 p1=req.POST['passwd']
 p2=req.POST['repasswd']
 if p1!=p2:
  return HttpResponse('Two Passwords  did not  match')
 else:
  o=Cust.objects.get(cust_id=req.POST['id'])
  o.passwd=p1
  o.save()
  return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px;"><center><form action="/"><button>Back to Home</button></form>New Password saved successfully....</center></body>')  


def update(req):
 try:
  o=Cust.objects.get(cust_id=req.POST['id'])
  if o.passwd!=req.POST['passwd'] or o.status==0:
   return HttpResponse('Customer Id does not exists  or  is blocked /deleted ..')
  else:
   return render(req,'updatefinal.html',{'id':o.cust_id})
 except:
  return HttpResponse('Customer Id does not exists..') 

def updatefinal(req):
 o=Cust.objects.get(cust_id=req.POST['id'])
 o.name=req.POST['name']
 o.balance=req.POST['bal']
 o.open_date=req.POST['dat']
 o.status=1
 o.save()
 return HttpResponse('Account details updated successfully...')



def modify(req):
 if 'changepass' in req.POST:
   return render(req,'newpass.html',{'id':int(req.POST['id']),'passwd':req.POST['passwd']})
 elif 'sendmoney' in req.POST:
   return render(req,'trans.html',{'id':int(req.POST['id']),'bal':float(req.POST['bal'])})
 elif 'showtrans' in req.POST:
   s=list(Trans.objects.filter(sendr_id=int(req.POST['id'])).values())
   r=list(Trans.objects.filter(recevr=int(req.POST['id'])).values())
   return render(req,'showtrans.html',{'r':r,'s':s})

def pay(req):
 if float(req.POST['sbal'])<float(req.POST['amt']):
  return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px"><center><form action="/"><button>Back to Home</button></form>Balance Not Sufficient...</center></body>')
 try:
  o=Cust.objects.get(cust_id=int(req.POST['rid']))
  if o.status==0:  
   return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px"><center><form action="/"><button>Back to Home</button></form>Receiver dont have account in bank... OR is blocked at current moment</center></body>')
  s=Cust.objects.get(cust_id=int(req.POST['sid']))
  # print(req.POST['amt'])
  if int(req.POST['amt']) < 0:
    return HttpResponse('<body style="background-color:#87CEEB; margin-top:50px"><center><form action="/"><button>Back to Home</button></form><h3>Invalid amount...</h3></center></body>')
  s.balance=float(req.POST['sbal'])-float(req.POST['amt'])
  s.save()
  o.balance=o.balance+float(req.POST['amt'])
  o.save()
  t=Trans.objects.create(recevr=o.cust_id,val=float(req.POST['amt']),status=1,sendr_id=Cust.objects.get(cust_id=req.POST['sid']).cust_id,dat=date.today())
  t.save()
  return HttpResponse('<body style="background-color:#87CEEB; margin-top:50px"><center><form action="/"><button>Back to Home</button></form><h3>Transaction successfull...</h3></center></body>')
 except Exception as e:
  print(e)
  return HttpResponse('<body style="background-color:#87CEEB;margin-top:50px"><center><form action="/"><button>Back to Home</button></form>Receiver dont have account in bank... OR is blocked  ar current moment OR invalid amount</center></body>')



def revert(req):
  try:
   o=Cust.objects.get(cust_id=req.POST['id'])
   if o.passwd!=req.POST['passwd'] or o.status==0:
    return HttpResponse('Customer Id does not Exist or is blocked at current moment..') 
   s=list(Trans.objects.filter(sendr_id=int(req.POST['id'])).values())
   r=list(Trans.objects.filter(recevr=int(req.POST['id'])).values())
   return render(req,'showtrans2.html',{'r':r,'s':s})  
  except:
   return HttpResponse('Customer Id does not Exist')
  
 
def deltrans(req):
 try:
  o=Trans.objects.get(trans_id=req.POST['tid'])
  s=Cust.objects.get(cust_id=o.sendr_id)
  r=Cust.objects.get(cust_id=o.recevr)
  s.balance=s.balance+o.val
  r.balance=r.balance-o.val
  s.save()
  r.save()
  Trans.objects.get(trans_id=req.POST['tid']).delete()
  return HttpResponse('Transaction Deleted Successfully...')
 except: 
  return HttpResponse('Invalid Transaction Id')  

  

 
  
#by harsh mehta




  
