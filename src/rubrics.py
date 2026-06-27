BASE_CRITERIA = {
    "tema": {
        "label": "Tema",
        "max_score": 2.0,
        "description": "Aderencia ao tema e desenvolvimento do assunto proposto sem fuga tematica.",
    },
    "estrutura_textual": {
        "label": "Estrutura textual",
        "max_score": 2.0,
        "description": "Organizacao em introducao, desenvolvimento e conclusao, sem exigir titulo.",
    },
    "tese": {
        "label": "Tese",
        "max_score": 2.0,
        "description": "Presenca de uma posicao central clara, defensavel e sustentada ao longo do texto.",
    },
    "capacidade_argumentativa": {
        "label": "Capacidade Argumentativa",
        "max_score": 2.0,
        "description": "Selecao, organizacao e interpretacao de informacoes, fatos e opinioes em defesa de um ponto de vista.",
    },
    "coerencia": {
        "label": "Coerencia",
        "max_score": 2.0,
        "description": "Organizacao logica, progressao das ideias e ausencia de contradicoes.",
    },
    "coesao": {
        "label": "Coesao",
        "max_score": 2.0,
        "description": "Uso de conectivos, paragrafos, pontuacao e ligacao clara entre as partes do texto.",
    },
    "repertorio_exemplos": {
        "label": "Repertorio e exemplos",
        "max_score": 2.0,
        "description": "Uso produtivo de dados, fatos, referencias, experiencias ou exemplos concretos.",
    },
    "norma_padrao": {
        "label": "Norma-padrao",
        "max_score": 2.0,
        "description": "Ortografia, concordancia, regencia, pontuacao e adequacao gramatical.",
    },
    "conclusao": {
        "label": "Conclusao",
        "max_score": 2.0,
        "description": "Fechamento do raciocinio, retomada da tese e, quando cabivel, proposta de encaminhamento.",
    },
    "vocabulario_precisao": {
        "label": "Vocabulario e precisao",
        "max_score": 2.0,
        "description": "Clareza lexical, precisao dos termos, variedade vocabular e baixa repeticao.",
    },
}

SCORE_COLUMNS = list(BASE_CRITERIA.keys())

CORRECTION_PROFILES = {
    "baixo": {
        "label": "Baixo Padrao",
        "description": "Mais tolerante e formativo. Indicado para rascunhos, iniciantes e primeiras versoes.",
        "score_adjustment": 0.6,
        "min_lines": 15,
        "max_lines": 40,
        "expectation": "Tema reconhecivel, tese inicial, tentativa de argumentacao, come o-meio-fim e linguagem compreensivel.",
    },
    "medio": {
        "label": "Medio Padrao",
        "description": "Equilibrado. Indicado para treino escolar, simulados e acompanhamento de evolucao.",
        "score_adjustment": 0.0,
        "min_lines": 20,
        "max_lines": 35,
        "expectation": "Estrutura completa, tese clara, argumentos compreensiveis, exemplos pertinentes, boa organizacao e poucos desvios gramaticais.",
    },
    "alto": {
        "label": "Alto Padrao",
        "description": "Mais exigente. Indicado para vestibulares concorridos, bancas rigorosas e textos quase prontos.",
        "score_adjustment": -0.6,
        "min_lines": 25,
        "max_lines": 35,
        "expectation": "Tese forte, repertorio pertinente, argumentacao critica, coerencia rigorosa, coesao precisa e dominio da norma-padrao.",
    },
}

def clamp_score(score: float) -> float:
    return min(max(score, 0.0), 10.0)

def apply_correction_profile(score: float, profile: str) -> float:
    profile_config = CORRECTION_PROFILES.get(profile, CORRECTION_PROFILES["medio"])
    return round(clamp_score(score + profile_config["score_adjustment"]), 2)

def estimate_line_count(text: str, average_chars_per_line: int = 72) -> int:
    if not text.strip():
        return 0
    return max(1, round(len(text.strip()) / average_chars_per_line))

def line_count_status(line_count: int, profile: str = "medio") -> tuple[str, str]:
    profile_config = CORRECTION_PROFILES.get(profile, CORRECTION_PROFILES["medio"])
    min_lines = profile_config["min_lines"]
    max_lines = profile_config["max_lines"]
    label = profile_config["label"]
    if line_count == 0:
        return "empty", "Digite uma redacao para estimar a quantidade de linhas."
    if line_count < min_lines:
        return "warning", f"No {label}, a redacao parece curta: estimativa de {line_count} linhas."
    if line_count > max_lines:
        return "warning", f"No {label}, a redacao parece longa: estimativa de {line_count} linhas."
    return "ok", f"Extensao estimada adequada para {label}: {line_count} linhas."

def score_label(score: float, profile: str = "medio") -> str:
    if profile == "alto":
        if score >= 8.5:
            return "Excelente para alto padrao"
        if score >= 7:
            return "Bom, mas ainda exige refinamento"
        if score >= 5:
            return "Mediano para alto padrao"
        return "Abaixo do alto padrao"
    if profile == "baixo":
        if score >= 8:
            return "Muito bom para etapa inicial"
        if score >= 6:
            return "Bom ponto de partida"
        if score >= 4:
            return "Precisa organizar melhor"
        return "Precisa de reescrita guiada"
    if score >= 8:
        return "Muito bom"
    if score >= 6:
        return "Bom"
    if score >= 4:
        return "Regular"
    return "Precisa melhorar"

def criteria_rows():
    return [
        {
            "Criterio": criterion["label"],
            "Pontuacao": f"0 a {criterion['max_score']:.0f}",
            "O que avalia": criterion["description"],
        }
        for criterion in BASE_CRITERIA.values()
    ]