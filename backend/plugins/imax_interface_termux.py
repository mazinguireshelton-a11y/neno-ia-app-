#!/usr/bin/env python3
"""
🎬 IMAX Terminal Interface - Versão compatível com Termux
"""

import os
import sys
import time
import threading
import json
from datetime import datetime

# Adicionar caminho para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from plugins.animacao_3d import Animacao3DPlugin
    ANIMATION_LOADED = True
except ImportError:
    print("❌ Plugin animacao_3d não encontrado. Usando modo simulação.")
    ANIMATION_LOADED = False
    class Animacao3DPlugin:
        def __init__(self):
            self.name = "Animação 3D Simulação"
            self.version = "1.0"
        
        def render(self, config):
            print(f"📊 Simulando renderização com config: {config}")
            total_frames = config.get('frames', 60)
            for i in range(total_frames):
                progress = (i + 1) / total_frames * 100
                print(f"🎬 Renderizando frame {i+1}/{total_frames} ({progress:.1f}%)")
                time.sleep(0.1)
            return {
                'status': 'success',
                'path': '/sdcard/IMAX_RENDER/simulacao.mp4',
                'format': 'mp4',
                'frames': config.get('frames', 60)
            }

class IMAXTerminalInterface:
    def __init__(self):
        self.is_rendering = False
        self.render_progress = 0
        self.render_thread = None
        self.animacao_plugin = Animacao3DPlugin()
        self.current_config = {
            'type': 'sistema_solar_imax',
            'quality': 'hd',
            'frames': 60,
            'fps': 30,
            'resolution': (1280, 720),
            'output_dir': '/sdcard/IMAX_RENDER'
        }

    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        """Imprime cabeçalho bonito"""
        print("🎬" + "="*60 + "🎬")
        print("            HOLLYWOOD IMAX PRODUCTION STUDIO")
        print("🎬" + "="*60 + "🎬")
        print()

    def show_menu(self):
        """Mostra menu principal"""
        self.clear_screen()
        self.print_header()
        
        print("📋 CONFIGURAÇÃO ATUAL:")
        print(f"   Tipo: {self.current_config['type']}")
        print(f"   Qualidade: {self.current_config['quality']}")
        print(f"   Frames: {self.current_config['frames']}")
        print(f"   FPS: {self.current_config['fps']}")
        print(f"   Resolução: {self.current_config['resolution'][0]}x{self.current_config['resolution'][1]}")
        print(f"   Saída: {self.current_config['output_dir']}")
        print()
        
        print("📝 MENU PRINCIPAL:")
        print("1. 🚀 Iniciar Renderização")
        print("2. ⚙️  Configurar Qualidade")
        print("3. 📊 Configurar Frames/FPS")
        print("4. 🖼️  Configurar Resolução")
        print("5. 📁 Configurar Diretório")
        print("6. ℹ️  Informações do Sistema")
        print("0. ❌ Sair")
        print()
        
        return input("Escolha uma opção: ")

    def configure_quality(self):
        """Configura qualidade"""
        self.clear_screen()
        self.print_header()
        print("🎯 CONFIGURAR QUALIDADE:")
        print("1. 🚀 Performance (720p, 60FPS)")
        print("2. 📺 HD (1080p, 30FPS)")
        print("3. 🔥 Ultra (2K, 45FPS)")
        print("4. 🎬 Cinema (4K, 60FPS)")
        
        choice = input("Escolha: ")
        qualities = {'1': 'performance', '2': 'hd', '3': 'ultra', '4': 'cinema'}
        if choice in qualities:
            self.current_config['quality'] = qualities[choice]
            print(f"✅ Qualidade definida para: {qualities[choice]}")

    def configure_frames(self):
        """Configura frames e FPS"""
        self.clear_screen()
        self.print_header()
        print("📊 CONFIGURAR FRAMES/FPS:")
        
        try:
            frames = int(input("Número de frames (10-1000): "))
            if 10 <= frames <= 1000:
                self.current_config['frames'] = frames
                print(f"✅ Frames definidos para: {frames}")
            else:
                print("❌ Valor fora do range permitido!")
                
            fps = int(input("FPS (1-60): "))
            if 1 <= fps <= 60:
                self.current_config['fps'] = fps
                print(f"✅ FPS definidos para: {fps}")
            else:
                print("❌ Valor fora do range permitido!")
                
        except ValueError:
            print("❌ Por favor, digite números válidos!")

    def configure_resolution(self):
        """Configura resolução"""
        self.clear_screen()
        self.print_header()
        print("🖼️ CONFIGURAR RESOLUÇÃO:")
        print("1. 640x480")
        print("2. 1280x720 (HD)")
        print("3. 1920x1080 (Full HD)")
        print("4. 3840x2160 (4K)")
        
        choice = input("Escolha: ")
        resolutions = {
            '1': (640, 480),
            '2': (1280, 720),
            '3': (1920, 1080),
            '4': (3840, 2160)
        }
        if choice in resolutions:
            self.current_config['resolution'] = resolutions[choice]
            print(f"✅ Resolução definida para: {resolutions[choice][0]}x{resolutions[choice][1]}")

    def configure_directory(self):
        """Configura diretório de saída"""
        self.clear_screen()
        self.print_header()
        print("📁 CONFIGURAR DIRETÓRIO DE SAÍDA:")
        print(f"Atual: {self.current_config['output_dir']}")
        new_dir = input("Novo diretório (Enter para manter): ")
        if new_dir.strip():
            if os.path.exists(new_dir):
                self.current_config['output_dir'] = new_dir
                print(f"✅ Diretório definido para: {new_dir}")
            else:
                print("❌ Diretório não existe!")
        time.sleep(1)

    def show_system_info(self):
        """Mostra informações do sistema"""
        self.clear_screen()
        self.print_header()
        print("ℹ️  INFORMAÇÕES DO SISTEMA:")
        print(f"Python: {sys.version}")
        print(f"Plataforma: {sys.platform}")
        print(f"Plugin 3D: {'✅ Carregado' if ANIMATION_LOADED else '❌ Simulação'}")
        print(f"Diretório atual: {os.getcwd()}")
        input("\nPressione Enter para continuar...")

    def start_render(self):
        """Inicia renderização"""
        if self.is_rendering:
            print("⚠️  Renderização já em andamento!")
            return
            
        print("🚀 INICIANDO RENDERIZAÇÃO...")
        print("📊 Configuração:", json.dumps(self.current_config, indent=2))
        print("⏰ Isso pode levar alguns minutos...")
        print("🛑 Press Ctrl+C para cancelar")
        print("-" * 50)
        
        self.is_rendering = True
        self.render_thread = threading.Thread(target=self.render_animation)
        self.render_thread.daemon = True
        self.render_thread.start()
        
        # Mostrar progresso
        try:
            while self.is_rendering and self.render_thread.is_alive():
                time.sleep(0.5)
                print(f"📈 Progresso: {self.render_progress}%", end='\r')
        except KeyboardInterrupt:
            print("\n🛑 Cancelando renderização...")
            self.is_rendering = False

    def render_animation(self):
        """Processo de renderização"""
        try:
            result = self.animacao_plugin.render(self.current_config)
            
            if result.get('status') == 'success':
                print(f"\n✅ RENDERIZAÇÃO CONCLUÍDA!")
                print(f"📁 Arquivo: {result.get('path')}")
                print(f"🎬 Formato: {result.get('format')}")
                print(f"📊 Frames: {result.get('frames')}")
            else:
                print(f"\n❌ ERRO: {result.get('message', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"\n🔥 ERRO CRÍTICO: {str(e)}")
        finally:
            self.is_rendering = False
            self.render_progress = 0

    def run(self):
        """Loop principal da interface"""
        while True:
            try:
                choice = self.show_menu()
                
                if choice == '1':
                    self.start_render()
                elif choice == '2':
                    self.configure_quality()
                elif choice == '3':
                    self.configure_frames()
                elif choice == '4':
                    self.configure_resolution()
                elif choice == '5':
                    self.configure_directory()
                elif choice == '6':
                    self.show_system_info()
                elif choice == '0':
                    print("👋 Saing... Até logo!")
                    break
                else:
                    print("❌ Opção inválida!")
                    time.sleep(1)
                    
                # Pequena pausa entre menus
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n🛑 Interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
                time.sleep(2)

def main():
    """Função principal"""
    print("🎬 Iniciando IMAX Terminal Interface...")
    time.sleep(1)
    
    interface = IMAXTerminalInterface()
    interface.run()

if __name__ == "__main__":
    main()
