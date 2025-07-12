from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

app = FastAPI()

class Query(BaseModel):
    name: str
    uf: str

async def buscar_advogado(nome: str, uf: str) -> dict:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://cna.oab.org.br/")
            await page.fill("#txtName", nome)
            await page.select_option("#cmbSeccional", uf)
            await page.click("#btnFind")
            try:
                await page.wait_for_selector("table tbody tr td a", timeout=7000)
                await page.click("table tbody tr td a")
            except PlaywrightTimeoutError:
                await browser.close()
                return {"erro": "Nenhum resultado encontrado para os critérios informados."}
            await page.wait_for_timeout(2000)
            try:
                dados = {
                    "oab": await page.locator("#numeroInscricao").inner_text(),
                    "nome": await page.locator("#nomeAdvogado").inner_text(),
                    "uf": await page.locator("#oabUF").inner_text(),
                    "categoria": await page.locator("#categoria").inner_text(),
                    "data_inscricao": await page.locator("#dataInscricao").inner_text(),
                    "situacao": await page.locator("#situacao").inner_text()
                }
            except Exception as e:
                await browser.close()
                return {"erro": f"Erro ao extrair dados do advogado: {str(e)}"}
            await browser.close()
            return dados
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)}"}

@app.post("/fetch_oab")
async def fetch_oab(query: Query):
    if not query.name or not query.uf:
        raise HTTPException(status_code=400, detail="Os campos 'name' e 'uf' são obrigatórios.")
    resultado = await buscar_advogado(query.name, query.uf)
    if "erro" in resultado:
        raise HTTPException(status_code=404, detail=resultado["erro"])
    return resultado