import traceback
from arxiv import Search, SortCriterion
from core.llm_manager import LLMManager

class ScientificAgent:
    ARXIV_CATEGORY_MAP = {
        "física cuántica": ["quant-ph", "physics.quant-ph"],
        "inteligencia artificial": ["cs.AI", "cs.ML"],
        "biomedicina": ["q-bio", "q-bio.BM", "q-bio.CB"],
        "astrofísica": ["astro-ph", "astro-ph.GA", "astro-ph.CO"]
    }
    def __init__(self, task, language="castellano", llm_provider='openai'):
        self.task = task
        self.language = language
        self.provider = llm_provider
    
    def retrieve_papers(self, query, domain=None, *args, **kwargs):
        try:
            print(f"Debug: Retrieving papers - Query: {query}, Domain: {domain}")
            
            # Mapear dominio a categorías de arXiv
            arxiv_categories = self.ARXIV_CATEGORY_MAP.get(domain, [])
            
            # Construir query de búsqueda más robusta
            search_queries = []
            
            # Si hay categorías de arXiv, generar múltiples queries
            if arxiv_categories:
                for category in arxiv_categories:
                    search_query = f"{query} AND cat:{category}"
                    search_queries.append(search_query)
            else:
                # Si no hay mapeo, usar query original
                search_queries.append(query)
            
            papers = []
            for search_query in search_queries:
                print(f"Debug: Trying search query: {search_query}")
                
                search = Search(
                    query=search_query,
                    max_results=5,
                    sort_by=SortCriterion.Relevance
                )
                
                for result in search.results():
                    try:
                        paper_info = {
                            "title": result.title,
                            "summary": result.summary,
                            "categories": result.categories,
                            "url": result.entry_id,
                            "authors": [author.name for author in result.authors]
                        }
                        papers.append(paper_info)
                    except Exception as inner_e:
                        print(f"Error procesando paper individual: {inner_e}")
                
                # Si encontramos papers, salimos del bucle
                if papers:
                    break
            
            print(f"Debug: Papers recuperados: {len(papers)}")
            
            return papers
        
        except Exception as e:
            print(f"Retrieval error: {e}")
            print(traceback.format_exc())
            return []

    def simplify_content(self, content, papers=None):
        """
        Simplifica el contenido científico de manera robusta con referencias a artículos originales.
        
        Args:
            content (str): Contenido científico a simplificar
            papers (list, optional): Lista de papers de arXiv para referencias
        """
        try:
            # Validar contenido
            if not content or len(content.strip()) < 10:
                return "No hay contenido científico suficiente para simplificar."
            
            # Preparar prompt de simplificación adaptado al idioma con referencias
            references_text = ""
            if papers:
                references_text = "\n\nReferencias científicas:\n" + "\n".join([
                    f"- {paper['title']} ({paper['url']})" 
                    for paper in papers[:3]  # Limitar a 3 referencias
                ])
            
            simplification_prompts = {
                "castellano": f"""Simplifica el siguiente texto científico para un público general, 
                usando un lenguaje claro y accesible. Explica los conceptos técnicos de manera sencilla. 
                Mantén un tono divulgativo y académico:

                {content}

                {references_text}
                """,
                "english": f"""Simplify the following scientific text for a general audience, 
                using clear and accessible language. Explain technical concepts in a simple way. 
                Maintain an informative and academic tone:

                {content}

                {references_text}
                """,
                # Puedes añadir más idiomas si lo necesitas
            }
            
            # Usar el prompt correspondiente al idioma
            prompt = simplification_prompts.get(self.language, simplification_prompts["castellano"])
            
            # Generar contenido simplificado usando LLMManager
            llm_manager = LLMManager(provider=self.provider)
            simplified_content = llm_manager.generate_content(
                prompt=prompt,
                platform="scientific_simplification",
                topic="simplificación científica",
                audience="público general",
                language=self.language
            )
            
            return simplified_content.text
        
        except Exception as e:
            print(f"Simplification error: {e}")
            return f"Error en la simplificación: Problema al procesar el contenido científico. Detalles: {str(e)}"

    def handle(self, *args, **kwargs):
        """
        Método handle con más información de depuración
        """
        try:
            query = args[0] if args else kwargs.get('query')
            domain = kwargs.get('domain')
            
            print(f"Debug: Handle method - Task: {self.task}, Query: {query}, Domain: {domain}")
            
            if not query:
                print("Error: No query provided")
                return None
            
            if self.task == "retrieval":
                return self.retrieve_papers(query, domain)
            elif self.task == "simplification":
                # Recuperar papers relacionados primero
                papers = self.retrieve_papers(query, domain)
                
                # Si no hay papers, intentar sin dominio
                if not papers:
                    print("Debug: No papers found with domain, retrying without domain")
                    papers = self.retrieve_papers(query)
                
                # Si aún no hay papers, usar contenido original
                if not papers:
                    return "No se encontraron documentos científicos relevantes."
                
                retrieval_text = " ".join([
                    f"Título: {paper['title']} - Resumen: {paper['summary']}" 
                    for paper in papers
                ])
                
                return self.simplify_content(retrieval_text, papers)
            elif self.task == "graph_enrichment":
                return self.basic_enrichment(query)
        except Exception as e:
            print(f"Error in {self.task} task: {e}")
            print(traceback.format_exc())
            return None

    def basic_enrichment(self, content):
        """
        Método de enriquecimiento básico sin dependencias externas
        """
        if not content or len(content.strip()) < 10:
            return "No hay contenido suficiente para enriquecer."
        
        try:
            # Añadir algunas notas contextuales
            enrichment_notes = {
                "castellano": "\n\nNotas adicionales:\n- Este contenido ha sido procesado y contextualizado para mejorar su comprensión.",
                "english": "\n\nAdditional notes:\n- This content has been processed and contextualized to improve understanding.",
                "français": "\n\nNotes supplémentaires :\n- Ce contenu a été traité et contextualisé pour améliorer la compréhension.",
                "italiano": "\n\nNote aggiuntive:\n- Questo contenuto è stato elaborato e contestualizzato per migliorare la comprensione."
            }
            
            note = enrichment_notes.get(self.language, enrichment_notes["castellano"])
            return content + note
        
        except Exception as e:
            print(f"Enrichment error: {e}")
            return content

class MultiAgentSystem:
    def __init__(self, language="castellano", llm_provider='openai'):
        self.agents = {
            "retrieval": ScientificAgent("retrieval", language, llm_provider),
            "simplification": ScientificAgent("simplification", language, llm_provider),
            "graph_enrichment": ScientificAgent("graph_enrichment", language, llm_provider)
        }
    
    def dispatch(self, task, *args, **kwargs):
        try:
            print(f"Dispatch debug:")
            print(f"Task: {task}")
            print(f"Args: {args}")
            print(f"Kwargs: {kwargs}")

            if task in self.agents:
                # Para graph_enrichment, añadir más flexibilidad en la extracción de contenido
                if task == "graph_enrichment":
                    content = kwargs.get('content')
                    
                    # Si no hay content en kwargs, intentar extraerlo de args
                    if content is None and args:
                        content = args[0]
                    
                    # Si aún no hay contenido, imprimir advertencia
                    if content is None:
                        print("WARNING: No content provided for graph_enrichment")
                        return "No hay contenido para enriquecer"
                    
                    return self.agents[task].handle(content, **kwargs)
                
                return self.agents[task].handle(*args, **kwargs)
            else:
                raise ValueError(f"Tarea desconocida: {task}")
        except Exception as e:
            print(f"Dispatch error: {e}")
            print(traceback.format_exc())
            return None