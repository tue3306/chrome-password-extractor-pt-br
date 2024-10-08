# **Chrome Passwords Extractor**

Este script Python foi criado para extrair senhas salvas dos perfis do Google Chrome no Windows e salvar essas informações em um arquivo de texto na área de trabalho do usuário.

**Nota Importante:** Este script está em fase de desenvolvimento e pode não funcionar perfeitamente em todos os cenários. A funcionalidade do código pode variar dependendo da versão do navegador e do sistema operacional. O código pode conter erros e não deve ser considerado uma solução final.

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

## **Arquivos Disponíveis**

- **`malware.py`**:
  - Este é o script Python fonte. Ele contém o código que realiza a extração das senhas do Chrome. Este arquivo é útil para visualização e compreensão do código.

- **`malware.exe`**:
  - Este é o executável gerado a partir do script Python. Ele pode ser executado diretamente no Windows para realizar a extração das senhas sem a necessidade de executar o script Python manualmente. O `malware.exe` é o arquivo que você deve usar para rodar a aplicação finalizada.

## **Observações**

- **Uso Ético e Legal**:
  - Este script deve ser utilizado apenas em computadores e perfis para os quais você tenha autorização. Utilizar este script sem permissão é ilegal e antiético.

- **Requisitos**:
  - Certifique-se de que o Google Chrome esteja fechado antes de executar o script para evitar problemas com arquivos bloqueados.

- **Problemas Potenciais**:
  - O script pode não funcionar corretamente se o Chrome estiver aberto ou se houver problemas de permissão com os arquivos. Verifique essas condições antes de rodar o script.
