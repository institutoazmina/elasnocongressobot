import re

def norm(text):
    text = text.strip(); # trim
    text = removeNone(text)
    text = truncLongName(text)
    return text

def removeNone(text):
    newText = text.replace( ' Situação: None.', '').replace(' Tramitação: None.', '').replace(', de autoria de None,', '')
    return newText

def repNameV1(m):
    names = m.group(2).split(', ')

    # mais de um author
    if (len(names) > 1):
        return m.group(1) + names[0] + ' e outros(as)' + m.group(3)

    return m.group(1) + names[0] + m.group(3)

def repNameV2(m):
    names = m.group(2).split(', ')

    firstName = names[0]
    if (len(names) > 1):
        print(len(firstName))
        print ("\n")
        if (len(firstName) > 20):
            nameParts = firstName.split(' ')
            firstName = ' '.join(nameParts[0:3]) + '…'

        return m.group(1) + firstName + ' e outros(as)' + m.group(3)

    if (len(firstName) > 20):
        nameParts = firstName.split(' ')
        firstName = ' '.join(nameParts[0:3]) + '…'

    return m.group(1) + firstName + m.group(3)


def truncLongName(text):
    if (len(text) < 280):
        return text # no mods needed

    newText = re.sub(r"(de autoria de )(.*)(, fala sobre)", repNameV1, text)

    # try again with without "e outros...")
    if (len(newText) > 280):
        newText = re.sub(r"(de autoria de )(.*)(, fala sobre)", repNameV2, text)

    # remove all authors
    if (len(newText) > 280):
        newText = re.sub(r", de autoria de .*, fala sobre", ', fala sobre', text)

    # if still too long, remove a lot of info
    if (len(newText) > 280):
        newText = re.sub(r"de autoria de.*sofreu alterações em sua tramitação\. ", '', text)

    return newText

print(norm("CÂMARA: PL 2753/2020, de autoria de Erika santos de souza Patrus Ananias de foo barPatrus Ananias de foo barPatrus Ananias de foo bar, fala sobre crianças e sofreu alterações em sua tramitação. Tramitação: Devolução ao Relator. Situação: Aguardando Parecer. http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor=1895093 "))