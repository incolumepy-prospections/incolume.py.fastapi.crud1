import pytest 
from fastapi import HTTPException
from fastapi.testclient import TestClient
import json


class TestAPI:
    @pytest.mark.parametrize(
        ['method', 'endpoint', 'json_data', 'status', 'content'],
        (
            pytest.param('get', '/', None, 404, {'detail': 'Not Found'}),
            pytest.param(
                'get',
                '/users', 
                None,
                200, 
                [
                    {'age': 28, 'date_joined': '2021-12-01', 'state': 'São Paulo', 'username': 'ada'}, 
                    {'age': 19, 'date_joined': '2021-12-02', 'state': 'Distrito Federal', 'username': 'ana'}, 
                    {'age': 52, 'date_joined': '2021-12-03', 'state': 'Acre', 'username': 'acã'},
                ]
            ),
            pytest.param('get', '/users/ada', None, 200, {'username': 'ada', 'date_joined': '2021-12-01', 'state': 'São Paulo', 'age': 28}),
            pytest.param(
                'post', 
                '/users', 
                {"username": "ava", "date_joined": "2023-04-27T19:49:02.843Z", "state": "Paraíba", "age": 10}, 
                200, 
                {'message': 'Successfully created user: ava'},
                # marks=pytest.mark.skip,
            ),
            pytest.param(
                'put', 
                '/users', 
                {'username': 'ava', 'date_joined': '2023-04-27T19:49:02.843Z', 'state': 'Goiás', 'age': 18}, 
                200, 
                {'message': 'Successfully updated user ava'},
                # marks=pytest.mark.skip,
            ),
            pytest.param(
                'patch', 
                '/users', 
                {'username': 'ava', 'date_joined': '2023-04-27T19:49:02.843000Z'}, 
                200, 
                {'message': 'Successfully updated user ava'},
                # marks=pytest.mark.skip,
            ),
            pytest.param(
                'delete', 
                '/users/ava', 
                None, 
                200, 
                {"message": "Successfully deleted user ava"},
                # marks=pytest.mark.skip,
            ),
            pytest.param(
                'post', 
                '/users', 
                {'username': 'ana', 'date_joined': '2023-04-27T19:49:02.843000Z'}, 
                409, 
                {"detail":"Cannot create user. Username ana already exists"}, 
                # marks=[pytest.mark.skip]
            ),
            pytest.param(
                'get', 
                '/users/ava', 
                {}, 
                404, 
                {'detail': 'Username ava not found'}, 
                # marks=[pytest.mark.skip]
                ),
        ),
    )
    def test_endpoint(self, method, endpoint, json_data, status, content, client: TestClient) -> None:
        match method:
            case 'get':
                response = client.get(endpoint)
            case 'post':
                response = client.post(endpoint, json=json_data)
            case 'put':
                response = client.put(endpoint, json=json_data)
            case 'patch':
                response = client.patch(endpoint, json=json_data)
            case 'delete':
                response = client.delete(endpoint)

        assert response.status_code == status, response.text
        data = response.json()
        assert data == content
