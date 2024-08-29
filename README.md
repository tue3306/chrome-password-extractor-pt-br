# **Chrome Passwords Extractor**

Este script Python foi criado para extrair senhas salvas dos perfis do Google Chrome no Windows e salvar essas informações em um arquivo de texto na área de trabalho do usuário.

## **Descrição do Código**

1. **Obtenção da Chave de Criptografia**:
   - O script lê a chave de criptografia do arquivo `Local State` do Chrome para descriptografar as senhas salvas.

2. **Armazenamento Temporário de Dados**:
   - Usa um arquivo de texto na área de trabalho para armazenar temporariamente as senhas extraídas.

3. **Descriptografia das Senhas**:
   - Descriptografa as senhas salvas usando a chave obtida. Se necessário, tenta um método alternativo de descriptografia.

4. **Fechamento do Chrome**:
   - Encerra todos os processos do Chrome para garantir que o banco de dados possa ser acessado sem problemas.

5. **Remoção do Arquivo Temporário**:
   - Remove o arquivo temporário usado para armazenar o banco de dados do Chrome após a extração das credenciais.

6. **Extração de Credenciais**:
   - Copia o banco de dados de logins de cada perfil do Chrome, lê as credenciais e salva as informações descriptografadas em um arquivo de texto.

7. **Processamento dos Perfis do Chrome**:
   - Localiza e processa todos os perfis do Chrome encontrados na pasta de dados do usuário para extrair e salvar as credenciais.

## **Observações**

- **Uso Ético e Legal**:
  - Este script deve ser utilizado apenas em computadores e perfis para os quais você tenha autorização. Utilizar este script sem permissão é ilegal e antiético.

- **Requisitos**:
  - Certifique-se de que o Google Chrome esteja fechado antes de executar o script para evitar problemas com arquivos bloqueados.

- **Problemas Potenciais**:
  - O script pode não funcionar corretamente se o Chrome estiver aberto ou se houver problemas de permissão com os arquivos. Verifique essas condições antes de rodar o script.

