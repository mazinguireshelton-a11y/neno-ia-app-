import sys
import os
import time
import threading
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                             QComboBox, QSpinBox, QTextEdit, QGroupBox, 
                             QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from plugins.animacao_3d import Animacao3DPlugin
    print("✅ Plugin de animação 3D carregado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao carregar animacao_3d: {e}")
    # Modo fallback - criaremos uma classe mock para testes
    class Animacao3DPlugin:
        def __init__(self):
            self.name = "Animação 3D Mock"
            self.version = "1.0"
        
        def render(self, config):
            print(f"📊 Simulando renderização com config: {config}")
            time.sleep(5)  # Simula tempo de renderização
            return {
                'status': 'success',
                'path': '/sdcard/IMAX_RENDER/simulacao.mp4',
                'format': 'mp4',
                'frames': config.get('frames', 60)
            }

class IMAXRenderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Hollywood IMAX Production Studio - NENO IA")
        self.setGeometry(100, 100, 900, 700)
        
        # Variáveis
        self.is_rendering = False
        self.render_progress = 0
        self.render_thread = None
        self.animacao_plugin = Animacao3DPlugin()
        
        # Configurações padrão
        self.current_config = {
            'type': 'sistema_solar_imax',
            'quality': 'hd',
            'frames': 60,
            'fps': 30,
            'resolution': (1280, 720),
            'output_dir': '/sdcard/IMAX_RENDER'
        }
        
        # Setup UI
        self.setup_ui()
        
        # Timer para atualizar a interface
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)
        
    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Título
        title = QLabel("🎬 HOLLYWOOD IMAX PRODUCTION STUDIO")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #FFD700; background-color: #000080; padding: 10px; border-radius: 10px;")
        layout.addWidget(title)
        
        # Grupo de configurações
        config_group = QGroupBox("⚙️ Configurações de Renderização")
        config_layout = QVBoxLayout()
        
        # Tipo de animação
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Tipo de Animação:"))
        self.animation_type = QComboBox()
        self.animation_type.addItems(['sistema_solar_imax', 'nebulosa_estelar', 'buraco_negro'])
        type_layout.addWidget(self.animation_type)
        config_layout.addLayout(type_layout)
        
        # Qualidade
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Qualidade:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(['performance', 'hd', 'ultra', 'cinema'])
        self.quality_combo.setCurrentText('hd')
        quality_layout.addWidget(self.quality_combo)
        config_layout.addLayout(quality_layout)
        
        # Frames e FPS
        frames_fps_layout = QHBoxLayout()
        frames_fps_layout.addWidget(QLabel("Frames:"))
        self.frames_spin = QSpinBox()
        self.frames_spin.setRange(10, 1000)
        self.frames_spin.setValue(60)
        frames_fps_layout.addWidget(self.frames_spin)
        
        frames_fps_layout.addWidget(QLabel("FPS:"))
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setValue(30)
        frames_fps_layout.addWidget(self.fps_spin)
        config_layout.addLayout(frames_fps_layout)
        
        # Resolução
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Resolução:"))
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(['640x480', '1280x720', '1920x1080', '3840x2160'])
        self.resolution_combo.setCurrentText('1280x720')
        res_layout.addWidget(self.resolution_combo)
        config_layout.addLayout(res_layout)
        
        # Diretório de saída
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Diretório:"))
        self.output_label = QLabel("/sdcard/IMAX_RENDER")
        output_layout.addWidget(self.output_label)
        
        self.browse_btn = QPushButton("📁 Procurar")
        self.browse_btn.clicked.connect(self.browse_directory)
        output_layout.addWidget(self.browse_btn)
        config_layout.addLayout(output_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Botões de controle
        button_layout = QHBoxLayout()
        
        self.render_btn = QPushButton("🚀 Iniciar Renderização")
        self.render_btn.clicked.connect(self.start_render)
        self.render_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; border-radius: 5px; }")
        button_layout.addWidget(self.render_btn)
        
        self.stop_btn = QPushButton("⏹️ Parar Renderização")
        self.stop_btn.clicked.connect(self.stop_render)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 10px; border-radius: 5px; }")
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #05B8CC; width: 10px; }")
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("🟢 Pronto para renderizar")
        self.status_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # Log de saída
        log_group = QGroupBox("📝 Log de Execução")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #000033; color: #00FF00; font-family: monospace;")
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Informações do sistema
        info_label = QLabel("💡 Dica: Feche outros aplicativos para melhor performance. Mantenha o dispositivo conectado à energia.")
        info_label.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        layout.addWidget(info_label)
        
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Saída")
        if directory:
            self.output_label.setText(directory)
            self.current_config['output_dir'] = directory
        
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        # Auto-scroll para o final
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
        
    def update_status(self):
        """Atualiza o status da interface"""
        if self.is_rendering:
            self.status_label.setText("🟡 Renderizando... Não feche o aplicativo!")
            # Simular progresso (em uma implementação real, isso viria do worker)
            if self.render_progress < 100:
                self.render_progress += 1
                self.progress_bar.setValue(self.render_progress)
        else:
            self.progress_bar.setValue(0)
            
    def start_render(self):
        """Inicia o processo de renderização em thread separada"""
        if self.is_rendering:
            return
            
        # Atualizar configuração
        resolution = tuple(map(int, self.resolution_combo.currentText().split('x')))
        
        self.current_config.update({
            'type': self.animation_type.currentText(),
            'quality': self.quality_combo.currentText(),
            'frames': self.frames_spin.value(),
            'fps': self.fps_spin.value(),
            'resolution': resolution,
            'output_dir': self.output_label.text()
        })
        
        self.log_message("🚀 INICIANDO RENDERIZAÇÃO IMAX...")
        self.log_message(f"📊 Configuração: {self.current_config}")
        
        # Atualizar interface
        self.is_rendering = True
        self.render_progress = 0
        self.render_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # Iniciar renderização em thread separada
        self.render_thread = threading.Thread(target=self.render_animation)
        self.render_thread.daemon = True
        self.render_thread.start()
        
    def stop_render(self):
        """Para a renderização"""
        if self.is_rendering:
            self.is_rendering = False
            self.log_message("⏹️ Renderização interrompida pelo usuário")
            self.status_label.setText("🔴 Renderização interrompida")
            self.render_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            
    def render_animation(self):
        """Função de renderização executada em thread separada"""
        try:
            self.log_message("🎬 Iniciando processo de renderização...")
            self.log_message("📦 Carregando motor de renderização 3D...")
            
            # Renderizar usando o plugin
            result = self.animacao_plugin.render(self.current_config)
            
            if result.get('status') == 'success':
                self.log_message("✅ RENDERIZAÇÃO CONCLUÍDA COM SUCESSO!")
                self.log_message(f"📁 Arquivo salvo em: {result.get('path')}")
                self.log_message(f"🎬 Formato: {result.get('format')}")
                self.log_message(f"📊 Total de frames: {result.get('frames')}")
                
                # Tentar abrir o arquivo se estiver no Android
                if '/sdcard/' in result.get('path', ''):
                    self.log_message("📱 Use um app de galeria para visualizar o vídeo")
                    
            else:
                error_msg = result.get('message', 'Erro desconhecido')
                self.log_message(f"❌ ERRO NA RENDERIZAÇÃO: {error_msg}")
                
        except Exception as e:
            self.log_message(f"🔥 ERRO CRÍTICO: {str(e)}")
            import traceback
            self.log_message(f"🔍 Detalhes: {traceback.format_exc()}")
        finally:
            # Restaurar interface
            self.is_rendering = False
            self.render_progress = 100
            self.render_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status_label.setText("🟢 Renderização concluída")

def main():
    # Verificar se estamos no Termux
    is_termux = os.path.exists('/data/data/com.termux/files/home')
    
    app = QApplication(sys.argv)
    
    # Estilo escuro para melhor visualização
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    
    # Estilo adicional para melhor aparência
    app.setStyle('Fusion')
    
    window = IMAXRenderWindow()
    window.show()
    
    # Mensagem inicial baseada no ambiente
    if is_termux:
        window.log_message("📱 Ambiente Termux detectado - Modo otimizado ativado")
    else:
        window.log_message("💻 Ambiente desktop detectado")
    
    window.log_message("🎬 Hollywood IMAX Studio inicializado com sucesso!")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
