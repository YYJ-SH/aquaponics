
import os
import uuid
from backend.models import ImageData
from backend.serializers import ImageDataSerializer
from backend.models import Member
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
import backend.yolov5.detect as detect
import uuid
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
import paho.mqtt.publish as publish

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
        
        
        
        lst = list(detect.run(source=save_path, weights='C:/Users/esccy/Documents/aquaponics/aqua/backend/yolov5/six.pt'))
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
    
# @api_view (['POST'])
# def register_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     email = request.data.get('email')

#     if User.objects.filter(username=username).exists():
#         return Response({'message': 'Username already exists'}, status=400)

#     user = User.objects.create_user(username=username, password=password, email=email)
#     return Response({'message': 'Registration successful'})

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageData

class ImageUploadView(APIView):
    def post(self, request, format=None):
        # Get the image file from the request
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image file provided.'}, status=400)

        # Save the image file to a specific directory
        image_path = f'media/{image_file.name}'  # Modify the directory path as needed
        with open(image_path, 'wb') as file:
            for chunk in image_file.chunks():
                file.write(chunk)

        # Save the image path, sensor values, and Arduino ID to the database
        arduino_id = request.data.get('arduinoId')
        sensor1 = request.data.get('sensor1')
        sensor2 = request.data.get('sensor2')
        image_data = ImageData(arduino_id=arduino_id, image_path=image_path, sensor1=sensor1, sensor2=sensor2)
        image_data.save()

        return Response({'success': 'Image uploaded and data saved.'}, status=200)

@api_view(['POST'])
def register_member(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    device_id = request.data.get('device_id')

    # Check if the email already exists in the database
    if Member.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    # Create a new member
    member = Member(name=name, email=email, password=password, device_id=device_id)
    member.save()

    return Response({'message': 'Member registered successfully'})

@api_view(['POST'])
def store_image_data(request):
    arduino_id = request.data.get('arduino_id')
    sensor1 = request.data.get('sensor1')
    sensor2 = request.data.get('sensor2')

    # Create a new ImageData instance
    image_data = ImageData(arduino_id=arduino_id, sensor1=sensor1, sensor2=sensor2)

    # Save the image_data to the database
    image_data.save()

    return Response({'message': 'Image data stored successfully'})    
@api_view(['GET'])
def get_data_by_arduino_id(request, arduino_id):
    # Retrieve the most recent 5 items with the specified arduino_id
    image_data = ImageData.objects.filter(arduino_id=arduino_id).order_by('-date')[:5]

    # Serialize the image_data
    serializer = ImageDataSerializer(image_data, many=True)

    # Return the serialized data in the response
    return Response(serializer.data)
@api_view(['POST'])
def arduinopic_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # Generate a unique filename using UUID
        image_name = str(uuid.uuid4()) + "_" + image_file.name
        save_path = os.path.join('C:/Users/esccy/Pictures/arduinoWebpics', 'images', image_name)

        # Save the image to the specified directory
        with open(save_path, 'wb') as file:
            for chunk in image_file.chunks():
                file.write(chunk)

        # Create an instance of ImageData and save it to the database
        image_data = ImageData(
            arduino_id=request.POST.get('arduino_id'),
            image_path=os.path.join('images', image_name),
            sensor1=int(request.POST.get('sensor1')),
            sensor2=int(request.POST.get('sensor2'))
        )
        image_data.save()

        return Response("Image saved successfully.")
    else:
        return HttpResponseBadRequest("Invalid request.")
def led_on(request):
    # MQTT 브로커 정보
    mqtt_broker = "mqtt.gabol.kr"
    mqtt_port = 1883
    mqtt_topic = "control"

    # MQTT 메시지
    message = "On"

    # MQTT 메시지 발행
    publish.single(mqtt_topic, message, hostname=mqtt_broker, port=mqtt_port)

    # HTTP 응답
    return HttpResponse("LED를 켰습니다.")

def led_off(request):
    # MQTT 브로커 정보
    mqtt_broker = "mqtt.gabol.kr"
    mqtt_port = 1883
    mqtt_topic = "control"

    # MQTT 메시지
    message = "Off"

    # MQTT 메시지 발행
    publish.single(mqtt_topic, message, hostname=mqtt_broker, port=mqtt_port)

    # HTTP 응답
    return HttpResponse("LED를 껐습니다.")
def moter_off(request):
    # MQTT 브로커 정보
    mqtt_broker = "mqtt.gabol.kr"
    mqtt_port = 1883
    mqtt_topic = "control"

    # MQTT 메시지
    message = "MoterOff"

    # MQTT 메시지 발행
    publish.single(mqtt_topic, message, hostname=mqtt_broker, port=mqtt_port)

    # HTTP 응답
    return HttpResponse("모터를 껐습니다.")
def moter_on(request):
    # MQTT 브로커 정보
    mqtt_broker = "mqtt.gabol.kr"
    mqtt_port = 1883
    mqtt_topic = "control"

    # MQTT 메시지
    message = "MoterOn"

    # MQTT 메시지 발행
    publish.single(mqtt_topic, message, hostname=mqtt_broker, port=mqtt_port)

    # HTTP 응답
    return HttpResponse("모터를 켰습니다.")
def moter_once(request):
    # MQTT 브로커 정보
    mqtt_broker = "mqtt.gabol.kr"
    mqtt_port = 1883
    mqtt_topic = "control"

    # MQTT 메시지
    message = "MoterOnce"

    # MQTT 메시지 발행
    publish.single(mqtt_topic, message, hostname=mqtt_broker, port=mqtt_port)

    # HTTP 응답
    return HttpResponse("모터를 한 번 작동합니다.")
def dark_neo(request):
    # MQTT 브로커 정보
    mqtt_broker = "mqtt.gabol.kr"
    mqtt_port = 1883
    mqtt_topic = "control"

    # MQTT 메시지
    message = "DarkNeo"

    # MQTT 메시지 발행
    publish.single(mqtt_topic, message, hostname=mqtt_broker, port=mqtt_port)

    # HTTP 응답
    return HttpResponse("네오픽셀이 어두워졌어요.")