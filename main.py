import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader, CSVLoader

import api_key

os.environ['GROQ_API_Key'] = api_key.api_key
chat = ChatGroq(model='llama3-70b-8192')

def carrega_csv():
    caminho_csv = "Docs\Tabela.csv"
    loader = CSVLoader(caminho_csv, encoding="utf-8")
    lista_documentos = loader.load()
    documento = " "
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def carrega_pdf():
    caminho_pdf = "./Docs/Catalogo-WEGA-Linha-Leve-2023-2024.pdf"
    loader = PyPDFLoader(caminho_pdf)
    lista_documentos = loader.load()
    documento = " "
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def resposta_bot(mensagem, documento):
    #mensagem_sistema = 'Você é um assistente para oficinas mecânicas apenas para auxílio na identificação de filtros entre outros itens para veículos que responde de forma simples e direta, você responderá os filtros e outros itens de acordo com as seguintes informações {informacao}'
    mensagem_sistema = 'Você é um assistente especializado para oficinas mecânicas. Sua função é ajudar na identificação de filtros e outros componentes automotivos que responde de forma simples e direta. Baseie suas respostas apenas nas informações fornecidas a seguir:  {informacao} Se você não encontrar dados suficientes para identificar corretamente o item solicitado, informe isso ao usuário de forma educada e recomende que ele consulte um profissional qualificado ou fabricante do veiculo.'
    mensagens_modelo = [('system', mensagem_sistema)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacao': documento}).content

mensagens = []

while True:
    pergunta = input("Usuário: ")
    if pergunta.lower() == "x":
        break
    mensagens.append(("user", pergunta))
    resposta = resposta_bot(mensagens, carrega_csv())
    mensagens.append(("assistant", resposta))
    print(f"Bot:  {resposta}")
print("Fim")