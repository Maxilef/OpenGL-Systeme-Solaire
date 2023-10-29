def calc_p_conjointe(OBS):
    """
    OBS : 1 ligne  == 1 réalisation dans le temps
          1 colone == Xi
    """


    if not len(OBS) : return dict()

    p = dict()
    nb_val = len(OBS[0])

    for real in OBS :
        nuplet = tuple(nuplet)
        if nuplet in p : p[nuplet] += 1
        else p[nuplet]=1

    for n in p : p[n] /= nb_val

    return p
