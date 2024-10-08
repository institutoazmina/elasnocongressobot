import re

"""
This module exports the assert_theme function.
That is used to assert if a proposal is relevant for the goal of this project.
"""


def assert_theme(input_obj):
    """
    This function use two different regex. One looking for terms on words on itself,
    and the other looks for words that are combined with another keyword.

    The return of this function is a boolean that indicates wether the row is relevant
    and the matches of both regex.
    """
    input_string = " ".join([value or "" for value in input_obj.values()])

    if not input_string.strip():
        return {"row_relevant": False, "temas": []}

    pattern1 = re.compile(r'\b(ABORTAMENTO|ABORTO|ABUSO SEXUAL|AMAMENTAÇÃO|ASSÉDIO|ASSÉDIO SEXUAL|BEBÊ|CASAMENTO|CASAMENTO INFANTIL|CONCEPÇÃO|CONTRACEPÇÃO|CONTRACEPTIVO|CRECHE|CRIANÇA|CYTOTEC|DIREITO À VIDA|DIREITO DOS HOMENS|DIREITO REPRODUTIVO|DIREITOS REPRODUTIVOS|DIVÓRCIO|DOMÉSTICA|EDUCAÇÃO DOMICILIAR|EDUCAÇÃO INFANTIL|EDUCAÇÃO SEXUAL|ESCOLA SEM PARTIDO|ESTUPRO|ESTUPRO DE VULNERÁVEL|EXPLORAÇÃO SEXUAL|FEMINICÍDIO|FEMININO|FEMINISMO|FETO|GÊNERO|GESTAÇÃO|GESTANTE|GRAVIDEZ|GUARDA DE FILHOS|GUARDA DOS FILHOS|HOMESCHOOLING|HOMICÍDIO DE MULHER|HOMOSSEXUAL|IDENTIDADE DE GÊNERO|IDEOLOGIA DE GÊNERO|IGUALDADE|IGUALDADE DE GÊNERO|INTERRUPÇÃO DA GESTAÇÃO|INTERRUPÇÃO DA GRAVIDEZ|LÉSBICA|LICENÇA MATERNIDADE|MACHISMO|MÃE|MARIA DA PENHA|MATERNIDADE|MIFEPRISTONE|MISOPROSTOL|MORTE DE MULHER|MUDANÇA DE SEXO|MULHER|MULHER NEGRA|MULHER TRANS|MULHERES INDÍGENAS|MULHERES NEGRAS|MULHERES QUILOMBOLAS|MULHERES TRANS|NASCITURO|NEGRA|ORIENTAÇÃO SEXUAL|PARTO|PROSTITUIÇÃO|READEQUAÇÃO SEXUAL|SEXO|SEXUALIDADE|TRABALHO DOMÉSTICO|TRANS|TRANSEX|TRANSGEN|TRANSEXUAL|TRANSEXUALIDADE|ÚTERO|VIOLÊNCIA CONTRA A MULHER|VIOLÊNCIA DE GÊNERO|VIOLÊNCIA POLÍTICA DE GÊNERO|VIOLÊNCIA DOMÉSTICA|VIOLÊNCIA OBSTÉTRICA|VIOLÊNCIA SEXUAL|SEXUAL)\b', re.IGNORECASE)
    pattern2 = re.compile(r'(?=.*\bmulher\b).*\b(COTAS|TRABALHO|RAÇA|PARTICIPAÇÃO POLÍTICA|RACIAL|POLÍTICA|RACISMO|RELIGIÃO|EDUCAÇÃO RELIGIOSA|DEUS)\b', re.IGNORECASE)

    matches = pattern1.findall(input_string) + pattern2.findall(input_string)
    return {"row_relevant": len(matches) > 0, "temas": matches}
