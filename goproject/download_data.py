'''
generar clave en node.js y descargarla
instalar node: sudo npm install -g node-firestore-import-export
firestore-export --accountCredentials path_del_json.json --backupFile path_del_backup.json
'''
import os

def download(account_file, output_file):
    os.system(f"firestore-export -a {account_file} -b {output_file} -p")
