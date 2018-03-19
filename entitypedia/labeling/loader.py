import codecs


def load(path):
    with codecs.open(path, encoding='utf-8') as f:
        sent = []
        sents = []
        for line in f:
            if line == '\n':
                sents.append(sent)
                sent = []
                continue
            morph_info = line.strip().split('\t')
            sent.append(morph_info)

    words = [[morph[0] for morph in sent] for sent in sents]
    poses = [[morph[1] for morph in sent] for sent in sents]
    labels = [[morph[-1] for morph in sent] for sent in sents]

    return words, poses, labels
