"""
Views for operations performed on meetups
"""
from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import Meetup, Tag, Image
from .serializers import MeetupSerializer, TagSerializer, FetchMeetupSerializer
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.validators import valid_meetup
from rest_framework.request import Request
from typing import Tuple
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
import json


class MeetupViews(APIView):
    """
    Views for meetup endpoints
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Post Endpoint for creating meetup
        POST /api/auth/meetups
        """
        is_valid_meetup, errors = valid_meetup(request)
        if is_valid_meetup:
            request.data['creator'] = request.user
            tags = request.data.get('tags')
            images = request.data.get('images')
            tag_list = []
            image_list = []
            if tags:
                for tag in tags:
                    tag_object, created = Tag.objects.update_or_create(
                        tag_name=tag,
                        defaults={
                            'tag_name': tag
                        }
                    )
                    tag_list.append(tag_object)
            if images:
                for image in images:
                    image_object, created = Image.objects.update_or_create(
                        image_url=image,
                        defaults={
                            'image_url': image
                        }
                    )
                    image_list.append(image_object)
            data = request.data
            serializer = MeetupSerializer(data=data)
            if not (request.user.is_staff):
                context = {
                    'error': 'Admin only can create meetup'
                }
                response = Response(
                    context,
                    status.HTTP_401_UNAUTHORIZED
                )
            elif serializer.is_valid():
                data = request.data
                meetup, created = Meetup.objects.update_or_create(
                    title=data.get('title'),
                    location=data.get('location'),
                    scheduled_date=data.get('scheduled_date'),
                    defaults={
                        'body': data.get('body'),
                        'creator': data.get('creator')
                    }
                )
                for image_object in image_list:
                    meetup.image_url.add(image_object)
                for tag_item in tag_list:
                    meetup.tags.add(tag_item)
                response = Response({
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED
                },
                    status=status.HTTP_201_CREATED
                )
            else:
                response = Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            response = Response(
                data=errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return response


class GetAllMeetups(APIView):
    """
    Class view for requesting all meetups
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        """
        A GET endpoint for getting all meetups in the database
        GET /api/meetups/
        """
        meetups = Meetup.objects.all()
        response = None
        if not meetups:
            response = Response({
                "error": "There are no meetups",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 1
            result_page = paginator.paginate_queryset(meetups, request)
            serializer = FetchMeetupSerializer(result_page, many=True)
            response = paginator.get_paginated_response(serializer.data)
        return response


class GetSpecificMeetup(APIView):
    """
    Class for handling get of specific meetups
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request, meetupid: str) -> Response:
        """
        A GET endpoint for getting specific meetup
        GET /api/meetups/<meetupId>
        """
        response = {}
        try:
            meetup = Meetup.objects.get(id=meetupid)
            serializer = FetchMeetupSerializer(meetup)
            response = {
                "data": [serializer.data],
                "status": status.HTTP_200_OK
            }
        except:
            response = {
                'error': 'A meetup with that id does not exist',
                'status': status.HTTP_404_NOT_FOUND
            }
        return Response(
            data=response,
            status=response.get('status')
        )


class GetUpcomingMeetups(APIView):
    """
    Class for handling the get of upcoming meetups
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        """
        Gets upcoming meetups
        GET /api/meetups/upcoming/
        """
        upcoming_meetups = Meetup.objects.filter(
            scheduled_date__gte=timezone.now())
        if upcoming_meetups:
            paginator = PageNumberPagination()
            paginator.page_size = 1
            result_page = paginator.paginate_queryset(
                upcoming_meetups, request)
            serializer = FetchMeetupSerializer(result_page, many=True)
            response = paginator.get_paginated_response(serializer.data)
        else:
            response = Response(
                data={
                    'error': 'There are no upcoming meetups',
                    'status': status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return response
