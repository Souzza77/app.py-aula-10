# Sistema de Visão Computacional em Streamlit

Aplicação pronta para produção desenvolvida em Python, com captura de câmera, análise de imagem com OpenCV, persistência de dados no banco relacional Serverless Neon.tech e pronta para deploy no Render.

## Arquitetura do Sistema

O projeto segue Arquitetura Limpa e os princípios SOLID:
- **`components/`**: Interface de Usuário desenvolvida em Streamlit.
- **`controllers/`**: Orquestração entre a interface e os serviços de negócio.
- **`services/`**: Implementação das pipelines de Visão Computacional (`VisionService`) e salvamento em disco (`StorageService`).
- **`repositories/`**: Abstração de acesso ao banco de dados com SQLAlchemy.
- **`models/`**: Mapeamento Objeto-Relacional (ORM).
- **`database/`**: Gerenciamento do pool de conexões PostgreSQL.

---

## Instalação e Execução Local

Não utilize ambientes virtuais (`venv`). Instale os pacotes diretamente no seu interpretador global Python 3.12+.

### 1. Instalar Dependências
```bash
pip install -r requirements.txt