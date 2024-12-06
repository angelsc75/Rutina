import json
import arxiv
import openai
from groq import Groq
import random
from typing import List, Dict, Optional
import translators as ts  # New import for translation

class ScientificContentRAG:
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
        domain: str = "física cuántica", 
        language: str = "castellano", 
        max_papers: int = 5,
        provider: str = 'openai'
    ):
        """
        Inicializa el sistema RAG para contenido científico.
        
        :param domain: Dominio científico para búsqueda
        :param language: Idioma de generación
        :param max_papers: Número máximo de papers a recuperar
        :param provider: Proveedor de LLM (openai o groq)
        """
        # Map the domain to its English equivalent
        self.domain_en = self.DOMAIN_MAP.get(domain.lower(), domain)
        self.domain = domain
        self.language = language
        self.max_papers = max_papers
        self.provider = provider
        
        # Inicializar cliente LLM
        if provider == 'openai':
            self.client = openai.OpenAI()
            self.model = "gpt-4o-mini"
        elif provider == 'groq':
            self.client = Groq()
            self.model = "llama3-8b-8192"
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")

    def _translate_query(self, query: str) -> str:
        """
        Traduce la consulta al inglés.
        
        :param query: Consulta original
        :return: Consulta traducida al inglés
        """
        try:
            # Usar translators para traducir
            translated_query = ts.translate_text(query, to_language='en')
            return translated_query
        except Exception as e:
            print(f"Translation error: {e}")
            return query  # Fallback to original query if translation fails

    def _search_arxiv_papers(self, query: str) -> List[Dict]:
        """
        Busca papers en arXiv relacionados con el dominio y query.
        
        :param query: Consulta de búsqueda específica
        :return: Lista de papers relevantes
        """
        # Translate query to English
        query_en = self._translate_query(query)
        
        full_query = f"{self.domain_en} {query_en}"
        
        search = arxiv.Search(
            query=full_query,
            max_results=self.max_papers,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for result in search.results():
            papers.append({
                'title': result.title,
                'summary': result.summary,
                'authors': [author.name for author in result.authors],
                'url': result.entry_id
            })
        
        return papers

    def _synthesize_content(self, papers: List[Dict], query: str) -> str:
        """
        Sintetiza contenido científico en el idioma especificado.
        
        :param papers: Lista de papers recuperados
        :param query: Consulta original
        :return: Contenido científico sintetizado en el idioma solicitado
        """
        # Translate query to English
        query_en = self._translate_query(query)
        
        paper_texts = "\n\n".join([
            f"Paper: {p['title']}\nSummary: {p['summary']}" 
            for p in papers
        ])
        
        # Mapeo de idiomas para el sistema
        language_instructions = {
            "castellano": "Spanish",
            "english": "English", 
            "français": "French",
            "italiano": "Italian"
        }
    
        
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
        
        user_prompt = f"""
        Specific Topic: {query_en}
        
        Scientific Papers:
        {paper_texts}
        
        Please write an article of approximately 500 words entirely in {language_instructions.get(self.language, 'the target language')}.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response.choices[0].message.content

    def _generate_knowledge_graph(self, papers: List[Dict]) -> List[Dict]:
        if not papers:
            return []
        
        try:
            # Usar un prompt más detallado para extraer relaciones más significativas
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": """
                        You are an advanced scientific knowledge graph generator. 
                        Your task is to extract the most meaningful and insightful 
                        semantic relationships between scientific concepts.
                        
                        Evaluation criteria:
                        - Prioritize causal relationships
                        - Focus on conceptual connections
                        - Highlight novel or unexpected links
                        - Ensure scientific accuracy
                        """
                    },
                    {
                        "role": "user", 
                        "content": f"""
                        Analyze these scientific papers and generate the most significant knowledge graph relationships.
                        
                        Guidelines:
                        - Extract 3-5 most impactful conceptual relationships
                        - Provide a brief (1-2 word) explanation for each relationship
                        - Format: Source Concept | Relationship Type | Target Concept | Brief Explanation

                        Papers Summaries:
                        {"\n\n".join([
                            f"Paper {i+1}: Title: {p['title']}\nSummary: {p['summary']}" 
                            for i, p in enumerate(papers)
                        ])}
                        """
                    }
                ],
                temperature=0.7  # Slightly higher creativity
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
            # Fallback with more structured random generation
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
    def _enrich_graph_relationships(self, graph_enrichment: List[Dict]) -> List[Dict]:
        """
        Método para enriquecer las relaciones con metadatos adicionales
        Incluye más registro de errores y manejo de casos especiales
        """
        try:
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
                        Provide a detailed enrichment of these scientific relationships in strict JSON format.
                        
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
                        
                        CRITICAL: Respond ONLY with VALID JSON. No additional text.
                        """
                    }
                ]
            )
            
            # Obtener texto de respuesta
            response_text = response.choices[0].message.content.strip()
            
            # Depuración: imprimir respuesta raw
            print("Raw Response:", response_text)
            
            # Intentar parsear JSON de múltiples maneras
            def parse_json(text):
                try:
                    # Método 1: Parseo directo
                    parsed = json.loads(text)
                    return parsed if isinstance(parsed, list) else None
                except json.JSONDecodeError:
                    try:
                        # Método 2: Remover texto antes y después del JSON
                        import re
                        json_match = re.search(r'\[.*\]', text, re.DOTALL | re.MULTILINE)
                        if json_match:
                            return json.loads(json_match.group(0))
                    except Exception as e:
                        print(f"JSON Extraction Error: {e}")
                    return None
            
            # Intentar parsear
            parsed_data = parse_json(response_text)
            
            if parsed_data is None:
                print("CRITICAL: Could not parse JSON")
                return graph_enrichment
            
            # Validar la estructura de los datos
            def validate_enrichment(item):
                required_keys = [
                    'source_concept', 'relation', 'target_concept', 
                    'significance', 'implications', 'confidence_level'
                ]
                return all(key in item for key in required_keys)
            
            # Filtrar y validar entradas
            valid_enrichments = [
                item for item in parsed_data 
                if validate_enrichment(item)
            ]
            
            if not valid_enrichments:
                print("No valid enrichments found. Using original data.")
                return graph_enrichment
            
            return valid_enrichments
        
        except Exception as e:
            print(f"Enrichment process failed: {e}")
            return graph_enrichment        

    def generate_scientific_graph_report(self, query: str) -> Dict:
        """
        Genera un informe científico con recuperación y síntesis de papers.
        
        :param query: Consulta científica específica
        :return: Diccionario con informe y metadata
        """
        # Translate query to English for consistent processing
        query_en = self._translate_query(query)
        
        # Recuperar papers
        papers = self._search_arxiv_papers(query_en)
        
        if not papers:
            return {
                'error': 'No scientific papers found',
                'papers': [],
                'graph_enrichment': []
            }
        
        # Sintetizar contenido
        scientific_content = self._synthesize_content(papers, query_en)
        
        # Generar grafo de conocimiento más inteligente
        graph_enrichment = self._generate_knowledge_graph(papers)
        try:
            graph_enrichment = self._enrich_graph_relationships(graph_enrichment)
        except Exception as e:
            print(f"Graph enrichment failed: {e}")
            # Use original graph_enrichment if enrichment fails
        
        return {
            'scientific_content': scientific_content,
            'papers': papers,
            'graph_enrichment': graph_enrichment
        }