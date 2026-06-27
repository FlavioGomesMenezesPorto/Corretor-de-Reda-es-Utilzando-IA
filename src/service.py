from pathlib import Path
from typing import List

from .data_processing import clean_text
from .model import EssayGraderModel
from .rubrics import (
    BASE_CRITERIA,
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
            raise ValueError("Digite uma redacao antes de avaliar.")
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
                "Texto forte para uma correcao rigorosa, com boa sustentacao argumentativa.",
                "Revise precisao vocabular, repertorio, conclusao, coesao e transicoes entre paragrafos.",
            ]
        if score >= 7:
            return [
                "Boa base, mas ainda falta refinamento para alto padrao.",
                "Aprofunde a capacidade argumentativa e reduza generalizacoes.",
            ]
        return [
            "Para alto padrao, o texto precisa de mais densidade argumentativa.",
            "Fortaleca tese, coerencia, coesao, repertorio e dominio gramatical.",
        ]
    if profile == "baixo":
        if score >= 7:
            return [
                "Bom desempenho para uma etapa inicial de treino.",
                "O proximo passo e aumentar repertorio, coerencia e coesao.",
            ]
        return [
            "Comece garantindo introducao, desenvolvimento e conclusao.",
            "Priorize clareza, coesao basica e relacao direta com o tema.",
        ]
    if score >= 8:
        return [
            "Texto bem encaminhado, com estrutura e argumentacao consistentes.",
            "Revise detalhes de coesao, coerencia, repertorio e modalidade escrita.",
        ]
    if score >= 6:
        return [
            "A redacao tem uma base boa, mas precisa de mais desenvolvimento.",
            "Fortaleca exemplos, conectivos, progressao logica e conclusao.",
        ]
    return [
            "A redacao precisa de revisao estrutural.",
            "Priorize tema, estrutura, tese, capacidade argumentativa, coerencia, coesao e conclusao.",
        ]

def correction_checklist(text: str, profile: str = "medio") -> List[str]:
    profile_config = CORRECTION_PROFILES.get(profile, CORRECTION_PROFILES["medio"])
    line_count = estimate_line_count(text)
    status, message = line_count_status(line_count, profile)
    checklist = [message]

    paragraphs = [paragraph.strip() for paragraph in text.splitlines() if paragraph.strip()]
    words = text.split()
    word_count = len(words)

    if paragraphs and len(paragraphs) < 3:
        checklist.append("Estrutura: use introducao, desenvolvimento e conclusao com paragrafos separados.")
    elif len(paragraphs) >= 3:
        checklist.append("Estrutura: ha separacao minima de paragrafos para introducao, desenvolvimento e conclusao.")

    if status != "ok":
        checklist.append(
            f"Nesse perfil, a extensao esperada fica entre {profile_config['min_lines']} "
            f"e {profile_config['max_lines']} linhas."
        )

    text_lower = text.lower()

    thesis_markers = [
        "defende-se",
        "argumenta-se",
        "e necessario",
        "e preciso",
        "deve",
        "torna-se",
        "nota-se",
        "percebe-se",
    ]
    if any(marker in text_lower for marker in thesis_markers):
        checklist.append("Tese: ha ind cios de posicionamento central no texto.")
    else:
        checklist.append("Tese: deixe mais clara a posicao central que sera defendida.")

    connectives = [
        "portanto",
        "logo",
        "assim",
        "desse modo",
        "dessa forma",
        "contudo",
        "porem",
        "entretanto",
        "no entanto",
        "alem disso",
        "ademais",
        "outrossim",
        "por conseguinte",
        "em suma",
    ]
    found_connectives = [connective for connective in connectives if connective in text_lower]
    if len(found_connectives) >= 3:
        checklist.append(f"Coesao: bom uso de conectivos, como {', '.join(found_connectives[:3])}.")
    elif found_connectives:
        checklist.append("Coesao: ha conectivos, mas vale diversificar para melhorar a ligacao entre ideias.")
    else:
        checklist.append("Coesao: poucos conectivos identificados; use marcadores como 'portanto', 'alem disso' e 'contudo'.")

    argument_markers = [
        "porque",
        "pois",
        "ja que",
        "visto que",
        "uma vez que",
        "devido a",
        "segundo",
        "de acordo com",
        "conforme",
        "nota-se",
        "e evidente",
    ]
    found_arguments = [marker for marker in argument_markers if marker in text_lower]
    if len(found_arguments) >= 2:
        checklist.append("Capacidade Argumentativa: ha marcas claras de justificativa e embasamento.")
    else:
        checklist.append("Capacidade Argumentativa: desenvolva melhor as justificativas com relacoes de causa, exemplo ou autoridade.")

    repertory_markers = [
        "segundo",
        "de acordo com",
        "conforme",
        "dados",
        "pesquisa",
        "historia",
        "historico",
        "sociedade",
        "exemplo",
        "por exemplo",
        "filosofia",
        "sociologia",
        "constitui",
        "constituicao",
    ]
    if any(marker in text_lower for marker in repertory_markers):
        checklist.append("Repertorio e exemplos: ha tentativa de usar referencia, dado ou exemplo concreto.")
    else:
        checklist.append("Repertorio e exemplos: inclua dados, fatos, referencias ou exemplos concretos para sustentar a tese.")

    conclusion_markers = ["portanto", "em suma", "conclui-se", "dessa forma", "desse modo", "assim"]
    final_part = " ".join(words[-60:]).lower()
    if any(marker in final_part for marker in conclusion_markers):
        checklist.append("Conclusao: ha ind cios de fechamento do raciocinio no trecho final.")
    else:
        checklist.append("Conclusao: finalize retomando a tese e fechando o raciocinio desenvolvido.")

    vague_words = ["coisa", "algo", "muito", "varios", "diversos", "bom", "ruim"]
    repeated_words = {
        word
        for word in words
        if len(word) > 4 and words.count(word) >= 4
    }
    if repeated_words or any(word in text_lower for word in vague_words):
        checklist.append("Vocabulario e precisao: reduza repeticoes e troque termos vagos por palavras mais precisas.")
    else:
        checklist.append("Vocabulario e precisao: o texto nao apresenta excesso evidente de termos vagos ou repeticoes.")

    sentence_count = max(1, text.count(".") + text.count("!") + text.count("?"))
    average_sentence_size = word_count / sentence_count
    if average_sentence_size > 35:
        checklist.append("Norma-padrao: revise pontuacao; ha frases longas que podem prejudicar clareza e gramatica.")
    else:
        checklist.append("Norma-padrao: mantenha atencao a ortografia, concordancia, regencia e pontuacao.")

    if word_count < 100:
        checklist.append("Coerencia: texto curto, o que pode limitar a progressao logica das ideias.")
    else:
        checklist.append("Coerencia: confira se os paragrafos avancam para uma conclusao sem contradicoes.")

    checklist.append("Tema: confira se todos os paragrafos respondem diretamente ao tema proposto.")
    checklist.append(f"Expectativa do perfil: {profile_config['expectation']}")

    return checklist

def correction_criteria_rows():
    return criteria_rows()

def required_core_criteria():
    return [criterion["label"] for criterion in BASE_CRITERIA.values()]