def JsonGenerator(response, status=True, source='FastAPI V1', statusCode=200, errorCode=None,
                  errorMessage=None, website='127.0.0.1:8000'):
    return {'provider': {'website': website, 'source': source}, 'response': response, 'status': status,
            'error': {'code': errorCode, 'message': errorMessage}}