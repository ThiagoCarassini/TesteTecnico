from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

app = FastAPI()

class Query(BaseModel):
    name: str
    uf: str

def buscar_advogado(nome: str, uf: str) -> dict:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://cna.oab.org.br/")

        time.sleep(2)

        campo_nome = driver.find_element(By.ID, "nome")
        campo_nome.send_keys(nome)

        campo_uf = driver.find_element(By.ID, "uf")
        campo_uf.send_keys(uf)

        campo_uf.send_keys(Keys.ENTER)

        time.sleep(3)

        try:
            primeiro_resultado = driver.find_element(By.CSS_SELECTOR, "table tbody tr td a")
            primeiro_resultado.click()
        except NoSuchElementException:
            return {"erro": "Nenhum resultado encontrado."}

        time.sleep(2)

        dados = {
            "oab": driver.find_element(By.ID, "numeroInscricao").text,
            "nome": driver.find_element(By.ID, "nome").text,
            "uf": driver.find_element(By.ID, "uf").text,
            "categoria": driver.find_element(By.ID, "categoria").text,
            "data_inscricao": driver.find_element(By.ID, "dataInscricao").text,
            "situacao": driver.find_element(By.ID, "situacao").text
        }

        return dados

    finally:
        driver.quit()

@app.post("/fetch_oab")
async def fetch_oab(query: Query):
    if not query.name or not query.uf:
        raise HTTPException(status_code=400, detail="Name and UF must be provided")

    resultado = buscar_advogado(query.name, query.uf)

    if "erro" in resultado:
        raise HTTPException(status_code=404, detail=resultado["erro"])

    return resultado
