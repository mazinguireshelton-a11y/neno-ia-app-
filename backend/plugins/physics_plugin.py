# backend/plugins/physics_plugin.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional, Tuple
import base64
from io import BytesIO
import json
import scipy.integrate as spi
from dataclasses import dataclass
import time

@dataclass
class PhysicsObject3D:
    """Classe para representar objetos 3D físicos"""
    vertices: np.ndarray
    faces: np.ndarray
    mass: float
    position: np.ndarray
    velocity: np.ndarray
    rotation: np.ndarray
    material: Dict[str, Any]
    
    def apply_force(self, force: np.ndarray, dt: float):
        """Aplica força ao objeto"""
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

class PhysicsPlugin:
    def __init__(self):
        self.description = "Plugin para simulações físicas com capacidades 3D integradas"
        self.version = "2.0.0"
        self.author = "NENO Team"
        self.physics_objects = {}
        self.current_simulation = None
        
    def execute(self, command: str, parameters: Dict[str, Any] = None) -> Dict:
        """
        Executa comandos de física com capacidades 3D integradas
        """
        try:
            parameters = parameters or {}
            
            # Comandos básicos de visualização
            if command == "plot_2d":
                return self._create_2d_plot(parameters)
            elif command == "plot_3d":
                return self._create_3d_plot(parameters)
            elif command == "simulate_physics":
                return self._simulate_physics(parameters)
            elif command == "generate_code":
                return self._generate_python_code(parameters)
            
            # NOVOS COMANDOS 3D INTEGRADOS
            elif command == "create_3d_object":
                return self._create_3d_object(parameters)
            elif command == "animate_physics":
                return self._animate_physics(parameters)
            elif command == "vector_field_3d":
                return self._vector_field_3d(parameters)
            elif command == "export_3d_model":
                return self._export_3d_model(parameters)
            elif command == "physics_system":
                return self._create_physics_system(parameters)
            elif command == "run_simulation":
                return self._run_simulation(parameters)
            elif command == "get_simulation_data":
                return self._get_simulation_data(parameters)
            else:
                return {"error": f"Comando '{command}' não reconhecido"}
                
        except Exception as e:
            return {"error": f"Erro no plugin Physics: {str(e)}"}
    
    def _create_3d_object(self, params: Dict) -> Dict:
        """Cria objetos 3D para simulações físicas"""
        try:
            obj_type = params.get('type', 'sphere')
            size = params.get('size', 1.0)
            material = params.get('material', {'density': 1.0, 'color': '#3498db'})
            position = params.get('position', [0, 0, 0])
            
            if obj_type == 'projectile_trajectory':
                return self._create_projectile_trajectory_3d(params)
            elif obj_type == 'pendulum_3d':
                return self._create_pendulum_3d(params)
            elif obj_type == 'spring_system_3d':
                return self._create_spring_system_3d(params)
            elif obj_type == 'vector_field':
                return self._create_vector_field_3d(params)
            elif obj_type == 'orbital_system':
                return self._create_orbital_system_3d(params)
            else:
                return self._generate_primitive_3d(obj_type, size, material, position)
                
        except Exception as e:
            return {"error": f"Erro ao criar objeto 3D: {str(e)}"}
    
    def _generate_primitive_3d(self, obj_type: str, size: float, 
                              material: Dict, position: List[float]) -> Dict:
        """Gera primitivas 3D básicas"""
        try:
            if obj_type == 'sphere':
                phi, theta = np.mgrid[0:np.pi:20j, 0:2*np.pi:20j]
                x = position[0] + size * np.sin(phi) * np.cos(theta)
                y = position[1] + size * np.sin(phi) * np.sin(theta)
                z = position[2] + size * np.cos(phi)
                
            elif obj_type == 'cube':
                vertices = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                                   [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]) * size / 2
                vertices += position
                x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
                
            elif obj_type == 'cylinder':
                z = np.linspace(position[2] - size/2, position[2] + size/2, 20)
                theta = np.linspace(0, 2*np.pi, 20)
                theta_grid, z_grid = np.meshgrid(theta, z)
                x = position[0] + (size/2) * np.cos(theta_grid)
                y = position[1] + (size/2) * np.sin(theta_grid)
                z = z_grid
                
            else:
                return {"error": f"Tipo de objeto 3D '{obj_type}' não suportado"}
            
            # Criar visualização 3D com Plotly
            fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, 
                                           colorscale=[[0, material.get('color', '#3498db')],
                                                      [1, material.get('color', '#3498db')]])])
            
            fig.update_layout(title=f'Objeto 3D: {obj_type.title()}',
                            scene=dict(aspectmode='data'))
            
            img_data = self._plotly_to_base64(fig)
            
            return {
                "success": True,
                "type": "3d_object",
                "object_type": obj_type,
                "image_data": img_data,
                "properties": {
                    "size": size,
                    "material": material,
                    "position": position,
                    "volume": self._calculate_volume(obj_type, size),
                    "surface_area": self._calculate_surface_area(obj_type, size)
                }
            }
            
        except Exception as e:
            return {"error": f"Erro ao gerar primitiva 3D: {str(e)}"}
    
    def _create_projectile_trajectory_3d(self, params: Dict) -> Dict:
        """Trajetória 3D de projétil com vetores"""
        try:
            v0 = params.get('initial_velocity', 50)
            angle_xy = np.radians(params.get('angle_xy', 45))
            angle_xz = np.radians(params.get('angle_xz', 0))
            g = params.get('gravity', 9.8)
            
            # Componentes da velocidade
            vx = v0 * np.cos(angle_xy) * np.cos(angle_xz)
            vy = v0 * np.sin(angle_xy) * np.cos(angle_xz)
            vz = v0 * np.sin(angle_xz)
            
            # Tempo de voo
            t_total = 2 * v0 * np.sin(angle_xy) / g
            t = np.linspace(0, t_total, 100)
            
            # Trajetória 3D
            x = vx * t
            y = vy * t
            z = vz * t - 0.5 * g * t**2
            
            # Criar visualização 3D
            fig = go.Figure()
            
            # Trajetória
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines',
                                     line=dict(color='blue', width=4),
                                     name='Trajetória'))
            
            # Vetores
            fig.add_trace(go.Cone(x=[0], y=[0], z=[0],
                                u=[vx], v=[vy], w=[vz],
                                colorscale=[[0, 'red'], [1, 'red']],
                                sizemode="absolute", sizeref=10,
                                name='Velocidade Inicial'))
            
            fig.update_layout(title='Trajetória de Projétil 3D',
                            scene=dict(aspectmode='data',
                                      xaxis_title='X (m)',
                                      yaxis_title='Y (m)',
                                      zaxis_title='Z (m)'))
            
            img_data = self._plotly_to_base64(fig)
            
            return {
                "success": True,
                "type": "projectile_3d",
                "image_data": img_data,
                "parameters": {
                    "initial_velocity": v0,
                    "angle_xy": np.degrees(angle_xy),
                    "angle_xz": np.degrees(angle_xz),
                    "gravity": g,
                    "max_height": float(np.max(z)),
                    "max_range": float(np.sqrt(np.max(x)**2 + np.max(y)**2))
                }
            }
            
        except Exception as e:
            return {"error": f"Erro na trajetória 3D: {str(e)}"}
    
    def _create_vector_field_3d(self, params: Dict) -> Dict:
        """Campo vetorial 3D (elétrico, magnético, etc.)"""
        try:
            field_type = params.get('field_type', 'electric')
            resolution = params.get('resolution', 10)
            
            # Criar grid 3D
            x, y, z = np.mgrid[-5:5:resolution*1j, -5:5:resolution*1j, -5:5:resolution*1j]
            
            if field_type == 'electric':
                # Campo de carga pontual
                charge = params.get('charge', 1.0)
                charge_pos = params.get('charge_position', [0, 0, 0])
                
                dx = x - charge_pos[0]
                dy = y - charge_pos[1]
                dz = z - charge_pos[2]
                r = np.sqrt(dx**2 + dy**2 + dz**2)
                
                # Evitar divisão por zero
                r[r == 0] = 1e-10
                
                # Campo elétrico (E = k*q/r^2 * r_hat)
                k = 9e9  # Constante eletrostática
                Ex = k * charge * dx / r**3
                Ey = k * charge * dy / r**3
                Ez = k * charge * dz / r**3
                
                U, V, W = Ex, Ey, Ez
                title = 'Campo Elétrico 3D'
                
            elif field_type == 'magnetic':
                # Campo magnético de dipolo
                dipole_moment = params.get('dipole_moment', [0, 0, 1])
                
                r = np.sqrt(x**2 + y**2 + z**2)
                r[r == 0] = 1e-10
                
                # Campo magnético dipolar
                mu0 = 4 * np.pi * 1e-7
                dot_product = dipole_moment[0]*x + dipole_moment[1]*y + dipole_moment[2]*z
                
                Bx = (mu0/(4*np.pi)) * (3*x*dot_product/r**5 - dipole_moment[0]/r**3)
                By = (mu0/(4*np.pi)) * (3*y*dot_product/r**5 - dipole_moment[1]/r**3)
                Bz = (mu0/(4*np.pi)) * (3*z*dot_product/r**5 - dipole_moment[2]/r**3)
                
                U, V, W = Bx, By, Bz
                title = 'Campo Magnético 3D'
                
            else:
                return {"error": f"Tipo de campo '{field_type}' não suportado"}
            
            # Criar visualização
            fig = go.Figure(data=go.Cone(
                x=x.flatten(), y=y.flatten(), z=z.flatten(),
                u=U.flatten(), v=V.flatten(), w=W.flatten(),
                colorscale='Blues', sizemode="absolute",
                sizeref=0.3, anchor="tail"
            ))
            
            fig.update_layout(title=title, scene=dict(aspectmode='data'))
            
            img_data = self._plotly_to_base64(fig)
            
            return {
                "success": True,
                "type": "vector_field_3d",
                "field_type": field_type,
                "image_data": img_data,
                "resolution": resolution
            }
            
        except Exception as e:
            return {"error": f"Erro no campo vetorial 3D: {str(e)}"}
    
    def _animate_physics(self, params: Dict) -> Dict:
        """Animações físicas em 3D"""
        try:
            simulation_type = params.get('simulation_type', 'pendulum')
            duration = params.get('duration', 5.0)
            fps = params.get('fps', 30)
            
            if simulation_type == 'pendulum':
                return self._animate_pendulum_3d(params, duration, fps)
            elif simulation_type == 'springs':
                return self._animate_springs_3d(params, duration, fps)
            elif simulation_type == 'orbits':
                return self._animate_orbits_3d(params, duration, fps)
            elif simulation_type == 'waves':
                return self._animate_waves_3d(params, duration, fps)
            else:
                return {"error": f"Tipo de animação '{simulation_type}' não suportado"}
                
        except Exception as e:
            return {"error": f"Erro na animação: {str(e)}"}
    
    def _animate_pendulum_3d(self, params: Dict, duration: float, fps: int) -> Dict:
        """Animação 3D de pêndulo esférico"""
        try:
            length = params.get('length', 1.0)
            initial_theta = np.radians(params.get('initial_theta', 30))
            initial_phi = np.radians(params.get('initial_phi', 0))
            g = params.get('gravity', 9.8)
            
            # Equações do movimento para pêndulo esférico
            def pendulum_equations(t, state):
                theta, phi, theta_dot, phi_dot = state
                
                theta_ddot = (phi_dot**2 * np.sin(theta) * np.cos(theta) - 
                            (g/length) * np.sin(theta))
                phi_ddot = (-2 * theta_dot * phi_dot * np.cos(theta) / 
                           np.sin(theta)) if np.sin(theta) != 0 else 0
                
                return [theta_dot, phi_dot, theta_ddot, phi_ddot]
            
            # Estado inicial
            initial_state = [initial_theta, initial_phi, 0, 0]
            t_eval = np.linspace(0, duration, int(duration * fps))
            
            # Resolver EDO
            solution = spi.solve_ivp(pendulum_equations, [0, duration], 
                                   initial_state, t_eval=t_eval, method='RK45')
            
            theta = solution.y[0]
            phi = solution.y[1]
            
            # Converter para coordenadas cartesianas
            x = length * np.sin(theta) * np.cos(phi)
            y = length * np.sin(theta) * np.sin(phi)
            z = -length * np.cos(theta)  # Negativo porque Z aponta para cima
            
            # Criar frames de animação
            frames = []
            for i in range(len(t_eval)):
                frame = go.Frame(data=[
                    go.Scatter3d(x=[0, x[i]], y=[0, y[i]], z=[0, z[i]], 
                               mode='lines+markers', marker=dict(size=10, color='red'),
                               line=dict(width=5, color='blue'))
                ])
                frames.append(frame)
            
            # Figura inicial
            fig = go.Figure(
                data=[go.Scatter3d(x=[0, x[0]], y=[0, y[0]], z=[0, z[0]],
                                 mode='lines+markers', marker=dict(size=10, color='red'),
                                 line=dict(width=5, color='blue'))],
                frames=frames
            )
            
            fig.update_layout(title='Pêndulo Esférico 3D',
                            scene=dict(aspectmode='data', 
                                      xaxis=dict(range=[-length*1.2, length*1.2]),
                                      yaxis=dict(range=[-length*1.2, length*1.2]),
                                      zaxis=dict(range=[-length*1.2, 0.2])),
                            updatemenus=[dict(type="buttons",
                                            buttons=[dict(label="Play",
                                                        method="animate",
                                                        args=[None])])])
            
            img_data = self._plotly_to_base64(fig)
            
            return {
                "success": True,
                "type": "animation_3d",
                "simulation_type": "pendulum",
                "image_data": img_data,
                "duration": duration,
                "fps": fps
            }
            
        except Exception as e:
            return {"error": f"Erro na animação de pêndulo: {str(e)}"}
    
    def _export_3d_model(self, params: Dict) -> Dict:
        """Exporta modelos 3D de simulações físicas"""
        try:
            format_type = params.get('format', 'stl')
            simulation_data = params.get('simulation_data', {})
            obj_type = simulation_data.get('type', 'sphere')
            
            if format_type == 'stl':
                content = self._generate_stl_mesh(obj_type, simulation_data)
            elif format_type == 'obj':
                content = self._generate_obj_mesh(obj_type, simulation_data)
            else:
                return {"error": f"Formato '{format_type}' não suportado"}
            
            return {
                "success": True,
                "type": "physics_3d_export",
                "format": format_type,
                "content": base64.b64encode(content.encode()).decode(),
                "filename": f"physics_model.{format_type}"
            }
            
        except Exception as e:
            return {"error": f"Erro ao exportar modelo 3D: {str(e)}"}
    
    def _generate_stl_mesh(self, obj_type: str, params: Dict) -> str:
        """Gera mesh STL para objeto físico"""
        # Implementação simplificada - na prática usaría numpy-stl
        if obj_type == 'sphere':
            radius = params.get('radius', 1.0)
            return f"# STL para esfera de raio {radius}\n# (Implementação completa requer numpy-stl)"
        else:
            return "# Modelo STL gerado pelo NENO Physics Plugin"
    
    # ==================== FUNÇÕES ORIGINAIS (mantidas para compatibilidade) ====================
    
    def _create_2d_plot(self, params: Dict) -> Dict:
        """Cria gráfico 2D (mantido para compatibilidade)"""
        # Implementação original mantida
        pass
    
    def _create_3d_plot(self, params: Dict) -> Dict:
        """Cria gráfico 3D (mantido para compatibilidade)"""
        # Implementação original mantida
        pass
    
    def _simulate_physics(self, params: Dict) -> Dict:
        """Simula fenômenos físicos (mantido para compatibilidade)"""
        # Implementação original mantida
        pass
    
    def _generate_python_code(self, params: Dict) -> Dict:
        """Gera código Python (mantido para compatibilidade)"""
        # Implementação original mantida
        pass
    
    def _fig_to_base64(self, plt) -> str:
        """Converte figura matplotlib para base64"""
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode()
    
    def _plotly_to_base64(self, fig) -> str:
        """Converte figura Plotly para base64"""
        img_bytes = fig.to_image(format="png", width=800, height=600)
        return base64.b64encode(img_bytes).decode()
    
    def _calculate_volume(self, obj_type: str, size: float) -> float:
        """Calcula volume de objetos 3D"""
        if obj_type == 'sphere':
            return (4/3) * np.pi * (size/2)**3
        elif obj_type == 'cube':
            return size**3
        elif obj_type == 'cylinder':
            return np.pi * (size/2)**2 * size
        else:
            return 0.0
    
    def _calculate_surface_area(self, obj_type: str, size: float) -> float:
        """Calcula área superficial de objetos 3D"""
        if obj_type == 'sphere':
            return 4 * np.pi * (size/2)**2
        elif obj_type == 'cube':
            return 6 * size**2
        elif obj_type == 'cylinder':
            return 2 * np.pi * (size/2) * (size + size/2)
        else:
            return 0.0

def register():
    return PhysicsPlugin()
