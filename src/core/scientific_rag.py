from arxiv import Search
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
# from langchain_community import FAISS
from neo4j import GraphDatabase

class ScientificContentRAG:
    def __init__(self, domain, language="castellano"):
        self.domain = domain
        self.language = language
        self.graph_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("user", "password"))
    
    def fetch_arxiv_papers(self, query):
        search = Search(
            query=query,
            max_results=10,
            sort_by="relevance",
        )
        return [result for result in search.results()]
    
    def enrich_with_knowledge_graph(self, content):
        # Enriquecer contenido utilizando un grafo de conocimiento
        with self.graph_driver.session() as session:
            query = """
            MATCH (n)-[r]->(m)
            WHERE n.name CONTAINS $term
            RETURN n, r, m LIMIT 10
            """
            results = session.run(query, term=content)
            enriched_data = [{"node": record["n"], "relation": record["r"]} for record in results]
        return enriched_data
    
    def generate_scientific_content(self, query):
        papers = self.fetch_arxiv_papers(query)
        content = " ".join([paper.summary for paper in papers])
        enriched_content = self.enrich_with_knowledge_graph(content)
        return enriched_content
