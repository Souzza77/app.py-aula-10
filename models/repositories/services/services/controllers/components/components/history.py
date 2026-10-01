import os
import json
import pandas as pd
import streamlit as st
from controllers.main_controller import MainController

def render_history_component(controller: MainController):
    st.subheader("Histórico de Análises")
    records = controller.fetch_all_analyses()

    if not records:
        st.info("Nenhuma análise registrada até o momento.")
        return

    data_list = []
    for r in records:
        data_list.append({
            "ID": r.id,
            "Data": r.created_at,
            "Descrição": r.descricao,
            "Pessoas": r.quantidade_pessoas,
            "Luminosidade": r.luminosidade,
            "Nitidez": r.nitidez,
            "Caminho": r.image_path
        })
    df = pd.DataFrame(data_list)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Exportar Histórico (CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='historico_visao_computacional.csv',
            mime='text/csv'
        )
    with col2:
        json_data = json.dumps([d["Data"].isoformat() if hasattr(d["Data"], 'isoformat') else str(d["Data"]) for d in data_list], indent=2)
        st.download_button(
            "Exportar Dados (JSON)",
            data=json_data,
            file_name='historico_visao_computacional.json',
            mime='application/json'
        )

    search = st.text_input("Filtrar por Descrição")
    if search:
        records = [r for r in records if search.lower() in (r.descricao or "").lower()]

    for item in records:
        with st.expander(f"Análise ID: #{item.id} - {item.created_at.strftime('%d/%m/%Y %H:%M:%S')}"):
            c1, c2 = st.columns([1, 2])
            with c1:
                if os.path.exists(item.image_path):
                    st.image(item.image_path, use_column_width=True)
                    with open(item.image_path, "rb") as file:
                        st.download_button(
                            label="Baixar Imagem",
                            data=file,
                            file_name=os.path.basename(item.image_path),
                            mime="image/jpeg",
                            key=f"dl_{item.id}"
                        )
                else:
                    st.warning("Arquivo de imagem não encontrado no disco.")
            with c2:
                st.write(f"**Descrição:** {item.descricao}")
                st.write(f"**Rostos Encontrados:** {item.rostos}")
                st.write(f"**Luminosidade:** {item.luminosidade}")
                st.write(f"**Nitidez:** {item.nitidez}")
                st.write(f"**Cores Predominantes:** {', '.join(item.cores or [])}")

                if st.button("Excluir Registro", key=f"del_{item.id}"):
                    if controller.delete_analysis(item.id):
                        st.success("Registro removido!")
                        st.rerun()