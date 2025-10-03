#!/usr/bin/env python3
# 🎤 TESTE PRÁTICO DE VOX.AI

import sys
import os
sys.path.insert(0, 'backend')

def test_voice_functionality():
    """Teste prático das funcionalidades de voz"""
    
    print("🎤 TESTE PRÁTICO VOX.AI")
    print("=" * 40)
    
    # 1. Testar Text-to-Speech
    print("1. 🗣️ Testando Text-to-Speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"   ✅ Pyttsx3 - {len(voices)} vozes disponíveis")
        engine.say("Teste de voz do sistema NENO IA")
        print("   🔊 Reproduzindo áudio...")
        engine.runAndWait()
    except Exception as e:
        print(f"   ❌ TTS error: {e}")
    
    # 2. Testar Speech Recognition
    print("2. 👂 Testando Speech Recognition...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        print("   ✅ SpeechRecognition carregado")
        
        # Testar com microfone
        with sr.Microphone() as source:
            print("   🎤 Microfone disponível")
            print("   💡 Fale algo para teste...")
            audio = r.listen(source, timeout=5)
            print("   ✅ Áudio capturado")
    except Exception as e:
        print(f"   ❌ STT error: {e}")
    
    # 3. Testar API de voz
    print("3. 🌐 Testando API de voz...")
    try:
        import requests
        response = requests.post(
            "http://localhost:5000/api/voice/speak",
            json={"text": "Teste de voz da API", "voice": "pt"}
        )
        if response.status_code == 200:
            print("   ✅ API de voz funcionando")
        else:
            print(f"   ❌ API status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API error: {e}")

if __name__ == "__main__":
    test_voice_functionality()
