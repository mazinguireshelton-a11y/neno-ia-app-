import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
import re
from datetime import datetime
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class CooperativeOrchestrator:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.complexity_threshold = 500  # Limite de tokens para considerar "complexo"
        self.max_workers = 3  # Máximo de provedores trabalhando juntos
        
    def analyze_complexity(self, prompt: str, task_type: str = "general") -> Dict:
        """
        Analisa a complexidade da tarefa para decidir se precisa de cooperação
        """
        # Análise básica de complexidade
        word_count = len(prompt.split())
        char_count = len(prompt)
        sentence_count = len(re.split(r'[.!?]+', prompt))
        
        # Verificar palavras-chave de complexidade
        complexity_keywords = [
            'ebook', 'livro', '100 páginas', 'longo', 'extenso', 'completo',
            'detalhado', 'profundo', 'pesado', 'complexo', 'capítulos',
            'seções', 'tópicos múltiplos', 'tutorial completo'
        ]
        
        has_complex_keywords = any(keyword in prompt.lower() for keyword in complexity_keywords)
        
        # Calcular score de complexidade
        complexity_score = (
            (word_count * 0.3) +
            (char_count * 0.1) + 
            (sentence_count * 0.5) +
            (100 if has_complex_keywords else 0)
        )
        
        needs_cooperation = complexity_score > self.complexity_threshold
        
        return {
            "complexity_score": complexity_score,
            "needs_cooperation": needs_cooperation,
            "word_count": word_count,
            "char_count": char_count,
            "sentence_count": sentence_count,
            "has_complex_keywords": has_complex_keywords,
            "recommended_workers": min(math.ceil(complexity_score / 300), self.max_workers)
        }
    
    def divide_task(self, prompt: str, num_workers: int) -> List[Dict]:
        """
        Divide uma tarefa complexa em subtarefas para cada provedor
        """
        if num_workers == 1:
            return [{"task": prompt, "role": "primary"}]
        
        # Prompt para dividir a tarefa
        division_prompt = f"""
        Divida a seguinte tarefa em {num_workers} partes coerentes e complementares:
        
        TAREFA PRINCIPAL:
        {prompt}
        
        Forneça as {num_workers} subtarefas em formato JSON, cada uma sendo um objeto com:
        - task: a descrição da subtarefa
        - role: o papel específico (pesquisador, escritor, revisor, etc.)
        - depends_on: se depende de outra subtarefa (opcional)
        """
        
        try:
            # Usar um provedor para dividir a tarefa
            division_result = self.llm_service.get_response(
                [{"role": "user", "content": division_prompt}],
                temperature=0.3
            )
            
            # Extrair JSON da resposta
            import json
            json_match = re.search(r'\[.*\]', division_result['content'], re.DOTALL)
            if json_match:
                subtasks = json.loads(json_match.group())
                return subtasks[:num_workers]
            
        except Exception as e:
            logger.warning(f"Erro ao dividir tarefa: {e}")
        
        # Fallback: divisão simples por tópicos
        return self._simple_task_division(prompt, num_workers)
    
    def _simple_task_division(self, prompt: str, num_workers: int) -> List[Dict]:
        """Divisão simples de tarefa baseada em palavras-chave"""
        keywords = prompt.lower().split()
        chunk_size = len(keywords) // num_workers
        
        subtasks = []
        for i in range(num_workers):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < num_workers - 1 else None
            chunk = ' '.join(keywords[start_idx:end_idx])
            
            subtasks.append({
                "task": f"{chunk} - parte {i+1} de {num_workers}",
                "role": ["pesquisador", "escritor", "revisor"][i % 3],
                "order": i + 1
            })
        
        return subtasks
    
    async def execute_cooperative_task(self, prompt: str, stream: bool = False) -> Dict:
        """
        Executa uma tarefa usando múltiplos provedores cooperativamente
        """
        # Analisar complexidade
        complexity = self.analyze_complexity(prompt)
        
        if not complexity["needs_cooperation"]:
            # Tarefa simples - usar apenas um provedor
            logger.info("Tarefa simples - usando provedor único")
            return await self._execute_single_provider(prompt, stream)
        
        # Tarefa complexa - usar cooperação
        num_workers = complexity["recommended_workers"]
        logger.info(f"Tarefa complexa - usando {num_workers} provedores cooperativamente")
        
        # Dividir tarefa
        subtasks = self.divide_task(prompt, num_workers)
        
        # Executar subtasks em paralelo
        results = await self._execute_parallel(subtasks, stream)
        
        # Combinar resultados
        final_result = await self._combine_results(results, prompt)
        
        return {
            "cooperative": True,
            "workers_used": num_workers,
            "complexity_analysis": complexity,
            "subtasks": subtasks,
            "final_result": final_result
        }
    
    async def _execute_single_provider(self, prompt: str, stream: bool) -> Dict:
        """Executa com provedor único"""
        result = self.llm_service.get_response(
            [{"role": "user", "content": prompt}],
            stream=stream
        )
        
        if stream:
            return {"stream": result, "cooperative": False}
        else:
            return {
                "content": result["content"],
                "cooperative": False,
                "workers_used": 1
            }
    
    async def _execute_parallel(self, subtasks: List[Dict], stream: bool) -> List[Dict]:
        """Executa subtasks em paralelo"""
        if stream:
            # Para streaming, execução sequencial (mais complexo)
            return await self._execute_sequential_streaming(subtasks)
        else:
            # Execução paralela para respostas completas
            return await self._execute_parallel_blocking(subtasks)
    
    async def _execute_parallel_blocking(self, subtasks: List[Dict]) -> List[Dict]:
        """Execução paralela bloqueante"""
        results = []
        
        with ThreadPoolExecutor(max_workers=len(subtasks)) as executor:
            # Mapear subtasks para futures
            future_to_task = {
                executor.submit(
                    self.llm_service.get_response,
                    [{"role": "user", "content": task["task"]}],
                    temperature=0.7
                ): task for task in subtasks
            }
            
            # Coletar resultados conforme ficam prontos
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append({
                        "task": task,
                        "result": result,
                        "success": True
                    })
                except Exception as e:
                    results.append({
                        "task": task,
                        "error": str(e),
                        "success": False
                    })
        
        return results
    
    async def _combine_results(self, results: List[Dict], original_prompt: str) -> Dict:
        """Combina resultados das subtasks"""
        successful_results = [r for r in results if r["success"]]
        
        if not successful_results:
            raise Exception("Todas as subtasks falharam")
        
        # Se apenas uma subtask, retornar diretamente
        if len(successful_results) == 1:
            return successful_results[0]["result"]
        
        # Combinar múltiplos resultados
        combined_content = "\n\n".join(
            f"## PARTE {i+1} - {result['task']['role']}\n{result['result']['content']}"
            for i, result in enumerate(successful_results)
        )
        
        # Prompt para combinação final
        combine_prompt = f"""
        Combine os seguintes resultados parciais em uma resposta coesa e completa:
        
        PROMPT ORIGINAL:
        {original_prompt}
        
        RESULTADOS PARCIAIS:
        {combined_content}
        
        Forneça uma resposta final integrada que una todos os aspectos de forma harmoniosa.
        """
        
        try:
            final_result = self.llm_service.get_response(
                [{"role": "user", "content": combine_prompt}],
                temperature=0.3
            )
            return final_result
        except Exception as e:
            logger.error(f"Erro ao combinar resultados: {e}")
            # Fallback: retornar conteúdo combinado cru
            return {"content": combined_content, "combined_raw": True}
    
    def get_cooperation_status(self) -> Dict:
        """Retorna status do sistema cooperativo"""
        return {
            "cooperative_system": "active",
            "max_workers": self.max_workers,
            "complexity_threshold": self.complexity_threshold,
            "available_providers": len(self.llm_service.providers),
            "provider_names": list(self.llm_service.providers.keys())
        }

# Instância global
cooperative_orchestrator = None

def init_cooperative_orchestrator(llm_service):
    global cooperative_orchestrator
    cooperative_orchestrator = CooperativeOrchestrator(llm_service)
    return cooperative_orchestrator
