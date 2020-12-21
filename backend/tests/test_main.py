from fastapi import status


def test_get_healthy(test_client):
    response = test_client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True


def test_completions(test_client):
    code = """\
#include <iostream>

struct S {
    int field1;
    float field2;
    double field3;
};

int main() {
    S s;
    s.
}
"""
    request = {
        "file_name": "code.cpp",
        "file_type": "cpp",
        "line_num": 11,
        "column_num": 7,
        "contents": code
    }
    response = test_client.post("/completions", json=request)
    assert response.status_code == status.HTTP_200_OK
    completions = sorted([c["insertion_text"] for c in response.json()["completions"]])
    assert completions == sorted(["field1", "field2", "field3", "operator=", "S::", "~S"])
