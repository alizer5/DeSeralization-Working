from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def student_detail(request,id):
    #This will get Student object instance with id
    stu=Student.objects.get(id=1) 
    # This wil convert stu into python native
    serializer=StudentSerializer(stu)
    # This will render python native into JSON
    # json_data=JSONRenderer().render(serializer.data)
    # #this will return json response
    # return HttpResponse(json_data,content_type='application/json')
    # By using JsonResponse we do not need to use JSONRenderer and HttpResponse
    return JsonResponse(serializer.data)


def student_list(request):
    #This will get Student object instance with id
    stu=Student.objects.all() 
    # This wil convert stu into python native
    serializer=StudentSerializer(stu,many=True)
    # This will render python native into JSON
    json_data=JSONRenderer().render(serializer.data)
    #this will return json response
    return HttpResponse(json_data,content_type='application/json')

def hello(request):
    return HttpResponse("Hello Django")

@csrf_exempt
def student_create(request):
    if request.method =="POST":
        json_data=request.body
        # send dat into stream
        stream=io.BytesIO(json_data)
        # Json Parser to parse data into Python Data
        pythondata=JSONParser().parse(stream)
        # made StudentSerializer class object and pass python data it converts data into complex data
        seriobj=StudentSerializer(data=pythondata)
        #  check if data is valid
        if seriobj.is_valid():
            seriobj.save()
            res={'msg':"Data Created"}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        
        json_data=JSONRenderer().render(seriobj.errors)
        return HttpResponse(json_data,content_type='application/json')
        
    
    