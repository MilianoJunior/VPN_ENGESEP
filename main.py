'''
Projeto de sistema de conexão entre cubículo-manutenção
'''

'''
Descrição do problema:
    Trabalho em uma empresa que faz a automação de pchs e cghs, e estamos com dificuldades de prestar 
manutenção para o cubículos instalados, por conta da distância entre a empresa e os cubículos.
    A ideia é usar o raspberry como ponte, para acessar os outros dispositivos, e atraves do notebook que está a 100km do
raspberry, se conectar no CLP, ou outros dispositivos da rede e dai, fazer a manutenção de forma remota.
    Existem quatros dispositivos que devem ser controlados remotamente, eles são:
        - relé de proteção, que possui comunicação via modbus TCP/IP;
        - regulador de tensão, que possui comunicação via modbus TCP/IP;
        - CLP, que possui comunicação via modbus TCP/IP;
        - Supervisório, que possui comunicação via modbus TCP/IP;
    O sistema deve ser capaz de se comunicar com os dispositivos, pode me ajudar?


'''

'''
Criando um ambiente de teste para o projeto
    - Dispositivos:
        - 2 CLPs, endereços 192.168.10.2(wago 1) e 192.168.10.3(wago 2) respectivamente;
        - 1 cMT-FHDX-820, endereço 192.168.10.50(cMT);
        - Raspberry Pi 3B+, endereço 192.168.10.60(rasp);
        - Gateway é o roteador TP-LINK modelo EC-220 - G5, endereço 192.168.10.1(rede 2), está conectado a internet com outro
        roteador que está na faixa de IP 192.168.0.1(rede 1);
        
    - Conexões:
        - wago 1, wago 2 e o cMT, estão conectados via cabo, com a rede 2, que disponibiliza acesso ao wifi com o nome de VPN_EngeSEP.
        - rasp está conectado na rede 2 pelo wifi.
        - Meu computador, está conectado pelo wifi da rede 1, chamada engesep, com DHCP automatico, o restante é estatico.
        
    Objetivo é configurar o rasp, com ajuda do python se for necessario, para ficar escutando o servidor da railway, que 
    terá um sistema de autenticação que será programado pelo python, quando o usuário, se autenticar pela railway, receberá acesso
    ao rasp, podendo acessar o wago 1, wago 2 e cMT, com a capacidade aos dispositivos, dai então, atraves de sua máquina, com sofwares 
    instalado na máquina do usuário, como o codesys, carregar e ler os códigos escritos no CLP.
    
    Pode me ajudar a continuar essa solução, configurando o rasp, e criando um programa em python para o rasp e servidor da railway.
        
'''

'''
    - Configuração do rasp:

'''
from multiprocessing import Process
from flask import Flask, request, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash

import os

app = Flask(__name__)

# Em um ambiente real, a senha deve ser armazenada de forma segura (por exemplo, em um banco de dados) e hash.
users = {
    "miliano": generate_password_hash("654123")
}


@app.route('/login', methods=['POST'])
def login():
    print('Login')
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and check_password_hash(users[username], password):
        # Aqui, você pode fornecer credenciais ou tokens para acesso ao Raspberry Pi.
        # proxy() # Redireciona para o Raspberry Pi
        return jsonify({"message": "Logado com sucesso!"}), 200
    return jsonify({"message": "Credenciais Invalidas!"}), 401

RASPBERRY_PI_URL = "http://186.227.147.69"

# @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE']) 51820
def proxy(path):
    ''' Encaminha todas as requisições para o Raspberry Pi '''
    full_url = f"{RASPBERRY_PI_URL}/{path}"
    response = requests.request(request.method, full_url, data=request.data, headers=request.headers)
    return (response.text, response.status_code, response.headers.items())



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# /bin/bash: line 1: hypercorn: command not found