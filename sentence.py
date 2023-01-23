# sentence.py

# Sentence Class

class Sentence:

    @staticmethod
    def check_null_or_empty(value):
        if (value!=None):
            if (len(value) == 0):
                return "n.d."
            else:
                return str(value)
        else:
            return "n.d."

    def __init__(self): # empty constructor
        self.sentence_ecli = None
        self.sentence_title = None
        self.sentence_type = None
        self.sentence_number = None
        self.tribunal_code = None
        self.tribunal_city = None
        self.tribunal_section = None
        self.recourse_number = None
        self.sentence_url = None
        self.sentence_filename = None
        # pass

    def toString(self):
        # print("Tipo (cig / cig_accordo_quadro_ / numero_gara):", str(self.cig_type))
        # print("cig / cig_accordo_quadro_ / numero_gara numero:", str(self.cig))
        # print("cig anno:",str(self.cig_year))
        # print("cig mese:",str(self.cig_month))
        print("Provvedimento - ECLI:",Sentence.check_null_or_empty(self.sentence_ecli))
        print("Provvedimento - titolo:",Sentence.check_null_or_empty(self.sentence_title))
        print("Provvedimento - tipo:",Sentence.check_null_or_empty(self.sentence_type))
        print("Provvedimento - numero:",Sentence.check_null_or_empty(self.sentence_number))
        print("Trubunale - codice:",Sentence.check_null_or_empty(self.tribunal_code))
        print("Trubunale - citta\':",Sentence.check_null_or_empty(self.tribunal_city))
        print("Trubunale - sezione:",Sentence.check_null_or_empty(self.tribunal_section))
        print("Ricorso - numero:",Sentence.check_null_or_empty(self.recourse_number))
        print("Sentenza - URL:",Sentence.check_null_or_empty(self.sentence_url))
        print("Sentenza - file:",Sentence.check_null_or_empty(self.sentence_filename))

    def toCSV(self):
        # string =  self.cig + ";"  + str(self.cig_type) + ";" + str(self.sentence_ecli) + ";" + str(self.sentence_title) + ";" + str(self.sentence_type) + ";" + str(self.sentence_number) +  ";" + str(self.tribunal_code) + ";" + str(self.tribunal_city) + ";" + str(self.tribunal_section) + ";" + str(self.recourse_number) + ";" + str(self.sentence_url) + ";" + str(self.sentence_filename)
        if (self.sentence_ecli!=None):
            ecli = Sentence.check_null_or_empty(self.sentence_ecli)
        else:
            ecli = "n.d."
        string =  ecli + ";" + Sentence.check_null_or_empty(self.sentence_title) + ";" + Sentence.check_null_or_empty(self.sentence_type) + ";" + Sentence.check_null_or_empty(self.sentence_number) +  ";" + Sentence.check_null_or_empty(self.tribunal_code) + ";" + Sentence.check_null_or_empty(self.tribunal_city) + ";" + Sentence.check_null_or_empty(self.tribunal_section) + ";" + Sentence.check_null_or_empty(self.recourse_number) + ";" + Sentence.check_null_or_empty(self.sentence_url) + ";" + Sentence.check_null_or_empty(self.sentence_filename)
        # "ID (cig, gara, accordo); tipo_ID; anno; mese; codice_ecli; provvedimento_titolo; provvedimento_tipo; sentenza_numero; tribunale_codice; tribunale_citta; tribunale_sezione; ricorso_numero; sentenza_url; sentenza_file"
        return string
