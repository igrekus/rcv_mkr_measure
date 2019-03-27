def calc_vswr(input_values: list):
    temp = map(lambda x: x/20, input_values)
    modulated = list(map(lambda x: pow(10, x), temp))
    output_gamma = map(lambda z: z[0] / z[1] if z[1] != 0 else 0.000001, zip(map(lambda x: 1 + x, modulated), map(lambda x: 1 - x, modulated)))
    return list(output_gamma)


def find_freq_index(freqs: list, threshold):
    df = freqs[1] - freqs[0]
    return next((i for i, f in enumerate(freqs) if (threshold - df) < f < (threshold + df)), 0)


def ref_pts_stats(gamma_inp, ind_dn_frq, ind_up_frq):
    eps = 1e-1
    threshold = 1.5
    return [[1 for g in gamma[ind_dn_frq:ind_up_frq + 1] if g > threshold + eps] for gamma in gamma_inp]


class MeasurementResult:

    def __init__(self,):
        self._freqs = list()
        self._mag_s21s = list()
        self._phs_s21s = list()
        self._mag_s11s = list()
        self._mag_s22s = list()
        self._states = list()

        self._gamma_input = list()
        self._gamma_output = list()

        self._low_threshold = 1.21e9
        self._high_threshold = 1.31e9
        self._low_index = 0
        self._high_index = 0

        self._s21_maxs = list()
        self._s21_mins = list()

        self._delta_Kp = 0.0
        self._s21_MAX = 0.0
        self._s21_MIN = 0.0
        self._avg_Kp = 0.0

        self._ref_pnt_inp = list()
        self._ref_pnt_outp = list()

        self._summ_inp = list()
        self._summ_outp = list()

        self.ready = False

    def process(self):
        self._calc_gammas()
        self._find_freqs()
        self._calc_limits()
        self._calc_out_params()
        self._calc_ref_points()
        self._calc_out_stats()

    def _calc_gammas(self):
        self._gamma_input = [calc_vswr(mags) for mags in self._mag_s11s]
        self._gamma_output = [calc_vswr(mags) for mags in self._mag_s22s]

    def _find_freqs(self):
        self._low_index = find_freq_index(self._freqs, threshold=self._low_threshold)
        self._high_index = find_freq_index(self._freqs, threshold=self._high_threshold)

    def _calc_limits(self):
        for i, data in enumerate(self._mag_s21s):
            temp = data[self._low_index:self._high_index + 1]
            mx, mn = max(temp), min(temp)
            self._s21_maxs.append(mx)
            self._s21_mins.append(mn)

            print('\nphase=', self._states[i])
            print('s21_max=', mx)
            print('s21_min=', mn)
            print('delta_s21=', mx - mn)

    def _calc_out_params(self):
        self._s21_MAX = max(self._s21_maxs)
        self._s21_MIN = min(self._s21_mins)
        self._delta_Kp = abs(self._s21_MAX) - abs(self._s21_MIN)
        self._avg_Kp = (self._s21_MAX + self._s21_MIN) / 2

    def _calc_ref_points(self):
        self._ref_pnt_inp = ref_pts_stats(self._gamma_input, self._low_index, self._high_index)
        self._ref_pnt_outp = ref_pts_stats(self._gamma_output, self._low_index, self._high_index)

    def _calc_out_stats(self):
        self._summ_inp = sum([sum(pts) for pts in self._ref_pnt_inp])
        self._summ_outp = sum([sum(pts) for pts in self._ref_pnt_outp])

    def __bool__(self):
        return self.ready

    @property
    def raw_data(self):
        return self._freqs, self._mag_s21s, self._phs_s21s, self._mag_s11s, self._mag_s22s, self._states

    @raw_data.setter
    def raw_data(self, args):
        self._freqs, self._mag_s21s, self._phs_s21s, self._mag_s11s, self._mag_s22s, self._states = args

    @property
    def freqs(self):
        return self._freqs

    # def ready(self):
    #     print(self._delta_Kp , self._s21_MAX , self._s21_MIN , self._avg_Kp , self._summ_inp , self._summ_outp)
    #     print(self._delta_Kp and self._s21_MAX and self._s21_MIN and self._avg_Kp and self._summ_inp and self._summ_outp)
    #     return self._delta_Kp and self._s21_MAX and self._s21_MIN and self._avg_Kp and self._summ_inp and self._summ_outp

