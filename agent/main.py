import requests
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate

def fetch_oab(name, uf):
    url = "http://127.0.0.1:8000/fetch_oab"
    payload = {"name": name, "uf": uf}
    response = requests.post(url, json=payload)
    return response.json()

def main():
    print("Pergunte sobre um advogado (ex: Qual a situação de FULANO DE TAL em SP?)")
    pergunta = input("Pergunta: ")
    nome = input("Nome do advogado: ")
    uf = input("UF: ")
    dados = fetch_oab(nome, uf)

    if "detail" in dados:
        print(f"Resposta do agente LLM: {dados['detail']}")
        return

    # Monta um prompt para o LLM gerar uma resposta em português
    prompt = PromptTemplate(
        input_variables=["pergunta", "dados"],
        template=(
            "Pergunta: {pergunta}\n"
            "Dados do advogado extraídos do site da OAB:\n"
            "{dados}\n"
            "Responda de forma clara e objetiva em português, usando apenas as informações fornecidas."
        )
    )

    llm = OpenAI(temperature=0, model="gpt-3.5-turbo")  # Configure sua chave OpenAI na variável de ambiente OPENAI_API_KEY
    resposta = llm(prompt.format(pergunta=pergunta, dados=dados))
    print("Resposta do agente LLM:")
    print(resposta)

if __name__ == "__main__":
    main()