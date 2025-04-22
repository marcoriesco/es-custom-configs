import os
import xml.etree.ElementTree as ET
import re

def extract_systems(input_file):
    """
    Extrai cada sistema do arquivo es_systems.cfg que tenha valor no path
    e cria arquivos individuais
    """
    # Lê o conteúdo do arquivo
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adiciona namespace temporário para facilitar o parsing
    content_with_ns = content.replace('<systemList>', '<systemList xmlns:es="http://dummy.namespace">')
    
    # Parse o XML
    root = ET.fromstring(content_with_ns)
    
    # Para cada sistema
    for system in root.findall('./system'):
        # Verifica se tem path e se o path não está vazio
        path_element = system.find('path')
        if path_element is None or not path_element.text or path_element.text.strip() == '':
            print(f"Pulando sistema sem path: {system.find('name').text}")
            continue
        
        # Pega o nome do sistema
        name = system.find('name').text
        
        # Cria um novo XML para este sistema
        new_root = ET.Element('systemList')
        new_root.append(system)
        
        # Converte para string
        system_xml = ET.tostring(new_root, encoding='utf-8', xml_declaration=True).decode('utf-8')
        
        # Restaura o formato original (remove o namespace temporário)
        system_xml = system_xml.replace(' xmlns:es="http://dummy.namespace"', '')
        
        # Adiciona o comentário original se estiver no arquivo original
        if '<!-- *** es_systems.cfg edited for RetroBat ***-->' in content:
            system_xml = system_xml.replace('<?xml version="1.0" encoding="utf-8"?>', 
                                           '<?xml version="1.0" encoding="UTF-8"?>\n<!-- *** es_systems.cfg edited for RetroBat ***-->')
        
        # Salva o arquivo
        output_file = f'es_systems_{name}.cfg'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(system_xml)
        
        print(f"Arquivo criado: {output_file}")

def main():
    input_file = "es_systems.cfg"  # Arquivo original
    
    # Verifica se o arquivo existe
    if not os.path.exists(input_file):
        print(f"Erro: O arquivo {input_file} não foi encontrado.")
        input_file = input("Por favor, digite o caminho completo para o arquivo es_systems.cfg: ")
        if not os.path.exists(input_file):
            print("Arquivo não encontrado. Encerrando.")
            return
    
    extract_systems(input_file)
    print("Processamento concluído!")

if __name__ == "__main__":
    main()