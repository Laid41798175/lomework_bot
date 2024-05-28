import os

def get_id(ctx) -> str:
    return str(ctx.author.id)

AMANNA_ID = os.getenv('AMANNA_ID')
BIJOCHAM_ID = os.getenv('BIJOCHAM_ID')
ELLENA_ID = os.getenv('ELLENA_ID')
LZ4_ID = os.getenv('LZ4_ID')
NEHAL0_ID_LIST = os.getenv('NEHAL0_ID').split(',')
ZEDO_ID = os.getenv('ZEDO_ID')

def get_owner(id: str) -> str:
    if id == AMANNA_ID:
        return 'Amanna'
    elif id == BIJOCHAM_ID:
        return 'BiJoCham'
    elif id == ELLENA_ID:
        return 'Ellena'
    elif id == LZ4_ID:
        return 'LZ4'
    elif id in NEHAL0_ID_LIST:
        return 'NeHal0'
    elif id == ZEDO_ID:
        return 'ZeDo'
    else:
        raise KeyError