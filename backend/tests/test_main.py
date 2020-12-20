from fastapi import status


def test_get_healthy(test_client):
    response = test_client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == True
