from pathlib import Path
import sys

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.service import (
    DEFAULT_MODEL_PATH,
    EssayGraderService,
    available_profiles,
    correction_checklist,
    correction_criteria_rows,
    feedback_points,
    score_label,
)


st.set_page_config(
    page_title="IntelliWrite AI",
    page_icon="IW",
    layout="wide",
)


@st.cache_resource
def get_service(model_path: str) -> EssayGraderService:
    service = EssayGraderService(model_path)
    if service.model_exists():
        service.load()
    return service


def main() -> None:
    st.title("IntelliWrite AI")
    st.caption("Correção experimental de redações com perfis de exigência")

    model_path = st.sidebar.text_input("Modelo", value=str(DEFAULT_MODEL_PATH))
    profiles = available_profiles()
    profile_options = list(profiles.keys())
    profile_labels = {key: value["label"] for key, value in profiles.items()}
    selected_profile = st.sidebar.selectbox(
        "Tipo de correção",
        options=profile_options,
        index=1,
        format_func=lambda key: profile_labels[key],
    )
    service = get_service(model_path)

    st.sidebar.divider()
    if service.model_exists():
        st.sidebar.success("Modelo encontrado")
    else:
        st.sidebar.error("Modelo não encontrado")
        st.sidebar.code(
            ".\\.venv\\Scripts\\python.exe src\\api.py train --data data\\redacoes_padrao.csv --model-path models\\essay_grader.joblib",
            language="bat",
        )

    st.sidebar.info(profiles[selected_profile]["description"])

    sample = (
        "Título: Tecnologia e responsabilidade social\n\n"
        "O avanço tecnológico modifica a forma como a sociedade aprende, trabalha e participa da vida pública. "
        "Entretanto, seus benefícios dependem de uso crítico, acesso democrático e responsabilidade coletiva..."
    )

    essay_text = st.text_area(
        "Cole a redação",
        value="",
        placeholder=sample,
        height=280,
    )

    uploaded_file = st.file_uploader("Ou envie um arquivo .txt", type=["txt"])
    if uploaded_file is not None:
        essay_text = uploaded_file.read().decode("utf-8", errors="replace")
        st.text_area("Texto do arquivo", value=essay_text, height=220, disabled=True)

    col_evaluate, col_clear = st.columns([1, 4])
    evaluate = col_evaluate.button("Avaliar redação", type="primary", use_container_width=True)
    col_clear.button("Limpar", use_container_width=False)

    if evaluate:
        if not service.model_exists():
            st.error("Treine o modelo antes de avaliar redações.")
            return

        try:
            score = service.predict_score(essay_text, selected_profile)
        except ValueError as error:
            st.warning(str(error))
            return

        label = score_label(score, selected_profile)
        st.subheader(f"Resultado - {profile_labels[selected_profile]}")

        metric_col, label_col = st.columns([1, 2])
        metric_col.metric("Nota prevista", f"{score:.2f}")
        label_col.write(f"Leitura geral: **{label}**")

        st.progress(min(max(score / 10, 0), 1))

        st.write("Pontos de atenção:")
        for point in feedback_points(score, selected_profile):
            st.write(f"- {point}")

        st.write("Checklist:")
        for point in correction_checklist(essay_text, selected_profile):
            st.write(f"- {point}")

    with st.expander("Critérios usados como referência"):
        st.dataframe(correction_criteria_rows(), hide_index=True, use_container_width=True)
        st.caption("A previsão automática estima a nota total. O perfil escolhido ajusta o nível de exigência.")

    with st.expander("Como treinar novamente"):
        st.code(
            ".\\.venv\\Scripts\\python.exe src\\api.py train --data data\\redacoes_padrao.csv --model-path models\\essay_grader.joblib",
            language="bat",
        )


if __name__ == "__main__":
    main()
