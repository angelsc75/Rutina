from arxiv import Search
from neo4j import GraphDatabase
import os
from typing import List, Dict, Any

class ScientificContentRAG:
    
    def __init__(self, domain, language="castellano"):
        self.domain = domain
        self.language = language
        self.graph_driver = None
    
    def _connect_neo4j(self):
        """Método privado para conectar a Neo4j con manejo de errores"""
        try:
            # Ensure environment variables are set correctly
            neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
            neo4j_password = os.getenv('NEO4J_PASSWORD', 'neo4j')
            
            self.graph_driver = GraphDatabase.driver(
                neo4j_uri, 
                auth=(neo4j_user, neo4j_password)
            )
            return self.graph_driver
        except Exception as e:
            print(f"Neo4j Connection Error: {e}")
            return None
    
    def fetch_arxiv_papers(self, query, max_results=10):
        try:
            search = Search(
                query=f"{self.domain} {query}",
                max_results=max_results
            )
            return [
                {
                    "title": result.title, 
                    "summary": result.summary, 
                    "authors": [str(author.name) for author in result.authors],
                    "url": result.entry_id
                } 
                for result in search.results()
            ]
        except Exception as e:
            print(f"ArXiv Search Error: {e}")
            return []
    
    def extract_keywords(self, content: str) -> List[str]:
        """Método básico de extracción de palabras clave"""
        # Implementación simplificada
        return [word.lower() for word in content.split() if len(word) > 3][:10]
    
    def enrich_with_knowledge_graph(self, content: str) -> List[Dict[str, Any]]:
        """Enriquecer contenido usando grafo de conocimiento"""
        if not self.graph_driver:
            self._connect_neo4j()
        
        try:
            with self.graph_driver.session() as session:
                keywords = self.extract_keywords(content)
                
                # Consulta de grafo más genérica
                query = """
                MATCH (n:Concept)-[r:RELATED_TO]->(m:Concept)
                WHERE any(keyword IN $keywords IN n.keywords)
                RETURN n.name as source_concept, 
                       type(r) as relation, 
                       m.name as target_concept 
                LIMIT 20
                """
                
                results = session.run(query, keywords=keywords)
                
                return [
                    {
                        "source_concept": record["source_concept"],
                        "relation": record["relation"],
                        "target_concept": record["target_concept"]
                    } 
                    for record in results
                ]
        
        except Exception as e:
            print(f"Graph Enrichment Error: {e}")
            return []
    
    def generate_scientific_graph_report(self, query, max_results=10):
        """Método principal para generar informe científico con grafo"""
        # Recuperar papers
        papers = self.fetch_arxiv_papers(query, max_results)
        
        # Combinar resúmenes de papers para enriquecimiento
        content = " ".join([paper['summary'] for paper in papers])
        
        # Enriquecer con grafo de conocimiento
        graph_enrichment = self.enrich_with_knowledge_graph(content)
        
        return {
            "papers": papers,
            "graph_enrichment": graph_enrichment
        }

    def __del__(self):
        """Cerrar la conexión del driver al destruir el objeto"""
        if self.graph_driver:
            self.graph_driver.close()
