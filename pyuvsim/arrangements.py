from abc import ABC

import numpy as np


class Arrangement(ABC):
    Nsrcs = 1

    _defaults = {}

    def __init__(self, **kwargs):
        for k, v in self._defaults.items():
            setattr(self, k, kwargs.pop(k, v))

        if kwargs:
            raise KeyError("The following keywords are not accepted in {}: {}".format(
                self.__class__.__name__, list(kwargs.keys()))
            )

    @property
    def alts(self):
        return [90.0] * self.Nsrcs

    @property
    def azs(self):
        return [90.0] * self.Nsrcs

    @property
    def fluxes(self):
        return [1.0] * self.Nsrcs

    @property
    def defining_dict(self):
        return {k: getattr(self, k) for k in self._defaults}


class OffZenith(Arrangement):
    def __init__(self, alt=None):
        self.alt = alt if alt is not None else 85.0

    @property
    def alts(self):
        return [self.alt] * self.Nsrcs


class Triangle(Arrangement):
    Nsrcs = 3
    _defaults = {'alt': 87.0}

    @property
    def alts(self):
        return [self.alt] * self.Nsrcs

    @property
    def azs(self):
        return [0.0, 120.0, 240.0]


class Cross(Arrangement):
    Nsrcs = 4
    alts = [88., 90., 86., 82.]
    azs = [270., 0., 90., 135.]
    fluxes = [5., 4., 1.0, 2.0]


class Zenith(Arrangement):
    _defaults = {"Nsrcs": 1}

    @property
    def azs(self):
        return [0.0] * self.Nsrcs

    @property
    def fluxes(self):
        return [1. / self.Nsrcs] * self.Nsrcs


class Random(Arrangement):
    _defaults = {"Nsrcs": 1, "min_alt": 30.0, "rseed": None}

    def __init__(self, **kwargs):
        super(Random, self).__init__(**kwargs)
        np.random.seed(self.rseed)
        self.rseed = np.random.get_state()[1][0]

    @property
    def alts(self):
        return np.random.uniform(self.min_alt, 90, self.Nsrcs)

    @property
    def azs(self):
        return np.random.uniform(0, 2 * np.pi, self.Nsrcs)

    @property
    def fluxes(self):
        return np.ones(self.Nsrcs, dtype=float)


class LongLine(Arrangement):
    _defaults = {"Nsrcs": 10, "min_alt": 5}

    @property
    def fluxes(self):
        return np.ones(self.Nsrcs, dtype=float)

    @property
    def alts(self):
        if self.Nsrcs % 2 == 0:
            length = 180 - self.min_alt * 2
            spacing = length / (self.Nsrcs - 1)
            max_alt = 90. - spacing / 2
            alts = np.linspace(self.min_alt, max_alt, self.Nsrcs // 2)
            return np.append(alts, np.flip(alts, axis=0))
        else:
            alts = np.linspace(self.min_alt, 90, (self.Nsrcs + 1) // 2)
            return np.append(alts, np.flip(alts[1:], axis=0))

    @property
    def azs(self):
        if self.Nsrcs % 2 == 0:
            return np.append(np.zeros(self.Nsrcs // 2, dtype=float) + 180.,
                             np.zeros(self.Nsrcs // 2, dtype=float))
        else:
            return np.append(np.zeros((self.Nsrcs + 1) // 2, dtype=float) + 180.,
                             np.zeros((self.Nsrcs - 1) // 2, dtype=float))


class HERAText(Arrangement):
    @property
    def azs(self):
        return np.array(
            [
                -254.055, -248.199, -236.310, -225.000, -206.565,
                -153.435, -123.690, -111.801, -105.945, -261.870,
                -258.690, -251.565, -135.000, -116.565, -101.310,
                -98.130, 90.000, 90.000, 90.000, 90.000, 90.000,
                -90.000, -90.000, -90.000, -90.000, -90.000,
                -90.000, 81.870, 78.690, 71.565, -45.000, -71.565,
                -78.690, -81.870, 74.055, 68.199, 56.310, 45.000,
                26.565, -26.565, -45.000, -56.310, -71.565
            ]
        )

    @property
    def alts(self):
        zas = np.array([7.280, 5.385, 3.606, 2.828, 2.236, 2.236, 3.606,
                        5.385, 7.280, 7.071, 5.099, 3.162, 1.414, 2.236,
                        5.099, 7.071, 7.000, 6.000, 5.000, 3.000, 2.000,
                        1.000, 2.000, 3.000, 5.000, 6.000, 7.000, 7.071,
                        5.099, 3.162, 1.414, 3.162, 5.099, 7.071, 7.280,
                        5.385, 3.606, 2.828, 2.236, 2.236, 2.828, 3.606, 6.325])
        return 90.0 - zas

    @property
    def Nsrcs(self):
        return self.alts.size
