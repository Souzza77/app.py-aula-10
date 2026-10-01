import streamlit as st
from PIL import Image
from controllers.main_controller import MainController

def render_camera_component(controller: MainController):
    st.subheader("Captura via Webcam")
    img_file_buffer = st.camera_input("Acesse a câmera do seu dispositivo")

    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption="Fotografia Capturada", use_column_width=True)

        if st.button("Analisar e Salvar Captura", type="primary"):
            with st.spinner("Processando dados de visão computacional..."):
                result = controller.process_capture(image)
                st.success("Processamento e armazenamento concluídos!")
                
                st.json({
                    "ID": result["id"],
                    "Rostos Identificados": result["rostos"],
                    "Luminosidade": result["luminosidade"],
                    "Nitidez": result["nitidez"],
                    "Cores Predominantes": result["cores"],
                    "Caminho do Arquivo": result["image_path"]
                })