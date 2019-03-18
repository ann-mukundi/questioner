"""
Views operations for the answers
"""
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from .models import Answer
from questions.models import Question
from meetups.models import Meetup
from .serializers import AnswerSerializer
from utils.validators import valid_string


class AnswersPostView(APIView):
    """
    Views for posting an answer
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, meetupId):
        """
        Post an answer
        """
        try:
            queryset = Meetup.objects.get(id=meetupId)
        except ValidationError:
            return Response(
                {
                    "error": "Meetup doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            queryset = Question.objects.all()
            request.data['creator'] = request.user
            serializer = AnswerSerializer(data=request.data)
            answer_body = Answer.objects.filter(body=request.data.get('body'))

            if serializer.is_valid():
                if answer_body:
                    return Response(
                        {
                            "error": "Answer already exist"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                Answer.objects.update_or_create(
                    body=request.data.get('body').strip(),
                    defaults={
                        'question': get_object_or_404(queryset, id=id),
                        'creator': request.data.get('creator')
                    }
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError:
            return Response(
                {
                    "error": "Question doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UpdateAnswer(APIView):
    """
    Deals with updating a specific answer
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, meetupId, questionId, answerId):
        try:
            queryset = Meetup.objects.get(id=meetupId)
        except ValidationError:
            error = {'error': 'The specified meetup does not exist'}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

        try:
            queryset = Question.objects.get(id=questionId)
        except ValidationError:
            error = {'error': 'The specified question does not exist'}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

        try:
            answer = Answer.objects.get(id=answerId)
            userid = request.user.id
            if userid != answer.creator.id:
                response = Response(data={'error': 'You cannot edit this answer. You did not post it'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            elif valid_string(request.data.get('body')) == False:
                response = Response(data={'error': 'Please enter a valid answer'},
                                    status=status.HTTP_400_BAD_REQUEST
                                    )
            elif userid == answer.creator.id:
                qs = Answer.objects.filter(
                    body=request.data.get('body'))
                qs = qs.exclude(pk=answer.id)
                if qs.exists():
                    return Response(
                        data={'Error': 'That answer already exists'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
                newbody = request.data.get('body').strip()
                answer.body = newbody
                answer.save()
                serializer = AnswerSerializer(answer)
                context = {
                    'message': 'You have successfully updated the answer',
                    'data': serializer.data
                }
                response = Response(
                    data=context,
                    status=status.HTTP_201_CREATED
                )
            return response

        except ValidationError:
            error = {'error': 'The specified answer does not exist'}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)