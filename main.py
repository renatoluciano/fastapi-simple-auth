from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Banco de dados temporário na memória do computador
db_usuarios = {}

# --- ROTAS DE INTERFACE (HTML) ---

@app.get("/")
def raiz(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})

@app.get("/cadastro")
def pagina_cadastro(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro.html", context={})

@app.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})

# Rota da página do Dashboard (Área Logada)
@app.get("/dashboard")
def pagina_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html", context={})

# --- ROTAS DE LÓGICA (PROCESSAMENTO) ---

# Recebe os dados do Cadastro
@app.post("/auth/cadastro")
def processar_cadastro(request: Request, email: str = Form(...), senha: str = Form(...)):
    if email in db_usuarios:
        return templates.TemplateResponse(
            request=request, 
            name="cadastro.html", 
            context={"erro": "Este e-mail já está cadastrado."}
        )
    
    db_usuarios[email] = {
        "email": email,
        "senha": senha
    }
    return RedirectResponse(url="/login", status_code=303)

# Recebe os dados do Login e valida as credenciais
@app.post("/auth/login")
def processar_login(request: Request, email: str = Form(...), senha: str = Form(...)):
    # 1. Busca o usuário no nosso dicionário
    usuario = db_usuarios.get(email)
    
    # 2. Se o usuário não existir ou a senha estiver errada, devolve um erro na tela
    if not usuario or usuario["senha"] != senha:
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"erro": "E-mail ou senha incorretos."}
        )
    
    # 3. Se tudo estiver certo, redireciona para a página de sucesso (Dashboard)
    return RedirectResponse(url="/dashboard", status_code=303)

# Rota que processa o encerramento da sessão
@app.get("/auth/logout")
def processar_logout():
    # Como não estamos usando cookies ainda, apenas redirecionamos para o login
    return RedirectResponse(url="/login", status_code=303)