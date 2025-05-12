import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader, CSVLoader

import api_key

# Chave da API
os.environ['GROQ_API_Key'] = api_key.api_key
chat = ChatGroq(model='llama3-70b-8192')

# Caminho relativo ao arquivo CSV
base_dir = os.path.dirname(__file__)  # Diretório do script atual
caminho_csv = os.path.join(base_dir, "Docs", "Tabela.csv")

# Função para carregar os dados do CSV
def carregar_dados_csv(caminho=caminho_csv, limite=50):
    if not os.path.exists(caminho):
        print(f"Arquivo {caminho} não encontrado.")
        return ""
    try:
        caminho_csv = "Docs\Tabela.csv"
        loader = CSVLoader(caminho_csv, encoding="utf-8")
        lista_documentos = loader.load()
        documento = " "
        for doc in lista_documentos[0:limite]:
            documento += doc.page_content
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return ""
    return documento
    

def carrega_pdf():
    caminho_pdf = "./Docs/Catalogo-WEGA-Linha-Leve-2023-2024.pdf"
    loader = PyPDFLoader(caminho_pdf)
    lista_documentos = loader.load()
    documento = " "
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def gerar_resposta(mensagens, documento):
    #mensagem_sistema = 'Você é um assistente para oficinas mecânicas apenas para auxílio na identificação de filtros entre outros itens para veículos que responde de forma simples e direta, você responderá os filtros e outros itens de acordo com as seguintes informações {informacao}'
    mensagem_sistema = 'Você é um assistente especializado para oficinas mecânicas. Sua função é ajudar na identificação de filtros e outros componentes automotivos que responde de forma simples e direta. Baseie suas respostas apenas nas informações fornecidas a seguir: {informacao} Se você não encontrar dados suficientes para identificar corretamente o item solicitado, informe isso ao usuário de forma educada e recomende que ele consulte um profissional qualificado ou fabricante do veiculo.'
    #mensagem_sistema = "Você é um assistente especializado para oficinas mecânicas que responde diretamente com base nas seguintes informações: {informacao}."
    
    mensagens_modelo = [('system', mensagem_sistema)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    
    chain = template | chat
    resposta = chain.invoke({'informacao': documento})
    return resposta.content

mensagens = []

def teste_bot():
    while True:
        pergunta = input("Usuário: ")
        if pergunta.lower() == "x":
            break
        mensagens.append(("user", pergunta))
        resposta = gerar_resposta(mensagens, carregar_dados_csv())
        mensagens.append(("assistant", resposta))
        