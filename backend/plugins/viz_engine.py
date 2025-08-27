# backend/plugins/viz_engine.py
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, Any
import base64
from io import BytesIO

class VisualizationEngine:
    def __init__(self):
        self.quality = "high"
        
    def create_linear_system_plot(self, A: np.ndarray, x: np.ndarray, b: np.ndarray) -> Dict:
        """Cria visualização para sistema linear"""
        try:
            # Heatmap da matriz
            fig = go.Figure(data=go.Heatmap(
                z=A,
                colorscale='Viridis',
                colorbar=dict(title="Valor")
            ))
            
            fig.update_layout(
                title="Matriz do Sistema Linear",
                xaxis_title="Colunas",
                yaxis_title="Linhas"
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            return {"error": f"Erro na visualização: {str(e)}"}
    
    def create_optimization_plot(self, history: list) -> Dict:
        """Cria visualização para otimização"""
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=list(range(len(history))),
                y=history,
                mode='lines+markers',
                name="Convergência"
            ))
            
            fig.update_layout(
                title="Convergência da Otimização",
                xaxis_title="Iteração",
                yaxis_title="Valor da Função",
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            return {"error": f"Erro na visualização: {str(e)}"}
    
    def create_3d_surface(self, func, x_range, y_range) -> Dict:
        """Cria superfície 3D para funções"""
        try:
            X, Y = np.meshgrid(x_range, y_range)
            Z = np.zeros_like(X)
            
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    Z[i, j] = func(np.array([X[i, j], Y[i, j]]))
            
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            
            fig.update_layout(
                title="Superfície da Função",
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y", 
                    zaxis_title="f(X, Y)"
                )
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            return {"error": f"Erro na visualização 3D: {str(e)}"}
    
    def _fig_to_dict(self, fig) -> Dict:
        """Converte figura para dicionário com base64"""
        try:
            # Para HTML interativo
            html = fig.to_html(include_plotlyjs='cdn')
            
            # Para imagem estática
            img_bytes = fig.to_image(format="png", width=1200, height=800)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            return {
                "success": True,
                "html": html,
                "image": img_base64,
                "format": "png"
            }
        except Exception as e:
            return {"error": f"Erro na conversão: {str(e)}"}
    
    def execute(self, command: str, parameters: Dict) -> Dict:
        """Interface para o NENO IA"""
        try:
            if command == "linear_system_viz":
                return self.create_linear_system_plot(
                    np.array(parameters['matrix']),
                    np.array(parameters['solution']),
                    np.array(parameters['vector'])
                )
                
            elif command == "optimization_viz":
                return self.create_optimization_plot(
                    parameters['history']
                )
                
            elif command == "3d_surface":
                return self.create_3d_surface(
                    parameters['function'],
                    parameters['x_range'],
                    parameters['y_range']
                )
                
            else:
                return {"error": f"Comando de visualização desconhecido: {command}"}
                
        except Exception as e:
            return {"error": f"Erro no VisualizationEngine: {str(e)}"}

def register():
    return VisualizationEngine()
