from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

# from common.kafka_producer import send_kafka_message # Commented out for now

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Kafka message for user registration
        # send_kafka_message('user_registered', {'user_id': user.id, 'username': user.username, 'email': user.email})

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user