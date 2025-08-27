import logging
import json
from datetime import datetime
import time
from functools import wraps
from flask import request, current_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Configurar Sentry para monitoramento
def init_monitoring(app):
    if app.config.get('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )

# Logger estruturado
class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        
    def log_request(self, message, extra=None):
        extra = extra or {}
        extra.update({
            'request_id': getattr(request, 'id', 'unknown'),
            'endpoint': request.endpoint,
            'method': request.method,
            'user_agent': request.user_agent.string,
            'ip': request.remote_addr
        })
        self.logger.info(message, extra=extra)
        
    def log_error(self, message, exception=None):
        extra = {
            'request_id': getattr(request, 'id', 'unknown'),
            'exception_type': type(exception).__name__ if exception else None,
            'exception_message': str(exception) if exception else None
        }
        self.logger.error(message, extra=extra)

# Decorator para métricas de performance
def track_performance(name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                duration = time.time() - start_time
                current_app.logger.info(
                    f"Performance {name}",
                    extra={'duration': duration, 'operation': name}
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                current_app.logger.error(
                    f"Error in {name}",
                    extra={'duration': duration, 'error': str(e), 'operation': name}
                )
                raise
        return decorated_function
    return decorator
