import requests
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from core.llm_manager import LLMManager
class ScientificContentRAG:
    def __init__(self, domain="quantum physics"):
        self.domain = domain
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def fetch_arxiv_papers(self, max_results=10):
        base_url = "http://export.arxiv.org/api/query?"
        search_query = f"search_query=cat:{self.domain}&start=0&max_results={max_results}"
        response = requests.get(base_url + search_query)
        
        # Parsear XML de respuesta
        root = ET.fromstring(response.content)
        papers = []
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://arxiv.org/schemas/atom}title').text
            summary = entry.find('{http://arxiv.org/schemas/atom}summary').text
            papers.append({'title': title, 'summary': summary})
        
        return papers
    
    def generate_scientific_content(self, query):
        # Obtener papers relevantes
        papers = self.fetch_arxiv_papers()
        
        # Generar embeddings
        query_embedding = self.embedding_model.encode([query])[0]
        paper_embeddings = self.embedding_model.encode([p['summary'] for p in papers])
        
        # Encontrar paper más similar
        similarities = cosine_similarity([query_embedding], paper_embeddings)[0]
        best_paper_idx = similarities.argmax()
        
        # Usar el paper más relevante para generar contenido
        context = papers[best_paper_idx]['summary']
        
        # Llamar al LLM para generar contenido divulgativo
        llm_manager = LLMManager()
        prompt = f"Explica de manera divulgativa el siguiente contexto científico: {context}"
        content = llm_manager.generate_content(prompt, "blog", self.domain, "público general")
        
        return content