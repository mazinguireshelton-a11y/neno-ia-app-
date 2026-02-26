# 📁 neno_sdxl_ultra_client.py
# 🔥 CLIENTE SDXL PARA TERMUX

import os
import requests
import base64
import hashlib
import json
from typing import Dict, List, Optional, Tuple
from io import BytesIO
from PIL import Image
from datetime import datetime
from pathlib import Path
import time

class NENOSDXLUltraGenerator:
    def __init__(self):
        self.name = "NENO SDXL Ultra Generator"
        self.version = "9.0"
        self.sdxl_url = "https://SEU_URL_DO_COLAB.ngrok-free.app/generate"  # Substituir pela URL do seu Colab
        self.cache_dir = os.path.expanduser("~/neno-ia-app/cache/sdxl_ultra_images")
        self.stats_file = os.path.expanduser("~/neno-ia-app/cache/sdxl_stats.json")
        
        Path(self.cache_dir).mkdir(exist_ok=True, parents=True)
        self._load_stats()
        
        print(f"🚀 {self.name} v{self.version} inicializado!")
        print("🎨 Stable Diffusion XL Ultra - Qualidade Hollywood")
        print("🌐 Conectado ao Google Colab - Zero processamento local")
        print(f"📊 Estatísticas: {self.stats['total_generated']} imagens geradas")
    
    def _load_stats(self):
        """Carrega estatísticas do sistema"""
        self.stats = {
            "total_generated": 0,
            "successful_generations": 0,
            "failed_generations": 0,
            "total_size_gb": 0,
            "styles_used": {},
            "categories_used": {},
            "start_time": datetime.now().isoformat()
        }
        
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats.update(json.load(f))
            except:
                pass
    
    def _save_stats(self):
        """Salva estatísticas do sistema"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def _update_stats(self, success: bool, style: str, category: str, size_mb: float):
        """Atualiza estatísticas"""
        self.stats["total_generated"] += 1
        if success:
            self.stats["successful_generations"] += 1
        else:
            self.stats["failed_generations"] += 1
        
        self.stats["styles_used"][style] = self.stats["styles_used"].get(style, 0) + 1
        self.stats["categories_used"][category] = self.stats["categories_used"].get(category, 0) + 1
        self.stats["total_size_gb"] += size_mb / 1024
        
        self._save_stats()
    
    def detect_category(self, prompt: str) -> str:
        """Detecta categoria automaticamente com algoritmo melhorado"""
        prompt_lower = prompt.lower()
        
        categories = {
            'fantasy': ['fantasy', 'magic', 'dragon', 'castle', 'wizard', 'elf', 'orc', 'medieval', 'mythical'],
            'sci-fi': ['sci-fi', 'scifi', 'space', 'spaceship', 'alien', 'robot', 'future', 'cyber', 'android', 'laser'],
            'cyberpunk': ['cyberpunk', 'neon', 'hologram', 'blade runner', 'futuristic city', 'dystopian'],
            'realistic': ['realistic', 'photorealistic', 'photo', 'real', 'authentic', 'natural'],
            'portrait': ['portrait', 'face', 'person', 'woman', 'man', 'girl', 'boy', 'human'],
            'landscape': ['landscape', 'mountain', 'forest', 'beach', 'nature', 'view', 'scenery'],
            'animal': ['animal', 'dog', 'cat', 'lion', 'tiger', 'bird', 'wildlife', 'pet'],
            'vehicle': ['car', 'vehicle', 'motorcycle', 'airplane', 'ship', 'truck', 'sports car'],
            'abstract': ['abstract', 'pattern', 'texture', 'colorful', 'geometric', 'modern art']
        }
        
        scores = {category: 0 for category in categories}
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    scores[category] += 3 if len(keyword.split()) > 1 else 1
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def get_recommended_style(self, category: str) -> str:
        """Recomenda estilo baseado na categoria"""
        style_mapping = {
            'fantasy': 'fantasy',
            'sci-fi': 'sci-fi',
            'cyberpunk': 'cyberpunk',
            'realistic': 'realistic',
            'portrait': 'cinematic',
            'landscape': 'realistic',
            'animal': 'realistic',
            'vehicle': 'realistic',
            'abstract': 'digital_art'
        }
        return style_mapping.get(category, 'realistic')
    
    def get_recommended_negative_prompt(self, category: str) -> str:
        """Retorna negative prompt recomendado baseado na categoria"""
        negative_prompts = {
            'portrait': 'blurry, low quality, distorted, bad anatomy, ugly, poorly drawn, text, watermark, extra limbs, missing limbs, disfigured, malformed hands, mutated hands',
            'landscape': 'blurry, low quality, distorted, bad proportions, ugly, poorly drawn, text, watermark, people, human, buildings',
            'animal': 'blurry, low quality, distorted, bad anatomy, ugly, poorly drawn, text, watermark, human, person, extra limbs',
            'fantasy': 'blurry, low quality, distorted, bad anatomy, ugly, poorly drawn, text, watermark, realistic, photo',
            'sci-fi': 'blurry, low quality, distorted, bad anatomy, ugly, poorly drawn, text, watermark, ancient, medieval',
            'cyberpunk': 'blurry, low quality, distorted, bad anatomy, ugly, poorly drawn, text, watermark, natural, daylight, sunny',
            'default': 'blurry, low quality, distorted, bad anatomy, ugly, poorly drawn, text, watermark'
        }
        return negative_prompts.get(category, negative_prompts['default'])
    
    def generate_sdxl_image(self, prompt: str, style: str = "realistic", 
                          width: int = 1024, height: int = 1024, 
                          negative_prompt: str = "", enhance_faces: bool = True,
                          upscale_factor: int = 1) -> Optional[Image.Image]:
        """Gera imagem com Stable Diffusion XL no Colab"""
        try:
            payload = {
                "prompt": prompt,
                "style": style,
                "width": width,
                "height": height,
                "negative_prompt": negative_prompt or self.get_recommended_negative_prompt(self.detect_category(prompt)),
                "guidance_scale": 8.0,
                "steps": 35,
                "use_refiner": True,
                "enhance_faces": enhance_faces,
                "upscale_factor": upscale_factor
            }
            
            headers = {'Content-Type': 'application/json', 'User-Agent': 'NENO-SDXL-ULTRA/9.0'}
            
            print(f"🌐 Conectando com SDXL Server...")
            start_time = time.time()
            
            response = requests.post(self.sdxl_url, json=payload, headers=headers, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    img_data = result["image"].split(",")[1]
                    image_data = base64.b64decode(img_data)
                    
                    # Verificação extra para garantir que a imagem é válida
                    if len(image_data) < 1000:
                        print(f"❌ Dados de imagem insuficientes: {len(image_data)} bytes")
                        return None
                    
                    # Tenta carregar a imagem
                    try:
                        image = Image.open(BytesIO(image_data))
                        # Verifica se a imagem não está corrompida
                        image.verify()
                        image = Image.open(BytesIO(image_data))  # Reabre após verificação
                        if image.width < 10 or image.height < 10:
                            print("❌ Imagem com dimensões inválidas")
                            return None
                            
                        generation_time = time.time() - start_time
                        print(f"✅ SDXL gerado em {generation_time:.1f}s | {width}x{height}")
                        return image
                    except Exception as e:
                        print(f"❌ Erro ao decodificar imagem: {e}")
                        return None
                else:
                    print(f"❌ Erro no SDXL: {result.get('error', 'Unknown')}")
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
            return None
            
        except requests.exceptions.Timeout:
            print("⏰ Timeout - Colab muito lento")
            return None
        except requests.exceptions.ConnectionError:
            print("🔌 Erro de conexão - Colab offline")
            return None
        except Exception as e:
            print(f"❌ Erro SDXL: {e}")
            return None
    
    def execute(self, prompt: str, size: str = "1024x1024", style: str = "auto", 
               num_images: int = 1, negative_prompt: str = "", enhance_faces: bool = True,
               upscale_factor: int = 1) -> Dict:
        """Executa geração de imagens com SDXL"""
        try:
            width, height = map(int, size.split('x'))
            images = []
            
            # Detecta categoria e estilo automático
            category = self.detect_category(prompt)
            if style == "auto":
                style = self.get_recommended_style(category)
            
            # Usa negative prompt recomendado se não fornecido
            if not negative_prompt:
                negative_prompt = self.get_recommended_negative_prompt(category)
            
            print(f"🎯 Categoria: {category} | Estilo: {style}")
            print(f"📝 Prompt: {prompt[:60]}...")
            print(f"🚫 Negative Prompt: {negative_prompt[:60]}...")
            
            for i in range(num_images):
                print(f"🎨 Gerando imagem {i+1}/{num_images}...")
                
                # Gera imagem com SDXL
                sdxl_image = self.generate_sdxl_image(
                    prompt, style, width, height, negative_prompt, 
                    enhance_faces, upscale_factor
                )
                
                if not sdxl_image:
                    return {
                        "success": False, 
                        "error": "SDXL server indisponível. Verifique se o Colab está rodando.",
                        "retry_after": 30
                    }
                
                # Salva resultado
                timestamp = int(datetime.now().timestamp())
                file_hash = hashlib.md5(f"{prompt}_{timestamp}_{i}".encode()).hexdigest()[:12]
                filename = f"sdxl_ultra_{file_hash}_{width}x{height}.png"
                filepath = os.path.join(self.cache_dir, filename)
                
                sdxl_image.save(filepath, "PNG", quality=95, optimize=True)
                
                # Calcula tamanho do arquivo
                file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
                
                # Converte para base64
                buffered = BytesIO()
                sdxl_image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                images.append({
                    "base64": f"data:image/png;base64,{img_str}",
                    "file_path": filepath,
                    "provider": "neno_sdxl_ultra",
                    "quality_score": 0.99,
                    "resolution": f"{sdxl_image.width}x{sdxl_image.height}",
                    "style": style,
                    "category": category,
                    "size_mb": round(file_size_mb, 2)
                })
                
                # Atualiza estatísticas
                self._update_stats(True, style, category, file_size_mb)
            
            return {
                'success': True,
                'images': images,
                'prompt': prompt,
                'size': size,
                'style': style,
                'category': category,
                'model': "Stable Diffusion XL 1.0",
                'total_generated': self.stats["total_generated"]
            }
                
        except Exception as e:
            self._update_stats(False, "error", "error", 0)
            return {"error": f"Erro na geração: {str(e)}"}
    
    def get_available_styles(self) -> List[str]:
        """Retorna estilos disponíveis"""
        try:
            response = requests.get(self.sdxl_url.replace('/generate', '/styles'), timeout=15)
            if response.status_code == 200:
                return response.json().get("styles", [])
        except:
            pass
        
        # Fallback se não conseguir conectar
        return ["realistic", "cinematic", "fantasy", "cyberpunk", "sci-fi", "painting", "anime", "concept", "hyperrealistic"]
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas completas do sistema"""
        return self.stats
    
    def clear_cache(self) -> Dict:
        """Limpa o cache de imagens"""
        try:
            cache_size = sum(os.path.getsize(f) for f in Path(self.cache_dir).rglob('*') if f.is_file())
            for file in Path(self.cache_dir).glob('*'):
                if file.is_file():
                    file.unlink()
            
            return {
                "success": True,
                "cleared_size_gb": round(cache_size / (1024**3), 2),
                "remaining_files": 0
            }
        except Exception as e:
            return {"error": f"Erro ao limpar cache: {str(e)}"}
    
    def get_cache_info(self) -> Dict:
        """Retorna informações do cache"""
        try:
            files = list(Path(self.cache_dir).glob('*'))
            total_size = sum(os.path.getsize(f) for f in files if f.is_file())
            
            return {
                "total_files": len(files),
                "total_size_gb": round(total_size / (1024**3), 2),
                "average_size_mb": round(total_size / max(1, len(files)) / (1024*1024), 1)
            }
        except:
            return {"total_files": 0, "total_size_gb": 0}

# Script de instalação e configuração
def setup_neno_sdxl():
    """Configura o ambiente NENO SDXL no Termux"""
    print("🔧 Configurando NENO SDXL Ultra no Termux...")
    
    # Cria diretórios necessários
    os.makedirs(os.path.expanduser("~/neno-ia-app/cache"), exist_ok=True)
    os.makedirs(os.path.expanduser("~/neno-ia-app/backend/plugins"), exist_ok=True)
    
    # Altera para o diretório de plugins
    os.chdir(os.path.expanduser("~/neno-ia-app/backend/plugins"))
    
    print("✅ Configuração concluída!")
    print("📁 Diretório: ~/neno-ia-app/backend/plugins")
    print("🚀 Use: python neno_sdxl_ultra_client.py")

def register_image_generator():
    return NENOSDXLUltraGenerator()

# Executa a configuração se o script for executado diretamente
if __name__ == '__main__':
    setup_neno_sdxl()
