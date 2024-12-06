import arxiv
import openai
from groq import Groq
import random
from typing import List, Dict, Optional

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

    def _search_arxiv_papers(self, query: str) -> List[Dict]:
        """
        Busca papers en arXiv relacionados con el dominio y query.
        
        :param query: Consulta de búsqueda específica
        :return: Lista de papers relevantes
        """
        full_query = f"{self.domain} {query}"
        
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
        You are a scientific communicator expert in {self.domain}. 
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
        Specific Topic: {query}
        
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

    def generate_scientific_graph_report(self, query: str) -> Dict:
        """
        Genera un informe científico con recuperación y síntesis de papers.
        
        :param query: Consulta científica específica
        :return: Diccionario con informe y metadata
        """
        # Recuperar papers
        papers = self._search_arxiv_papers(query)
        
        if not papers:
            return {
                'error': 'No se encontraron papers relevantes',
                'papers': [],
                'graph_enrichment': []
            }
        
        # Sintetizar contenido
        scientific_content = self._synthesize_content(papers, query)
        
        
        # Simular enriquecimiento con grafo de conocimiento
        graph_enrichment = [
            {
                'source_concept': random.choice(papers)['title'].split()[:2],
                'relation': random.choice(['relacionado con', 'influye en', 'deriva de']),
                'target_concept': random.choice(papers)['title'].split()[-2:]
            }
            for _ in range(3)  # Generar 3 relaciones aleatorias
        ]
        
        return {
            'scientific_content': scientific_content,
            'papers': papers,
            'graph_enrichment': graph_enrichment
        }
    