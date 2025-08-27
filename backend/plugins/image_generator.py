"""
Plugin de geração de imagens para a NENO IA
"""
import os
import requests
from typing import Dict, Optional
import base64
from io import BytesIO
from PIL import Image

class ImageGeneratorPlugin:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.stabilityai_api_key = os.getenv("STABILITYAI_API_KEY")
        self.midjourney_api_key = os.getenv("MIDJOURNEY_API_KEY")
    
    def execute(self, prompt: str, size: str = "1024x1024", 
               style: str = "vivid", num_images: int = 1) -> Dict:
        """Gera imagens a partir de prompt"""
        try:
            # Prioridade: OpenAI DALL-E
            if self.openai_api_key:
                return self._generate_openai(prompt, size, style, num_images)
            
            # Fallback: Stability AI
            elif self.stabilityai_api_key:
                return self._generate_stabilityai(prompt, size, num_images)
                
            # Fallback: Outros serviços
            else:
                return {"error": "Nenhum serviço de geração de imagens configurado"}
                
        except Exception as e:
            return {"error": f"Erro na geração de imagem: {str(e)}"}
    
    def _generate_openai(self, prompt: str, size: str, style: str, num_images: int) -> Dict:
        """Gera imagem usando OpenAI DALL-E"""
        import openai
        
        client = openai.OpenAI(api_key=self.openai_api_key)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=num_images,
            style=style
        )
        
        images = []
        for image_data in response.data:
            images.append({
                "url": image_data.url,
                "revised_prompt": image_data.revised_prompt
            })
        
        return {
            "images": images,
            "provider": "openai",
            "model": "dall-e-3"
        }
    
    def _generate_stabilityai(self, prompt: str, size: str, num_images: int) -> Dict:
        """Gera imagem usando Stability AI"""
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {self.stabilityai_api_key}",
            "Content-Type": "application/json"
        }
        
        width, height = map(int, size.split('x'))
        
        data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": num_images,
            "steps": 30
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        images = []
        
        for i, image_data in enumerate(result.get("artifacts", [])):
            images.append({
                "base64": image_data["base64"],
                "seed": image_data["seed"],
                "index": i
            })
        
        return {
            "images": images,
            "provider": "stabilityai",
            "model": "stable-diffusion-xl-1024-v1-0"
        }
    
    def download_image(self, url: str, format: str = "webp") -> Optional[bytes]:
        """Faz download e converte imagem"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            # Converte para o formato desejado
            output = BytesIO()
            img.save(output, format=format.upper())
            
            return output.getvalue()
            
        except Exception as e:
            print(f"Erro no download da imagem: {e}")
            return None

def register():
    return ImageGeneratorPlugin()
