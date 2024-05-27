import datetime

import jwt
from django.db.models import Count
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, IdentificationNumber, Donation
from .serializers import UserSerializer, IdentificationNumberSerializer, DonationSerializer
from django.db import transaction


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        with transaction.atomic():
            id_number = IdentificationNumber.objects.filter(number=request.data['id_number']).first()

            if id_number is None:
                raise AuthenticationFailed('Sign-up unsuccessful. Contact your vendor.')

            if not request.data['id_number'].isdigit() or len(request.data['id_number']) != 13:
                return Response({"detail": "The ID number must contain exactly 13 digits."}, status=400)

            if not request.data['phoneNumber'].isdigit() or len(request.data['phoneNumber']) != 10:
                return Response({"detail": "The phone number must contain exactly 10 digits."}, status=400)

            userSerializer = UserSerializer(data=request.data)
            userSerializer.is_valid(raise_exception=True)
            userSerializer.save()
            # Récupérer les utilisateurs ayant déjà deux donateurs
            donator = User.objects.filter(id=userSerializer.data.get('id')).first()

            users_with_two_donors = Donation.objects.values('user').annotate(donor_count=Count('donator')).filter(
                donor_count=2)

            # Si des utilisateurs ont déjà deux donateurs
            if users_with_two_donors.exists():
                # Récupérer les IDs des utilisateurs ayant déjà deux donateurs
                users_with_two_donors_ids = [user['user'] for user in users_with_two_donors]

                # Récupérer le prochain utilisateur dans la table User qui n'a aucun donateur après ceux qui ont deux donateurs
                next_user = User.objects.exclude(id__in=users_with_two_donors_ids).filter(
                    id__gt=users_with_two_donors_ids[-1]).first()

                if next_user:
                    # Attribuer le prochain utilisateur comme donateur pour le nouvel utilisateur
                    Donation.objects.create(user=next_user, donator=donator, amount=500, status='pending')
                    return Response(userSerializer.data)

            if not users_with_two_donors.exists():
                # Sélectionner le premier utilisateur dans la table User comme le donateur
                first_user = User.objects.first()

                if first_user:
                    # Attribuer le premier utilisateur comme donateur pour le nouvel utilisateur
                    Donation.objects.create(user=first_user, donator=donator, amount=500, status='pending')
                    return Response(userSerializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Incorrect credentials!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect credentials!')
        if not user.is_active:
            raise AuthenticationFailed(' Your account is blocked. Please contact your supplier!')

        response = Response()
        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        response.data = {
            'message': 'success',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data,
            'status': response.status_code
        }
        response.set_cookie(key='token', value=str(refresh.access_token), httponly=True)
        return response


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk=None):

        user = User.objects.get(id=pk)
        if not user:
            raise Http404("User not found")

        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True

        user.save();
        serializer = UserSerializer(user)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class UsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UsersListActivityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Récupérer tous les utilisateurs actifs
        active_users = User.objects.filter(is_active=True)
        result = []

        for user in active_users:
            # Récupérer les dons de l'utilisateur
            donations = Donation.objects.filter(user=user)

            # Vérifier si l'utilisateur a moins de 2 dons
            if len(donations) < 2:
                # Si l'utilisateur a moins de 2 dons, l'ajouter à la liste de résultats
                user_serializer = UserSerializer(user)
                donations_serializer = DonationSerializer(donations, many=True)
                result.append({
                    'user': user_serializer.data,
                    'donations': donations_serializer.data
                })
            else:
                # Vérifier si l'utilisateur a au moins un don en 'confirmed' et un don en 'received'
                has_confirmed_donation = False
                has_received_donation = False
                has_pending_donation = False

                for donation in donations:
                    if donation.status == 'confirmed':
                        has_confirmed_donation = True
                    elif donation.status == 'received':
                        has_received_donation = True
                    elif donation.status == 'pending':
                        has_pending_donation = True

                # Si l'utilisateur a un don en 'confirmed' et un don en 'received', l'ajouter à la liste de résultats
                if has_confirmed_donation or has_pending_donation:
                    user_serializer = UserSerializer(user)
                    donations_serializer = DonationSerializer(donations, many=True)
                    result.append({
                        'user': user_serializer.data,
                        'donations': donations_serializer.data
                    })

        return Response(result)


class UserReceivedDonation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.filter(status='received')
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)


class UserDonationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        donations = Donation.objects.filter(user_id=user_id)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        donation = Donation.objects.get(id=pk)
        if not donation:
            raise Http404("User not found")
        if donation.status == 'received':
            return Response({"status": "success", "data": ''}, status=status.HTTP_200_OK)
        elif donation.status == 'confirmed':
            donation.status = 'received'
        else:
            donation.status = 'confirmed'
        donation.save();
        serializer = DonationSerializer(donation)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class UsersBlockedListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_active=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'success',
            'status': response.status_code
        }
        return response


class IdentificationNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            item = IdentificationNumber.objects.get(id=id)
            serializer = IdentificationNumberSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = IdentificationNumber.objects.all()
        serializer = IdentificationNumberSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IdentificationNumberSerializer(data=request.data)

        if not request.data['number'].isdigit() or len(request.data['number']) != 13:
            return Response({"detail": "The number must contain exactly 13 digits."}, status=400)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        item = IdentificationNumber.objects.get(id=pk)
        serializer = IdentificationNumberSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            item = IdentificationNumber.objects.get(id=pk)
            item.delete()
            return Response({"status": "success", "data": "Item Deleted"})
        except IdentificationNumber.DoesNotExist:
            return Response({"status": "error", "data": "Item not found"}, status=404)
