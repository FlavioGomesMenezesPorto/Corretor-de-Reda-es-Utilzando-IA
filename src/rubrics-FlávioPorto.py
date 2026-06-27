BASE_CRITERIA = {
    "tema": {
        "label": "Tema",
        "max_score": 2.0,
        "description": "Aderência ao tema, repertório e desenvolvimento do assunto proposto.",
    },
    "tipo_texto": {
        "label": "Tipo de texto",
        "max_score": 2.0,
        "description": "Estrutura dissertativo-argumentativa, tese, argumentos e conclusão.",
    },
    "capacidade_argumentativa": {
        "label": "Capacidade Argumentativa",
        "max_score": 2.0,
        "description": "Seleção, relação, organização e interpretação de informações, fatos e opiniões em defesa de um ponto de vista.",
    },
    "coerencia": {
        "label": "Coerência",
        "max_score": 2.0,
        "description": "Organização lógica, progressão das ideias e ausência de contradições.",
    },
    "coesao": {
        "label": "Coesão",
        "max_score": 2.0,
        "description": "Conectivos, parágrafos, pontuação e ligação entre as partes do texto.",
    },
    "modalidade": {
        "label": "Modalidade escrita",
        "max_score": 2.0,
        "description": "Adequação à norma-padrão, vocabulário e precisão gramatical.",
    },
}

SCORE_COLUMNS = list(BASE_CRITERIA.keys())

CORRECTION_PROFILES = {
    "alto": {
        "label": "Correção de Alto Padrão",
        "description": "Mais exigente. Indicada para vestibulares concorridos, bancas rigorosas e textos quase prontos.",
        "score_adjustment": -0.6,
        "min_lines": 25,
        "max_lines": 35,
        "expectation": "Tese clara, repertório pertinente, argumentação crítica, coesão precisa e domínio da norma-padrão.",
    },
    "medio": {
        "label": "Correção de Médio Padrão",
        "description": "Equilibrada. Indicada para treino escolar, simulados e acompanhamento de evolução.",
        "score_adjustment": 0.0,
        "min_lines": 20,
        "max_lines": 35,
        "expectation": "Estrutura completa, argumentos compreensíveis, boa organização e poucos desvios gramaticais.",
    },
    "baixo": {
        "label": "Correção de Baixo Padrão",
        "description": "Mais tolerante e formativa. Indicada para rascunhos, iniciantes e primeiras versões.",
        "score_adjustment": 0.6,
        "min_lines": 15,
        "max_lines": 40,
        "expectation": "Tema reconhecível, tentativa de argumentação, começo-meio-fim e linguagem compreensível.",
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
        
    # Removido a lógica de contar "explicit_lines" porque em textos colados 
    # da web, uma quebra de linha representa um parágrafo inteiro.
    # Basear na quantidade de caracteres é muito mais fiável.
    return max(1, round(len(text.strip()) / average_chars_per_line))

    explicit_lines = [line for line in text.splitlines() if line.strip()]
    if len(explicit_lines) > 1:
        return len(explicit_lines)

    return max(1, round(len(text.strip()) / average_chars_per_line))


def line_count_status(line_count: int, profile: str) -> tuple[str, str]:
    profile_config = CORRECTION_PROFILES.get(profile, CORRECTION_PROFILES["medio"])
    min_lines = profile_config["min_lines"]
    max_lines = profile_config["max_lines"]
    label = profile_config["label"]

    if line_count == 0:
        return "empty", "Digite uma redação para estimar a quantidade de linhas."
    if line_count < min_lines:
        return "warning", f"No perfil {label}, a redação parece curta: estimativa de {line_count} linhas."
    if line_count > max_lines:
        return "warning", f"No perfil {label}, a redação parece longa: estimativa de {line_count} linhas."
    return "ok", f"Extensão estimada adequada para {label}: {line_count} linhas."


def score_label(score: float, profile: str) -> str:
    if profile == "alto":
        if score >= 8.5:
            return "Excelente para alto padrão"
        if score >= 7:
            return "Bom, mas ainda exige refinamento"
        if score >= 5:
            return "Mediano para alto padrão"
        return "Abaixo do alto padrão"

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
            "Critério": criterion["label"],
            "Pontuação": f"0 a {criterion['max_score']:.0f}",
            "O que avalia": criterion["description"],
        }
        for criterion in BASE_CRITERIA.values()
    ]
