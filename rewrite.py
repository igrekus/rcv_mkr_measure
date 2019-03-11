import sys

from excelresult import ExcelResult
from instumentcontroller import InstrumentController
from measurementresult import MeasurementResult


def measure(pna_addr='TCPIP0::192.168.1.61::inst0::INSTR'):

    instrs = InstrumentController(pna_address=pna_addr)

    freqs = instrs.freqs
    mag_s21_arr, phs_s21_arr, mag_s11_arr, mag_s22_arr, st_arr = instrs.measurements

    instrs.close_rig()

    result = MeasurementResult(freqs, mag_s21_arr, phs_s21_arr, mag_s11_arr, mag_s22_arr, st_arr)
    result.process()

    print('delta Kp=', result._delta_Kp)
    print('approx median amp=', result._avg_Kp)
    print('Max S21 = ', result._s21_MAX)
    print('Min S21 = ', result._s21_MIN)

    print()
    print('VSWR in < 1.5') if result._summ_inp == 0 else print('warning: VSWR in > 1.5')
    print('VSWR out < 1.5') if result._summ_outp == 0 else print('warning: VSWR out > 1.5')

    xlsx = ExcelResult(freqs, st_arr, result._gamma_input, result._gamma_output, mag_s21_arr, phs_s21_arr)
    xlsx.save()


if __name__ == '__main__':
    measure(pna_addr=sys.argv[1])
