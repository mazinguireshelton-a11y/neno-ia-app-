#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import importlib.util
import os

app = FastAPI(title="NENO IA API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar rotas migradas
routes_dir = "backend/routes"
for route_file in os.listdir(routes_dir):
    if route_file.endswith(".py") and route_file != "__init__.py":
        module_name = route_file[:-3]
        spec = importlib.util.spec_from_file_location(module_name, f"{routes_dir}/{route_file}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'router'):
            app.include_router(module.router, prefix="/api")
            print(f"✅ Rota {module_name} carregada")

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "NENO IA FastAPI está funcionando!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
