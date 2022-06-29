import os
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.messagebox import askokcancel, showinfo, WARNING


def get_language_name(lang_code):
	lang_dict = {
	"AAR": "Afar",
	"ABK": "Abkhazian",
	"ACE": "Achinese (Aceh)",
	"ACH": "Acoli",
	"ADA": "Adangme",
	"ADY": "Adyghe; Adygei",
	"AFA": "Afro-Asiatic (Other)",
	"AFH": "Afrihili",
	"AFR": "Afrikaans",
	"AIN": "Ainu",
	"AKA": "Akan",
	"AKK": "Akkadian (Babylonian)",
	"ALB": "Albanian",
	"ALE": "Aleut",
	"ALG": "Algonquian languages",
	"ALT": "Southern Altai",
	"AMH": "Amharic",
	"ANG": "English-Old (ca.450-1100)",
	"ANP": "Angika",
	"APA": "Apache languages",
	"ARA": "Arabic",
	"ARC": "Aramaic (Syria)",
	"ARG": "Aragonese",
	"ARM": "Armenian (Hayeren)",
	"ARN": "Araucanian (S. Central Chile)",
	"ARP": "Arapaho",
	"ART": "Artificial (Other)",
	"ARW": "Arawak",
	"ASM": "Assamese (Indo-Iranian sub family)",
	"AST": "Asturian-Bable-Leonese-Asturleonese",
	"ATH": "Athapascan languages",
	"AUS": "Australianl anguages",
	"AVA": "Avaric",
	"AVE": "Avestan",
	"AWA": "Awadhi",
	"AYM": "Aymara",
	"AZE": "Azerbaijani (Azeri)",
	"BAD": "Banda",
	"BAI": "Bamileke languages",
	"BAK": "Bashkir",
	"BAL": "Baluchi",
	"BAM": "Bambara",
	"BAN": "Balinese",
	"BAQ": "Basque",
	"BAS": "Basa",
	"BAT": "Baltic (Other)",
	"BEJ": "Beja",
	"BEL": "Belarussian",
	"BEM": "Bemba",
	"BEN": "Bengali (Bangla)",
	"BER": "Berber (Other)",
	"BHO": "Bhojpuri",
	"BIH": "Bihari",
	"BIK": "Bikol",
	"BIN": "Bini",
	"BIS": "Bislama",
	"BLA": "Siksika (Blackfoot)",
	"BNT": "Bantu (Other)",
	"BOS": "Bosnian",
	"BRA": "Braj",
	"BRE": "Breton (Brez)",
	"BTK": "Batak (Indonesia)",
	"BUA": "Buriat",
	"BUG": "Buginese (Bugi)",
	"BUL": "Bulgarian",
	"BUR": "Burmese (Myanmasa)",
	"BYN": "Blin; Bilin",
	"CAD": "Caddo",
	"CAI": "Central American Indian (Oth.)",
	"CAK": "Cakchiquel, Kaqchikel",
	"CAR": "Carib",
	"CAT": "Catalan",
	"CAU": "Caucasian (Other)",
	"CEB": "Cebuano",
	"CEL": "Celtic (Other)",
	"CHA": "Chamorro",
	"CHB": "Chibcha",
	"CHE": "Chechen",
	"CHG": "Chagatai",
	"CHI": "Chinese (Zhongwen)",
	"CHK": "Chuukese",
	"CHM": "Mari",
	"CHN": "Chinookjargon",
	"CHO": "Choctaw",
	"CHP": "Chipewyan",
	"CHR": "Cherokee",
	"CHU": "Church Slavic",
	"CHV": "Chuvash",
	"CHY": "Cheyenne",
	"CJS": "Shor",
	"CMC": "Chamic languages",
	"CMN": "Mandarin Dialect",
	"CNR": "Montenegrin",
	"COP": "Coptic",
	"COR": "Cornish",
	"COS": "Corsican",
	"CPE": "Creoles and pidgins-English-based (Other)",
	"CPF": "Creoles and pidgins-French-based (Other)",
	"CPP": "Creoles and pidgins-Portuguese-based (Other)",
	"CRE": "Cree",
	"CRH": "Crimean Tatar; Crimean Turkish",
	"CRP": "Creoles and pidgins (Other)",
	"CSB": "Kashubian",
	"CUS": "Cushitic (Other)",
	"CZE": "Czech",
	"DAK": "Dakota",
	"DAN": "Danish",
	"DAR": "Dargwa",
	"DAY": "Dayak",
	"DEL": "Delaware",
	"DEN": "Slave (Athapascan)",
	"DGR": "Dogrib",
	"DIN": "Dinka",
	"DIV": "Divehi (Maldives)",
	"DJC": "Dar Daju Daju",
	"DOI": "Dogri",
	"DRA": "Dravidian (Other)",
	"DSB": "Lower Sorbian",
	"DUA": "Duala",
	"DUM": "Dutch-Middle (ca.1050-1350)",
	"DUT": "Dutch",
	"DYU": "Dyula",
	"DZO": "Dzongkha (Bhutani)",
	"EFI": "Efik",
	"EGY": "Egyptian (Ancient)",
	"EKA": "Ekajuk",
	"ELX": "Elamite",
	"ENG": "English",
	"ENM": "English-Middle (1100-1500)",
	"EPO": "Esperanto",
	"EST": "Estonian (Eesti)",
	"EWE": "Ewe",
	"EWO": "Ewondo",
	"FAN": "Fang",
	"FAO": "Faroese (Faeroese Island)",
	"FAT": "Fanti",
	"FIJ": "Fijian",
	"FIL": "Filipino; Pilipino",
	"FIN": "Finnish (Suomi)",
	"FIU": "Finno-Ugrian",
	"FNG": "Fanagalo",
	"FON": "Fon",
	"FRE": "French",
	"FRM": "French-Middle (ca.1400-1600)",
	"FRO": "French-Old (ca.842-1400)",
	"FRR": "Northern Frisian",
	"FRS": "Eastern Frisian",
	"FRY": "Frisian (Frysk)",
	"FUL": "Fulah",
	"FUR": "Friulian",
	"GAA": "Ga",
	"GAY": "Gayo",
	"GBA": "Gbaya",
	"GEM": "Germanic (Other)",
	"GEO": "Georgian (Kartuli)",
	"GER": "German",
	"GEZ": "Geez",
	"GIL": "Gilbertese (Kiribati)",
	"GLA": "Gaelic (Scots)",
	"GLE": "Irish",
	"GLG": "Gallegan (Galician-Galego)",
	"GLV": "Manx",
	"GMH": "German-Middle High (ca.1050-1500)",
	"GOH": "German-Old High (ca.750-1050)",
	"GON": "Gondi",
	"GOR": "Gorontalo",
	"GOT": "Gothic",
	"GRB": "Grebo",
	"GRC": "Greek-Ancient (to1453)",
	"GRE": "Greek-Modern (1453-)(Ellinika)",
	"GRN": "Guarani",
	"GSW": "Swiss German",
	"GUJ": "Gujarati",
	"GWI": "Gwich'in",
	"HAI": "Haida",
	"HAT": "Haitian; Haitian Creole",
	"HAU": "Hausa (Nigeria)",
	"HAW": "Hawaiian",
	"HAZ": "Hazaragi",
	"HBS": "Serbo-Croatian",
	"HEB": "Hebrew (Iwrith)",
	"HER": "Herero (Namibia)",
	"HIL": "Hiligaynon",
	"HIM": "Himachali",
	"HIN": "Hindi",
	"HIT": "Hittite",
	"HMN": "Hmong",
	"HMO": "HiriMotu",
	"HRV": "Croatian",
	"HSB": "Upper Sorbian",
	"HUN": "Hungarian (Magyar)",
	"HUP": "Hupa",
	"IBA": "Iban",
	"IBO": "Igbo",
	"ICE": "Icelandic",
	"IDO": "Ido",
	"III": "Sichuan Yi; Nuosu",
	"IJO": "Ijo",
	"IKU": "Inuktitut",
	"ILE": "Interlingue",
	"ILO": "Iloko",
	"INA": "Interlingua",
	"INC": "Indic (Other)",
	"IND": "Indonesian",
	"INE": "Indo-European (Other)",
	"INH": "Ingush",
	"IPK": "Inupiak",
	"IRA": "Iranian (Other)",
	"IRO": "Iroquoian languages",
	"ITA": "Italian",
	"JAV": "Javanese",
	"JBO": "Lojban",
	"JPN": "Japanese (Nihongo)",
	"JPR": "Judeo-Persian",
	"JRB": "Judeo-Arabic",
	"KAA": "Kara-Kalpak",
	"KAB": "Kabyle",
	"KAC": "Kachin",
	"KAL": "Kalaallisut",
	"KAM": "Kamba",
	"KAN": "Kannada",
	"KAR": "Karen",
	"KAS": "Kashmiri",
	"KAU": "Kanuri",
	"KAW": "Kawi",
	"KAZ": "Kazakh",
	"KBD": "Kabardian",
	"KEA": "Kabuverdianu",
	"KHA": "Khasi",
	"KHI": "Khoisan (Other)",
	"KHM": "Khmer (Cambodian)",
	"KHO": "Khotanese (or Saka-EastIranian)",
	"KIK": "Kikuyu (Northern Kenya)",
	"KIN": "Kinyarwanda (Rwanda)",
	"KIR": "Kirghiz",
	"KLS": "Kalasha",
	"KMB": "Kimbundu",
	"KOK": "Konkani",
	"KOM": "Komi",
	"KON": "Kongo",
	"KOR": "Korean",
	"KOS": "Kosraean",
	"KPE": "Kpelle",
	"KRC": "Karachay-Balkar",
	"KRL": "Karelian",
	"KRO": "Kru",
	"KRU": "Kurukh",
	"KUA": "Kuanyama",
	"KUM": "Kumyk",
	"KUR": "Kurdish",
	"KUT": "Kutenai",
	"LAD": "Ladino",
	"LAH": "Lahnda",
	"LAM": "Lamba",
	"LAO": "Lao",
	"LAT": "Latin",
	"LAV": "Latvian (lettish-letonian)",
	"LBJ": "Ladakhi",
	"LEZ": "Lezghian",
	"LIM": "Limburgan; Limburger; Limburgish",
	"LIN": "Lingala",
	"LIT": "Lithuanian",
	"LKT": "Lakota",
	"LOL": "Mongo",
	"LOZ": "Lozi",
	"LTZ": "Letzeburgesch",
	"LUA": "Luba-Lulua",
	"LUB": "Luba-Katanga",
	"LUG": "Ganda (or Baganda-Uganda)",
	"LUI": "Luiseno",
	"LUN": "Lunda",
	"LUO": "Luo",
	"LUS": "Lushai",
	"MAC": "Macedonian",
	"MAD": "Madurese",
	"MAG": "Magahi",
	"MAH": "Marshall",
	"MAI": "Maithili",
	"MAK": "Makasar",
	"MAL": "Malayalam",
	"MAN": "Mandingo",
	"MAO": "Maori",
	"MAP": "Austronesian (Other-Malayo-Polynesian)",
	"MAR": "Marathi",
	"MAS": "Masai",
	"MAY": "Malay",
	"MDF": "Moksha",
	"MDR": "Mandar",
	"MEN": "Mende",
	"MEY": "Hassaniyya",
	"MGA": "Irish-Middle (900-1200)",
	"MIC": "Micmac",
	"MIN": "Minangkabau",
	"MIS": "Miscellaneous languages",
	"MKH": "Mon-Khmer (Other)",
	"MLG": "Malagasy",
	"MLT": "Maltese",
	"MNC": "Manchu",
	"MNI": "Manipuri",
	"MNO": "Manobo languages",
	"MOH": "Mohawk",
	"MOL": "Moldavian",
	"MON": "Mongolian",
	"MOS": "Mossi (More)",
	"MUL": "Multiple languages",
	"MUN": "Mundal anguages",
	"MUS": "Creek (Muskogee)",
	"MWL": "Mirandese",
	"MWR": "Marwari",
	"MYN": "Mayan languages",
	"MYV": "Erzya",
	"NAH": "Aztec (Nahuatl)",
	"NAI": "North American Indian (Other)",
	"NAP": "Neapolitan",
	"NAQ": "Khoekhoe, Nama",
	"NAU": "Nauru",
	"NAV": "Navajo",
	"NBL": "Ndebele-South",
	"NDE": "Ndebele-North",
	"NDO": "Ndonga",
	"NDS": "Low German; Low Saxon; German, Low; Saxon, Low",
	"NEP": "Nepali",
	"NEW": "Newari",
	"NIA": "Nias",
	"NIC": "Niger-Kordofanian (Other)",
	"NIU": "Niuean",
	"NNO": "Norwegian Nynorsk; Nynorsk, Norwegian",
	"NOB": "Bokmål, Norwegian; Norwegian Bokmål",
	"NOD": "Northern Thai",
	"NOG": "Nogai",
	"NON": "Norse-Old",
	"NOR": "Norwegian",
	"NQO": "N'Ko",
	"NSO": "Sohto-Northern",
	"NUB": "Nubian languages",
	"NWC": "Classical Newari; Old Newari; Classical Nepal Bhasa",
	"NYA": "Nyanja",
	"NYM": "Nyamwezi",
	"NYN": "Nyankole",
	"NYO": "Nyoro",
	"NZI": "Nzima",
	"OCI": "Occitan (post1500)",
	"OJI": "Ojibwa",
	"ORI": "Oriya",
	"ORM": "Oromo (Galla or Afan)",
	"OSA": "Osage",
	"OSS": "Ossetic",
	"OTA": "Turkish-Ottoman (1500-1928)",
	"OTO": "Otomian languages",
	"PAA": "Papuan(Other)",
	"PAG": "Pangasinan",
	"PAL": "Pahlavi",
	"PAM": "Pampanga",
	"PAN": "Panjabi ",
	"PAP": "Papiamento",
	"PAU": "Palauan",
	"PEO": "Persian-Old (ca.600-400B.C.)",
	"PER": "Persian (Farsi)",
	"PEZ": "Eastern Penan",
	"PHI": "Philippine (Other)",
	"PHN": "Phoenician",
	"PLI": "Pali",
	"POL": "Polish",
	"PON": "Pohnpeian",
	"POR": "Portuguese",
	"PRA": "Prakrit languages",
	"PRO": "Provencal-Old (to 1500)",
	"PRS": "Afghan Persian, Dari",
	"PUS": "Pushto (or Pachto-Afghan)",
	"QSI": "Silent Film",
	"QUE": "Quechua",
	"RAJ": "Rajasthani",
	"RAP": "Rapanui",
	"RAR": "Rarotongan",
	"RCF": "Réunion Creole French",
	"ROA": "Romance (Other)",
	"ROH": "Raeto-Romance",
	"ROM": "Romany",
	"RUM": "Romanian",
	"RUN": "Rundi (or Kirundi)",
	"RUP": "Aromanian; Arumanian; Macedo-Romanian",
	"RUS": "Russian",
	"RUY": "Central Okinawan",
	"SAD": "Sandawe",
	"SAG": "Sango",
	"SAH": "Yakut",
	"SAI": "South American Indian (Other)",
	"SAL": "Salishan languages",
	"SAM": "Samaritan Aramaic",
	"SAN": "Sanskrit",
	"SAS": "Sasak",
	"SAT": "Santali",
	"SCN": "Sicilian",
	"SCO": "Scots",
	"SEL": "Selkup",
	"SEM": "Semitic (Other)",
	"SGA": "Irish-Old (to 900)",
	"SGN": "Sign Languages",
	"SHN": "Shan",
	"SID": "Sidamo",
	"SIN": "Sinhalese",
	"SIO": "Siouan languages",
	"SIT": "Sino-Tibetan (Other)",
	"SLA": "Slavic (Other)",
	"SLO": "Slovak",
	"SLV": "Slovenian",
	"SMA": "Southern Sami",
	"SME": "Northern Sami",
	"SMI": "Sami languages",
	"SMJ": "Lule Sami",
	"SMN": "Inari Sami",
	"SMO": "Samoan",
	"SMS": "Skolt Sami",
	"SNA": "Shona",
	"SND": "Sindhi",
	"SNK": "Soninke",
	"SOG": "Sogdian",
	"SOM": "Somali",
	"SON": "Songhai",
	"SOT": "Sotho",
	"SPA": "Spanish",
	"SRD": "Sardinian",
	"SRN": "Sranan Tongo",
	"SRP": "Serbian",
	"SRR": "Serer",
	"SSA": "Nilo-Saharan (Other)",
	"SSW": "Swati (Siswant-Siswati)",
	"SUK": "Sukuma",
	"SUN": "Sundanese",
	"SUS": "Susu(Guinea)",
	"SUX": "Sumerian",
	"SWA": "Swahili",
	"SWE": "Swedish",
	"SYC": "Classical Syriac",
	"SYR": "Syriac",
	"TAH": "Tahitian",
	"TAI": "Tai (Other)",
	"TAM": "Tamil",
	"TAT": "Tatar",
	"TEL": "Telugu",
	"TEM": "Timne",
	"TER": "Tereno",
	"TET": "Tetum",
	"TGK": "Tajik",
	"TGL": "Tagalog",
	"THA": "Thai",
	"TIB": "Tibetan (Bodskad)",
	"TIG": "Tigre",
	"TIR": "Tigrinya",
	"TIV": "Tiv",
	"TKL": "Tokelau",
	"TLH": "Klingon; tlh Ingan-Hol",
	"TLI": "Tlingit",
	"TMH": "Tamashek",
	"TOG": "Tonga (Nyasa)",
	"TON": "Tonga (Tonga Islands)",
	"TPI": "Tok Pisin",
	"TSI": "Tsimshian",
	"TSN": "Tswana (Setswana)",
	"TSO": "Tsonga",
	"TUK": "Turkmen",
	"TUM": "Tumbuka",
	"TUP": "Tupi languages",
	"TUR": "Turkish",
	"TUT": "Altaic (Other)",
	"TVL": "Tuvalu",
	"TWI": "Twi",
	"TYV": "Tuvinian",
	"UDM": "Udmurt",
	"UGA": "Ugaritic",
	"UIG": "Uighur",
	"UKR": "Ukrainian",
	"UMB": "Umbundu",
	"UND": "Undetermined",
	"URD": "Urdu",
	"UZB": "Uzbek",
	"VAI": "Vai",
	"VEN": "Venda",
	"VIE": "Vietnamese",
	"VOL": "Volapuk",
	"VOT": "Votic",
	"WAK": "Wakashan languages",
	"WAL": "Walamo",
	"WAR": "Waray",
	"WAS": "Washo",
	"WEL": "Welsh",
	"WEN": "Sorbian languages",
	"WLN": "Walloon",
	"WOD": "Wolani",
	"WOL": "Wolof",
	"XAL": "Kalmyk; Oirat",
	"XCA": "Cantonese",
	"XCH": "Chadic",
	"XCI": "Swiss Italian dialect",
	"XCS": "Caspian",
	"XHO": "Xhosa",
	"XLA": "Laz",
	"XPY": "Pygmies language",
	"XWA": "Wallon",
	"YAO": "Yao",
	"YAP": "Yapese",
	"YID": "Yiddish",
	"YOR": "Yoruba",
	"YPK": "Yupik languages",
	"ZAP": "Zapotec",
	"ZBL": "Blissymbols",
	"ZEN": "Zenaga",
	"ZGH": "Standard Moroccan Tamazight",
	"ZHA": "Zhuang",
	"ZND": "Zande",
	"ZUL": "Zulu",
	"ZUN": "Zuni",
	"ZZA": "Zaza; Dimili; Dimli; Kirdki; Kirmanjki; Zazaki"
	}
	lang_fullname = lang_dict.get( lang_code.upper() )
	return lang_fullname

