
  # Frontend Design for Hansu

  This is a code bundle for Frontend Design for Hansu. The original project is available at https://www.figma.com/design/vhR26v14yHp6JzUIw5979O/Frontend-Design-for-Hansu.

  ## Running the code

  Run `npm i` to install the dependencies.

  Run `npm run dev` to start the development server.

## Integração com backend (Hub_Painel)

- O frontend agora consome os endpoints HTTP em `VITE_API_BASE_URL` (padrão: `http://localhost:8000/api`).
- Para subir a API do backend: 
  1. `cd Hub_Painel/HUB`
  2. `pip install -r requirements.txt`
  3. `uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000`
- Para subir o frontend com o endpoint customizado:
  - `VITE_API_BASE_URL=http://localhost:8000/api npm run dev`

