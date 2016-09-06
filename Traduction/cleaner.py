
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from itertools import izip
from argparse import ArgumentParser, RawTextHelpFormatter
from codecs import open as copen
import re,os,logging



punctuation = re.compile(u'[?@[\\\\\\]\\^_`{!"#$%&\'()*+,-./:;<=>|}~]')
log = logging.getLogger()



def charge_dictio(path):
    with copen(path) as f:
        words = (w.strip().lower() for w in f)
        words = set(words)
        return words


def gen_name(path):
    d = os.path.dirname(path)
    n = os.path.basename(path)
    n = 'CL___' + n
    return os.path.join(d, n)


def iteration_ligne(chemin1, chemin2):
    fichier1 = copen(chemin1, encoding='utf-8')
    fichier2 = copen(chemin2, encoding='utf-8')
    for p_line in izip(fichier1, fichier2):
        yield p_line
    fichier1.close()
    fichier2.close()


def tokenize(envoi):
    envoi = envoi.lower()
    envoi = punctuation.sub(u' ', envoi).strip()
    envoi = envoi.split()
    return envoi

def mots_clean(words, tokens):
    return [t for t in tokens if t not in words]

def dif(words, tokens):
    m = len(tokens)
    tokens = [t for t in tokens if t in words]
    n = len(tokens)
    return m, n

def passe(dict_w, stop_w, pair, abs_t=None, rel_t=None):
    tokens = tokenize(pair[0])
    tokens = mots_clean(stop_w, tokens)
    m, n = dif(dict_w, tokens)
    if abs_t is not None:
        if n < abs_t:
            return False
    if rel_t is not None:
        try:
            r = n/m
            if r < rel_t:
                return False
        except ZeroDivisionError:
            return False
    return True


def main(args):
    stop_w = []
    dict_w = []
    
    if args.dictionary:
        dict_w = charge_dictio(args.dictionary)
    if args.stop_words:
        stop_w = charge_dictio(args.stop_words)
    fichier1 = copen(gen_name(args.paths[0]), 'w', encoding='utf-8')
    fichier2 = copen(gen_name(args.paths[1]), 'w', encoding='utf-8')
    for i, pair in enumerate(iteration_ligne(*args.paths)):
        if passe(dict_w, stop_w, pair, abs_t=args.abs_diff, rel_t=args.rel_diff):
            fichier1.write(pair[0])
            fichier2.write(pair[1])
        if i % 1000 == 0:
            log.info('Lignes Traitee %i', i+1)
    fichier1.close()
    fichier2.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('paths', nargs=2, help='chemin vers deux fichiers de corpus paralelle ')
    parser.add_argument('--dictionary', help='chemin de dictionnaire')
    parser.add_argument('--stop_words', help='chemin vers le fichier qui contient les stop words')
    parser.add_argument('--abs_diff', type=int, default=None, help='  difference absolute pour lengeristement des phrases')
    parser.add_argument('--rel_diff', type=float, default=None, help='difference relative pour lengeristement des phrases')
    main(parser.parse_args())
