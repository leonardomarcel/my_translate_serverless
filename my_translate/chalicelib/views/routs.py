import boto3
from chalice import Blueprint 
from chalicelib.utils.translate import Tanslater

extra_routes_translate = Blueprint(__name__)


# ssm = boto3.client('ssm')
# chave_teste = ssm.get_parameter(Name='/my_translate/google-credentials')
# chave_teste = chave_teste['Parameter']['Value']


@extra_routes_translate.route('/translate', methods=['POST', 'GET'])
def translate():
    request = extra_routes_translate.current_request
    #message = 'Este é um teste da API de tradução usando o google gloud'
    data = request.json_body
    message = data.get('message')
    language = data.get('language')
    translater = Tanslater(message, language)
    return {'message': translater.trans(),
            'Language': language}

# @extra_routes_translate.route('/ssm')
# def ssm_parameter():
#     return {'response': chave_teste}