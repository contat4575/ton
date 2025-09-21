import os
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import asyncio

# A lógica robusta do seu viral_integration_service.py seria refatorada aqui.

async def capture_screenshot(url: str, session_id: str) -> Dict[str, Any]:
    """
    Captura um screenshot de uma URL usando Selenium.
    """
    print(f"[ScreenshotTool] Capturando: {url}")
    
    # Cria o diretório se não existir
    session_dir = f"sessions/{session_id}/screenshots"
    os.makedirs(session_dir, exist_ok=True)
    
    filename = f"{url.replace('https://', '').replace('http://', '').replace('/', '_')[:50]}.png"
    filepath = os.path.join(session_dir, filename)

    # Configuração do Selenium Headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        # Aguarda um pouco para a página renderizar
        await asyncio.sleep(5)
        driver.save_screenshot(filepath)
        driver.quit()
        
        print(f"[ScreenshotTool] Screenshot salvo em: {filepath}")
        return {"success": True, "url": url, "filepath": filepath}

    except Exception as e:
        print(f"[ScreenshotTool] Erro ao capturar {url}: {e}")
        return {"success": False, "url": url, "error": str(e)}