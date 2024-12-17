import os
import pytest
from unittest.mock import patch, mock_open
#from boto3.exceptions import Boto3Error
from moto.ssm import mock_ssm
import boto3

from ..translate import Tanslater  

@pytest.fixture
def mock_google_client():
    """Mocka o cliente do Google Translate."""
    with patch("google.cloud.translate_v2.Client") as mock_client:
        yield mock_client
@pytest.fixture
def mock_google_credentials_env():
    """Fixture para limpar a variável de ambiente."""
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    yield
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        del os.environ['GOOGLE_APPLICATION_CREDENTIALS']

@pytest.fixture
def ssm_mock():
    """Configura o mock do SSM da AWS usando 'moto'."""
    with mock_ssm():
        ssm = boto3.client('ssm', region_name='us-east-1')
        ssm.put_parameter(
            Name='google_credentials',
            Value='{"type": "service_account", "project_id": "fake_project"}',
            Type='SecureString'
        )
        yield ssm

# ---------- TESTES DE UNIDADE ---------- #

def test_setup_google_credentials(ssm_mock):
    """Testa o método _setup_google_credentials isoladamente."""
    # Verificar o caminho usado conforme o sistema operacional
    expected_path = "/tmp/google_credentials.json" if os.name == "posix" else "./tmp/google_credentials.json"

    with patch("boto3.client", return_value=ssm_mock):
        with patch("builtins.open", mock_open()) as mock_file:
            tanslater = Tanslater(message="Hello", language="es")
            tanslater._setup_google_credentials()

            # Verificação
            mock_file.assert_called_with(expected_path, "w")
            handle = mock_file()
            handle.write.assert_called_once_with('{"type": "service_account", "project_id": "fake_project"}')

def test_trans_success(mock_google_client):
    """Testa o método trans com sucesso."""
    mock_client_instance = mock_google_client.return_value
    mock_client_instance.translate.return_value = {"translatedText": "Hola"}

    tanslater = Tanslater(message="Hello", language="es")
    result = tanslater.trans()
    
    assert result == "Hola"
    mock_client_instance.translate.assert_called_once_with("Hello", target_language="es")
