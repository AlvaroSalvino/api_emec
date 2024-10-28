from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import base64

app = Flask(__name__)

def get_instituicao_enderecos(codigo_instituicao):
    url = f'http://emec.mec.gov.br/emec/consulta-ies/listar-endereco/d96957f455f6405d14c6542552b0f6eb/{base64.b64encode(codigo_instituicao.encode()).decode()}/list/1000'
    html = requests.get(url).text
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

def get_instituicao_cursos(cod_endereco, cod_instituicao):
    url = f'http://emec.mec.gov.br/emec/consulta-ies/listar-curso-endereco/d96957f455f6405d14c6542552b0f6eb/{base64.b64encode(cod_instituicao.encode()).decode()}/aa547dc9e0377b562e2354d29f06085f/{base64.b64encode(cod_endereco.encode()).decode()}/list/1000'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    cursos = []

    tbody = soup.find_all('tbody')
    for row in tbody:
        cols = row.find_all('td')
        if len(cols) > 0:
            curso = cols[0].get_text(strip=True)
            cursos.append(curso)

    return cursos

@app.route('/enderecos/<int:codigo_instituicao>', methods=['GET'])
def get_enderecos(codigo_instituicao):
    enderecos = get_instituicao_enderecos(str(codigo_instituicao))
    return jsonify(enderecos)

@app.route('/cursos/<int:cod_endereco>/<int:cod_instituicao>', methods=['GET'])
def get_cursos(cod_endereco, cod_instituicao):
    cursos = get_instituicao_cursos(str(cod_endereco), str(cod_instituicao))
    return jsonify(cursos)

if __name__ == '__main__':
    app.run(debug=True)
