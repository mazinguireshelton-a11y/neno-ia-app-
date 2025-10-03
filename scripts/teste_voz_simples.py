#!/usr/bin/env python3
# 🎤 TESTE SIMPLES DE VOZ PARA TERMUX

import subprocess
import requests

def teste_simples():
    print("🎤 TESTE SIMPLES DE VOZ")
    print("=" * 35)
    
    # 1. Testar eSpeak
    print("1. 🔈 Testando eSpeak...")
    try:
        subprocess.run(['espeak', '-v', 'pt', 'Teste do eSpeak'], check=True)
        print("✅ eSpeak funcionando!")
    except:
        print("❌ eSpeak não funcionou")
    
    # 2. Testar gTTS com termux-media-player
    print("\n2. 🔉 Testando gTTS...")
    try:
        from gtts import gTTS
        import tempfile
        
        tts = gTTS(text='Teste do gTTS no Termux', lang='pt')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            print("📁 Áudio salvo, tentando reproduzir...")
            subprocess.run(['termux-media-player', 'play', f.name])
            input("Pressione Enter após ouvir o áudio...")
            subprocess.run(['termux-media-player', 'stop'])
        
        print("✅ gTTS funcionando!")
    except Exception as e:
        print(f"❌ gTTS error: {e}")
    
    # 3. Testar API de voz do backend (se estiver rodando)
    print("\n3. 🌐 Testando backend...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=3)
        if response.status_code == 200:
            print("✅ Backend rodando!")
        else:
            print("❌ Backend não responde")
    except:
        print("❌ Backend não está rodando")

if __name__ == "__main__":
    teste_simples()
