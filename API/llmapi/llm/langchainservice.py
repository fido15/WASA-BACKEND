from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class AIHelper:
    def __init__(self,model="llama3.1"):
         self.model = OllamaLLM(model=model)
    
    def helloWorld(self ,question="who are you ?"):
         template = """Question:{question}
         Answer:"""
         prompt = ChatPromptTemplate.from_template(template)
         chain = prompt |self.model
         response = chain.invoke({"question":question})
         return response

    def Country(self,content):
         template="""Content:{content}
         Answer:please tell me in one word  which continent this article refers to."""
         prompt = ChatPromptTemplate.from_template(template)
         chain = prompt |self.model
         response = chain.invoke({"content":content})
         return response
         
    def  Categories(self,content,category):
        template = """Content: {content}
          Categories: {categories}
          Answer: In one word only, specify the category or suggest a new one."""
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt |self.model
        response = chain.invoke({"content":content,"categories":category})
        return response