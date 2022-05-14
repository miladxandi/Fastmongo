def JsonGenerator(response, status=True, errorCode=None, errorMessage=None, statusCode=200, source='FastAPI V1',
                   website='127.0.0.1:8000'):
    return {'provider': {'website': website, 'source': source}, 'response': response, 'status': status,
            'error': {'code': errorCode, 'message': errorMessage}}