# Sistema de Controle de Patrimônio Institucional

Sistema desktop (Python + Tkinter) com banco de dados MySQL para cadastrar
o patrimônio da instituição, vincular itens a departamentos e registrar
quem está usando cada item.

## Passo a passo para rodar

1. **Instale o MySQL** (se ainda não tiver): https://dev.mysql.com/downloads/installer/
   Durante a instalação, defina uma senha para o usuário `root` e anote-a.

2. **Crie o banco de dados**, abrindo um terminal na pasta do projeto e rodando:
   ```
   mysql -u root -p < schema.sql
   ```
   (vai pedir a senha que você definiu na instalação)

3. **Instale as dependências do Python:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure a senha do banco** no arquivo `db.py`, na variável `DB_CONFIG`,
   trocando `SUA_SENHA_AQUI` pela senha do seu MySQL.

5. **Rode o sistema:**
   ```
   python app.py
   ```
