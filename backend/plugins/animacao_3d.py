"""
🎬 SISTEMA DE RENDERIZAÇÃO 3D REAL COM OPENGL ES
Versão: 10.0 - Renderização 3D Real • Compatível Termux • Integração NENO IA
"""

import os
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import logging
import math
import json
import random
import colorsys
from typing import Dict, Any, List, Optional, Tuple, Callable
import sys
from pathlib import Path

# Tentar importar OpenGL ES (compatível com Termux)
try:
    from OpenGL.GLES2 import *
    from OpenGL.GLES2.OES import *
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.arrays import ArrayDatatype
    from OpenGL.raw.GLES2 import _types
    from OpenGL.raw.GLES2.VERSION.GLES2_2_0 import *
    OPENGL_AVAILABLE = True
except ImportError as e:
    logger.warning(f"OpenGL não disponível: {e}")
    OPENGL_AVAILABLE = False

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('neno_3d_renderer')

# =========================================================
# SHADERS OPENGL ES (GLSL ES para mobile/termux)
# =========================================================

VERTEX_SHADER = """
#version 300 es
precision mediump float;
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec3 normal;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out vec3 fragColor;
out vec3 fragNormal;
out vec3 fragPosition;
void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
    fragColor = color;
    fragNormal = mat3(transpose(inverse(model))) * normal;
    fragPosition = vec3(model * vec4(position, 1.0));
}
"""

FRAGMENT_SHADER = """
#version 300 es
precision mediump float;
in vec3 fragColor;
in vec3 fragNormal;
in vec3 fragPosition;
uniform vec3 lightPos;
uniform vec3 viewPos;
out vec4 outColor;
void main() {
    // Luz ambiente
    float ambientStrength = 0.3;
    vec3 ambient = ambientStrength * fragColor;
    
    // Luz difusa
    vec3 norm = normalize(fragNormal);
    vec3 lightDir = normalize(lightPos - fragPosition);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * fragColor;
    
    // Luz especular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - fragPosition);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = specularStrength * spec * vec3(1.0, 1.0, 1.0);
    
    // Combinação final
    vec3 result = (ambient + diffuse + specular);
    outColor = vec4(result, 1.0);
}
"""

SIMPLE_VERTEX_SHADER = """
#version 300 es
precision mediump float;
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
uniform mat4 mvp;
out vec3 fragColor;
void main() {
    gl_Position = mvp * vec4(position, 1.0);
    fragColor = color;
}
"""

SIMPLE_FRAGMENT_SHADER = """
#version 300 es
precision mediump float;
in vec3 fragColor;
out vec4 outColor;
void main() {
    outColor = vec4(fragColor, 1.0);
}
"""

# =========================================================
# SISTEMA DE RENDERIZAÇÃO 3D REAL
# =========================================================

