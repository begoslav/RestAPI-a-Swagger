# REST API – Swagger dokumentace

Tento projekt obsahuje dokumentaci REST API vytvořenou pomocí nástroje Swagger (OpenAPI 3.0).  
Dokumentace je definována v souboru `swagger.yaml` a zobrazena pomocí Swagger UI v souboru `index.html`.

## Požadavky

Pro lokální spuštění dokumentace je potřeba:

- libovolný webový prohlížeč (např. Chrome, Firefox, Edge)
- volitelně: Python nebo jiný jednoduchý lokální server

---

## Spuštění projektu

### Možnost 1 – Otevření přímo z disku
1. Naklonujte nebo stáhněte repozitář:
   ```bash
   git clone https://github.com/begoslav/RestAPI-a-Swagger.git

2. Otevřete soubor index.html v prohlížeči.
    Swagger UI načte soubor swagger.yaml a zobrazí API dokumentaci.


### Možnost 2 – Otevření přímo z disku
1. Spusťte následující příkaz v kořenovém adresáři projektu:
    python -m http.server 8080

2. Poté otevřete v prohlížeči adresu:
    http://localhost:8080  
