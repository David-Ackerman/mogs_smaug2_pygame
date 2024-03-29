from src.interfaces.card_model import Deck

cards: list[Deck] = [{
    "onGameId": None,
    "card_id": "1",
    "card_name": "Frost Queen",
    "card_image": "assets/images/cards/1.png",
    "card_type": "monster effect",
    "card_element": "cryo",
    "card_attack": 40,
    "card_def": 35,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Efeito congelar: Durante a fase do adversário, sacrificando 2 mana esta carta pode congelar uma carta inimiga.",
},
    {
    "onGameId": None,
    "card_id": "2",
    "card_name": "Infortuno de gelo",
    "card_image": "assets/images/cards/2.png",
    "card_type": "monster effect",
    "card_element": "cryo",
    "card_attack": 25,
    "card_def": 14,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Quando invocado pode congelar uma carta no campo inimigo.",
},
    {
    "onGameId": None,
    "card_id": "3",
    "card_name": "Dykro, O pecado de gelo",
    "card_image": "assets/images/cards/3.png",
    "card_type": "monster effect",
    "card_element": "cryo",
    "card_attack": 0,
    "card_def": 0,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Efeito Aprisionado: para invocar essa carta é necessário sacrificar duas cartas que estão em seu campo, seu poder de ataque e de defesa será definido pela soma do poder dessas duas cartas",
},

    {
    "onGameId": None,
    "card_id": "5",
    "card_name": "Soulice",
    "card_image": "assets/images/cards/5.png",
    "card_type": "monster",
    "card_element": "cryo",
    "card_attack": 25,
    "card_def": 20,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Há boatos que essas criaturas eram pessoas que se perderam em meio a tempestade de gelo, e agora vagam sem rumo pelo deserto congelado de frost.",
},
    {
    "onGameId": None,
    "card_id": "6",
    "card_name": "Mega-Mecha Mutt",
    "card_image": "assets/images/cards/6.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 40,
    "card_def": 45,
    "card_cust": 9,
    "card_effect": None,
    "card_description": "Feito da tecnologia de ponta esse mamute de aço com chifres pontudos é capaz de destruir tudo pelo seu caminho.",
},

    {
    "onGameId": None,
    "card_id": "9",
    "card_name": "Mecha Monge",
    "card_image": "assets/images/cards/9.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 35,
    "card_def": 25,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Soldados mecânicos com a instrução de proteger o templo de Soma de ameaças e intrusos, melhor ficar longe uma porrada desses caras deixam marcas.",
},
    {
    "onGameId": None,
    "card_id": "10",
    "card_name": "Tail Hammer",
    "card_image": "assets/images/cards/10.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 20,
    "card_def": 15,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Os machos dessa espécie possuem uma grande extensão rochosa que vai da sua cabeça e ombros até sua cauda que possuí a aparência de um martelo. São animais territoriais e esmagam facilmente qualquer um que entre no seu território.",
},
    {
    "onGameId": None,
    "card_id": "11",
    "card_name": "Samurai Roostermage",
    "card_image": "assets/images/cards/11.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 15,
    "card_def": 15,
    "card_cust": 2,
    "card_effect": None,
    "card_description": "Este corajoso galo abandonou seu clã e sua família para seguir uma árdua jornada com o objetivo de se tornar um samurai e deixar seu legado.",
},

    {
    "onGameId": None,
    "card_id": "14",
    "card_name": "Kator Furry",
    "card_image": "assets/images/cards/14.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 25,
    "card_def": 15,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Efeito Forja Viva: Pode ressuscitar do cemitério um personagem de até 3 de mana do tipo Knight aumentando seu poder de ataque em +5. ",
},
    {
    "onGameId": None,
    "card_id": "15",
    "card_name": "Hiena Guerreira Invocada",
    "card_image": "assets/images/cards/15.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 30,
    "card_def": 5,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Criatura das trevas que carrega a própria guerra nos olhos, comanda um grupo de hienas menores para abater seus adversários.",
},
    {
    "onGameId": None,
    "card_id": "16",
    "card_name": "Mercenário",
    "card_image": "assets/images/cards/16.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 35,
    "card_def": 25,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Lobo solitário na lista negra do governo sendo um exímio guerreiro na arte da espada, aguardando qualquer brecha para matar seus oponentes.",
},
    {
    "onGameId": None,
    "card_id": "17",
    "card_name": "Presa do deserto",
    "card_image": "assets/images/cards/17.png",
    "card_type": "monster",
    "card_element": "knight",
    "card_attack": 20,
    "card_def": 5,
    "card_cust": 2,
    "card_effect": None,
    "card_description": "Pequenas e malandras criaturas do deserto, utiliza o veneno de suas presas afiadas para abater criaturas com o triplo de seu tamanho.",
},
    {
    "onGameId": None,
    "card_id": "18",
    "card_name": "Ruler",
    "card_image": "assets/images/cards/18.png",
    "card_type": "monster effect",
    "card_element": "anemo",
    "card_attack": 15,
    "card_def": 15,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Principios celestiais: A cada rodada seu poder de ataque Aumenta em 10, após 5 stacks o efeito é resetado",
},
    {
    "onGameId": None,
    "card_id": "19",
    "card_name": "Sirene dos ventos",
    "card_image": "assets/images/cards/19.png",
    "card_type": "monster effect",
    "card_element": "anemo",
    "card_attack": 20,
    "card_def": 20,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Frenesi: Quando em campo, aumenta em 5 o poder de ataque e defesa de qualquer criatura do tipo Anemo (inclui a si propria)",
},
    {
    "onGameId": None,
    "card_id": "20",
    "card_name": "Rasante veloz",
    "card_image": "assets/images/cards/20.png",
    "card_type": "monster",
    "card_element": "anemo",
    "card_attack": 25,
    "card_def": 10,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Com a precisão perfeita atira fechas letais em seus inimigos.",
},
    {
    "onGameId": None,
    "card_id": "21",
    "card_name": "Hatpunk",
    "card_image": "assets/images/cards/21.png",
    "card_type": "monster effect",
    "card_element": "anemo",
    "card_attack": 20,
    "card_def": 15,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Crazy broom: Essa carta só poder ser destruída por uma carta do mesmo elemento",
},
    {
    "onGameId": None,
    "card_id": "22",
    "card_name": "Frognácio",
    "card_image": "assets/images/cards/22.png",
    "card_type": "monster effect",
    "card_element": "anemo",
    "card_attack": 15,
    "card_def": 15,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Iron Palm: Com sua palma de aço pode derrotar qualquer inimigo com menos 3 de mana mesmo se o poder do inimigo for mais elevado que o seu.",
},
    {
    "onGameId": None,
    "card_id": "23",
    "card_name": "Cyclone",
    "card_image": "assets/images/cards/23.png",
    "card_type": "monster",
    "card_element": "anemo",
    "card_attack": 45,
    "card_def": 15,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Testemunhe o poder da natureza.",
},

    {
    "onGameId": None,
    "card_id": "25",
    "card_name": "Coruja armada",
    "card_image": "assets/images/cards/25.png",
    "card_type": "monster",
    "card_element": "anemo",
    "card_attack": 15,
    "card_def": 5,
    "card_cust": 1,
    "card_effect": None,
    "card_description": "Uma fofa e traiçoeira coruja que está pronta para te matar.",
},
    {
    "onGameId": None,
    "card_id": "26",
    "card_name": "Juulgart´s",
    "card_image": "assets/images/cards/26.png",
    "card_type": "monster",
    "card_element": "dendro",
    "card_attack": 40,
    "card_def": 35,
    "card_cust": 8,
    "card_effect": None,
    "card_description": "Criaturas colossais que vivem se alimentando de árvores e a vegetação ao seu redor.",
},

    {
    "onGameId": None,
    "card_id": "28",
    "card_name": "Árvore da vida",
    "card_image": "assets/images/cards/28.png",
    "card_type": "monster effect",
    "card_element": "dendro",
    "card_attack": 0,
    "card_def": 50,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Benção Natural: quando em campo, defensores da arvore da vida recebem 5 de ataque e defesa adicionais. \n“Uma mãe cuida de seus filhos”  ~ Oog do Sul",
},
    {
    "onGameId": None,
    "card_id": "29",
    "card_name": "Candelabro da fronteira",
    "card_image": "assets/images/cards/29.png",
    "card_type": "monster effect",
    "card_element": "dendro",
    "card_attack": 25,
    "card_def": 15,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Mana: Quando destruído, lhe concede 1 de mana",
},
    {
    "onGameId": None,
    "card_id": "30",
    "card_name": "Andarilha",
    "card_image": "assets/images/cards/30.png",
    "card_type": "monster effect",
    "card_element": "dendro",
    "card_attack": 25,
    "card_def": 15,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Vagalume: Quando destruída essa carta invoca uma guardião da floresta pra seu campo.",
},
    {
    "onGameId": None,
    "card_id": "31",
    "card_name": "Guardiões da floresta",
    "card_image": "assets/images/cards/31.png",
    "card_type": "monster",
    "card_element": "dendro",
    "card_attack": 30,
    "card_def": 35,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Nascidos da ceiva da árvore sagrada, rodeiam e protegem a sua terra de invasores e inimigos.",
},
    {
    "onGameId": None,
    "card_id": "32",
    "card_name": "Pequeno Froky",
    "card_image": "assets/images/cards/32.png",
    "card_type": "monster effect",
    "card_element": "dendro",
    "card_attack": 10,
    "card_def": 10,
    "card_cust": 1,
    "card_effect": None,
    "card_description": "Mana: Quando destruído, froky lhe concede 1 de mana",
},

    {
    "onGameId": None,
    "card_id": "34",
    "card_name": "Elfa da floresta",
    "card_image": "assets/images/cards/34.png",
    "card_type": "monster",
    "card_element": "dendro",
    "card_attack": 20,
    "card_def": 15,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Faz parte da guarda que protege a árvore santa, utiliza magia e os segredos élficos para proteger sua terra natal.",
},
    {
    "onGameId": None,
    "card_id": "35",
    "card_name": "Mong Musg",
    "card_image": "assets/images/cards/35.png",
    "card_type": "monster effect",
    "card_element": "dendro",
    "card_attack": 20,
    "card_def": 20,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Reforço dos protegidos: Quando destruído invoca em seu campo de batalha 2 Cogu´s Armado.",
},
    {
    "onGameId": None,
    "card_id": "36",
    "card_name": "Cogu´s Armado",
    "card_image": "assets/images/cards/36.png",
    "card_type": "monster",
    "card_element": "dendro",
    "card_attack": 15,
    "card_def": 15,
    "card_cust": 2,
    "card_effect": None,
    "card_description": "A espreita na floresta vigiando seus amigos cogumelos para que ninguém os ameaçem.",
},
    {
    "onGameId": None,
    "card_id": "37",
    "card_name": "Passion Engine",
    "card_image": "assets/images/cards/37.png",
    "card_type": "monster",
    "card_element": "dendro",
    "card_attack": 20,
    "card_def": 0,
    "card_cust": 2,
    "card_effect": None,
    "card_description": "Uma pequena engrenagem que caiu de um moinho e recebeu vida graças a um mago que não tinha muito o que fazer. Vive a vida vagando pela floresta e admirando os insetos.",
},
    {
    "onGameId": None,
    "card_id": "38",
    "card_name": "void trolls",
    "card_image": "assets/images/cards/38.png",
    "card_type": "monster",
    "card_element": "dendro",
    "card_attack": 20,
    "card_def": 10,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Dizem que a floresta e suas criaturas foram criadas pela mãe natureza, exceto por esses abomináveis e horripilantes seres que vagam a floresta caçando por mulheres e crianças. Essa pode ser uma das razões para que os pais mandem seus filhos ficarem longe da floresta",
},
    {
    "onGameId": None,
    "card_id": "39",
    "card_name": "Verdadeira Árvore da vida",
    "card_image": "assets/images/cards/39.png",
    "card_type": "monster effect",
    "card_element": "dendro",
    "card_attack": 0,
    "card_def": 0,
    "card_cust": 0,
    "card_effect": None,
    "card_description": "Condição: Essa carta só pode ser invocada sacrificando 3 cartas do tipo dendro. O poder dessa carta será definido pela soma do poder de todas essas cartas.",
},
    {
    "onGameId": None,
    "card_id": "40",
    "card_name": "Cabeça de Martelo",
    "card_image": "assets/images/cards/40.png",
    "card_type": "monster",
    "card_element": "hydro",
    "card_attack": 20,
    "card_def": 15,
    "card_cust": 2,
    "card_effect": None,
    "card_description": "Assassino nato dos mares, sente o cheiro de sangue a quilômetros mas só enxerga oque está nos dois lados.",
},
    {
    "onGameId": None,
    "card_id": "41",
    "card_name": "Dukleos",
    "card_image": "assets/images/cards/41.png",
    "card_type": "monster",
    "card_element": "hydro",
    "card_attack": 40,
    "card_def": 20,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Criatura que vive nas profundezas dos oceanos, com sua aparência e forma perfeitas para viver nas profundezas das trevas.",
},
    {
    "onGameId": None,
    "card_id": "42",
    "card_name": "Azuli dos mares",
    "card_image": "assets/images/cards/42.png",
    "card_type": "monster",
    "card_element": "hydro",
    "card_attack": 20,
    "card_def": 20,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Sobe as ordens da rainha dos oceanos protege os mares de pescadores e seres mal intencionados.",
},
    {
    "onGameId": None,
    "card_id": "43",
    "card_name": "Nagi, A aprendiz",
    "card_image": "assets/images/cards/43.png",
    "card_type": "monster effect",
    "card_element": "hydro",
    "card_attack": 30,
    "card_def": 15,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Furto de Mana: A cada rodada furta para si +1 de mana do adversário.",
},
    {
    "onGameId": None,
    "card_id": "44",
    "card_name": "Herói das Ondas",
    "card_image": "assets/images/cards/44.png",
    "card_type": "monster effect",
    "card_element": "hydro",
    "card_attack": 40,
    "card_def": 30,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Zona: Para cada carta hydro em seu cemitério essa carta ganha 3 de ataque e perde 1 de defesa",
},
    {
    "onGameId": None,
    "card_id": "45",
    "card_name": "Bubble Elf",
    "card_image": "assets/images/cards/45.png",
    "card_type": "monster effect",
    "card_element": "hydro",
    "card_attack": 30,
    "card_def": 15,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Bolha: A cada round adversário pode imobilizar o ataque de qualquer criatura inimiga.",
},
    {
    "onGameId": None,
    "card_id": "46",
    "card_name": "Mãe dos Mares",
    "card_image": "assets/images/cards/46.png",
    "card_type": "monster effect",
    "card_element": "hydro",
    "card_attack": 35,
    "card_def": 20,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Maldição: Quando invocada, está carta trás um Azuli dos Mares para o campo de batalha.",
},
    {
    "onGameId": None,
    "card_id": "47",
    "card_name": "Hydromera",
    "card_image": "assets/images/cards/47.png",
    "card_type": "monster",
    "card_element": "hydro",
    "card_attack": 40,
    "card_def": 20,
    "card_cust": 10,
    "card_effect": None,
    "card_description": "Reza a lenda que uma mulher foi colocada sob uma maldição e se transformou nessa criatura terrível. Pescadores contam que em alto mar é possível ouvir os gritos desse monstro.",
},
    {
    "onGameId": None,
    "card_id": "48",
    "card_name": "Bekilusteus",
    "card_image": "assets/images/cards/48.png",
    "card_type": "monster",
    "card_element": "hydro",
    "card_attack": 25,
    "card_def": 10,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Dominam os oceanos com sua fome e suas características predatórias, devorando esse bioma de cima a baixo.",
},
    {
    "onGameId": None,
    "card_id": "49",
    "card_name": "Enchanter of the seas",
    "card_image": "assets/images/cards/49.png",
    "card_type": "monster",
    "card_element": "hydro",
    "card_attack": 20,
    "card_def": 15,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Enchanter: Com sua beleza atraí os homens em alto mar, os levando para sua própria perdição. Cartas com 4 de mana ou menos perdem seu poder de ataque e defesa pela metade por 2 rounds.",
},
    {
    "onGameId": None,
    "card_id": "50",
    "card_name": "Fire Golem",
    "card_image": "assets/images/cards/50.png",
    "card_type": "monster",
    "card_element": "pyro",
    "card_attack": 20,
    "card_def": 10,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Essas criaturas habitam ao redor de vulcões e queimam qualquer coisa que encontram na sua frente.",
},
    {
    "onGameId": None,
    "card_id": "51",
    "card_name": "Hell Viper´s",
    "card_image": "assets/images/cards/51.png",
    "card_type": "monster",
    "card_element": "pyro",
    "card_attack": 15,
    "card_def": 10,
    "card_cust": 2,
    "card_effect": None,
    "card_description": "Víboras raivosas que foram amaldiçoadas, quando se sentem ameaçadas transformam sua própria pele em chamas.",
},
    {
    "onGameId": None,
    "card_id": "52",
    "card_name": "Hell Bird´s",
    "card_image": "assets/images/cards/52.png",
    "card_type": "monster",
    "card_element": "pyro",
    "card_attack": 20,
    "card_def": 10,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Criaturas aéreas que queimam como brasas. Dizem que são descendentes da grande fênix.",
},
    {
    "onGameId": None,
    "card_id": "53",
    "card_name": "Hell Blade",
    "card_image": "assets/images/cards/53.png",
    "card_type": "monster effect",
    "card_element": "pyro",
    "card_attack": 25,
    "card_def": 15,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Brasa: Quando atacar reduz o poder do inimigo em 10",
},

    {
    "onGameId": None,
    "card_id": "57",
    "card_name": "El Tigre",
    "card_image": "assets/images/cards/57.png",
    "card_type": "monster effect",
    "card_element": "pyro",
    "card_attack": 35,
    "card_def": 25,
    "card_cust": 6,
    "card_effect": None,
    "card_description": "Maniaco: Para cada criatura de fogo em campo aumenta seu poder de ataque em +7 e defesa em +3.",
},
    {
    "onGameId": None,
    "card_id": "58",
    "card_name": "Masashi Akuma",
    "card_image": "assets/images/cards/58.png",
    "card_type": "monster effect",
    "card_element": "pyro",
    "card_attack": 30,
    "card_def": 20,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Manejo Duplo: Essa cara é capaz de atacar duas vezes.",
},
    {
    "onGameId": None,
    "card_id": "59",
    "card_name": "Worm´s Hell",
    "card_image": "assets/images/cards/59.png",
    "card_type": "monster",
    "card_element": "pyro",
    "card_attack": 15,
    "card_def": 15,
    "card_cust": 2,
    "card_effect": None,
    "card_description": "Surgem da terra em busca de alimento surpreendendo e incinerando suas pressas. Pelo menos não comem nada cru.",
},
    {
    "onGameId": None,
    "card_id": "60",
    "card_name": "Maldição do incapaz",
    "card_image": "assets/images/cards/60.png",
    "card_type": "trap",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Bloqueio: bloqueia uma carta do adversario por 2 rounds",
},
    {
    "onGameId": None,
    "card_id": "61",
    "card_name": "Julgamento do mestre",
    "card_image": "assets/images/cards/61.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Aniquilação: Destrói qualquer carta da arena",
},
    {
    "onGameId": None,
    "card_id": "62",
    "card_name": "Ruína das lâminas",
    "card_image": "assets/images/cards/62.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Gume: Aflige feridas dolorosas na carta adversária diminuindo o Poder de ataque da carta em -15",
},
    {
    "onGameId": None,
    "card_id": "63",
    "card_name": "Agouro Elemental",
    "card_image": "assets/images/cards/63.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Agouro: Quando usada essa carta aumenta em 15 o poder de ataque e 10 o de defesa de qualquer carta em seu campo. ",
},
    {
    "onGameId": None,
    "card_id": "64",
    "card_name": "Agouro Elemental Reforçado",
    "card_image": "assets/images/cards/64.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Agouro: Quando usada essa carta aumenta em +25 o poder de ataque e +15 o de defesa de qualquer carta em seu campo.",
},
    {
    "onGameId": None,
    "card_id": "65",
    "card_name": "Lamento do Mago",
    "card_image": "assets/images/cards/65.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 7,
    "card_effect": None,
    "card_description": "Maldição: Quando ativado retira 15 de ataque dos monstros inimigos por duas rodadas, sacrificando 25 do seus pontos de vida.",
},
    {
    "onGameId": None,
    "card_id": "66",
    "card_name": "Flecha do arcanjo",
    "card_image": "assets/images/cards/66.png",
    "card_type": "trap",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Reverter: Durante o ataque do oponente pode trocar os ataques de um monstro seu pelo monstro atacante",
},
    {
    "onGameId": None,
    "card_id": "67",
    "card_name": "Açoito Premeditado",
    "card_image": "assets/images/cards/67.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Açougue: Retira o poder de ataque e defesa de qualquer carta da arena por um round.",
},
    {
    "onGameId": None,
    "card_id": "68",
    "card_name": "Rhapsody Arcano",
    "card_image": "assets/images/cards/68.png",
    "card_type": "trap",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 8,
    "card_effect": None,
    "card_description": "Alado: Bloqueia o ataque da carta adversária e ataca imediatamente está carta com o poder dobrado de seu ataque.",
},
    {
    "onGameId": None,
    "card_id": "69",
    "card_name": "Dissasper Coin",
    "card_image": "assets/images/cards/69.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Maldição: Reduz o poder de ataque e defesa de uma carta do oponente em 15 por uma rodada.",
},
    {
    "onGameId": None,
    "card_id": "70",
    "card_name": "Clock Command",
    "card_image": "assets/images/cards/70.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Relógio: Nega qualquer ação do adversário, não permitindo que jogue por uma rodada.",
},
    {
    "onGameId": None,
    "card_id": "71",
    "card_name": "Contrato: sangue por sangue",
    "card_image": "assets/images/cards/71.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Trato: Enquanto essa carta estiver em campo você e adversario perdem 70 de vida no inicio de cada rodada.",
},
    {
    "onGameId": None,
    "card_id": "72",
    "card_name": "Força da Natureza",
    "card_image": "assets/images/cards/72.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 3,
    "card_effect": None,
    "card_description": "Bensão: lhe concede 125 pontos de vida.",
},
    {
    "onGameId": None,
    "card_id": "73",
    "card_name": "Elemental Return",
    "card_image": "assets/images/cards/73.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Renascer: Traz para arena um monstro elemental do seu cemitério",
},
    {
    "onGameId": None,
    "card_id": "74",
    "card_name": "Chamado do Cavaleiro",
    "card_image": "assets/images/cards/74.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 4,
    "card_effect": None,
    "card_description": "Renascer: Retira uma carta do tipo Knight do cemitério e a envia para a arena.",
},
    {
    "onGameId": None,
    "card_id": "75",
    "card_name": "Last Whisper",
    "card_image": "assets/images/cards/75.png",
    "card_type": "trap",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Foice: Rouba uma carta aleatória da mão do adversário e coloca em sua arena até o fim do seu round de ataque, após isso a carta é destruída e enviada ao cemitério inimigo.",
},
    {
    "onGameId": None,
    "card_id": "76",
    "card_name": "Cristal Queen",
    "card_image": "assets/images/cards/76.png",
    "card_type": "spell",
    "card_element": None,
    "card_attack": None,
    "card_def": None,
    "card_cust": 5,
    "card_effect": None,
    "card_description": "Acorrentado: Ao custo de 150 dos seus pontos de vida esta carta zera o poder de ataque e defesa de qualquer carta do oponente, enquanto estiver em campo",
},
]
