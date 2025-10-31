# Akciový broker API
Tento projekt demonstruje jednoduché REST API vytvořené pomocí Pythonu a Flasku s integrovanou Swagger dokumentací (OpenAPI).  

---

## Požadavky na software

Pro spuštění aplikace je potřeba mít nainstalováno:

- **Python 3.10+**
- **pip** (správce balíčků pro Python)
- Balíčky:
  - `Flask`
  - `flasgger`
  - `PyYAML`

---

## Jak aplikaci spustit lokálně

1. Naklonujte nebo stáhněte tento repozitář z GitHubu.
2. Otevřete složku projektu v terminálu.
3. Nainstalujte potřebné knihovny:

   ```bash
   pip install flask flasgger pyyaml
4. Spusťte aplikaci:
   ```bash
   python app.py
5. Po spuštění aplikace otevřete webový prohlížeč a přejděte na:
   http://localhost:8080/api


## Autorizace

Některé endpointy vyžadují **Bearer token** pro ověření uživatele.

### Postup:

1. V rozhraní Swaggeru otevřete endpoint:
   - POST /clients

   a odešlete přihlašovací údaje:
   ```json
   {
     "nickname": "test",
     "address": "1234"
   }
2. API odpoví JSON objektem obsahujícím přístupový token, například:
   ```json
   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
   }
3. Tento token si zkopírujte (bez uvozovek) a v pravém horním rohu klikněte na tlačítko Authorize.
4. Do pole vložíte váš token.
5. Kliknete na authorize.
6. Nyní můžete volat všechny chráněné endpointy, které vyžadují ověření uživatele.
