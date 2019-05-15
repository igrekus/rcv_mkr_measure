from excelresult import ExcelResult
from instumentcontroller import InstrumentController
from measurementresult import MeasurementResult


def measure(pna_addr='GPIB1::10::INSTR'):

    instrs = InstrumentController(pna_address=pna_addr)
    instrs.connect()
    instrs.measure()
    instrs.disconnect()

    result = MeasurementResult()
    result.raw_data = instrs.measurements
    result.process()

    print('delta Kp=', result._delta_Kp)
    print('approx median amp=', result._avg_Kp)
    print('Max S21 = ', result._s21_MAX)
    print('Min S21 = ', result._s21_MIN)

    print()
    print('VSWR in < 1.5') if result._summ_inp == 0 else print('warning: VSWR in > 1.5')
    print('VSWR out < 1.5') if result._summ_outp == 0 else print('warning: VSWR out > 1.5')

    xlsx = ExcelResult(result.freqs, result._states, result._gamma_input, result._gamma_output, result._mag_s21s, result._phs_s21s)
    xlsx.save()


if __name__ == '__main__':
    measure()
