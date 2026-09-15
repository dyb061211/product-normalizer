from unittest.mock import Mock
import ai.listing_service
from ai.listing_service import generate_listing
from ai.schemas import ProductInput,GeneratedListing
import pytest
from ai.exceptions import LLMOutputError
from ai.prompts import SYSTEM_PROMPT

def test_generate_listing_success(monkeypatch):
    product=ProductInput(
        sku="A001",
        title="Portable Camping Chair",
        color="Green",
        category="Outdoor",
        price=29.99
    )
    fake_response = Mock()
    fake_response.output_text = """
    {
        "sku": "A001",
        "listing_title": "Portable Green Camping Chair",
        "bullet_points": [
            "Portable design for outdoor use",
            "Green finish for outdoor settings",
            "Suitable for camping and travel"
        ],
        "description": "A portable green camping chair designed for outdoor activities."
    }
    """
    fake_client = Mock()
    fake_client.create_response.return_value = fake_response
    monkeypatch.setattr(
        ai.listing_service,
        "LLMClient",
        Mock(return_value=fake_client)
    )
    result = generate_listing(product)
    assert isinstance(result, GeneratedListing)
    assert result.sku == "A001"
    assert result.listing_title == "Portable Green Camping Chair"
    assert len(result.bullet_points) == 3

def test_generate_listing_raises_when_llm_returns_invalid_json(monkeypatch):
    product = ProductInput(
        sku="A001",
        title="Portable Camping Chair",
        color="Green",
        category="Outdoor",
        price=29.99
    )
    fake_response = Mock()
    fake_response.output_text = "this is not json"
    fake_client = Mock()
    fake_client.create_response.return_value = fake_response
    monkeypatch.setattr(
        ai.listing_service,
        "LLMClient",
        Mock(return_value=fake_client)
    )
    with pytest.raises(LLMOutputError) as exc:
        generate_listing(product)
        assert str(exc.value) == "Invalid LLM output"
    assert fake_client.create_response.call_count == 1

def test_generate_listing_raises_when_schema_validation_fails(monkeypatch):
    product = ProductInput(
        sku="A001",
        title="Portable Camping Chair",
        color="Green",
        category="Outdoor",
        price=29.99
    )
    fake_response = Mock()
    fake_response.output_text = """
    {
        "sku": "A001",
        "listing_title": "Portable Green Camping Chair",
        "bullet_points": [
            "Portable design",
            "Green color"
        ],
        "description": "A portable camping chair."
    }
    """
    fake_client = Mock()
    fake_client.create_response.return_value = fake_response
    monkeypatch.setattr(
        ai.listing_service,
        "LLMClient",
        Mock(return_value=fake_client)
    )
    with pytest.raises(LLMOutputError) as exc:
        generate_listing(product)
    assert str(exc.value) == "Invalid LLM output"

def test_generate_listing_calls_dependencies_correctly(monkeypatch):
    product = ProductInput(
        sku="A001",
        title="Portable Camping Chair",
        color="Green",
        category="Outdoor",
        price=29.99
    )
    prompt_mock = Mock(
        return_value="FAKE USER PROMPT"
    )
    monkeypatch.setattr(
        ai.listing_service,
        "build_listing_prompt",
        prompt_mock
    )
    fake_response = Mock()
    fake_response.output_text = """
    {
        "sku": "A001",
        "listing_title": "Portable Green Camping Chair",
        "bullet_points": [
            "Portable design",
            "Green finish",
            "Suitable for outdoor use"
        ],
        "description": "A portable camping chair."
    }
    """
    fake_client = Mock()
    fake_client.create_response.return_value = fake_response
    client_class_mock = Mock(
        return_value=fake_client
    )
    monkeypatch.setattr(
        ai.listing_service,
        "LLMClient",
        client_class_mock
    )
    result = generate_listing(product)
    prompt_mock.assert_called_once_with(product)
    client_class_mock.assert_called_once_with()
    expected_schema = GeneratedListing.model_json_schema()
    expected_text = {
        "format": {
            "type": "json_schema",
            "name": "generated_listing",
            "schema": expected_schema
        }
    }
    fake_client.create_response.assert_called_once_with(
        instructions=SYSTEM_PROMPT,
        input_text="FAKE USER PROMPT",
        text=expected_text
    )
    assert isinstance(result, GeneratedListing)