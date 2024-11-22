from langchain.llms import OpenAI
from langchain.chains import SimpleSequentialChain

# Crear un modelo LLM
llm = OpenAI(temperature=0.7)

# Cadena simple de pasos
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Escribe un ensayo breve sobre {topic}",
)

# Crear un pipeline sencillo
chain = SimpleSequentialChain(chains=[llm])
output = chain.run("inteligencia artificial")

print(output)
