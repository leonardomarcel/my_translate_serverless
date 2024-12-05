import boto3
from chalice import Blueprint
from chalicelib.utils.translate import Tanslater

extra_routes_translate = Blueprint(__name__)


# ssm = boto3.client('ssm')
# chave_teste = ssm.get_parameter(Name='/my_translate/google-credentials')
# chave_teste = chave_teste['Parameter']['Value']


@extra_routes_translate.route('/translate/{language}')
def translate(language):
    message = 'Este é um teste da API de tradução usando o google gloud'
    translater = Tanslater(message, language)
    return {'response': translater.trans()}

# @extra_routes_translate.route('/ssm')
# def ssm_parameter():
#     return {'response': chave_teste}