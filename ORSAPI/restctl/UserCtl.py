
  

from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import User
from service.forms import UserForm
from service.service.UserService import UserService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage

from django.http.response import JsonResponse
import json


class UserCtl(BaseCtl): 
    def get(self,request, params = {}):
        service=UserService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res["data"]})

    def delete(self,request, params = {}):
        service=UserService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            service.delete(params["id"])
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is Successfully deleted"
        else:
            res["error"]=True
            res["message"]="Data is not deleted"
        return JsonResponse({"data":res["data"]})

    def search(self,request, params = {}):
        json_request=json.loads(request.body)
        if(json_request):
            params["login_id"]=json_request.get("login_id",None)
        
        service=UserService()
        c=service.search(params)
        res={}
        data=[]
        for x in c:
            data.append(x.to_json())
        if(c!=None):
            res["data"]=data
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res})

    def form_to_model(self,obj,request):
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.firstName = request["firstName"]
        obj.lastName = request["lastName"]
        obj.login_id = request["login_id"] 
        obj.password = request["password"]
        obj.confirmpassword = request["confirmpassword"]
        obj.dob = request["dob"]
        obj.address = request["address"]
        obj.gender = request["gender"]
        obj.mobilenumber = request["mobilenumber"]
        obj.role_Id = request["role_Id"]
        obj.role_Name = request["role_Name"]
        return obj
    
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] =requestForm["dob"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] =requestForm["role_Id"]
    
    def save(self,request, params = {}):
        json_request=json.loads(request.body)

        self.request_to_form(json_request) 
        emsg=EmailMessage()
        emsg.to= [self.form["login_id"]]
        e={}
        e["login"]= self.form["login_id"]
        e["password"]=self.form["password"]
        emsg.subject= "ORS Registration Successful"    
      
        mailResponse=EmailService.send(emsg,"signUp",e)  
        r=self.form_to_model(User(), json_request)
        service=UserService()
        c=service.save(r)
        res={}
       
        if(mailResponse==1):
            res["data"]=r.to_json()
            res["error"]=False
            res["message"]="Data is Successfully saved"
           
        else:
            res["error"]=True
            res["message"]="Data is not saved"
        return JsonResponse({"data":res})
    

      
    def get_template(self):
        return "orsapi/User.html"          

        
    def get_service(self):
        return UserService()        


       



