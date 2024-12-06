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
        """
        Genera un grafo de conocimiento basado en relaciones semánticas de los papers.
        
        :param papers: Lista de papers
        :return: Lista de relaciones de conocimiento
        """
        if not papers:
            return []
        
        try:
            # Usar LLM para generar relaciones semánticas más inteligentes
            paper_texts = "\n\n".join([
                f"Paper: {p['title']}\nSummary: {p['summary']}" 
                for p in papers
            ])
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert scientific knowledge graph generator. Extract key semantic relationships between scientific concepts."
                    },
                    {
                        "role": "user", 
                        "content": f"""
                        Analyze these scientific papers and generate 3-5 meaningful knowledge graph relationships.
                        Format each relationship as: 
                        source_concept (paper title) | relation type | target_concept (another paper title or key concept)

                        Papers:
                        {paper_texts}
                        """
                    }
                ]
            )
            
            # Parsear respuesta del LLM
            relations_text = response.choices[0].message.content
            
            # Parsear texto de relaciones
            graph_enrichment = []  # Inicializa una lista vacía para almacenar las relaciones

            for line in relations_text.split('\n'):  # Divide el texto en líneas
                if '|' in line:  # Verifica si la línea contiene el separador '|'
                    parts = line.split('|')  # Divide la línea en partes usando '|'
                    
                    if len(parts) == 3:  # Verifica que la línea tenga exactamente 3 partes
                        graph_enrichment.append({  # Agrega un diccionario a la lista
                            'source_concept': parts[0].strip(),  # Primer elemento (concepto fuente)
                            'relation': parts[1].strip(),  # Segundo elemento (tipo de relación)
                            'target_concept': parts[2].strip()  # Tercer elemento (concepto destino)
                        })
            
            return graph_enrichment
        
        except Exception as e:
            print(f"Error generating knowledge graph: {e}")
            # Fallback to random relations if generation fails
            return [
                {
                    'source_concept': random.choice(papers)['title'].split()[:2],
                    'relation': random.choice(['related to', 'influences', 'derives from']),
                    'target_concept': random.choice(papers)['title'].split()[-2:]
                }
                for _ in range(3)
            ]

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
        
        return {
            'scientific_content': scientific_content,
            'papers': papers,
            'graph_enrichment': graph_enrichment
        }