import hashlib


def encipher():
    ipt = input('s')
    hl = hashlib.md5()
    hl.update(ipt.encode(encoding='utf-8'))
    if hl.hexdigest() == 'bcedc450f8481e89b1445069acdc3dd9':
        return True