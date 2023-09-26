import re

def assert_theme(input_obj):
    input_string = ' '.join([value or '' for value in input_obj.values()])

    if not input_string.strip():
        return {"row_relevant": False, "temas": []}

    pattern = re.compile(r'\b(mulheres|mulher|violência contra a mulher|violência doméstica|aborto|violência sexual|feminicídio|assédio sexual|estupro|licença maternidade|mulheres|feminino|trabalho doméstico|maria da penha|interrupção da gravidez|interrupção da gestação|interrupção de gestação|interrupção de gravidez|direitos reprodutivos|direito reprodutivo|direitos à vida|direito à vida|contracepção|contraceptivos|violência obstétrica|misoprostol|mifepristone|cytotec|gestação|gravidez|violência familiar|morte de mulher|morte de mulheres|homicídio de mulher|homicídio de mulheres|assédio|estupro de vulnerável|abuso sexual|mulher negra|mulheres negras|maternidade|mãe|amamentação|leite materno|feminismo|identidade de gênero|machismo|guarda de filhos|guarda dos filhos|igualdade de gênero|educação sexual|ideologia de gênero|transexualidade|transexual|mulher trans|mulheres trans|mudança de sexo|exploração sexual|prostituição|racismo|sexualidade|sexo|sexo|deus|educação religiosa|violência de gênero|parto|homeschooling|educação domiciliar|educação infantil|creches|casamento infantil|homossexual|homossexualidade|homossexualismo|orientação sexual|opção sexual|criança|sexo biológico|gênero|gestante)\b', re.IGNORECASE)
    matches = pattern.findall(input_string)
    return {"row_relevant": len(matches) > 0, "temas": matches}