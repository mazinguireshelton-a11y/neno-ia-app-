"""
🎬 Renderizador Confiável para Termux
Método frame-by-frame que SEMPRE funciona
"""

import os
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw

class RenderizadorConfiável:
    def __init__(self):
        self.name = "Renderizador Confiável"
        self.version = "1.0"
    
    def renderizar(self, config):
        """Método 100% confiável - SEM matplotlib"""
        frames = config.get('frames', 30)
        fps = config.get('fps', 15)
        output_dir = config.get('output_dir', '/sdcard/IMAX_RENDER')
        width, height = config.get('resolution', (640, 480))
        
        os.makedirs(output_dir, exist_ok=True)
        temp_dir = f"{output_dir}/temp_frames"
        os.makedirs(temp_dir, exist_ok=True)
        
        output_path = f"{output_dir}/render_{int(time.time())}.mp4"
        
        print("🎬 Iniciando renderização confiável...")
        print(f"📊 Frames: {frames}, FPS: {fps}, Resolução: {width}x{height}")
        
        # Gerar frames simples mas visuais
        for i in range(frames):
            # Criar imagem com gradiente animado
            img = Image.new('RGB', (width, height), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Gradiente animado
            progress = i / frames
            r = int(255 * progress)
            g = int(255 * (1 - progress))
            b = int(128 + 127 * np.sin(progress * 2 * np.pi))
            
            # Desenhar círculo animado
            circle_size = 100 + 50 * np.sin(progress * 2 * np.pi)
            draw.ellipse([
                width//2 - circle_size,
                height//2 - circle_size,
                width//2 + circle_size,
                height//2 + circle_size
            ], fill=(r, g, b))
            
            # Texto com progresso
            draw.text((10, 10), f"Frame {i+1}/{frames}", fill=(255, 255, 255))
            
            frame_path = f"{temp_dir}/frame_{i:04d}.jpg"
            img.save(frame_path, quality=90)
            
            if i % 10 == 0:
                print(f"📸 Frame {i+1}/{frames}")
        
        print("🎞️  Convertendo frames para vídeo...")
        
        # Comando FFmpeg - JÁ PROVAMOS QUE FUNCIONA
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', f'{temp_dir}/frame_%04d.jpg',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '23',
            '-preset', 'fast',
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Limpar arquivos temporários
            for arquivo in os.listdir(temp_dir):
                os.remove(f"{temp_dir}/{arquivo}")
            os.rmdir(temp_dir)
            
            if result.returncode == 0:
                if os.path.exists(output_path):
                    size = os.path.getsize(output_path) / 1024
                    return {
                        'status': 'success',
                        'path': output_path,
                        'frames': frames,
                        'size_kb': size,
                        'method': 'frame_by_frame_safe'
                    }
                else:
                    return {
                        'status': 'error',
                        'message': 'Arquivo não foi criado'
                    }
            else:
                return {
                    'status': 'error',
                    'message': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': 'Timeout - FFmpeg travado'
            }

# Instância global
renderizador_confiavel = RenderizadorConfiável()
