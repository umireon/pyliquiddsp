cdef extern from 'liquid/liquid.h':
    void liquid_firdes_rrcos(unsigned int _k, unsigned int _m, float _beta, float _dt, float * _h)
    cdef struct fskdem_s:
        pass
    ctypedef fskdem_s * fskdem
    fskdem fskdem_create(unsigned int _m, unsigned int _k, float _bandwidth)
