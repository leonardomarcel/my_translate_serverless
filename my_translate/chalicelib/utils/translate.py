from google.cloud import translate_v2 as translate
import os
import boto3


class Tanslater:
    def __init__(self, message, language):
        self.message = message
        self.language = language
    
    def _setup_google_credentials(self):
        """Recupera as credenciais do Parameter Store e configura o ambiente."""
        parameter_name = 'google_credentials'
        credentials_path = '/tmp/google_credentials.json' if os.name == 'posix' else './tmp/google_credentials.json'

        # Verifica se o diretório './tmp' existe, se não, cria
        os.makedirs(os.path.dirname(credentials_path), exist_ok=True)
        
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        credentials = response['Parameter']['Value']
        
        # Salva as credenciais temporariamente no /tmp
        with open(credentials_path, 'w') as cred_file:
            cred_file.write(credentials)
        
        # Configura a variável de ambiente
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    def trans(self):
        self._setup_google_credentials()
        translate_client = translate.Client()
        text = self.message
        target = self.language
        try:
            translation = translate_client.translate(text, target_language=target)
        except Exception as e:
            return {"error": "Translation failed: was it a valid language?"}
        
        return translation["translatedText"]
