from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import base64

app = Flask(__name__)

def get_instituicao_enderecos(codigo_instituicao):
    # URL para obter os endereços da instituição
    url = f'http://emec.mec.gov.br/emec/consulta-ies/listar-endereco/d96957f455f6405d14c6542552b0f6eb/{base64.b64encode(codigo_instituicao.encode()).decode()}/list/1000'
    html = requests.get(url).text
    
    # Usando BeautifulSoup para processar o HTML
    soup = BeautifulSoup(html, 'html.parser')
    enderecos = {}
    
    tbody = soup.find_all('tbody')
    for row in tbody:
        cols = row.find_all('td')
        if len(cols) > 0:
            enderecos[cols[0].get_text(strip=True)] = {
                'denominacao': cols[1].get_text(strip=True),
                'endereco': cols[2].get_text(strip=True),
                'polo': cols[3].get_text(strip=True),
                'municipio': cols[4].get_text(strip=True),
                'UF': ''.join(filter(str.isalpha, cols[5].get_text(strip=True)))
            }
    
    return enderecos

@app.route('/enderecos/<int:codigo_instituicao>', methods=['GET'])
def get_enderecos(codigo_instituicao):
    enderecos = get_instituicao_enderecos(str(codigo_instituicao))
    return jsonify(enderecos)

if __name__ == '__main__':
    app.run(debug=True)
