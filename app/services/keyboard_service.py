
KEYBOARD_LAYOUTS = {
    "Tamil": [
        list("அஆஇஈஉஊஎஏஐஒஓஔ"),
        list("கஙசஞடணதநபம"),
        list("யரலவழளறனஜஷஸஹ"),
        list("ாிீுூெேைொோௌ்")
    ],

    "Hindi": [
        list("अआइईउऊऋएऐओऔ"),
        list("कखगघङचछजझञ"),
        list("टठडढणतथदधन"),
        list("पफबभमयरलवशषसह"),
        list("ािीुूृेैोौंः्")
    ],

    "Telugu": [
        list("అఆఇఈఉఊఋఎఏఐఒఓఔ"),
        list("కఖగఘఙచఛజఝఞ"),
        list("టఠడఢణతథదధన"),
        list("పఫబభమయరలవశషసహ"),
        list("ాిీుూృెేైొోౌంః్")
    ],

    "Malayalam": [
        list("അആഇഈഉഊഋഎഏഐഒഓഔ"),
        list("കഖഗഘങചഛജഝഞ"),
        list("ടഠഡഢണതഥദധന"),
        list("പഫബഭമയരലവശഷസഹളഴറ"),
        list("ാിീുൂൃെേൈൊോൌംഃ്")
    ]
}


def get_keyboard_layout(language):
    if language not in KEYBOARD_LAYOUTS:
        raise ValueError(f"Unsupported language: {language}")

    return KEYBOARD_LAYOUTS[language]


def get_supported_keyboard_languages():
    return list(KEYBOARD_LAYOUTS.keys())