def createSubjectTags(searchzut, fieldnamesfromfile):
	# determine the 
	# of subjects (if 1 in searchzut, then 
	# find equivalent subject name filenamesfromfile
	
	t = '\n\t<subject>'
	subject_list = []
	for cnt in range(0, len(searchzut)):
		#print("TESTing subjects - cnt = ",cnt, ' fieldnamesfromfile[cnt]',fieldnamesfromfile[cnt])
		#print("searchzut[cnt] = ", searchzut[cnt])
		x = searchzut[cnt]
		if x == 1:
			x = fieldnamesfromfile[cnt].replace("_", " ")
			subject_list.append(x)
	
	for i in range(0, len(subject_list)):
		t += "\n\t\t<part>" + subject_list[i] + "</part>"
	t += '\n\t</subject>'
	return t

def createLanguageTags(lang_string):
	lang_list = lang_string.split()
	lang_str = ""
	for i in range(0, len(lang_list)):
		l = lang_list[i].strip()
		full_name = get_language_name( l )
		lang_str += "\n\t\t<language langcode=' "+l+" '>"+str(full_name)+"</language>"
	return lang_str
	

def createEAD(fieldnamesfromfile, searchzut):
	# constants for names
	MAINAGENCYCODE = 0
	TITLE_PROPER_ORG_OR_PERSON = 1
	SUBTITLE = 2
	AUTHOR = 3
	SPONSOR = 4
	PUBLISHER = 5
	ADDRESSLINE = 6
	NAME_OF_COLLECTION = 7
	ENCODED_BY = 8
	PUBLISHER  = 9
	LANGUAGES = 10
	PREFER_CITE = 11
	PHYSICAL_LOCATION_YOUR_URL = 12
	YOUR_CONTACT_URL = 13
	
	# -------------- from current script - take the webpage name and make as .xml
	#eadPageName = "EAD_TESTO.xml"
	#searchzut = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	#fieldnamesfromfile =  ['Bluebeard', 'David_Lawrence', 'Esek_Hopkins', 'John_Paul_Jones', 'Sloop_Gaspée', 'USS_Congress', 'USS_Constitution', 'USS_President', 'Bangor', 'Bar_Harbor', 'Bath', 'Boothbay', 'Calais', 'Camden', 'Cutler', 'Georges_Banks', 'Grand_Banks', 'Isle_au_Haut', 'Kennebunkport', 'Limestone', 'Portland', 'Rockport', 'Saco', 'Seaports', 'Searsport', 'Winter', 'Yarmouth', 'Other_Harbor', 'Aircraft_Carrier', 'Amphibious', 'Barque', 'Barquentine', 'Batteau', 'Battleship', 'Blockade_runner', 'Brig', 'Brigantine', 'Catboat', 'Catamaran', 'Clipper', 'Coastal_defense_ship', 'Collier', 'Corvette', 'Cruise_ship', 'Cruiser', 'Destroyer', 'Dinghy', 'Dory', 'Fire_ship', 'Ferry', 'Frigate', 'Full_rigged_ship', 'Galliot', 'Gunboat', 'Indiaman', 'Ironclad', 'Landing_Ship', 'Liberty_ship', 'Lifeboat', 'Littoral', 'Lobster_Boat', 'Longship', 'Man_of_war', 'Merchant_raider', 'Merchantman', 'Military_ship', 'Monitor', 'Motor_vessel', 'Ocean_liner', 'Packet', 'Paddle_steamer', 'Pinnace', 'Pram', 'Royal_Mail_Ship', 'Schooner', 'Settee', 'Shallop', 'Ship_of_the_line', 'Slave_ship', 'Sloop', 'Snow', 'Steamship', 'Tramp_steamer', 'Troopship', 'Victory_ship', 'Whaler', 'Yacht', 'Boatswain', 'Capitan', 'Chandlers', 'Crew', 'Fisherman', 'Flag_Officer', 'Flags', 'Gunner', 'Lieutenant', 'Lobsterman', 'Longshoreman', 'Midshipman', 'Pilot', 'Other_Crew']
	
	
	# ---------------------------------------- construct the EAD .xml file.
	eadpageTitle = simpledialog.askstring(title="Title", prompt="EAD - Please name your EAD file.")
	
	if eadpageTitle == "":
		eadpageTitle = "Demo EAD"
	else:
		eadpageTitle = eadpageTitle.translate({ord(ch):'_' for ch in "?/: @#$%^&*()=≠±+-'‘’"})

	eadpageTitle =  eadpageTitle + ".ead"
	

	# get eadinfo_from file
	ead_profile_demo_file = "output_profile_and_templates/ead_profile_demo.txt"
	with open(ead_profile_demo_file, 'r') as f:
		ead_data = f.readlines()  # creates a list of the above data
	ead_data = [x.strip() for x in ead_data]
	
	
	# prepare EAD string
	ead_str = '<ead> '+\
	'\n\t<eadheader audience="internal" countryencoding="iso3166-1" '+\
	'\n\tdateencoding="iso8601" langencoding="iso639-2"  '+\
	'\n\trepositoryencoding="iso15511"> '+\
	'\n\t<eadid countrycode="us" mainagencycode=\" '+(ead_data[MAINAGENCYCODE]).strip()+' \">'+\
	'\n\t' + eadpageTitle +\
	'\n\t</eadid>'+\
	'\n\t<filedesc>'+\
	'\n\t\t	<titlestmt> '+\
	'\n\t\t\t	<titleproper>'+(ead_data[TITLE_PROPER_ORG_OR_PERSON]).strip()+\
	'\n\t\t\t		</titleproper> '+\
	'\n\t\t		<subtitle>An inventory of '+(ead_data[SUBTITLE]).strip() +'</subtitle> '+\
	'\n\t\t		<author>Finding aid prepared by '+(ead_data[AUTHOR]).strip() +'</author>'+\
	'\n\t\t		<sponsor>'+(ead_data[SPONSOR]).strip() +'</sponsor>'+\
	'\n\t	</titlestmt> '+\
	'\n\t	<publicationstmt>'+\
	'\n\t\t		<publisher encodinganalog="Publisher">'+(ead_data[PUBLISHER]).strip() +'</publlisher>'+\
	'\n\t\t		<address>'+\
	'\n\t\t\t			<addressline>' + (ead_data[ADDRESSLINE]).strip() +'</addressline> '+\
	'\n\t\t		</address> '+\
	'\n\t	</publicationstmt>'+\
	'\n\t	<seriesstmt>'+\
	'\n\t\t		<p>'+(ead_data[NAME_OF_COLLECTION]).strip() +'</p>'+\
	'\n\t	</seriesstmt>'+\
	'\n\t</filedesc> '+\
	'\n\t<profiledesc>'+\
	'\n\t\t	<creation>Finding aid encoded by '+(ead_data[ENCODED_BY]).strip()  +\
	'\n\t\t\t		<date>generatedOnDate</date> '+\
	'\n\t\t	</creation>'+\
	'\n\t\t	<langusage>Finding aid written in'
	
	ead_str += createLanguageTags(ead_data[LANGUAGES])
	
	ead_str +=  '\n\t	</langusage> '+\
	'\n\t</profiledesc>'+\
	'\n\t<revisiondesc>'+\
	'\n\t\t	<change>'+\
	'\n\t\t\t		<date></date>'+\
	'\n\t\t\t		<item>[REASON FOR CHANGE]</item>'+\
	'\n\t\t	</change>'+\
	'\n\t</revisiondesc>'+\
	'\n\t</eadheader> '+\
	'\n\t<archdesc>'+\
	'\n\t<did>'+\
	'\n\t\t	<unitid></unitid> '+\
	'\n\t\t	<repository></repository>'+\
	'\n\t\t	<origination> '+\
	'\n\t\t\t		<corpnane> </corpname> '+\
	'\n\t\t	</origination> '+\
	'\n\t\t	<unittitle> </unittitle>'+\
	'\n\t\t	<unitdate> </unitdate>'+\
	'\n\t\t	<langmaterial> '+\
	'\n\t\t\t		<language>'+\
	'\n\t\t\t		</language> '+\
	'\n\t\t	</langmaterial> '+\
	'\n\t\t	<abstract>[NOTES]</abstract>'+\
	'\n\t\t	<physdesc>Webpage</physdesc>'+\
	'\n\t\t	<physloc>'+ (ead_data[PHYSICAL_LOCATION_YOUR_URL ]).strip() +' </physloc> '+\
	'\n\t</did>'+\
	'\n\t<descgrp type="admininfo"> '+\
	'\n\t\t	<prefercite>'+(ead_data[PREFER_CITE]).strip() + '</prefercite> '+\
	'\n\t\t	<acqinfo></acqinfo>'+\
	'\n\t</descgrp> '+\
	'\n\t<dsc>'+\
	'\n\t<c01></c01> '+\
	'\n\t<did>'+\
	'\n\t\t	<physloc>[FILENAME]</physloc> '+\
	'\n\t\t	<container></container> '+\
	'\n\t\t	<unittitle> </unittitle> '+\
	'\n\t\t	<unitdate> </unitdate> '+\
	'\n\t\t	<physdesc> </physdesc>'+\
	'\n\t</did> '+\
	'\n\t</dsc> '+\
	'\n\t</archdesc>'+\
	'\n\t<controlaccess>'
	
	ead_str += createSubjectTags(searchzut, fieldnamesfromfile)

	ead_str += '\n\t</controlaccess>'+\
	'\n\t<control>'+\
	'\n\t\t	<recordid>[RECNO]</recordid>'+\
	'\n\t\t	<filedesc>'+\
	'\n\t\t\t		<titlestmt>'+\
	'\n\t\t\t			<titleproper>[ some thing tba ]</titleproper>'+\
	'\n\t\t		</titlestmt>'+\
	'\n\t\t		<editionstmt>'+\
	'\n\t\t\t			<edition>1st</edition>'+\
	'\n\t\t			<publicationstmt>'+\
	'\n\t\t\t				<publisher>'+(ead_data[PUBLISHER]).strip() +'</publisher>'+\
	'\n\t\t			<publicationstmt>'+\
	'\n\t	</filedesc>'+\
	'\n\t	<notestmt>'+\
	'\n\t	<controlnote>'+\
	'\n\t\t		<p>Contact information:'+\
	'\n\t\t\t			<ref show="new" actuate="onrequest" href=" '+(ead_data[YOUR_CONTACT_URL]).strip() +'">'+\
	"\n\t\t\t ' " + (ead_data[YOUR_CONTACT_URL]).strip() +"'" +\
	'\n\t\t\t			</ref>'+\
	'\n\t\t		</p>'+\
	'\n\t	</controlnote>'+\
	'\n\t	<controlnote>'+\
	'\n\t\t		<p>Catalog Record:'+\
	'\n\t\t\t			<ref href="" actuate="onrequest" '+\
	'\n\t\t\t			linktitle="MARC record for collection"></ref>'+\
	'\n\t\t		</p>'+\
	'\n\t\t	</controlnote>'+\
	'\n\t	</notestmt>'+\
'\n</ead>'

	#return ead_str

	
	f = open(eadpageTitle, "w")
	f.write(ead_str)
	f.close()
	messagebox.showinfo("Information","Your EAD file is created "+eadpageTitle)
	
	

if __name__ == "__main__":
	createEAD(fieldnamesfromfile, searchzut)
