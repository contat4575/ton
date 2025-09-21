from typing import Dict, Any, Optional
import aiohttp
import trafilatura
from bs4 import BeautifulSoup

async def extract_content_robust(url: str) -> Optional[Dict[str, Any]]:
    """
    Extrai conteúdo de uma URL usando trafilatura com fallback para BeautifulSoup.
    """
    print(f"[ExtractionTool] Extraindo de: {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20, ssl=False) as response:
                if response.status != 200:
                    print(f"[ExtractionTool] Erro HTTP {response.status} para {url}")
                    return None
                html = await response.text()

        # Método Principal: Trafilatura
        extracted_text = trafilatura.extract(html, include_comments=False, include_tables=False)

        if extracted_text and len(extracted_text) > 200:
            print(f"[ExtractionTool] Sucesso com Trafilatura: {len(extracted_text)} caracteres.")
            return {"url": url, "content": extracted_text, "method": "trafilatura"}

        # Fallback: BeautifulSoup
        print(f"[ExtractionTool] Trafilatura falhou, usando fallback BeautifulSoup para {url}")
        soup = BeautifulSoup(html, 'html.parser')
        # Remove tags de script e style
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        fallback_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        if fallback_text and len(fallback_text) > 100:
            print(f"[ExtractionTool] Sucesso com BeautifulSoup: {len(fallback_text)} caracteres.")
            return {"url": url, "content": fallback_text, "method": "beautifulsoup"}

        return None

    except Exception as e:
        print(f"[ExtractionTool] Erro crítico ao extrair de {url}: {e}")
        return None