class OpenGLRenderer:
    """Motor de renderização 3D real com OpenGL ES"""
    
    def __init__(self, width, height):
        # 🔥 VERIFICAÇÃO CRÍTICA: Se não tem display, não tenta OpenGL
        if not os.environ.get("DISPLAY"):
            logger.warning("⚠️  Sem display X11 - OpenGL não disponível")
            return
        
        self.initialized = False  # Definido mesmo sem OpenGL
        if not OPENGL_AVAILABLE:
            logger.error("OpenGL ES não está disponível no sistema")
            return
        self.width = width
        self.height = height
        self.program = None
        if not OPENGL_AVAILABLE:
            logger.error("OpenGL ES não está disponível no sistema")
            return
            
        try:
            # Inicializar contexto OpenGL
            glutInit(sys.argv)
            glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
            glutInitWindowSize(width, height)
            glutCreateWindow(b"NENO 3D Render")
            
            # Configurações básicas
            glEnable(GL_DEPTH_TEST)
            glClearColor(0.1, 0.1, 0.2, 1.0)
            
            # Compilar shaders
            self.program = self.compile_shaders(SIMPLE_VERTEX_SHADER, SIMPLE_FRAGMENT_SHADER)
            
            self.initialized = True
            logger.info(f"✅ Renderizador OpenGL ES inicializado: {width}x{height}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar OpenGL: {e}")
            self.initialized = False
    
        glShaderSource(vertex_shader, vertex_source)
        glCompileShader(vertex_shader)
        
        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex_shader).decode()
            raise Exception(f"Erro compilando vertex shader: {error}")
        
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_source)
        glCompileShader(fragment_shader)
        
        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment_shader).decode()
            raise Exception(f"Erro compilando fragment shader: {error}")
        
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        
        if not glGetProgramiv(program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(program).decode()
            raise Exception(f"Erro linkando programa: {error}")
        
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        
        return program
    
    def render_cube(self, position=(0, 0, 0), scale=1.0, rotation=(0, 0, 0), color=(1.0, 0.5, 0.2)):
        """Renderiza um cubo 3D com iluminação básica"""
        if not self.initialized:
            return None
            
        try:
            glUseProgram(self.program)
            
            # Definir matrizes de transformação
            model = self.create_model_matrix(position, scale, rotation)
            view = self.create_view_matrix()
            projection = self.create_projection_matrix()
            
            mvp = np.dot(projection, np.dot(view, model))
            mvp_location = glGetUniformLocation(self.program, "mvp")
            glUniformMatrix4fv(mvp_location, 1, GL_FALSE, mvp)
            
            # Definir vértices do cubo (8 vértices)
            vertices = np.array([
                # Front face
                -0.5, -0.5,  0.5,  # 0
                 0.5, -0.5,  0.5,  # 1
                 0.5,  0.5,  0.5,  # 2
                -0.5,  0.5,  0.5,  # 3
                
                # Back face
                -0.5, -0.5, -0.5,  # 4
                 0.5, -0.5, -0.5,  # 5
                 0.5,  0.5, -0.5,  # 6
                -0.5,  0.5, -0.5,  # 7
            ], dtype=np.float32) * scale
            
            # Cores para cada vértice
            colors = np.array([
                color, color, color, color,  # Front face
                color, color, color, color,  # Back face
            ], dtype=np.float32).flatten()
            
            # Índices para desenhar os triângulos
            indices = np.array([
                # Front face
                0, 1, 2, 2, 3, 0,
                # Back face
                5, 4, 7, 7, 6, 5,
                # Top face
                3, 2, 6, 6, 7, 3,
                # Bottom face
                4, 5, 1, 1, 0, 4,
                # Right face
                1, 5, 6, 6, 2, 1,
                # Left face
                4, 0, 3, 3, 7, 4
            ], dtype=np.uint16)
            
            # Configurar buffers
            vao = glGenVertexArrays(1)
            glBindVertexArray(vao)
            
            vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(0)
            
            color_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
            glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(1)
            
            ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
            
            # Renderizar
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_SHORT, None)
            
            # Limpar
            glBindVertexArray(0)
            glDeleteBuffers(1, [vbo])
            glDeleteBuffers(1, [color_vbo])
            glDeleteBuffers(1, [ebo])
            glDeleteVertexArrays(1, [vao])
            
            return self.capture_frame()
            
        except Exception as e:
            logger.error(f"Erro renderizando cubo: {e}")
            return None
    
    def create_model_matrix(self, position, scale, rotation):
        """Cria matriz de modelo com translação, escala e rotação"""
        model = np.identity(4, dtype=np.float32)
        
        # Translação
        model[3, 0] = position[0]
        model[3, 1] = position[1]
        model[3, 2] = position[2]
        
        # Escala
        model[0, 0] = scale
        model[1, 1] = scale
        model[2, 2] = scale
        
        # Rotação (Euler angles)
        rx, ry, rz = rotation
        rx_mat = np.identity(4, dtype=np.float32)
        ry_mat = np.identity(4, dtype=np.float32)
        rz_mat = np.identity(4, dtype=np.float32)
        
        rx_mat[1, 1] = math.cos(rx)
        rx_mat[1, 2] = -math.sin(rx)
        rx_mat[2, 1] = math.sin(rx)
        rx_mat[2, 2] = math.cos(rx)
        
        ry_mat[0, 0] = math.cos(ry)
        ry_mat[0, 2] = math.sin(ry)
        ry_mat[2, 0] = -math.sin(ry)
        ry_mat[2, 2] = math.cos(ry)
        
        rz_mat[0, 0] = math.cos(rz)
        rz_mat[0, 1] = -math.sin(rz)
        rz_mat[1, 0] = math.sin(rz)
        rz_mat[1, 1] = math.cos(rz)
        
        model = np.dot(model, np.dot(rz_mat, np.dot(ry_mat, rx_mat)))
        
        return model
    
    def create_view_matrix(self):
        """Cria matriz de visualização (câmera)"""
        view = np.identity(4, dtype=np.float32)
        # Posição da câmera ligeiramente afastada
        view[3, 2] = -5.0  # Move a câmera para trás
        return view
    
    def create_projection_matrix(self):
        """Cria matriz de projeção perspectiva"""
        aspect = self.width / self.height
        fov = math.radians(45.0)
        near = 0.1
        far = 100.0
        
        f = 1.0 / math.tan(fov / 2.0)
        projection = np.zeros((4, 4), dtype=np.float32)
        
        projection[0, 0] = f / aspect
        projection[1, 1] = f
        projection[2, 2] = (far + near) / (near - far)
        projection[2, 3] = -1.0
        projection[3, 2] = (2.0 * far * near) / (near - far)
        
        return projection
    
    def capture_frame(self):
        """Captura o frame atual como imagem PIL"""
        try:
            # Ler pixels do buffer
            glReadBuffer(GL_FRONT)
            data = glReadPixels(0, 0, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)
            
            # Converter para imagem PIL
            image = Image.frombytes("RGBA", (self.width, self.height), data)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL tem origem no canto inferior esquerdo
            image = image.convert("RGB")
            
            return image
            
        except Exception as e:
            logger.error(f"Erro capturando frame: {e}")
            # Fallback: imagem preta
            return Image.new("RGB", (self.width, self.height), (0, 0, 0))
    
    def cleanup(self):
        """Limpa recursos OpenGL"""
        if self.program:
            glDeleteProgram(self.program)

