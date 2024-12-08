import json
import logging
import os
import arxiv  # Biblioteca para buscar papers en arXiv
from dotenv import load_dotenv
import openai  # Cliente de OpenAI para generación de texto
from groq import Groq  # Cliente alternativo de LLM
import random  # Para generación de grafos de conocimiento de respaldo
from typing import List, Dict, Optional  # Tipado de datos
import translators as ts  # Biblioteca para traducción de consultas
from langsmith import Client, traceable  # Decorador para seguimiento y rastreo de funciones
from langchain.callbacks import LangChainTracer

# Cargar variables de entorno
load_dotenv()

class ScientificContentRAG:
    # Mapeo de dominios científicos entre español e inglés
    # Esto permite búsquedas más precisas en diferentes idiomas
    DOMAIN_MAP = {
        "física cuántica": "Quantum Physics",
        "inteligencia artificial": "Artificial Intelligence", 
        "neurociencia": "Neuroscience",
        "biología molecular": "Molecular Biology",
        "astrofísica": "Astrophysics",
        "cambio climático": "Climate Change",
        "genética": "Genetics",
        "nanotecnología": "Nanotechnology",
        "robótica": "Robotics",
        "computación cuántica": "Quantum Computing"
    }
    
    def __init__(
        self, 
        domain: str = "física cuántica",  # Dominio científico por defecto
        language: str = "castellano",     # Idioma de salida por defecto
        max_papers: int = 5,              # Límite de papers a recuperar
        provider: str = 'openai'          # Proveedor de LLM por defecto
    ):
        """
        Constructor del sistema RAG (Retrieval-Augmented Generation) científico.
        
        Características principales:
        - Mapea dominios científicos
        - Configura proveedor de LLM
        - Permite personalización de búsqueda
        """
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
         # Configurar LangSmith
        try:
            self.langsmith_client = Client(
                api_key=os.getenv('LANGCHAIN_API_KEY'),
                
            )
        except Exception as e:
            self.logger.error(f"Error inicializando LangSmith: {e}")
            self.langsmith_client = None
            
        self.tracer = LangChainTracer()
        # Convertir el dominio a su equivalente en inglés para búsquedas más precisas
        self.domain_en = self.DOMAIN_MAP.get(domain.lower(), domain)
        self.domain = domain
        self.language = language
        self.max_papers = max_papers
        self.provider = provider
        
        # Inicialización dinámica del cliente LLM según el proveedor
        if provider == 'openai':
            self.client = openai.OpenAI()
            self.model = "gpt-4o-mini"  # Modelo más reciente y eficiente
        elif provider == 'groq':
            self.client = Groq()
            self.model = "llama3-8b-8192"  # Modelo alternativo de Groq
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")
        
    
    def _translate_query(self, query: str) -> str:
        """
        Traduce consultas al inglés para búsquedas más precisas.
        
        Características:
        - Usa librería de traducción externa
        - Maneja errores de traducción
        - Fallback a consulta original si falla
        """
        try:
            # Traducción robusta usando librería translators
            translated_query = ts.translate_text(query, to_language='en')
            return translated_query
        except Exception as e:
            print(f"Translation error: {e}")
            return query  # Si falla, usa consulta original

    @traceable(name="search_arxiv_papers", run_type="llm", tags=["scientific-content"])
    def _search_arxiv_papers(self, query: str) -> List[Dict]:
        """
        Búsqueda de papers científicos en arXiv.
        
        Proceso:
        1. Traduce consulta
        2. Combina dominio y consulta
        3. Busca en arXiv
        4. Extrae metadatos relevantes
        """
        # Traducir consulta para búsqueda precisa
        query_en = self._translate_query(query)
        
        # Combinar dominio y consulta para mayor precisión
        full_query = f"{self.domain_en} {query_en}"
        
        # Búsqueda en arXiv con parámetros configurables
        search = arxiv.Search(
            query=full_query,
            max_results=self.max_papers,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        # Recolectar información de papers
        papers = []
        for result in search.results():
            papers.append({
                'title': result.title,
                'summary': result.summary,
                'authors': [author.name for author in result.authors],
                'url': result.entry_id
            })
        extra_metadata = {
        "query": query, 
        "domain": self.domain_en, 
        "papers_found": len(papers), 
        "language": self.language, 
        "max_results_configured": self.max_papers
    }
        return papers

    @traceable(name="synthesize_content", run_type="llm", tags=["scientific-content"])
    def _synthesize_content(self, papers: List[Dict], query: str) -> str:
        """
        Sintetiza contenido científico utilizando LLM.
        
        Proceso avanzado de generación:
        1. Preparar papers
        2. Configurar instrucciones de sistema
        3. Generar contenido adaptado a idioma y dominio
        """
        # Traducir consulta
        query_en = self._translate_query(query)
        
        # Formatear textos de papers
        paper_texts = "\n\n".join([
            f"Paper: {p['title']}\nSummary: {p['summary']}" 
            for p in papers
        ])
        
        # Mapeo de idiomas para instrucciones
        language_instructions = {
            "castellano": "Spanish",
            "english": "English", 
            "français": "French",
            "italiano": "Italian"
        }
    
        # Prompt de sistema altamente estructurado
        system_prompt = f"""
        You are a scientific communicator expert in {self.domain_en}. 
        Your goal is to generate a one-page scientific article 
        that is comprehensible for a general audience.
        
        Instructions:
        - Base the article on the provided papers
        - Explain concepts in a simple manner
        - Use clear and accessible language
        - Maintain scientific rigor
        - VERY IMPORTANT: Write the entire article in {language_instructions.get(self.language, 'the specified language')}
        """
        
        # Prompt de usuario con papers y detalles específicos
        user_prompt = f"""
        Specific Topic: {query_en}
        
        Scientific Papers:
        {paper_texts}
        
        Please write an article of approximately 500 words entirely in {language_instructions.get(self.language, 'the target language')}.
        """
        
        # Generación de contenido con LLM
        response = self.client.chat.completions.create(
    model=self.model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    extra_headers={
        "X-Langsmith-Trace": "true"  # Opcional: añade un header para identificación
    }
)
        
        return response.choices[0].message.content

    @traceable(name="generate_knowledge_graph", run_type="llm", tags=["scientific-content"])
    def _generate_knowledge_graph(self, papers: List[Dict]) -> List[Dict]:
        """
        Generación de grafo de conocimiento avanzado.
        
        Características:
        - Extracción semántica de relaciones
        - Manejo de errores con generación de respaldo
        - Priorización de relaciones significativas
        """
        if not papers:
            return []
        
        try:
            # Generación de grafo con LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": """
                        Advanced scientific knowledge graph generator. 
                        Extract meaningful semantic relationships.
                        """
                    },
                    {
                        "role": "user", 
                        "content": f"""
                        Generate most significant knowledge graph relationships.
                        
                        Guidelines:
                        - Extract 3-5 impactful conceptual relationships
                        - Provide brief explanations
                        - Format: Source Concept | Relationship | Target Concept | Explanation

                        Papers Summaries:
                        {"\n\n".join([
                            f"Paper {i+1}: Title: {p['title']}\nSummary: {p['summary']}" 
                            for i, p in enumerate(papers)
                        ])}
                        """
                    },
                    
                ],
                extra_headers={
        "X-Langsmith-Trace": "true"
    },
                temperature=0.7  # Mayor creatividad
            )
            
            # Procesamiento avanzado de relaciones
            relations_text = response.choices[0].message.content
            graph_enrichment = []
            
            for line in relations_text.split('\n'):
                if '|' in line:
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) >= 3:
                        relation_dict = {
                            'source_concept': parts[0],
                            'relation': parts[1],
                            'target_concept': parts[2],
                            'explanation': parts[3] if len(parts) > 3 else "No explanation"
                        }
                        graph_enrichment.append(relation_dict)
            
            return graph_enrichment
        
        except Exception as e:
            print(f"Advanced graph generation error: {e}")
            # Generación de respaldo con relaciones aleatorias
            return [
                {
                    'source_concept': papers[0]['title'].split()[:2],
                    'relation': random.choice([
                        'theoretical connection', 
                        'methodological influence', 
                        'conceptual derivation'
                    ]),
                    'target_concept': papers[-1]['title'].split()[-2:],
                    'explanation': 'Preliminary relationship'
                }
                for _ in range(3)
            ]
    @traceable(name="enrich_graph_relationships", run_type="llm", tags=["scientific-content"])
    def _enrich_graph_relationships(self, graph_enrichment: List[Dict]) -> List[Dict]:
        """
        Enriquecimiento de relaciones del grafo con metadatos adicionales.
        
        Características:
        - Procesamiento robusto de JSON
        - Múltiples estrategias de extracción
        - Validación estricta de estructura
        """
        try:
            # Generación de enriquecimiento con LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "Enrich scientific concept relationships with context and significance."
                    },
                    {
                        "role": "user", 
                        "content": f"""
                        Provide enriched scientific relationships in strict JSON.
                        
                        Original Relationships:
                        {json.dumps(graph_enrichment, indent=2)}
                        
                        FORMAT STRICTLY AS:
                        [
                            {{
                                "source_concept": "string",
                                "relation": "string",
                                "target_concept": "string",
                                "significance": "high/medium/low",
                                "implications": "Short description",
                                "confidence_level": "high/medium/low"
                            }}
                        ]
                        """
                    }
                ],
                extra_headers={
        "X-Langsmith-Trace": "true"
    }
            )
            
            # Procesamiento robusto de JSON
            response_text = response.choices[0].message.content.strip()
            
            def parse_json(text):
                try:
                    # Múltiples estrategias de parseo
                    parsed = json.loads(text)
                    return parsed if isinstance(parsed, list) else None
                except json.JSONDecodeError:
                    # Estrategias de extracción alternativas
                    import re
                    json_match = re.search(r'\[.*\]', text, re.DOTALL | re.MULTILINE)
                    if json_match:
                        return json.loads(json_match.group(0))
                return None
            
            # Validaciones y procesamiento
            parsed_data = parse_json(response_text)
            
            def validate_enrichment(item):
                required_keys = [
                    'source_concept', 'relation', 'target_concept', 
                    'significance', 'implications', 'confidence_level'
                ]
                return all(key in item for key in required_keys)
            
            # Filtrado de enriquecimientos válidos
            valid_enrichments = [
                item for item in parsed_data 
                if validate_enrichment(item)
            ]
            
            return valid_enrichments or graph_enrichment
        
        except Exception as e:
            print(f"Enrichment process failed: {e}")
            return graph_enrichment

    @traceable(name="generate_scientific_graph_report", run_type="llm", tags=["scientific-content"])
    def generate_scientific_graph_report(self, query: str) -> Dict:
        """
        Método principal: genera informe científico completo.
        
        Proceso integral:
        1. Traducir consulta
        2. Buscar papers
        3. Sintetizar contenido
        4. Generar grafo de conocimiento
        5. Enriquecer grafo
        """
        # Traducir consulta para procesamiento consistente
        query_en = self._translate_query(query)
        
        # Recuperar papers científicos
        papers = self._search_arxiv_papers(query_en)
        
        if not papers:
            return {
                'error': 'No scientific papers found',
                'papers': [],
                'graph_enrichment': []
            }
        
        # Sintetizar contenido científico
        scientific_content = self._synthesize_content(papers, query_en)
        
        # Generar y enriquecer grafo de conocimiento
        graph_enrichment = self._generate_knowledge_graph(papers)
        try:
            graph_enrichment = self._enrich_graph_relationships(graph_enrichment)
        except Exception as e:
            print(f"Graph enrichment failed: {e}")
        
        # Retornar informe científico completo
        return {
            'scientific_content': scientific_content,
            'papers': papers,
            'graph_enrichment': graph_enrichment
        }