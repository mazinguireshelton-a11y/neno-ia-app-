#!/usr/bin/env python3
# 🚀 SERVIDOR SIMPLES NENO IA

try:
    from fastapi import FastAPI
    import uvicorn
    USING_FASTAPI = True
except:
    from fastapi import Flask, jsonify
    USING_FASTAPI = False

if USING_FASTAPI:
    app = FastAPI(title="NENO IA")
    
    @app.get("/")
    async def root():
        return {"message": "NENO IA FastAPI funcionando!"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
        
else:
    app = FastAPI(__name__)
    
    @app.route("/")
    def root():
        return jsonify({"message": "NENO IA Flask funcionando!"})
    
    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

if __name__ == "__main__":
    if USING_FASTAPI:
        print("🚀 Iniciando FastAPI na porta 5000")
        uvicorn.run(app, host="0.0.0.0", port=5000)
    else:
        print("🚀 Iniciando Flask na porta 5000")
        uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)host="0.0.0.0", port=5000, debug=True)
