from pathlib import Path
from typing import List

from .data_processing import clean_text
from .model import EssayGraderModel
from .rubrics import (
    CORRECTION_PROFILES,
    apply_correction_profile,
    criteria_rows,
    estimate_line_count,
    line_count_status,
    score_label as profile_score_label,
)


DEFAULT_MODEL_PATH = Path("models/essay_grader.joblib")


class EssayGraderService:
    def __init__(self, model_path: str | Path = DEFAULT_MODEL_PATH):
        self.model_path = Path(model_path)
        self.grader = EssayGraderModel()
        self.loaded = False

    def load(self) -> None:
        self.grader.load(str(self.model_path))
        self.loaded = True

    def predict_score(self, text: str, profile: str = "medio") -> float:
        if not self.loaded:
            self.load()

        cleaned = clean_text(text)
        if not cleaned:
            raise ValueError("Digite uma redação antes de avaliar.")

        base_score = self.grader.predict([cleaned])[0]
        return apply_correction_profile(base_score, profile)

    def model_exists(self) -> bool:
        return self.model_path.exists()


def available_profiles():
    return CORRECTION_PROFILES


def score_label(score: float, profile: str = "medio") -> str:
    return profile_score_label(score, profile)


def feedback_points(score: float, profile: str = "medio") -> List[str]:
    if profile == "alto":
        if score >= 8.5:
            return [
                "Texto forte para uma correção rigorosa, com boa sustentação argumentativa.",
                "Revise precisão vocabular, repertório e transições entre parágrafos.",
            ]
        if score >= 7:
            return [
                "Boa base, mas ainda falta refinamento para alto padrão.",
                "Aprofunde análise crítica e reduza generalizações.",
            ]
        return [
            "Para alto padrão, o texto precisa de mais densidade argumentativa.",
            "Fortaleça tese, repertório, progressão lógica e domínio gramatical.",
        ]

    if profile == "baixo":
        if score >= 7:
            return [
                "Bom desempenho para uma etapa inicial de treino.",
                "O próximo passo é aumentar repertório e melhorar coesão.",
            ]
        return [
            "Comece garantindo introdução, desenvolvimento e conclusão.",
            "Priorize clareza, frases mais completas e relação direta com o tema.",
        ]

    if score >= 8:
        return [
            "Texto bem encaminhado, com estrutura e argumentação consistentes.",
            "Revise detalhes de coesão, repertório e modalidade escrita.",
        ]
    if score >= 6:
        return [
            "A redação tem uma base boa, mas precisa de mais desenvolvimento.",
            "Fortaleça exemplos, conectivos e conclusão.",
        ]
    return [
        "A redação precisa de revisão estrutural.",
        "Priorize tema, tese, organização dos parágrafos e clareza das ideias.",
    ]


def correction_checklist(text: str, profile: str = "medio") -> List[str]:
    profile_config = CORRECTION_PROFILES.get(profile, CORRECTION_PROFILES["medio"])
    line_count = estimate_line_count(text)
    status, message = line_count_status(line_count, profile)
    checklist = [message]

    # Separar as linhas ignorando as que estão vazias (funciona com \n ou \n\n)
    linhas = [linha.strip() for linha in text.splitlines() if linha.strip()]
    
    # 2. Nova contagem de Parágrafos
    paragraph_count = len(linhas)
    if paragraph_count and paragraph_count < 3:
        checklist.append("Estrutura: Use introdução, desenvolvimento e conclusão com parágrafos separados.")

    if status != "ok":
        checklist.append(
            f"Nesse perfil, a extensão esperada fica entre {profile_config['min_lines']} "
            f"e {profile_config['max_lines']} linhas."
        )

    # Coesão
    connectives = ["portanto", "logo", "assim", "então", "desse modo", "dessa forma", "contudo", "porém", "entretanto", "no entanto", "todavia", "além disso", "ademais", "outrossim", "por conseguinte", "em suma"]
    text_lower = text.lower()
    found_connectives = [c for c in connectives if c in text_lower]
    if len(found_connectives) >= 3:
        checklist.append(f"Coesão: Bom uso de conectivos (ex: {', '.join(found_connectives[:3])}).")
    elif len(found_connectives) > 0:
        checklist.append("Coesão: Uso básico de conectivos, tente diversificar mais para melhorar a ligação entre as frases e parágrafos.")
    else:
        checklist.append("Coesão: Poucos conectivos identificados. Use termos como 'portanto', 'além disso', 'contudo' para ligar as ideias.")

    # Capacidade Argumentativa
    arg_markers = ["porque", "pois", "já que", "visto que", "uma vez que", "dado que", "devido a", "em virtude de", "segundo", "de acordo com", "conforme", "para que", "a fim de", "nota-se", "prova-se", "é evidente"]
    found_args = [m for m in arg_markers if m in text_lower]
    if len(found_args) >= 2:
        checklist.append("Capacidade Argumentativa: Há marcas claras de justificativa e embasamento no texto.")
    else:
        checklist.append("Capacidade Argumentativa: Faltam marcadores de justificativa e embasamento (ex: 'porque', 'visto que', 'segundo'). Desenvolva mais seus argumentos.")

    # Coerência
    if len(text.split()) < 100:
         checklist.append("Coerência: Texto muito curto, o que pode prejudicar a progressão lógica e o aprofundamento das ideias sem deixar pontas soltas.")
    else:
         checklist.append("Coerência: Certifique-se de que não há contradições entre os parágrafos e de que a progressão de ideias leva a uma conclusão lógica.")

    checklist.append(f"Expectativa do perfil: {profile_config['expectation']}")
    return checklist


def correction_criteria_rows():
    return criteria_rows()
