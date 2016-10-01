import numpy as np
cimport numpy as np

cimport cliquid

def liquid_firdes_rrcos(int k, int m, float beta, float dt=0, float[::1] out = None):
    outlen = k*m*2+1
    if out is None:
        out = np.empty(outlen, dtype=np.float32)
    else:
        if len(out) != outlen:
            raise ValueError('out must be {}-element array'.format(outlen))
    cliquid.liquid_firdes_rrcos(k, m, beta, dt, &out[0])
    return np.asarray(out)

def fskdem_create(int m, int k, float bandwidth):
    cliquid.fskdem_create(m, k, bandwidth)
