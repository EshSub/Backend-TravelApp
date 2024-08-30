from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)            
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new message
        self.perform_create(serializer)
        
        # Get the conversation ID from the newly created message
        conversation_id = serializer.validated_data['conversation'].conversation_id
        current_message = serializer.validated_data['message']

        # Retrieve the last 20 messages from the conversation
        # messages = Message.objects.filter(conversation_id=conversation_id).order_by('-date', '-time')[:20]
        
        # Create a JSON representation of the conversation history
        # messages_json = self.create_conversation_json(messages)
        # message_json = messages.values('date', 'time', 'message', 'place')        

        # If the conversation is AI-based, pass the conversation ID and current message to the AI response function
        conversation = Conversation.objects.get(conversation_id=conversation_id)

        # If the conversation is AI-based, pass the JSON to the AI response function
        # conversation = Conversation.objects.get(conversation_id=conversation_id)

        if conversation.isAI:
            ai_response = self.get_response_AI(conversation_id, current_message)
            # Optionally, save the AI response as a new message in the conversation
            Message.objects.create(
                conversation=conversation,
                date=serializer.validated_data['date'],
                time=serializer.validated_data['time'],
                message=ai_response
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_conversation_json(self, messages):
        conversation_history = []
        for message in messages:
            conversation_history.append({
                'date': message.date.isoformat(),
                'time': message.time.isoformat(),
                'message': message.message,
                'place': message.place.place_name if message.place else None,
                'guide': message.guide.username if message.guide else None,
            })
        return conversation_history
    
    def get_response_AI(self, conversation_id, current_message):
        # Placeholder function for AI response
        return "This is an AI generated response"