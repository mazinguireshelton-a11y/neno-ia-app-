#!/usr/bin/env python3
# 🎤 TESTE COMPLETO DO SISTEMA VOX.AI

import os
import sys
import importlib
import subprocess
from pathlib import Path

def test_vox_system():
    print("🎤 TESTANDO SISTEMA VOX.AI")
    print("=" * 50)
    
    # 1. Verificar se o módulo de voz existe
    print("1. 🔍 Verificando módulos de voz...")
    
    vox_paths = [
        "backend/services/voice_service.py",
        "backend/routes/voice.py", 
        "backend/plugins/voice_plugin.py",
        "vox_ai.py",
        "voice_system.py"
    ]
    
    vox_modules = []
    for path in vox_paths:
        if os.path.exists(path):
            vox_modules.append(path)
            print(f"   ✅ {path}")
        else:
            print(f"   ❌ {path} - Não encontrado")
    
    # 2. Testar imports de voz
    print("\n2. 🔄 Testando imports de voz...")
    
    voice_imports = [
        "speech_recognition",
        "pyttsx3", 
        "gtts",
        "pyaudio",
        "wave",
        "audioop"
    ]
    
    for lib in voice_imports:
        try:
            importlib.import_module(lib)
            print(f"   ✅ {lib} - Disponível")
        except ImportError:
            print(f"   ❌ {lib} - Não instalado")
    
    # 3. Verificar serviços de voz no backend
    print("\n3. 🏗️ Verificando serviços de voz...")
    
    try:
        sys.path.insert(0, 'backend')
        
        # Verificar se existe serviço de voz
        if os.path.exists("backend/services/voice_service.py"):
            from services.voice_service import VoiceService
            print("   ✅ VoiceService encontrado")
        else:
            print("   ❌ VoiceService não encontrado")
            
        # Verificar rotas de voz
        if os.path.exists("backend/routes/voice.py"):
            print("   ✅ Rotas de voz encontradas")
        else:
            print("   ❌ Rotas de voz não encontradas")
            
    except Exception as e:
        print(f"   ⚠️ Erro nos serviços: {e}")
    
    # 4. Testar funcionalidades básicas de áudio
    print("\n4. 🔊 Testando funcionalidades de áudio...")
    
    # Verificar se o sistema tem capacidades de áudio
    audio_tests = [
        ("Reprodução de áudio", "aplay --version 2>/dev/null || echo 'aplay não encontrado'"),
        ("Gravação de áudio", "arecord --version 2>/dev/null || echo 'arecord não encontrado'"),
        ("PulseAudio", "pulseaudio --version 2>/dev/null || echo 'PulseAudio não encontrado'")
    ]
    
    for test_name, command in audio_tests:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "não encontrado" not in result.stdout:
            print(f"   ✅ {test_name} - Disponível")
        else:
            print(f"   ❌ {test_name} - Não disponível")
    
    # 5. Testar TTS (Text-to-Speech)
    print("\n5. 🗣️ Testando Text-to-Speech...")
    
    tts_options = [
        ("pyttsx3", "python -c \"import pyttsx3; print('pyttsx3 ok')\""),
        ("gTTS", "python -c \"from gtts import gTTS; print('gTTS ok')\""),
        ("espeak", "espeak --version 2>/dev/null || echo 'espeak não encontrado'")
    ]
    
    for tts_name, command in tts_options:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "ok" in result.stdout or "não encontrado" not in result.stdout:
            print(f"   ✅ {tts_name} - Disponível")
        else:
            print(f"   ❌ {tts_name} - Não disponível")
    
    # 6. Testar STT (Speech-to-Text)
    print("\n6. 👂 Testando Speech-to-Text...")
    
    stt_options = [
        ("SpeechRecognition", "python -c \"import speech_recognition; print('SpeechRecognition ok')\""),
        ("pocketsphinx", "python -c \"import pocketsphinx; print('pocketsphinx ok')\" 2>/dev/null || echo 'pocketsphinx não disponível'")
    ]
    
    for stt_name, command in stt_options:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "ok" in result.stdout or "não disponível" not in result.stdout:
            print(f"   ✅ {stt_name} - Disponível")
        else:
            print(f"   ❌ {stt_name} - Não disponível")

def test_voice_api():
    print("\n7. 🌐 Testando API de voz...")
    
    # Verificar se o servidor está rodando
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Servidor rodando")
            
            # Testar endpoints de voz
            voice_endpoints = [
                "/api/voice/speak",
                "/api/voice/listen", 
                "/api/voice/status"
            ]
            
            for endpoint in voice_endpoints:
                try:
                    response = requests.get(f"http://localhost:5000{endpoint}", timeout=3)
                    print(f"   ✅ {endpoint} - Respondendo")
                except:
                    print(f"   ❌ {endpoint} - Não responde")
        else:
            print("   ❌ Servidor não está respondendo")
            
    except Exception as e:
        print(f"   ❌ Erro na API: {e}")

def install_voice_dependencies():
    print("\n8. 📦 Instalando dependências de voz...")
    
    dependencies = [
        "speechrecognition",
        "pyttsx3",
        "gtts",
        "pyaudio",
        "pocketsphinx"
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"   ✅ {dep} - Instalado")
        except subprocess.CalledProcessError:
            print(f"   ❌ {dep} - Falha na instalação")

def create_voice_test():
    print("\n9. 🧪 Criando teste de voz prático...")
    
    voice_test_code = '''#!/usr/bin/env python3
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
'''
    
    with open("test_vox_practico.py", "w") as f:
        f.write(voice_test_code)
    
    print("   ✅ Teste prático criado: test_vox_practico.py")

if __name__ == "__main__":
    test_vox_system()
    test_voice_api()
    install_voice_dependencies()
    create_voice_test()
    
    print("\n🎯 TESTE VOX.AI CONCLUÍDO!")
    print("💡 Comando para teste prático: python test_vox_practico.py")
