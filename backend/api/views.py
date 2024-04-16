from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note


class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    # only authenticated users can access this view (JWT)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            # adding author manually, as coded requirement in serializers
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDeleteView(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    # ensure user can only delete notes that belong to them
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    # built in generic view, automatically handles the creation of a new user
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # allow any user to create a new user
