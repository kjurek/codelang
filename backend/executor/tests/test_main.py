from fastapi import status
import os

from src import settings


def test_compile_success(test_client):
    code = """
    #include <iostream>

    int main() {
        std::cout << "Hello world!" << std::endl;
        return 0;
    }
    """
    request = {"session_id": "test_session", "contents": code, "flags": ["-std=c++11"]}
    response = test_client.post("/compile", json=request)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "stdout": "",
        "stderr": "",
        "returncode": 0
    }
    assert os.path.exists(os.path.join(settings.CODE_DIR, "test_session", "code.cpp"))
    assert os.path.exists(os.path.join(settings.CODE_DIR, "test_session", "out"))


def test_compile_failure(test_client):
    code = """
    #include <iostream>

    int main() {
        undefined_variable = 10;
        return 0;
    }
    """
    request = {"session_id": "test_session", "contents": code, "flags": ["-std=c++11"]}
    response = test_client.post("/compile", json=request)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["returncode"] == 1
    assert response.json()["stdout"] == ""
    assert "error: ‘undefined_variable’ was not declared in this scope" in response.json()["stderr"]


def test_execute_success(test_client):
    code = """
    #include <iostream>

    int main(int argc, char** argv) {
        for (int i = 1; i < argc; ++i) {
           std::cout << argv[i] << std::endl;
        }
        return 0;
    }
    """
    request_compile = {"session_id": "test_session", "contents": code, "flags": ["-std=c++11"]}
    response_compile = test_client.post("/compile", json=request_compile)
    assert response_compile.status_code == status.HTTP_200_OK

    request = {"session_id": "test_session", "arguments": ["arg1", "arg2"]}
    response = test_client.post("/execute", json=request)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "stdout": "arg1\narg2\n",
        "stderr": "",
        "returncode": 0,
    }


def test_execute_failure(test_client):
    code = """
    #include <iostream>

    int main(int argc, char** argv) {
        std::cerr << "Failure message" << std::endl;
        return 123;
    }
    """
    request_compile = {"session_id": "test_session", "contents": code, "flags": ["-std=c++11"]}
    response_compile = test_client.post("/compile", json=request_compile)
    assert response_compile.status_code == status.HTTP_200_OK
    assert response_compile.json()["stderr"] == ""
    assert response_compile.json()["returncode"] == 0

    request = {"session_id": "test_session", "arguments": []}
    response = test_client.post("/execute", json=request)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "stdout": "",
        "stderr": "Failure message\n",
        "returncode": 123,
    }


def test_execute_failure_session_doesnt_exist(test_client):
    request = {"session_id": "test_session", "arguments": []}
    response = test_client.post("/execute", json=request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Session doesn't exist"}


def test_execute_failure_code_isnt_compiled(test_client):
    session_dir = os.path.join(settings.CODE_DIR, "test_session")
    os.makedirs(session_dir)
    request = {"session_id": "test_session", "arguments": []}
    response = test_client.post("/execute", json=request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Code isn't compiled"}
