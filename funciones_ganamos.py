import requests
import os
import pandas as pd
import streamlit as st
from funciones_ganamos import *



csv_file = 'data.csv'


def login_ganamos(usuario, contrasenia):
    import requests

    url = 'https://agents.ganamos.bet/api/user/login'

    data = {
        "password": contrasenia,
        "username": usuario    
    }

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://agents.ganamos.bet",
        "Referer": "https://agents.ganamos.bet/",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return {}, None

        try:
            response_json = response.json()
        except Exception as e:
            print("⚠️ Error al parsear JSON del login:", e)
            print("Respuesta cruda:", response.text)
            return {}, None

        # Extraer la cookie de sesión
        session_id = response.cookies.get("session")
        if not session_id:
            print("⚠️ Login exitoso pero no se recibió la cookie de sesión")
            return {}, None

        header_check = {
            "Accept": "application/json",
            "Referer": "https://agents.ganamos.bet/",
            "User-Agent": "Mozilla/5.0",
            "cookie": f'session={session_id}'
        }

        url_check = "https://agents.ganamos.bet/api/user/check"
        response_check = requests.get(url_check, headers=header_check)

        if response_check.status_code != 200:
            print("❌ Falló /user/check:", response_check.text)
            return {}, None

        try:
            parent_id = response_check.json()['result']['id']
        except Exception as e:
            print("⚠️ Error al parsear JSON de /user/check:", e)
            print("Respuesta:", response_check.text)
            return {}, None

        url_users = 'https://agents.ganamos.bet/api/agent_admin/user/'
        params_users = {
            'count': '10',
            'page': '0',
            'user_id': parent_id,
            'is_banned': 'false',
            'is_direct_structure': 'false'
        }

        response_users = requests.get(url_users, params=params_users, headers=header_check)

        if response_users.status_code != 200:
            print("❌ Falló /agent_admin/user:", response_users.text)
            return {}, None

        try:
            lista_usuarios = {
                x['username']: x['id'] for x in response_users.json()["result"]["users"]
            }
        except Exception as e:
            print("⚠️ Error al parsear JSON de /agent_admin/user:", e)
            print("Respuesta:", response_users.text)
            return {}, None

        return lista_usuarios, session_id

    except Exception as e:
        print("🔥 Excepción general en login_ganamos:", str(e))
        return {}, None

def carga_ganamos(alias, monto, usuario, contrasenia):
    usuarios, session_id= login_ganamos(usuario,contrasenia)
    
    id_usuario = usuarios[alias]
    url_carga_ganamos = f'https://agents.ganamos.bet/api/agent_admin/user/{id_usuario}/payment/'

    payload_carga = {"operation":0,
                    "amount":monto}


    header_carga = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }

    response_carga_ganamos = requests.post(url_carga_ganamos,json=payload_carga,headers=header_carga, cookies={'session':session_id})
    
    url_balance = 'https://agents.ganamos.bet/api/user/balance'
    header_check= {"accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }
    response_balance = requests.get(url_balance, headers=header_check)
    balance_ganamos = response_balance.json()['result']['balance']
    if response_carga_ganamos.json()['error_message'] is None:
        return True, balance_ganamos
    else:
         return False , balance_ganamos
    
    
def retirar_ganamos(alias, monto, usuario, contrasenia):
    lista_usuarios, session_id= login_ganamos(usuario,contrasenia)
    id_usuario = lista_usuarios[alias]
    url_carga_ganamos = f'https://agents.ganamos.bet/api/agent_admin/user/{id_usuario}/payment/'

    payload_carga = {"operation":1,
                    "amount":monto}


    header_retiro = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }
    response_carga_ganamos = requests.post(url_carga_ganamos,json=payload_carga,headers=header_retiro, cookies={'session':session_id})

    url_balance = 'https://agents.ganamos.bet/api/user/balance'
    header_check= {"accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }
    response_balance = requests.get(url_balance, headers=header_check)
    balance_ganamos = response_balance.json()['result']['balance']
    if response_carga_ganamos.json()['error_message'] is None:
        return True, balance_ganamos
    else:
         return False, balance_ganamos
    

def nuevo_jugador(nueva_contrasenia, nuevo_usuario, usuario, contrasenia ):
    lista_usuarios, session_id= login_ganamos(usuario,contrasenia)
    print(session_id)

    url_nuevo_usuario = 'https://agents.ganamos.bet/api/agent_admin/user/'

    data = {
        "email": "a",
        "first_name": "a",
        "last_name": "a",
        "password": f"{nueva_contrasenia}",
        "role": 0,
        "username": f"{nuevo_usuario}"
    }

    header_check = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
        "priority": "u=1, i",
        "referer": "https://agents.ganamos.bet/",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        'cookie': f'session={session_id}'
        }

    response = requests.post(url_nuevo_usuario, json=data, headers=header_check)
    if response.json()['status'] == 0:
        return 'Usuario creado',lista_usuarios    
    if 'already exist' in response.json()['error_message']:
        return 'El usuario ya existe, Prueba con otro usuario',lista_usuarios
    

csv_file = 'data.csv'

def guardar_usuario(usuario, contraseña):
    if not usuario or not contraseña:
        st.warning('Debe ingresar un usuario y una contraseña.')
        return False  # Devuelve False si faltan datos

    resultado, lista_usuarios = nuevo_jugador(
        nuevo_usuario=usuario,
        nueva_contrasenia=contraseña,
        usuario='adminflamingo',
        contrasenia='1111aaaa'
    )

    if 'Usuario creado' in resultado:
        nuevo_dato = pd.DataFrame({'user': [usuario], 'password': [contraseña]})
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, nuevo_dato], ignore_index=True)
        else:
            df = nuevo_dato

        df.to_csv(csv_file, index=False)
        st.success('Usuario creado!!!')
        return True  # Devuelve True si fue exitoso

    else:
        st.warning(resultado)
        return False  # Devuelve False si no fue exitoso