# =========================================================
# SISTEMA HÍBRIDO DE RENDERIZAÇÃO
# =========================================================

class HybridRenderer:
    """Sistema híbrido que usa OpenGL quando disponível, fallback para PIL"""
    
    def __init__(self, config):
        self.config = config
        self.width, self.height = config.params['resolution']
        self.initialized = True  # HybridRenderer sempre inicializado
        self.current_frame = 0
        self.time = 0.0
        self.frame_time = 1.0 / config.params['fps']
        
        # Inicializar renderizador OpenGL se disponível
        self.opengl_renderer = None
        if OPENGL_AVAILABLE:
            try:
                self.opengl_renderer = OpenGLRenderer(self.width, self.height)
                logger.info("✅ Renderizador OpenGL inicializado")
            except Exception as e:
                logger.warning(f"⚠️ OpenGL não pôde ser inicializado: {e}")
                self.opengl_renderer = None
        else:
            logger.info("ℹ️  Usando renderizador PIL (fallback)")
        
        logger.info(f"🎥 Renderizador híbrido inicializado: {self.width}x{self.height}")
    
    def render_frame(self):
        """Renderiza um frame usando o melhor método disponível"""
        try:
            # Tentar OpenGL primeiro
            if self.opengl_renderer and self.opengl_renderer.initialized:
                img = self._render_with_opengl()
            else:
                img = self._render_with_pil()
            
            # Aplicar efeitos pós-processamento
            if self.config.params.get('antialiasing', True):
                img = img.filter(ImageFilter.SMOOTH)
            
            # Adicionar informações técnicas
            draw = ImageDraw.Draw(img)
            self._add_professional_info(draw)
            
            self.current_frame += 1
            self.time += self.frame_time
            
            return img
            
        except Exception as e:
            logger.error(f"❌ Erro no renderizador híbrido: {str(e)}")
            return self._render_fallback()
    
    def _render_with_opengl(self):
        """Renderiza usando OpenGL 3D real"""
        category = self.config.params['category']
        anim_type = self.config.params['animation_type']
        
        # Limpar buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if category == 'matematica' and anim_type == 'funcao_3d':
            return self._render_3d_function_opengl()
        elif category == 'fisica' and anim_type == 'trajetoria':
            return self._render_trajectory_opengl()
        elif category == 'espaco':
            return self._render_space_content_opengl()
        else:
            # Renderização 3D genérica - cubo giratório
            rotation = (self.time * 0.5, self.time * 0.8, self.time * 0.3)
            return self.opengl_renderer.render_cube(
                position=(0, 0, 0),
                scale=1.0,
                rotation=rotation,
                color=(0.8, 0.3, 0.2)
            )
    
    def _render_with_pil(self):
        """Renderiza usando PIL (fallback)"""
        img = Image.new('RGB', (self.width, self.height), self.config.params['background_color'])
        draw = ImageDraw.Draw(img)
        
        category = self.config.params['category']
        anim_type = self.config.params['animation_type']
        
        # Renderizar fundo
        if category in ['matematica', 'fisica', 'educativo']:
            self._render_scientific_background(draw, img)
        elif category in ['espaco']:
            self._render_space_background(draw, img)
        else:
            self._render_abstract_background(draw, img)
        
        # Renderizar conteúdo
        if category == 'matematica':
            self._render_mathematical_content(draw, anim_type)
        elif category == 'fisica':
            self._render_physics_content(draw, anim_type)
        elif category == 'espaco':
            self._render_space_content(draw, anim_type)
        
        return img
    
    def _render_3d_function_opengl(self):
        """Renderiza função 3D com OpenGL"""
        # Implementação simplificada - pontos 3D para função z = f(x,y)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Parâmetros da função
        scale = 0.1
        time_factor = self.time * 0.5
        
        # Renderizar múltiplos cubos representando a função
        for x in range(-5, 6, 2):
            for y in range(-5, 6, 2):
                try:
                    # Função z = sin(x² + y² + tempo)
                    z = math.sin((x*x + y*y) * 0.2 + time_factor) * 2
                    
                    # Cor baseada na altura
                    color = (
                        0.5 + 0.5 * math.sin(z * 0.5),
                        0.3 + 0.3 * math.cos(z * 0.7 + 1.0),
                        0.8 + 0.2 * math.sin(z * 0.3 + 2.0)
                    )
                    
                    # Renderizar cubo nesta posição
                    self.opengl_renderer.render_cube(
                        position=(x * 0.3, y * 0.3, z * 0.3),
                        scale=0.1,
                        rotation=(0, 0, 0),
                        color=color
                    )
                    
                except Exception as e:
                    logger.warning(f"Erro renderizando ponto 3D: {e}")
        
        return self.opengl_renderer.capture_frame()
    
    def _render_trajectory_opengl(self):
        """Renderiza trajetória com OpenGL"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Parâmetros da trajetória
        angle = 45  # graus
        velocity = 5
        gravity = 9.8
        radians = math.radians(angle)
        
        # Renderizar esferas ao longo da trajetória
        for t in np.arange(0, 2.0, 0.2):
            x = velocity * math.cos(radians) * t
            y = velocity * math.sin(radians) * t - 0.5 * gravity * t**2
            
            if y >= -2.0:  # Limite inferior
                # Cor que muda com o tempo
                color = (
                    0.8 + 0.2 * math.sin(t * 5.0),
                    0.5 + 0.3 * math.cos(t * 3.0 + 1.0),
                    0.2 + 0.5 * math.sin(t * 2.0 + 2.0)
                )
                
                self.opengl_renderer.render_cube(
                    position=(x * 0.2, y * 0.2, 0),
                    scale=0.05 + t * 0.02,
                    rotation=(t * 2.0, t * 3.0, t * 1.5),
                    color=color
                )
        
        return self.opengl_renderer.capture_frame()
    
    def _render_space_content_opengl(self):
        """Renderiza conteúdo espacial com OpenGL"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Renderizar "sol" central
        self.opengl_renderer.render_cube(
            position=(0, 0, 0),
            scale=0.3,
            rotation=(self.time * 0.1, self.time * 0.2, 0),
            color=(1.0, 0.8, 0.1)
        )
        
        # Renderizar "planetas" orbitando
        num_planets = 3
        for i in range(num_planets):
            angle = 2 * math.pi * i / num_planets + self.time * (0.5 + i * 0.2)
            distance = 1.0 + i * 0.5
            
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance * 0.7
            
            planet_color = (
                0.2 + 0.3 * math.sin(i * 1.3),
                0.4 + 0.4 * math.cos(i * 2.1),
                0.6 + 0.2 * math.sin(i * 0.7)
            )
            
            self.opengl_renderer.render_cube(
                position=(x, y, 0),
                scale=0.1 + i * 0.03,
                rotation=(self.time * (0.3 + i * 0.1), self.time * (0.4 + i * 0.15), 0),
                color=planet_color
            )
        
        return self.opengl_renderer.capture_frame()
    
    # Métodos de fallback (mantidos da versão anterior)
    def _render_scientific_background(self, draw, img):
        for y in range(self.height):
            intensity = int(20 + 30 * (y / self.height))
            draw.line([(0, y), (self.width, y)], fill=(intensity, intensity, intensity + 40))
        
        grid_size = 50
        for x in range(0, self.width, grid_size):
            draw.line([(x, 0), (x, self.height)], fill=(50, 50, 80, 100))
        for y in range(0, self.height, grid_size):
            draw.line([(0, y), (self.width, y)], fill=(50, 50, 80, 100))
    
    def _render_space_background(self, draw, img):
        for y in range(self.height):
            blue = int(10 + 20 * (y / self.height))
            draw.line([(0, y), (self.width, y)], fill=(0, 0, blue))
        
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=(brightness, brightness, brightness))
    
    def _render_mathematical_content(self, draw, anim_type):
        if anim_type == 'funcao_3d':
            self._render_3d_function(draw)
    
    def _render_physics_content(self, draw, anim_type):
        if anim_type == 'trajetoria':
            self._render_trajectory(draw)
    
    def _render_space_content(self, draw, anim_type):
        if anim_type == 'naves_espaciais':
            self._render_space_battle(draw)
    
    def _render_3d_function(self, draw):
        center_x, center_y = self.width // 2, self.height // 2
        scale = 15
        
        for x in range(-8, 9, 2):
            for y in range(-8, 9, 2):
                try:
                    z = (x**2 + y**2) / 20
                    screen_x = center_x + x * scale
                    screen_y = center_y - y * scale - z * scale
                    size = 4
                    color = (255, 100, 100)
                    draw.ellipse([screen_x-size, screen_y-size, screen_x+size, screen_y+size], fill=color)
                except:
                    pass
    
    def _render_trajectory(self, draw):
        center_x, center_y = self.width // 4, self.height * 3 // 4
        scale = 10
        
        angle = 45
        velocity = 50
        gravity = 9.8
        radians = math.radians(angle)
        
        points = []
        for t in np.arange(0, 10, 0.5):
            x = velocity * math.cos(radians) * t
            y = velocity * math.sin(radians) * t - 0.5 * gravity * t**2
            
            if y >= 0:
                screen_x = center_x + x * scale
                screen_y = center_y - y * scale
                points.append((screen_x, screen_y))
                draw.ellipse([screen_x-2, screen_y-2, screen_x+2, screen_y+2], fill=(255, 200, 100))
        
        if len(points) > 1:
            draw.line(points, fill=(0, 255, 0), width=2)
        
        draw.ellipse([center_x-5, center_y-5, center_x+5, center_y+5], fill=(255, 0, 0))
    
    def _render_space_battle(self, draw):
        num_ships = 5
        time_factor = self.time * 0.5
        
        for i in range(num_ships):
            angle = 2 * math.pi * i / num_ships + time_factor
            distance = min(self.width, self.height) * 0.3
            
            x = self.width // 2 + distance * math.cos(angle)
            y = self.height // 2 + distance * math.sin(angle) * 0.7
            
            size = 12
            points = [
                (x, y - size),
                (x - size * 0.7, y + size * 0.5),
                (x + size * 0.7, y + size * 0.5)
            ]
            draw.polygon(points, fill=(100, 150, 255), outline=(200, 200, 255))
            draw.rectangle([x-2, y+size*0.5, x+2, y+size*0.5+8], fill=(255, 200, 0))
    
    def _render_fallback(self):
        img = Image.new('RGB', (self.width, self.height), (20, 20, 40))
        draw = ImageDraw.Draw(img)
        
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 2)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=(200, 200, 255))
        
        draw.text((self.width//2-100, self.height//2), "NENO 3D RENDER", fill=(255, 255, 255))
        return img
    
    def _add_professional_info(self, draw):
        try:
            font = ImageFont.load_default()
            info = (f"FRAME {self.current_frame+1:04d}/{self.config.params['frames']} | "
                   f"TIME {self.time:.2f}s | {self.config.params['quality']}")
            draw.text((10, self.height - 20), info, fill=(255, 255, 255, 180), font=font)
        except:
            pass

# =========================================================
# ATUALIZAÇÃO DO SISTEMA UNIVERSAL PARA USAR RENDERIZADOR HÍBRIDO
# =========================================================

class UniversalAnimationSystem:
    """Sistema universal de animação com renderização 3D real"""
    
    def __init__(self):
        self.name = "Universal Animation System"
        self.version = "10.0"
        
    def create_animation(self, params):
        """Cria animação com renderização 3D real quando disponível"""
        try:
            config = UniversalAnimationConfig(params)
            
            logger.info(f"🎬 Criando animação 3D: {config.params['category']}.{config.params['animation_type']}")
            logger.info(f"📊 Config: {config.params['resolution']} {config.params['fps']}FPS")
            logger.info(f"🔧 OpenGL disponível: {OPENGL_AVAILABLE}")
            
            start_time = time.time()
            
            # Renderizar frames
            renderer = HybridRenderer(config)
            frame_paths = []
            
            for frame_idx in range(config.params['frames']):
                frame = renderer.render_frame()
                frame_path = f"{config.temp_dir}/frame_{frame_idx:06d}.png"
                frame.save(frame_path, 'PNG', compress_level=6)
                frame_paths.append(frame_path)
                
                if frame_idx % 10 == 0:
                    logger.info(f"📸 Frame {frame_idx+1}/{config.params['frames']}")
            
            # Criar vídeo
            result = self._create_video(config, frame_paths)
            
            # Estatísticas
            render_time = time.time() - start_time
            result.update({
                'render_time': render_time,
                'fps_actual': config.params['frames'] / render_time,
                'total_frames': config.params['frames'],
                'resolution': config.params['resolution'],
                'opengl_used': OPENGL_AVAILABLE and renderer.opengl_renderer is not None
            })
            
            logger.info(f"✅ Animação concluída em {render_time:.1f}s")
            logger.info(f"🎮 OpenGL utilizado: {result['opengl_used']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na criação: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _create_video(self, config, frame_paths):
        """Cria vídeo profissional (mantido da versão anterior)"""
        output_path = f"{config.output_dir}/{config.params['filename']}"
        
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(config.params['fps']),
            '-i', f'{config.temp_dir}/frame_%06d.png',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '23',
            '-preset', 'fast',
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            self._cleanup_temp_files(config.temp_dir)
            
            if result.returncode == 0 and os.path.exists(output_path):
                size = os.path.getsize(output_path)
                duration = config.params['frames'] / config.params['fps']
                
                return {
                    'status': 'success',
                    'path': output_path,
                    'format': 'mp4',
                    'size_bytes': size,
                    'duration': duration,
                    'bitrate': size * 8 / duration / 1000 if duration > 0 else 0
                }
            else:
                raise Exception(f"FFmpeg error: {result.stderr}")
                
        except Exception as e:
            self._cleanup_temp_files(config.temp_dir)
            raise e
    
    def _cleanup_temp_files(self, temp_dir):
        try:
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file))
                os.rmdir(temp_dir)
        except:
            pass

# =========================================================
# PLUGIN ATUALIZADO PARA NENO IA
# =========================================================

class NenoAnimationPlugin:
    """Plugin de animação 3D universal com OpenGL para NENO IA"""
    
    def __init__(self):
        self.name = "NENO Universal 3D Animation"
        self.version = "10.0"
        self.supported_formats = ['mp4', 'gif', 'png_sequence']
        self.animation_system = UniversalAnimationSystem()
        
        logger.info(f"🎬 Plugin de animação 3D inicializado: {self.name} v{self.version}")
        logger.info(f"🔧 Suporte OpenGL: {OPENGL_AVAILABLE}")
    
    def info(self):
        """Informações do plugin"""
        return {
            "name": self.name,
            "version": self.version,
            "supported_formats": self.supported_formats,
            "opengl_available": OPENGL_AVAILABLE,
            "capabilities": self.get_capabilities(),
            "categories": UniversalAnimationConfig.ANIMATION_CATEGORIES
        }
    
    def render(self, params):
        """Renderização principal com suporte a OpenGL"""
        try:
            logger.info("🎬 NENO IA - Iniciando renderização 3D universal")
            
            # Processar parâmetros
            processed_params = self._process_parameters(params)
            
            # Criar animação
            result = self.animation_system.create_animation(processed_params)
            
            # Log de resultado
            if result['status'] == 'success':
                logger.info(f"✅ NENO IA - Renderização concluída: {result['path']}")
                logger.info(f"🎮 OpenGL utilizado: {result.get('opengl_used', False)}")
            else:
                logger.error(f"❌ NENO IA - Erro na renderização: {result.get('message', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ NENO IA - Erro no plugin: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _process_parameters(self, params):
        """Processa e valida parâmetros"""
        default_params = {
            'resolution': (640, 480),
            'fps': 30,
            'frames': 60,
            'quality': 'alta',
            'category': 'matematica',
            'animation_type': 'funcao_3d',
            'background_color': (20, 20, 40),
            'filename': 'neno_animation.mp4',
            'antialiasing': True
        }
        
        # Mesclar parâmetros
        processed = default_params.copy()
        processed.update(params)
        
        # Validar resolução
        if processed['resolution'] not in UniversalAnimationConfig.RESOLUTION_PROFILES.values():
            processed['resolution'] = UniversalAnimationConfig.RESOLUTION_PROFILES['hd']
        
        # Validar categoria
        if processed['category'] not in UniversalAnimationConfig.ANIMATION_CATEGORIES:
            processed['category'] = 'matematica'
        
        return processed
    
    def get_capabilities(self):
        """Retorna capacidades do sistema"""
        return {
            "3d_render": OPENGL_AVAILABLE,
            "real_time_preview": False,
            "physics_simulation": True,
            "mathematical_functions": True,
            "particle_systems": True,
            "text_rendering": True,
            "gradients": True,
            "export_formats": ["mp4", "gif", "png"]
        }

# =========================================================
# CONFIGURAÇÃO (mantida da versão anterior)
# =========================================================

class UniversalAnimationConfig:
    """Configuração universal para animações"""
    
    RESOLUTION_PROFILES = {
        'baixa': (320, 240),
        'media': (640, 480),
        'hd': (1280, 720),
        'full_hd': (1920, 1080),
        '4k': (3840, 2160),
        'cinema_4k': (4096, 2160),
        '8k': (7680, 4320),
        'imax': (10240, 5760)
    }
    
    QUALITY_PROFILES = {
        'rascunho': {'antialiasing': False, 'particles': 100},
        'normal': {'antialiasing': True, 'particles': 500},
        'alta': {'antialiasing': True, 'particles': 2000},
        'ultra': {'antialiasing': True, 'particles': 10000},
        'cinema': {'antialiasing': True, 'particles': 50000}
    }
    
    ANIMATION_CATEGORIES = {
        'matematica': ['funcao_3d', 'fractal', 'geometria', 'calculus'],
        'fisica': ['trajetoria', 'ondas', 'particulas', 'mecanica'],
        'espaco': ['naves_espaciais', 'planetas', 'nebulosas', 'buracos_negros'],
        'abstrato': ['formas', 'cores', 'movimento', 'psicodelico'],
        'educativo': ['moleculas', 'atomos', 'celulas', 'sistemas']
    }
    
    def __init__(self, params):
        self.params = self._process_params(params)
        self.temp_dir = self._create_temp_dir()
        self.output_dir = params.get('output_dir', 'output')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _process_params(self, params):
        processed = params.copy()
        
        # Processar perfil de qualidade
        quality = params.get('quality', 'alta')
        if quality in self.QUALITY_PROFILES:
            processed.update(self.QUALITY_PROFILES[quality])
        
        # Processar resolução
        resolution = params.get('resolution', 'hd')
        if isinstance(resolution, str) and resolution in self.RESOLUTION_PROFILES:
            processed['resolution'] = self.RESOLUTION_PROFILES[resolution]
        
        # Garantir valores padrão
        processed.setdefault('fps', 30)
        processed.setdefault('frames', 60)
        processed.setdefault('category', 'matematica')
        processed.setdefault('animation_type', 'funcao_3d')
        processed.setdefault('background_color', (20, 20, 40))
        processed.setdefault('filename', 'neno_animation.mp4')
        
        return processed
    
    def _create_temp_dir(self):
        temp_dir = f"temp_{int(time.time())}"
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

# =========================================================
# INICIALIZAÇÃO PARA TERMUX
# =========================================================

def init_termux_environment():
    """Inicializa ambiente Termux para OpenGL ES"""
    try:
        # Verificar se estamos no Termux
        if 'com.termux' in os.environ.get('PREFIX', ''):
            logger.info("📱 Ambiente Termux detectado")
            
            # Verificar se temos acesso a OpenGL ES
            try:
                # Tentar inicializar contexto mínimo
                os.environ['DISPLAY'] = ':0'
                
                # Verificar se temos bibliotecas necessárias
                result = subprocess.run(['pkg', 'list-installed'], 
                                      capture_output=True, text=True)
                
                if 'mesa' not in result.stdout:
                    logger.info("📦 Instalando bibliotecas gráficas...")
                    subprocess.run(['pkg', 'install', 'mesa', 'freeglut', '-y'], 
                                  capture_output=True)
                
                return True
            except Exception as e:
                logger.warning(f"⚠️ Configuração Termux incompleta: {e}")
                return False
        return False
    except:
        return False

# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

if __name__ == "__main__":
    # Inicializar ambiente Termux se necessário
    init_termux_environment()
    
    # Exemplo de uso
    plugin = NenoAnimationPlugin()
    
    # Parâmetros de exemplo
    params = {
        'resolution': 'hd',
        'fps': 30,
        'frames': 60,
        'quality': 'alta',
        'category': 'matematica',
        'animation_type': 'funcao_3d',
        'filename': 'exemplo_3d_real.mp4'
    }
    
    print("🔧 Informações do plugin:")
    print(json.dumps(plugin.info(), indent=2))
    
    print("\n🎬 Iniciando renderização 3D...")
    result = plugin.render(params)
    
    print("\n📊 Resultado:")
    print(json.dumps(result, indent=2))

# =========================================================
# INSTÂNCIA GLOBAL PARA INTEGRAÇÃO
# =========================================================

# Instância global do plugin
animacao_3d_plugin = NenoAnimationPlugin()

def get_plugin():
    """Interface padrão para integração"""
    return animacao_3d_plugin

# =========================================================
# TESTE DE INTEGRAÇÃO
# =========================================================

if __name__ == "__main__":
    """Teste de integração com o sistema NENO"""
    print("🧪 Testando integração com NENO IA...")
    
    plugin = get_plugin()
    print(f"🔧 Plugin: {plugin.info()["name"]} v{plugin.info()["version"]}")
    
    # Teste rápido
    test_result = plugin.render({
        "category": "fisica",
        "animation_type": "trajetoria", 
        "quality": "balanced",
        "frames": 15
    })
    
    print(f"🎬 Resultado: {test_result["status"]}")
    if test_result["status"] == "success":
        print(f"📁 Arquivo: {test_result["path"]}")
    
    print("✅ Integração concluída!")
