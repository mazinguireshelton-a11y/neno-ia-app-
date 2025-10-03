#!/usr/bin/env python3
# 🎤 SISTEMA DE VOZ ADAPTADO PARA TERMUX

import os
import subprocess
import requests
from gtts import gTTS
import tempfile

class VozTermux:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
    def falar_espeak(self, texto, lingua='pt'):
        """Usa eSpeak para síntese de voz"""
        try:
            comando = f'espeak -v {lingua} "{texto}" 2>/dev/null'
            subprocess.run(comando, shell=True)
            return True
        except Exception as e:
            print(f"❌ eSpeak error: {e}")
            return False
    
    def falar_gtts(self, texto, lingua='pt'):
        """Usa gTTS (Google Text-to-Speech)"""
        try:
            # Criar arquivo de áudio temporário
            tts = gTTS(text=texto, lang=lingua)
            audio_file = os.path.join(self.temp_dir, 'voz_temp.mp3')
            tts.save(audio_file)
            
            # Reproduzir usando termux-media-player
            subprocess.run(['termux-media-player', 'play', audio_file])
            
            # Aguardar um pouco e limpar
            subprocess.run(['sleep', '3'])
            os.remove(audio_file)
            return True
            
        except Exception as e:
            print(f"❌ gTTS error: {e}")
            return False
    
    def falar(self, texto, metodo='auto'):
        """Faz a IA falar - método automático"""
        print(f"🗣️  IA diz: {texto}")
        
        if metodo == 'espeak' or metodo == 'auto':
            if self.falar_espeak(texto):
                return True
        
        if metodo == 'gtts' or metodo == 'auto':
            if self.falar_gtts(texto):
                return True
        
        # Fallback: mostrar apenas texto
        print("💡 (Sistema de áudio não disponível - mostrando apenas texto)")
        return False
    
    def ouvir_gtts(self):
        """Reconhecimento de voz simplificado usando termux-speech-to-text"""
        try:
            result = subprocess.run(['termux-speech-to-text'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"❌ STT error: {e}")
            return None
    
    def ouvir(self):
        """Ouve o usuário"""
        print("🎤 Fale agora... (aguardando 10 segundos)")
        try:
            texto = self.ouvir_gtts()
            if texto:
                print(f"👂 Você disse: {texto}")
                return texto
            else:
                print("❌ Não foi possível entender o áudio")
                return None
        except Exception as e:
            print(f"❌ Erro ao ouvir: {e}")
            return None

# Teste prático
def testar_voz_termux():
    print("🎤 TESTE DE VOZ TERMUX")
    print("=" * 40)
    
    voz = VozTermux()
    
    # Testar fala
    print("1. 🗣️ Testando síntese de voz...")
    if voz.falar("Olá! Eu sou a NENO IA. Sistema de voz adaptado para Termux!"):
        print("✅ Voz funcionando!")
    else:
        print("❌ Problemas com síntese de voz")
    
    # Testar audição (opcional - precisa de permissão)
    print("\n2. 👂 Testando reconhecimento de voz...")
    print("💡 Para testar reconhecimento, execute separadamente:")
    print("   termux-microphone-record")
    print("   termux-speech-to-text")

if __name__ == "__main__":
    testar_voz_termux()
