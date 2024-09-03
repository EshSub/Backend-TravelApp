from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from datetime import datetime
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        # add user to request data
        request.data['user'] = user.id
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
        conversation_id = serializer.validated_data['conversation'].id  # Corrected field reference
        current_message = serializer.validated_data['message']
        messages = Message.objects.filter(conversation_id=conversation_id).order_by('-date', '-time')[:5]
        message_history = messages.values('date', 'time', 'message')

        conversation = Conversation.objects.get(id=conversation_id)  # Corrected field reference
        print("conversation", conversation)

        if conversation.isAI:
            ai_response = self.get_response_AI(conversation_id, message_history)

            Message.objects.create(
                conversation_id=conversation.id,  # Corrected field reference  
                date=datetime.now().date(),  # Current date
                time=datetime.now().time(),  # Current time
                message=ai_response,
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
