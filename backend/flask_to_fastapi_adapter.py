"""
Adaptador para converter funcionalidades Flask → FastAPI
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse

def flask_to_fastapi(flask_func):
    """Decorator para adaptar funções Flask para FastAPI"""
    async def fastapi_wrapper(request: Request):
        # Simular objeto request do Flask
        class FlaskRequest:
            def __init__(self, fastapi_request):
                self.fastapi_request = fastapi_request
                self.json = None
            
            async def get_json(self):
                if self.json is None:
                    self.json = await self.fastapi_request.json()
                return self.json
        
        flask_req = FlaskRequest(request)
        result = await flask_func(flask_req)
        return JSONResponse(result)
    
    return fastapi_wrapper
