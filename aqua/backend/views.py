
import os
import uuid

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
import backend.yolov5.detect as detect

@api_view(['POST'])
def yolov5_detection(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        print(image_file)
        image_name = str(uuid.uuid4()) + "_" + image_file.name  # Generate a unique filename using UUID
        save_path = os.path.join('C:/Users/esccy/Pictures/aquapics/', image_name)
        print(save_path)
        with open(save_path, 'wb') as file:
            for chunk in image_file.chunks():
                file.write(chunk)
        
        
        
        lst = list(detect.run(source=save_path))
        label = lst[0].split()[-1]
        # Perform YOLOv5 detection on the saved image
        label = label.rstrip(',')
        print(label)

        # Process the detection results and return a response
        response_data = {'results': label}
        return Response(response_data)
    else:
        return Response({'error': 'Invalid request'}, status=400)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'})
    else:
        return Response({'message': 'Invalid credentials'}, status=400)
    
@api_view (['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': 'Registration successful'})
