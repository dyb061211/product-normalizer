from unittest.mock import Mock
from ai.client import LLMClient
import httpx
from openai import APITimeoutError,AuthenticationError
import ai.client
import pytest
from ai.exceptions import LLMConnectionError,LLMAuthenticationError

def test_create_response_success():
    llm_client=LLMClient(
        api_key="test-key",
        max_attempts=3
    )
    fake_response=Mock()
    fake_response.usage.input_tokens=100
    fake_response.usage.output_tokens=50
    fake_response.usage.total_tokens=150
    llm_client.client.responses.create=Mock(
        return_value=fake_response
    )
    result=llm_client.create_response(
        instructions="system",
        input_text="user",
        text={}
    )
    assert result is fake_response
    assert llm_client.client.responses.create.call_count==1
    llm_client.client.responses.create.assert_called_once_with(
        model=llm_client.model,
        instructions="system",
        input="user",
        text={}
    )

def test_create_response_retries_then_succeeds(monkeypatch):
    monkeypatch.setattr(
        ai.client.time,
        "sleep",
        lambda seconds:None
    )
    llm_client=LLMClient(
        api_key="test-key",
        max_attempts=3
    )
    request=httpx.Request(
        "POST",
        "https://api.deepseek.com/responses"
    )
    error1=APITimeoutError(request=request)
    error2=APITimeoutError(request=request)
    fake_response = Mock()
    fake_response.usage.input_tokens = 100
    fake_response.usage.output_tokens = 50
    fake_response.usage.total_tokens = 150
    llm_client.client.responses.create=Mock(
        side_effect=[
            error1,
            error2,
            fake_response
        ]
    )
    result=llm_client.create_response(
        instructions="system",
        input_text="user",
        text={}
    )
    assert result is fake_response
    assert llm_client.client.responses.create.call_count==3

def test_create_response_raise_after_all_retries_fail(monkeypatch):
    monkeypatch.setattr(
        ai.client.time,
        "sleep",
        lambda secondes:None
    )
    llm_client=LLMClient(
        api_key="test-key",
        max_attempts=3
    )
    request=httpx.Request(
        "POST",
        "https://api.deepseek.com/responses"
    )
    error1=APITimeoutError(request=request)
    error2=APITimeoutError(request=request)
    error3=APITimeoutError(request=request)
    llm_client.client.responses.create=Mock(
        side_effect=[
            error1,
            error2,
            error3
        ]
    )
    with pytest.raises(LLMConnectionError) as exc:
        llm_client.create_response(
            instructions="system",
            input_text="user",
            text={}
        )
    assert str(exc.value) == "LLM connection failed"
    assert llm_client.client.responses.create.call_count==3

def test_create_response_authentication_error_does_not_retry(monkeypatch):
    sleep_mock=Mock()
    monkeypatch.setattr(
        ai.client.time,
        "sleep",
        sleep_mock
    )
    llm_client=LLMClient(
        api_key="test-key",
        max_attempts=3
    )
    request=httpx.Request(
        "POST",
        "https://api.deepseek.com/responses"
    )
    response=httpx.Response(
        status_code=401,
        request=request
    )
    auth_error=AuthenticationError(
        "invalid api key",
        response=response,
        body={}
    )
    llm_client.client.responses.create=Mock(
        side_effect=auth_error
    )
    with pytest.raises(LLMAuthenticationError) as exc:
        llm_client.create_response(
            instructions="system",
            input_text="user",
            text={}
        )
    assert str(exc.value) == "LLM authentication failed"
    assert llm_client.client.responses.create.call_count==1
    sleep_mock.assert_not_called()

def test_llm_client_rejects_invalid_max_attempts():
    with pytest.raises(ValueError) as exc:
        LLMClient(
            api_key="test-key",
            max_attempts=0
        )
    assert str(exc.value) == "max_attempts must be at least 1"