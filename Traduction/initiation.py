# alignement mot a mot
SourceWLexicon = {}
TargetWLexicon = {}
# alignement inverse ident vers mot
RSourceWLexicon = {}
RTargetWLexicon = {}


def trans(file_path, lexicon, rlexicon, ident):
    with open(file_path, 'r') as fichier:
        for line in fichier:
            mots = line.split()
            for mot in mots:
                cle = mot.lower()
                if cle not in lexicon:
                    lexicon[cle] = ident
                    rlexicon[ident] = cle
                    ident += 1
    fichier.close()


def map_mot_ident(source_file, target_file):
    ident = 0
    trans(source_file, SourceWLexicon, RSourceWLexicon, ident)
    ident = 0
    trans(target_file, TargetWLexicon, RTargetWLexicon, ident)


SOURCE_PATH = 'data/CL___en.txt'
TARGET_PATH = 'data/CL___fr.txt'
map_mot_ident(SOURCE_PATH, TARGET_PATH)
print "\n  - Representation de mots SOURCE en ident :"
print SourceWLexicon
print "\n        ########################## \n \n - Representation de mots CIBLE en ident "
print TargetWLexicon
raw_input()



