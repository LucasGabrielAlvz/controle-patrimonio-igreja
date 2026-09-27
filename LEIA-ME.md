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

## Como usar

1. Aba **Departamentos**: cadastre os setores da instituição (já vem com
   alguns exemplos: Louvor, Infantil, Cozinha, Secretaria, Manutenção —
   edite conforme a realidade do local).
2. Aba **Itens**: cadastre cada bem do patrimônio, vinculando a um
   departamento.
3. Aba **Movimentação**: registre quando alguém retira um item para uso, e
   registre a devolução quando o item voltar.
4. Aba **Relatório**: veja quantos itens cada departamento tem e quantos
   estão em uso no momento.

## Para o Trabalho Final

- Use este sistema já com os dados reais da instituição.
- Tire prints de tela mostrando o sistema em uso com o patrimônio real.
- Grave um vídeo curto (até 5 minutos) demonstrando o cadastro e a
  movimentação de um item real.
- Peça uma breve declaração da liderança confirmando que o sistema foi
  aplicado.
