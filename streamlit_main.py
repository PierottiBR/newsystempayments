import streamlit as st
from funciones_ganamos import *


main = st.set_page_config(page_title="test ganamos")

col1, col2 = st.columns(2)
with col1:
    nuevo_usuario = st.text_input("nombre")
    contrasenia_nueva = st.text_input("contraseña")
    ok_button = st.button("crear usuario")
    if ok_button and nuevo_usuario and contrasenia_nueva:
        respuesta,usuarios=nuevo_jugador(nueva_contrasenia=contrasenia_nueva,nuevo_usuario=nuevo_usuario,usuario="adminflamingo", contrasenia="1111aaaa")
        if respuesta == 'Usuario creado':
            st.success(respuesta)
        else:
            st.error(respuesta)

if main == "__main__":
    main()