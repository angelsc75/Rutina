import traceback
from arxiv import Search, SortCriterion
from core.llm_manager import LLMManager

class ScientificAgent:
    def __init__(self, task, language="castellano", llm_provider='openai'):
        self.task = task
        self.language = language
        self.provider = llm_provider
    
    def handle(self, query, *args):
        try:
            if self.task == "retrieval":
                return self.retrieve_papers(query)
            elif self.task == "simplification":
                return self.simplify_content(query)
            elif self.task == "graph_enrichment":
                return self.basic_enrichment(query)
        except Exception as e:
            print(f"Error in {self.task} task: {e}")
            print(traceback.format_exc())
            return None
    
    def retrieve_papers(self, query, *args, **kwargs):
        try:
            search = Search(
                query=query or "scientific research",
                max_results=5,
                sort_by=SortCriterion.Relevance
            )
            
            papers = []
            for result in search.results():
                papers.append({
                    "title": result.title,
                    "summary": result.summary,
                    "url": result.entry_id
                })
            
            if not papers:
                return "No se encontraron documentos científicos relacionados."
            
            # Combinar títulos y resúmenes
            return " ".join([f"Título: {paper['title']} - Resumen: {paper['summary']}" for paper in papers])
        
        except Exception as e:
            print(f"Retrieval error: {e}")
            return f"Error en la recuperación: {e}"

    def simplify_content(self, content):
        """
        Simplifica el contenido científico de manera más robusta.
        """
        try:
            # Validar contenido
            if not content or len(content.strip()) < 10:
                return "No hay contenido científico suficiente para simplificar."
            
            # Preparar prompt de simplificación adaptado al idioma
            simplification_prompts = {
                "castellano": f"""Simplifica el siguiente texto científico para un público general, 
                usando un lenguaje claro y accesible. Explica los conceptos técnicos de manera sencilla:

                {content}""",
                "english": f"""Simplify the following scientific text for a general audience, 
                using clear and accessible language. Explain technical concepts in a simple way:

                {content}""",
                "français": f"""Simplifiez ce texte scientifique pour un public général, 
                en utilisant un langage clair et accessible. Expliquez les concepts techniques de manière simple :

                {content}""",
                "italiano": f"""Semplifica questo testo scientifico per un pubblico generico, 
                usando un linguaggio chiaro e accessibile. Spiega i concetti tecnici in modo semplice:

                {content}"""
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

    def basic_enrichment(self, content):
        """
        Método de enriquecimiento básico sin dependencias externas
        """
        if not content:
            return content
        
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
            if task in self.agents:
                return self.agents[task].handle(*args, **kwargs)
            else:
                raise ValueError(f"Tarea desconocida: {task}")
        except Exception as e:
            print(f"Dispatch error: {e}")
            return None