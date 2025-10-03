#!/usr/bin/env python3
# 🎤 TESTE SIMPLES DO SISTEMA DE VOZ

import os
import sys

def teste_voz_simples():
    print("🎤 TESTE SIMPLES - SISTEMA DE VOZ")
    print("=" * 40)
    
    # Verificar se existe sistema de voz
    caminhos_voz = [
        "backend/services/voice_service.py",
        "backend/routes/voice.py",
        "vox_ai.py",
        "voice_system.py"
    ]
    
    print("1. 🔍 Procurando arquivos de voz...")
    for caminho in caminhos_voz:
        if os.path.exists(caminho):
            print(f"   ✅ {caminho} - ENCONTRADO!")
            with open(caminho, 'r') as f:
                conteudo = f.read()
                if 'def speak' in conteudo or 'def listen' in conteudo:
                    print(f"      🔊 Tem funções de voz")
                if 'text-to-speech' in conteudo.lower() or 'tts' in conteudo.lower():
                    print(f"      🗣️  Tem TTS")
                if 'speech-to-text' in conteudo.lower() or 'stt' in conteudo.lower():
                    print(f"      👂 Tem STT")
        else:
            print(f"   ❌ {caminho} - não encontrado")
    
    # Testar imports básicos
    print("\n2. 🔄 Testando bibliotecas de voz...")
    bibliotecas = ['pyttsx3', 'speech_recognition', 'gtts']
    
    for lib in bibliotecas:
        try:
            __import__(lib)
            print(f"   ✅ {lib} - instalada")
        except ImportError:
            print(f"   ❌ {lib} - não instalada")
    
    # Verificar se o servidor tem endpoints de voz
    print("\n3. 🌐 Verificando API de voz...")
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=3)
        if response.status_code == 200:
            print("   ✅ Servidor rodando")
            
            # Tentar endpoints de voz comuns
            endpoints = ['/api/voice', '/voice', '/api/speak', '/api/listen']
            for endpoint in endpoints:
                try:
                    response = requests.get(f"http://localhost:5000{endpoint}", timeout=2)
                    if response.status_code != 404:
                        print(f"   ✅ {endpoint} - responde")
                    else:
                        print(f"   ❌ {endpoint} - não encontrado")
                except:
                    print(f"   ❌ {endpoint} - erro de conexão")
    except:
        print("   ❌ Servidor não está rodando")
    
    print("\n🎯 RESUMO DO SISTEMA DE VOZ:")
    print("💡 Comandos para testar:")
    print("   python test_vox_practico.py - Teste completo")
    print("   python -c \"import pyttsx3; engine=pyttsx3.init(); engine.say('Teste'); engine.runAndWait()\" - Teste TTS simples")

if __name__ == "__main__":
    teste_voz_simples()
