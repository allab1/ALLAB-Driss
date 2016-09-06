import os, sys, math
import operator
import codecs


out = open('score.txt', 'w')


def charge_donee(cand, ref):
    
    references = []
    if '.txt' in ref:
        fichier_ref = codecs.open(ref, 'r', 'utf-8')
        references.append(fichier_ref.readlines())
    else:
        for root, dossier, files in os.walk(ref):
            for f in files:
                fichier_ref = codecs.open(os.path.join(root, f), 'r', 'utf-8')
                references.append(fichier_ref.readlines())
    candidate_file = codecs.open(cand, 'r', 'utf-8')
    candidate = candidate_file.readlines()
    return candidate, references

def Geometric(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))


def n_gram(candidate, references, n):
    cl_compte = 0
    count = 0
    r = 0
    c = 0
    for si in range(len(candidate)):
        # calcul de precision de chaque phrase
        ref_counts = []
        ref_lengths = []
        # construire un dictionnaire de n-gram 
        for reference in references:
            ref_sentence = reference[si]
            ngram_d = {}
            mots = ref_sentence.strip().split()
            ref_lengths.append(len(mots))
            limits = len(mots) - n + 1
            for i in range(limits):
                ngram = ' '.join(mots[i:i + n]).lower()
                if ngram in ngram_d.keys():
                    ngram_d[ngram] += 1
                else:
                    ngram_d[ngram] = 1
            ref_counts.append(ngram_d)
        
        cand_sentence = candidate[si]
        cand_dict = {}
        mots = cand_sentence.strip().split()
        limits = len(mots) - n + 1
        for i in range(0, limits):
            ngram = ' '.join(mots[i:i + n]).lower()
            if ngram in cand_dict:
                cand_dict[ngram] += 1
            else:
                cand_dict[ngram] = 1
        cl_compte += clip_compte(cand_dict, ref_counts)
        count += limits
        r += closest_lenght(ref_lengths, len(mots))
        c += len(mots)
    if cl_compte == 0:
        pr = 0
    else:
        pr = float(cl_compte) / count
    bp = brievete(c, r)
    return pr, bp

def brievete(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1 - (float(r) / c))
    return bp

def clip_compte(cand_d, ref_ds):
    count = 0
    for m in cand_d.keys():
        m_w = cand_d[m]
        m_max = 0
        for ref in ref_ds:
            if m in ref:
                m_max = max(m_max, ref[m])
        m_w = min(m_w, m_max)
        count += m_w
    return count


def closest_lenght(ref_l, cand_l):
    """ la reference la plus proche au candidat """
    diff = abs(cand_l - ref_l[0])
    best = ref_l[0]
    for ref in ref_l:
        if abs(cand_l - ref) < diff:
            diff = abs(cand_l - ref)
            best = ref
    return best


def Score_bleu():
    candidate, references = charge_donee(sys.argv[1], sys.argv[2])

    precisions = []
    for i in range(4):
        pr, bp = n_gram(candidate, references, i + 1)
        precisions.append(pr)
    Score_bleu = Geometric(precisions) * bp
    print Score_bleu
    out.write(str(Score_bleu))

Score_bleu()
