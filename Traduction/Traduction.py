# coding: utf-8
"""  et je vous renouvelle tous mes vux en espérant que vous avez passé de bonnes vacances.
Comme vous avez pu le constater, le grand "bogue de l'an 2000" ne s'est pas produit. En revanche, les citoyens d'un certain nombre de nos pays ont été victimes de catastrophes naturelles qui ont vraiment été terribles.
Vous avez souhaité un débat à ce sujet dans les prochains jours, au cours de cette période de session.


and I would like once again to wish you a happy new year in the hope that you enjoyed a pleasant festive period.
Although, as you will have seen, the dreaded 'millennium bug' failed to materialise, still the people in a number of countries suffered a series of natural disasters that truly were dreadful.
You have requested a debate on this subject in the course of the next few days, during this part-session.
"""


from scipy.stats import entropy
from initiation import SourceWLexicon, TargetWLexicon
from initiation import SOURCE_PATH, TARGET_PATH
import numpy as np


V = len(SourceWLexicon)  # taille de vocabulaire

MatriceProba = np.zeros((2, V, V))  # matrice de probabilite

InitialMatrice = np.zeros((V, V)) # initialisation de la matrice de probabilite
InitialMatrice.fill(1/float(V))


CompteurMatrice = {}  # compteur de la matrice


# une fonction qui retourne une liste des identifiants des mots sources et targets

def MotIdentifie(ligne_source, ligne_cible):
    source_Mots = ligne_source.split()
    target_Mots = ligne_cible.split()
    source_id = [SourceWLexicon[Mot.lower()] for Mot in source_Mots]
    target_id = [TargetWLexicon[Mot.lower()] for Mot in target_Mots]
    return source_id, target_id


def Table_frequence(ligne_source, ligne_cible):
    """ une focntion qui prend la ligne source et la ligne cible comme parametre et 
        retourne la table de frequence concernaant les mots sources et les mots cibles
    """
    source_w = {}
    target_w = {}
    source_id, target_id = MotIdentifie(ligne_source, ligne_cible)
    for ident in source_id:
        source_w[ident] = source_w.get(ident, 0) + 1
    for ident in target_id:
        target_w[ident] = target_w.get(ident, 0) + 1
    return source_w, target_w


def cal_expected_count(ligne_source, ligne_cible):
    # le calcul prevu en utilisant la probabilite initialise uniform
  
    global InitialMatrice, CompteurMatrice
    source_w, target_w = Table_frequence(ligne_source, ligne_cible)
    # chercher les mots uniques
    for s_id in source_w:
        for t_id in target_w:
            norm = sum([InitialMatrice[ident][t_id] for ident in source_w])
            p = InitialMatrice[s_id][t_id]/float(norm)
            exp_count = source_w[s_id] * target_w[t_id] * p
            key = (s_id, t_id)
            CompteurMatrice[key] = exp_count


def remplir_Deno_MatriceProba():
    """Ecriture de  count(w, a) comme un numerateur et 
        la colone Sum comme denominateur a la matrice de probabilite 
    """
    global CompteurMatrice, MatriceProba
    jth_col_sum = {}
    for key in CompteurMatrice:
        i, j = key
        # ajout de numerateur
        MatriceProba[0][i][j] = MatriceProba[0][i][j] + CompteurMatrice[key]
        # ajout de denominateurinateur (somme de la colone j

        denominateur = 0
        if j not in jth_col_sum:
            for k in CompteurMatrice:
                if k[1] == j:
                    denominateur = denominateur + CompteurMatrice[k]
                    jth_col_sum[j] = denominateur
    for j in jth_col_sum:
        denominateur = jth_col_sum[j]
        MatriceProba[1][:, j:j+1] = MatriceProba[1][i][j] + denominateur


def clear_CompteurMatrice():
    """ efaccer le compteur de matrice
    """
    CompteurMatrice.clear()


def probabilite(fichier_source, fichier_cible):
    """une fonction qui permet de calculer la probabilite revisee en utilisant le calcul prevu des pairs
        et retourne la mise a jour de la probabilite de la matrice  
    """
    global MatriceProba
    for sl, tl in zip(fichier_source, fichier_cible):
        cal_expected_count(sl, tl)
        remplir_Deno_MatriceProba()
        clear_CompteurMatrice()
    return MatriceProba[0]/MatriceProba[1]


def calcule_entropie(mat):
    """ cette fonction permet de calculer l'entropie de chaque colone de la matrice de probabilite mise a jour (updated matrix)
    """
    entropy_col = []
    len_col = mat.shape[-1]
    for i in xrange(len_col):
        en = entropy(mat[:, i:i+1])
        entropy_col.append(en[0])
    return entropy_col

def main():

    fichier_source = open(SOURCE_PATH, 'r')
    fichier_cible = open(TARGET_PATH, 'r')
    global InitialMatrice, MatriceProba
    c = 0
    while True:
        c += 1
        tmpMat = InitialMatrice[:, :]
        InitialMatrice = probabilite(fichier_source, fichier_cible)
        print "Iteration %s:    Entropie = %s" % (c, calcule_entropie(InitialMatrice))
        # vider la matrice de probabilite
        MatriceProba.fill(0.)
        fichier_source.seek(0)
        fichier_cible.seek(0)
        if np.allclose(tmpMat, InitialMatrice):  # tester si identique 
            break
    fichier_source.close()
    fichier_cible.close()
    
    print """
    
    ======== Matrice de probabilite finale : %s Iteration ======
    """ %c
    print InitialMatrice



if __name__ == '__main__':
    main()
