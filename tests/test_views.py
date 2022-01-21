import pytest
from django.conf import settings
from rest_framework.test import APIClient
from friendship.models import Friend, FriendshipRequest
from rest_friendship.serializers import FriendSerializer
from tests.serializers import UserTestSerializer
from .factories import UserFactory

# Add tests for serializers and settings import.

@pytest.mark.django_db(transaction=True)
def test_create_friend_request_without_message():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()

    client = APIClient()
    client.force_authenticate(user=user1)
    data = {'user_id': user2.id}
    response = client.post('/friends/add_friend/', data=data)
    assert response.status_code == 201
    assert response.data['from_user'] == user1.id
    assert response.data['to_user'] == user2.id
    assert response.data['message'] == ''
    assert FriendshipRequest.objects.filter(pk=response.data['id']).count() == 1


@pytest.mark.django_db(transaction=True)
def test_list_friends():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    Friend.objects.add_friend(
        user3,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    for friend_request in FriendshipRequest.objects.filter(to_user=user1):
        friend_request.accept()

    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.get('/friends/add_friend/')
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db(transaction=True)
def test_create_friend_request():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()

    client = APIClient()
    client.force_authenticate(user=user1)
    data = {'user_id': user2.username, 'message': 'Hi there!'}
    response = client.post('/friends/add_friend/', data=data)
    assert response.status_code == 201
    assert response.data['from_user'] == user1.id
    assert response.data['to_user'] == user2.id
    assert response.data['message'] == 'Hi there!'
    assert FriendshipRequest.objects.filter(pk=response.data['id']).count() == 1


@pytest.mark.django_db(transaction=True)
def test_create_friend_request_unauthenticated():

    # Create users
    user2 = UserFactory()

    client = APIClient()
    data = {'user_id': user2.username, 'message': 'Hi there!'}
    response = client.post('/friends/add_friend/', data=data)
    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
def test_list_friend_requests():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    Friend.objects.add_friend(
        user3,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.get('/friends/requests/')
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['to_user'] == user1.id


@pytest.mark.django_db(transaction=True)
def test_list_sent_friend_requests():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    Friend.objects.add_friend(
        user3,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    client = APIClient()
    client.force_authenticate(user=user2)
    response = client.get('/friends/sent_requests/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['to_user'] == user1.id


@pytest.mark.django_db(transaction=True)
def test_list_rejected_friend_requests():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    Friend.objects.add_friend(
        user3,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    for friend_request in FriendshipRequest.objects.filter(to_user=user1):
        friend_request.reject()

    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.get('/friends/rejected_requests/')
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['to_user'] == user1.id


@pytest.mark.django_db(transaction=True)
def test_accept_friend_request():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    fr = FriendshipRequest.objects.filter(to_user=user1).first()

    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.post('/friends/requests/accept_request/', data={'id':fr.id})
    assert response.status_code == 201
    assert Friend.objects.are_friends(user1, user2)


@pytest.mark.django_db(transaction=True)
def test_accept_friend_request_of_other_user():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    fr = FriendshipRequest.objects.filter(to_user=user1).first()

    client = APIClient()
    client.force_authenticate(user=user2)
    response = client.post('/friends/requests/accept_request/', data={'id':fr.id})
    assert response.status_code == 404
    assert not Friend.objects.are_friends(user1, user2)


@pytest.mark.django_db(transaction=True)
def test_reject_friend_request():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    fr = FriendshipRequest.objects.filter(to_user=user1).first()

    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.post('/friends/requests/reject_request/', data={'id':fr.id})
    assert response.status_code == 201
    assert not Friend.objects.are_friends(user1, user2)


@pytest.mark.django_db(transaction=True)
def test_reject_friend_request_of_other_user():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    fr = FriendshipRequest.objects.filter(to_user=user1).first()

    client = APIClient()
    client.force_authenticate(user=user2)
    response = client.post('/friends/requests/reject_request/', data={'id':fr.id})
    assert response.status_code == 404
    assert not Friend.objects.are_friends(user1, user2)


@pytest.mark.django_db(transaction=True)
def test_delete_friend():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    Friend.objects.add_friend(
        user3,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    for friend_request in FriendshipRequest.objects.filter(to_user=user1):
        friend_request.accept()
    
    friend_obj = Friend.objects.are_friends(user1, user2)

    assert friend_obj
    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.post('/friends/remove_friend/', data={'id':friend_obj.id})
    assert response.status_code == 204
    assert response.data['message'] == 'deleted'
    assert not Friend.objects.are_friends(user1, user2)


@pytest.mark.django_db(transaction=True)
def test_delete_friend_not_your_friend():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    for friend_request in FriendshipRequest.objects.filter(to_user=user1):
        friend_request.accept()
        
    friend_obj = Friend.objects.are_friends(user1, user3)

    assert not friend_obj
    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.post('/friends/remove_friend/', data={'id':friend_obj.id})
    assert response.status_code == 304
    assert response.data['message'] == 'not deleted'
