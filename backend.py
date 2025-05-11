import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader, CSVLoader

import api_key

os.environ['GROQ_API_Key'] = api_key.api_key
chat = ChatGroq(model='llama3-70b-8192')

base_dir = os.path.dirname(__file__)  # Diretório do script atual
caminho_csv = os.path.join(base_dir, "Docs", "Tabela.csv")

def carregar_dados_csv(caminho=caminho_csv, limite=100):
    if not os.path.exists(caminho):
        print(f"Arquivo {caminho} não encontrado.")
        return ""
    try:
        loader = CSVLoader(
            caminho, encoding="utf-8"
            )
        documentos = loader.load()
        conteudos = [
            doc.page_content.strip()
            for doc in documentos[:limite]
            if doc.page_content.strip() and len(doc.page_content.strip()) > 10
        ]
        return "\n".join(conteudos)
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return ""

def carrega_pdf():
    caminho_pdf = "./Docs/Catalogo-WEGA-Linha-Leve-2023-2024.pdf"
    loader = PyPDFLoader(caminho_pdf)
    lista_documentos = loader.load()
    documento = " "
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def gerar_resposta(mensagem, documento):
    #mensagem_sistema = 'Você é um assistente para oficinas mecânicas apenas para auxílio na identificação de filtros entre outros itens para veículos que responde de forma simples e direta, você responderá os filtros e outros itens de acordo com as seguintes informações {informacao}'
    mensagem_sistema = 'Você é um assistente especializado para oficinas mecânicas. Sua função é ajudar na identificação de filtros e outros componentes automotivos que responde de forma simples e direta. Baseie suas respostas apenas nas informações fornecidas a seguir:  {informacao} Se você não encontrar dados suficientes para identificar corretamente o item solicitado, informe isso ao usuário de forma educada e recomende que ele consulte um profissional qualificado ou fabricante do veiculo.'
    chain = mensagem_sistema | chat
    resposta = chain.invoke({'informacao': documento})
    return resposta.content

mensagens = []

def fazer_pergunta(pergunta):
    
    while True:
        pergunta = input("Usuário: ")
        if pergunta.lower() == "x":
            break
        mensagens.append(("user", pergunta))
        resposta = gerar_resposta(mensagens, carregar_dados_csv())
        mensagens.append(("assistant", resposta))
        print(f"Bot:  {resposta}")
        mensagens.append(("user", pergunta))
        resposta = gerar_resposta(mensagens, carregar_dados_csv)
        mensagens.append(("assistant", resposta))
        return resposta
print("Fim")