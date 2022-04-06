 # Controle Irrigação
 
Endpoints de automação sistema de irrigação automatico:
 - CRUD: 
   - Plantas: nome, descrição, categoria, vaso e irrigador(id);
   - Irrigador: nome, descrição;
   - Configuração: data de início, horário de irrigação, minuto da irrigação, ativo, fluxo da água, pressão, tempo abertura;


Para ambiente linux.

Para clonar o projeto -> `git clone https://github.com/jackteruya/controle-hidro.git`

Com do docker instaldo, caso não tenha -> https://docs.docker.com/engine/install/ e https://docs.docker.com/compose/install/

Caso queira utilizar o Banco de dados postgres crie um banco ou se preferir tem um arquivo docker-compose.yml para subir um container, mas recomendo que faça isso em um diretório separa do projeto atual.
- `$ docker-compose up database` ou `$ docker-compose up database -d` caso queira fechar o terminal ;
- No diretório do projeto exporte a url do banco `export DATABASE_URL=postgresql://postgres:postgres@localhost:5778/postgres`, caso contrario sera usado o SQLite;

Instalando os requirements:
- `$ pip install -r requirements.txt`;

Com o banco de dados rodando, inicie as migrations:
- `$ alembic updrade head`

Roando o projeto:
- `$ uvicorn main:app --reload`;
- Caso a porta padrão 8000 estiver em uso `$ uvicorn main:app --reload --port 8001` ou altere a porta conforme desejar;


Obs.: Foi incluido um arquivo json do Insomnia com os endpoints
