# backend/utils/constants.py
"""Constantes """

# ==================== MODOS DISPONÍVEIS ====================
MODES = {
    # ==================== MODOS PRINCIPAIS ====================
    "default": {
        "name": "Padrão", 
        "icon": "💬", 
        "color": "#10b981",
        "category": "geral",
        "description": "Modo geral para conversas e tarefas cotidianas"
    },
    
    # ==================== MODOS TÉCNICOS ====================
    "programmer": {
        "name": "Programador", 
        "icon": "👨‍💻", 
        "color": "#8b5cf6",
        "category": "tecnico",
        "description": "Desenvolvimento, código, debugging e arquitetura de software"
    },
    
    # ==================== MODOS CIENTÍFICOS ====================
    "research": {
        "name": "Pesquisa", 
        "icon": "🔬", 
        "color": "#f59e0b",
        "category": "cientifico",
        "description": "Pesquisa acadêmica, análise de dados e metodologia científica"
    },
    
    "physics_basic": {
        "name": "Física Básica", 
        "icon": "📊", 
        "color": "#6366f1",
        "category": "cientifico",
        "level": "iniciante",
        "description": "Simulações simples, gráficos e visualizações 3D básicas",
        "3d_capabilities": True,
        "interactive_3d": False
    },
    
    "physics_advanced": {
        "name": "Física Avançada", 
        "icon": "⚛️", 
        "color": "#06b6d4", 
        "category": "cientifico",
        "level": "intermediário",
        "description": "Simulações complexas, análise profunda e modelagem 3D avançada",
        "3d_capabilities": True,
        "interactive_3d": True,
        "real_time_simulation": True
    },
    
    # ==================== NOVO MODO: SUPER COMPUTAÇÃO ====================
    "super_compute": {
        "name": "Super Computação", 
        "icon": "🚀", 
        "color": "#ff6b6b",
        "category": "tecnico",
        "level": "avançado",
        "description": "Computação de alto desempenho, algoritmos complexos e processamento paralelo",
        "high_performance": True,
        "parallel_processing": True,
        "cluster_computing": True,
        "big_data": True
    },
    
    # ==================== MODOS CRIATIVOS ====================
    "creative": {
        "name": "Criativo", 
        "icon": "🎨", 
        "color": "#ec4899",
        "category": "criativo", 
        "description": "Ideias, histórias, conteúdo criativo e brainstorming"
    },
    
    # ==================== MODOS DE COMUNICAÇÃO ====================
    "voice": {
        "name": "Voz", 
        "icon": "🎙️", 
        "color": "#3b82f6",
        "category": "comunicacao",
        "description": "Conversação natural por voz em múltiplos idiomas",
        "multilingual": True,
        "supported_languages": ["pt-BR", "en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "ja-JP", "zh-CN", "ru-RU", "ar-SA"],
        "real_time": True
    }
}

# ==================== CATEGORIAS ORGANIZADAS ====================
MODE_CATEGORIES = {
    "geral": {
        "name": "Geral",
        "color": "#10b981",
        "modes": ["default"]
    },
    "tecnico": {
        "name": "Técnico", 
        "color": "#8b5cf6",
        "modes": ["programmer", "super_compute"]  # ✅ ADICIONADO super_compute
    },
    "cientifico": {
        "name": "Científico",
        "color": "#f59e0b", 
        "modes": ["research", "physics_basic", "physics_advanced"]
    },
    "criativo": {
        "name": "Criativo",
        "color": "#ec4899",
        "modes": ["creative"]
    },
    "comunicacao": {
        "name": "Comunicação",
        "color": "#3b82f6",
        "modes": ["voice"]
    }
}

# ==================== CAPACIDADES POR MODO ====================
MODE_CAPABILITIES = {
    "default": ["conversação", "respostas_gerais", "informações"],
    
    "programmer": [
        "python", "javascript", "java", "c++", "html_css",
        "sql", "nosql", "apis", "frameworks", "debugging",
        "arquitetura", "devops", "documentação"
    ],
    
    "super_compute": [  # ✅ NOVAS CAPACIDADES
        "algoritmos_complexos", "processamento_paralelo", 
        "computação_distribuída", "high_performance_computing",
        "big_data_processing", "cluster_computing", 
        "optimização_algoritmos", "simulações_larga_escala",
        "análise_desempenho", "load_balancing", "gpu_computing",
        "computação_cientifica", "modelagem_matemática_avançada"
    ],
    
    "creative": [
        "storytelling", "brainstorm", "conceitos", "narrativa",
        "conteúdo_criativo", "ideias", "inovação"
    ],
    
    "research": [
        "análise_dados", "metodologia", "revisão", "estatística",
        "pesquisa_acadêmica", "referências", "citações"
    ],
    
    "physics_basic": [
        "gráficos_2d", "gráficos_3d", "simulações_simples",
        "visualização_básica", "exportação_imagens",
        "objetos_3d_básicos", "animações_simples",
        "cálculos_básicos", "vetores_simples"
    ],
    
    "physics_advanced": [
        "simulações_tempo_real", "equações_diferenciais", "análise_complexa",
        "animações_3d", "exportação_dados", "análise_física",
        "modelagem_3d_avançada", "simulações_interativas",
        "geração_de_malhas", "visualização_volumétrica",
        "física_colisões", "dinâmica_corpos_rígidos",
        "campos_vetoriais", "simulações_partículas",
        "renderização_física", "exportação_modelos_3d"
    ],
    
    "voice": [
        "stt", "tts", "conversação", "comandos_voz",
        "transcrição", "síntese_vocal", "multilíngue",
        "detecção_automática_idioma", "tradução_em_tempo_real",
        "dicionário_fonético", "correção_pronúncia"
    ]
}

# ==================== TIPOS DE SIMULAÇÃO FÍSICA ====================
PHYSICS_SIMULATION_TYPES = {
    "mecânica": [
        "projétil", "pêndulo", "molas", "colisões",
        "plano_inclinado", "movimento_circular", "gravitação",
        "rotação", "torque", "momentum", "energia"
    ],
    "termodinâmica": [
        "condução", "convecção", "radiação",
        "máquinas_térmicas", "transferência_calor",
        "gases_ideais", "entropia", "ciclos_térmicos"
    ],
    "eletromagnetismo": [
        "campos_elétricos", "campos_magnéticos", "circuitos",
        "ondas_eletromagnéticas", "indução_magnética",
        "capacitores", "indutores", "transformadores"
    ],
    "ótica": [
        "reflexão", "refração", "lentes", "espelhos",
        "interferência", "difração", "polarização",
        "ótica_geométrica", "ótica_física"
    ],
    "fluidos": [
        "hidrostática", "hidrodinâmica", "pressão",
        "empuxo", "vazão", "turbulência",
        "equação_bernoulli", "viscosidade"
    ],
    "quântica": [
        "poço_infinito", "oscillador_harmônico",
        "túnel_quântico", "spin", "orbitals"
    ],
    "relatividade": [
        "dilatação_temporal", "contração_espacial",
        "efeito_doppler_relativístico", "gravitação_relativística"
    ]
}

# ==================== TIPOS DE COMPUTAÇÃO AVANÇADA ====================
SUPER_COMPUTE_TYPES = {  # ✅ NOVA SEÇÃO
    "otimização": [
        "algoritmos_genéticos", "enxame_de_partículas", 
        "simulated_annealing", "otimização_convexa",
        "programação_inteira", "otimização_combinatória"
    ],
    "paralelismo": [
        "multithreading", "multiprocessing", "gpu_computing",
        "cluster_computing", "cloud_computing", "distributed_systems"
    ],
    "simulação": [
        "monte_carlo", "dinâmica_molecular", "computação_fluidos",
        "elementos_finitos", "simulações_cosmológicas", "modelagem_climática"
    ],
    "big_data": [
        "mapreduce", "spark", "hadoop", "processamento_streaming",
        "data_mining", "machine_learning_larga_escala"
    ],
    "alto_desempenho": [
        "vectorization", "memory_optimization", "cache_optimization",
        "load_balancing", "fault_tolerance", "high_availability"
    ]
}

# ==================== OBJETOS 3D FÍSICOS ====================
PHYSICS_3D_OBJECTS = {
    "primitivos": [
        "cubo", "esfera", "cilindro", "cone", 
        "pirâmide", "toro", "plano", "disco",
        "caixa", "capsula", "elipsoide"
    ],
    "superfícies": [
        "parametrica", "revolução", "extrusão",
        "malha_pontos", "superfície_implícita",
        "nurbs", "bezier", "superfície_algebrica"
    ],
    "corpos_rígidos": [
        "poliedro", "prisma", "antiprisma",
        "sólido_platônico", "sólido_arquimediano",
        "sólido_catalan", "poliedro_estrelado"
    ],
    "ferramentas_visuais": [
        "vetores", "campos", "trajetórias",
        "superfícies_equipotenciais", "linhas_campo",
        "isolinhas", "volume_rendering", "partículas"
    ],
    "sistemas_complexos": [
        "sistema_solar", "átomo", "molécula",
        "estrutura_cristalina", "fluido", "campo_eletromagnético"
    ]
}

# ==================== FERRAMENTAS SUPER COMPUTAÇÃO ====================
SUPER_COMPUTE_TOOLS = {  # ✅ NOVA SEÇÃO
    "frameworks": [
        "mpi", "openmp", "cuda", "opencl", "openacc",
        "hadoop", "spark", "dask", "ray", "kubernetes"
    ],
    "linguagens": [
        "c++", "fortran", "python", "julia", "rust",
        "go", "java", "scala"
    ],
    "plataformas": [
        "aws_batch", "azure_batch", "google_cloud_platform",
        "slurm", "torque", "openstack", "docker_swarm"
    ],
    "bibliotecas": [
        "numpy", "scipy", "pytorch", "tensorflow", "jax",
        "numba", "cython", "petsc", "trilinos"
    ]
}

# ==================== CONFIGURAÇÕES PADRÃO POR MODO ====================
DEFAULT_MODE_CONFIGS = {
    "physics_basic": {
        "resolution": "medium",
        "auto_export": True,
        "interactive": False,
        "3d_quality": "low",
        "physics_engine": "simples",
        "max_particles": 1000,
        "real_time": False
    },
    
    "physics_advanced": {
        "resolution": "high",
        "precision": "double", 
        "real_time": True,
        "interactive": True,
        "3d_quality": "high",
        "physics_engine": "avançado",
        "max_particles": 100000,
        "collision_detection": True,
        "multibody_dynamics": True
    },
    
    "super_compute": {  # ✅ NOVAS CONFIGURAÇÕES
        "precision": "double",
        "parallel_processing": True,
        "max_threads": "auto",
        "memory_optimization": True,
        "cache_optimization": True,
        "vectorization": True,
        "error_tolerance": 1e-10,
        "max_iterations": 1000000,
        "convergence_threshold": 1e-8
    },
    
    "programmer": {
        "language": "python",
        "documentation_style": "google",
        "testing_framework": "pytest"
    },
    
    "voice": {
        "auto_detect_language": True,
        "fallback_language": "pt-BR",
        "voice_speed": "normal",
        "voice_style": "natural",
        "auto_punctuation": True,
        "profanity_filter": True,
        "background_noise_reduction": True
    }
}

# ==================== NÍVEIS DE DIFICULDADE ====================
PHYSICS_LEVELS = {
    "iniciante": {
        "color": "#10b981",
        "description": "Para estudantes e curiosos",
        "math_level": "básico",
        "max_complexity": "sistemas_simples",
        "visualization": "gráficos_2d_3d_básicos"
    },
    "intermediário": {
        "color": "#3b82f6", 
        "description": "Para universitários e entusiastas",
        "math_level": "intermediário",
        "max_complexity": "sistemas_multicorpo",
        "visualization": "animação_3d_interativa"
    },
    "avançado": {
        "color": "#ef4444",
        "description": "Para pesquisadores e profissionais",
        "math_level": "avançado",
        "max_complexity": "sistemas_complexos",
        "visualization": "simulação_tempo_real"
    }
}

# ==================== MOTORES FÍSICOS DISPONÍVEIS ====================
PHYSICS_ENGINES = {
    "simples": {
        "name": "Motor Simples",
        "description": "Para simulações básicas e educacionais",
        "capabilities": ["cinemática", "colisões_simples", "gravidade"],
        "performance": "leve"
    },
    "avançado": {
        "name": "Motor Avançado",
        "description": "Para simulações realistas e complexas",
        "capabilities": ["dinâmica_multicorpo", "deformação", "fluidos", "tecido"],
        "performance": "pesado"
    }
}

# ==================== MOTORES SUPER COMPUTAÇÃO ====================
SUPER_COMPUTE_ENGINES = {  # ✅ NOVA SEÇÃO
    "cpu_parallel": {
        "name": "Paralelismo CPU",
        "description": "Processamento paralelo em múltiplos núcleos CPU",
        "capabilities": ["multithreading", "multiprocessing", "vectorization"],
        "performance": "alto"
    },
    "gpu_accelerated": {
        "name": "Aceleração GPU",
        "description": "Computação massivamente paralela em GPU",
        "capabilities": ["cuda", "opencl", "tensor_cores", "ray_tracing"],
        "performance": "extremamente_alto"
    },
    "distributed": {
        "name": "Sistema Distribuído",
        "description": "Computação em cluster com múltiplos nós",
        "capabilities": ["mpi", "spark", "kubernetes", "load_balancing"],
        "performance": "massivo"
    }
}

# ==================== IDIOMAS SUPORTADOS ====================
SUPPORTED_LANGUAGES = {
    "pt-BR": {
        "name": "Português (Brasil)",
        "native_name": "Português Brasileiro",
        "flag": "🇧🇷",
        "voice_models": ["female_1", "male_1", "female_2"],
        "stt_accuracy": 0.95,
        "tts_quality": 0.92
    },
    "en-US": {
        "name": "English (US)",
        "native_name": "American English", 
        "flag": "🇺🇸",
        "voice_models": ["female_1", "male_1", "female_2", "male_2"],
        "stt_accuracy": 0.98,
        "tts_quality": 0.96
    },
    "es-ES": {
        "name": "Español (España)",
        "native_name": "Español",
        "flag": "🇪🇸",
        "voice_models": ["female_1", "male_1"],
        "stt_accuracy": 0.94,
        "tts_quality": 0.91
    },
    "fr-FR": {
        "name": "Français (France)",
        "native_name": "Français",
        "flag": "🇫🇷",
        "voice_models": ["female_1", "male_1"],
        "stt_accuracy": 0.93,
        "tts_quality": 0.90
    },
    "de-DE": {
        "name": "Deutsch (Deutschland)",
        "native_name": "Deutsch",
        "flag": "🇩🇪",
        "voice_models": ["female_1", "male_1"],
        "stt_accuracy": 0.92,
        "tts_quality": 0.89
    },
    "it-IT": {
        "name": "Italiano (Italia)",
        "native_name": "Italiano",
        "flag": "🇮🇹",
        "voice_models": ["female_1", "male_1"],
        "stt_accuracy": 0.91,
        "tts_quality": 0.88
    },
    "ja-JP": {
        "name": "日本語 (日本)",
        "native_name": "日本語",
        "flag": "🇯🇵",
        "voice_models": ["female_1", "male_1"],
        "stt_accuracy": 0.89,
        "tts_quality": 0.87
    },
    "zh-CN": {
        "name": "中文 (中国)",
        "native_name": "简体中文",
        "flag": "🇨🇳",
        "voice_models": ["female_1", "male_1"],
        "stt_accuracy": 0.88,
        "tts_quality": 0.86
    },
    "ru-RU": {
        "name": "Русский (Россия)",
        "native_name": "Русский",
        "flag": "🇷🇺",
        "voice_models": ["female_1", "male_1"],
        "stt_accuracy": 0.90,
        "tts_quality": 0.88
    },
    "ar-SA": {
        "name": "العربية (沙特阿拉伯)",
        "native_name": "العربية",
        "flag": "🇸🇦",
        "voice_models": ["male_1", "male_2"],
        "stt_accuracy": 0.87,
        "tts_quality": 0.85,
        "right_to_left": True
    }
    
    # ... (outros idiomas mantidos)
}

# ==================== LIMITES DA APLICAÇÃO ====================
MAX_MESSAGE_LENGTH = 4000
MAX_CONVERSATION_LENGTH = 20
MAX_FILE_SIZE_MB = 25
MAX_VOICE_DURATION = 120  # segundos
MAX_COMPUTE_TIME = 300    # ✅ NOVO: tempo máximo para super computação

# ==================== TIPOS DE ARQUIVO PERMITIDOS ====================
ALLOWED_FILE_TYPES = [
    "txt", "pdf", "docx", "doc", 
    "jpg", "jpeg", "png", "gif",
    "mp3", "wav", "ogg",
    "csv", "md", "json"
]

# ==================== FORMATOS DE EXPORTAÇÃO 3D ====================
EXPORT_FORMATS = {
    "visualização": ["png", "jpg", "gif", "svg", "webp"],
    "dados": ["csv", "json", "hdf5", "vtk", "xdmf"],
    "modelos_3d": ["stl", "obj", "ply", "gltf", "glb", "fbx"],
    "animação": ["gif", "mp4", "webm", "avi"],
    "código": ["python", "matlab", "c++", "julia", "rust"],
    "interativo": ["html", "javascript", "webgl"]
}

# ==================== FORMATOS SUPER COMPUTAÇÃO ====================
SUPER_COMPUTE_FORMATS = {  # ✅ NOVA SEÇÃO
    "dados_científicos": ["hdf5", "netcdf", "fits", "root"],
    "performance_data": ["json", "csv", "parquet", "avro"],
    "modelos_otimização": ["mps", "lp", "nl", "pyomo"],
    "resultados_simulação": ["vtu", "vts", "xdmf", "ensight"]
}

# ==================== CONFIGURAÇÕES DE API ====================
DEFAULT_LLM_MODELS = {
    "openai": "gpt-4o-mini",
    "openrouter": "openai/gpt-4o-mini",
    "groq": "llama-3.1-70b-versatile"
}

# ==================== TEMPOS DE TIMEOUT (segundos) ====================
TIMEOUTS = {
    "llm_request": 60,
    "voice_transcription": 30,
    "file_upload": 120,
    "web_request": 15,
    "super_compute": 300  # ✅ NOVO: timeout para computação pesada
}

# ==================== MENSAGENS PADRÃO ====================
DEFAULT_MESSAGES = {
    "welcome": "Olá! Sou o NENO, seu assistente de IA. Como posso ajudá-lo hoje?",
    "thinking": "Estou pensando...",
    "computing": "🔄 Processamento intensivo em andamento...",  # ✅ NOVA
    "error": "Desculpe, ocorreu um erro. Por favor, tente novamente.",
    "empty_input": "Por favor, digite uma mensagem.",
    "file_too_large": "Arquivo muito grande. Tamanho máximo: {}MB",
    "invalid_file_type": "Tipo de arquivo não permitido. Tipos válidos: {}",
    "voice_not_supported": "Modo voz não suportado neste navegador.",
    "compute_timeout": "⏰ Tempo de computação excedido. Tente uma tarefa menor."  # ✅ NOVA
}

# ==================== CÓDIGOS DE STATUS ====================
STATUS_CODES = {
    "success": 200,
    "created": 201,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "timeout": 408,
    "server_error": 500,
    "service_unavailable": 503,
    "compute_overload": 529  # ✅ NOVO: servidor sobrecarregado
}
