from diplom_project.logger import logger

class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request);
        status = response.status_code
        if 200 >= status < 300:
            logger.success({
                'status': status
            })
        elif status >= 300 and status < 400:
            logger.info({
                'status': status,
                'body': response.data
            })
        elif status >= 400 and status < 500:
            logger.error({
                'status': status,
                'body': response.data
            })
        elif status >= 500:
            logger.critical({
                'status': status,
                'body': response.data
            })
        return response

    def process_response(self, request, response):
        logger.error({
            'error': response
        })
        return response