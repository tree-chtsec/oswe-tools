import itertools

def perm(charset, number):
    return itertools.imap(''.join, itertools.product(charset, repeat=number))
