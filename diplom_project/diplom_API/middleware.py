from diplom_project.logger import logger

class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request);
        status = response.status_code
        request_path = request.META.get('PATH_INFO')
        request_data = response.data if response.data is not None else None 
        if 200 >= status < 300:
            logger.success({
                'status': status,
                'request_path': request_path
            })
        elif status >= 300 and status < 400:
            logger.info({
                'status': status,
                'request_path': request_path,
                'body': request_data
            })
        elif status >= 400 and status < 500:
            logger.error({
                'status': status,
                'request_path': request_path,
                'body': request_data
            })
        elif status >= 500:
            logger.critical({
                'status': status,
                'request_path': request_data,
                'body': response.data
            })
        return response

    def process_response(self, request, response):
        logger.error({
            'error': response
        })
        return response