"""
Tests for Azure OpenAI support in browser-use-mcp-server.

This module tests the initialization of LLMs with both standard OpenAI
and Azure OpenAI configurations.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.server import initialize_llm


@pytest.fixture
def standard_openai_env():
    """Set up environment for standard OpenAI tests."""
    original_env = {k: v for k, v in os.environ.items()}
    
    # Set standard OpenAI variables
    os.environ["OPENAI_API_KEY"] = "test-key-standard"
    
    # Clear Azure variables if they exist
    for var in ["OPENAI_API_TYPE", "OPENAI_API_BASE", "AZURE_OPENAI_DEPLOYMENT"]:
        if var in os.environ:
            del os.environ[var]
    
    yield
    
    # Restore original environment
    for k in list(os.environ.keys()):
        if k not in original_env:
            del os.environ[k]
    for k, v in original_env.items():
        os.environ[k] = v


@pytest.fixture
def azure_openai_env():
    """Set up environment for Azure OpenAI tests."""
    original_env = {k: v for k, v in os.environ.items()}
    
    # Set Azure OpenAI variables
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_KEY"] = "test-key-azure"
    os.environ["OPENAI_API_BASE"] = "https://test.openai.azure.com"
    os.environ["OPENAI_API_VERSION"] = "2023-05-15"
    os.environ["AZURE_OPENAI_DEPLOYMENT"] = "test-deployment"
    
    yield
    
    # Restore original environment
    for k in list(os.environ.keys()):
        if k not in original_env:
            del os.environ[k]
    for k, v in original_env.items():
        os.environ[k] = v


@pytest.fixture
def incomplete_azure_env():
    """Set up environment with incomplete Azure OpenAI configuration."""
    original_env = {k: v for k, v in os.environ.items()}
    
    # Set only partial Azure config
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_KEY"] = "test-key-azure"
    
    # Remove other required Azure variables
    for var in ["OPENAI_API_BASE", "AZURE_OPENAI_DEPLOYMENT"]:
        if var in os.environ:
            del os.environ[var]
    
    yield
    
    # Restore original environment
    for k in list(os.environ.keys()):
        if k not in original_env:
            del os.environ[k]
    for k, v in original_env.items():
        os.environ[k] = v


# Test standard OpenAI without using mocks
def test_standard_openai_initialization(standard_openai_env):
    """Test that standard OpenAI initialization uses the right parameters."""
    llm = initialize_llm()
    
    # Verify it's a ChatOpenAI instance
    from langchain_openai import ChatOpenAI
    assert isinstance(llm, ChatOpenAI)
    
    # Check that key parameters are set correctly
    assert llm.model_name == 'gpt-4o'
    assert llm.temperature == 0.0


@patch('langchain_openai.AzureChatOpenAI')
def test_azure_openai_initialization(mock_azure_chat_openai, azure_openai_env):
    """Test that Azure OpenAI is initialized correctly with the right parameters."""
    mock_instance = MagicMock()
    mock_azure_chat_openai.return_value = mock_instance
    
    # Initialize LLM
    llm = initialize_llm()
    
    # Verify AzureChatOpenAI was called with Azure parameters
    mock_azure_chat_openai.assert_called_once()
    args, kwargs = mock_azure_chat_openai.call_args
    
    # Verify key parameters for Azure were included
    assert 'deployment_name' in kwargs
    assert kwargs['deployment_name'] == 'test-deployment'
    assert 'api_key' in kwargs
    assert kwargs['api_key'] == 'test-key-azure'
    assert 'azure_endpoint' in kwargs
    assert kwargs['azure_endpoint'] == 'https://test.openai.azure.com'
    assert 'openai_api_version' in kwargs
    assert kwargs['openai_api_version'] == '2023-05-15'


def test_incomplete_azure_configuration(incomplete_azure_env):
    """Test that initialization fails with incomplete Azure configuration."""
    # Verify that initialization raises ValueError
    with pytest.raises(ValueError) as excinfo:
        llm = initialize_llm()
    
    # Check that the error message mentions missing variables
    error_msg = str(excinfo.value)
    assert "missing required variables" in error_msg.lower()
    assert "OPENAI_API_BASE" in error_msg
    assert "AZURE_OPENAI_DEPLOYMENT" in error_msg