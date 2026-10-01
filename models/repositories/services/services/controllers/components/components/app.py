import streamlit as st
from database.connection import init_db
from controllers.main_controller import MainController
from components.camera import render_camera_component
from components.history import render_history_component
from components.dashboard import render_dashboard_component
from utils.logger import logger

st.set_page_config(
    page_title="Visão Computacional Streamlit",
    page_icon="📷",
    layout="wide"
)

@st.cache_resource
def setup_infrastructure():
    logger.info("Inicializando conexão e tabelas de banco de dados...")
    init_db()

def main():
    setup_infrastructure()
    controller = MainController()

    st.title("Sistema de Visão Computacional")
    st.caption("Captura de câmera em tempo real, métricas de OpenCV e persistência via Neon.tech")

    st.sidebar.title("Navegação")
    menu = st.sidebar.radio(
        "Selecione o Módulo",
        ["Capturar Foto", "Histórico", "Dashboard"]
    )

    st.sidebar.write("---")
    st.sidebar.markdown("**Status da Conexão:** 🟢 Conectado ao Neon.tech")

    if menu == "Capturar Foto":
        render_camera_component(controller)
    elif menu == "Histórico":
        render_history_component(controller)
    elif menu == "Dashboard":
        render_dashboard_component(controller)

if __name__ == "__main__":
    main()