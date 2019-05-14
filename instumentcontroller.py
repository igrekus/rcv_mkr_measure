import sys
import time

from arduino.jerome import Jerome, JeromeSerialMock
from instr.agilente8362b import AgilentE8362B
from pnamkrmock import PnaMkrMock

is_mock = True


def parse_float_list(lst):
    return list(map(lambda x: float(x), lst.split(',')))


class InstrumentController:

    phases = [
        22.5,
        45.0,
        90.0,
        180.0
    ]

    bit_states = {
        0: [0, 0, 0, 0],
        1: [1, 0, 0, 0],
        2: [0, 1, 0, 0],
        3: [1, 1, 0, 0],
        4: [0, 0, 1, 0],
        5: [1, 0, 1, 0],
        6: [0, 1, 1, 0],
        7: [1, 1, 1, 0],
        8: [0, 0, 0, 1],
        9: [1, 0, 0, 1],
        10: [0, 1, 0, 1],
        11: [1, 1, 0, 1],
        12: [0, 0, 1, 1],
        13: [1, 0, 1, 1],
        14: [0, 1, 1, 1],
        15: [1, 1, 1, 1]
    }

    def __init__(self, pna_address):
        self._pna_addr = pna_address
        self._jerome: Jerome = None
        self._pna: AgilentE8362B = None

        self._freqs = list()
        self._mag_s11s = list()
        self._mag_s22s = list()
        self._mag_s21s = list()
        self._phs_s21s = list()
        self._phase_values = list()

    def _clear(self):
        self._freqs = list()
        self._mag_s11s = list()
        self._mag_s22s = list()
        self._mag_s21s = list()
        self._phs_s21s = list()
        self._phase_values = list()

    def _prepare_rig(self, ):
        if not self._find_rig():
            if not self._jerome:
                print('error: jerome not found')
            if not self._pna:
                print('error: PNA not found')
            sys.exit(1)
        else:
            # TODO extract project-specific logic and result validation here
            self._jerome.mkr_init()
            self.mkr_init()
            print('\n-- instruments ready --\n')
        return True

    def _find_rig(self):
        if is_mock:
            self._jerome = Jerome(JeromeSerialMock())
            self._pna = AgilentE8362B(',PNA MKR mock,,', PnaMkrMock())
            return True

        self._jerome = Jerome.try_find()
        try:
            self._pna = AgilentE8362B.from_address_string(self._pna_addr)
        except RuntimeError as ex:
            print('RUNTIME ERROR:', ex)
        if not self._pna:
            self._pna, res = AgilentE8362B.try_find()
        return self._jerome and self._pna

    def _measure_s_params(self):
        for state in self.bit_states.values():
            self._phase_values.append(self._phase_for_state(state))

            self._jerome.mkr_set_bit_pattern(state)

            if not is_mock:
                time.sleep(0.1)

            # TODO extract measurement class
            self._mag_s21s.append(parse_float_list(self.mkr_read_measurement(chan=1, parameter='CH1_S21')))
            self._phs_s21s.append(parse_float_list(self.mkr_read_measurement(chan=2, parameter='CH2_S21')))
            self._mag_s11s.append(parse_float_list(self.mkr_read_measurement(chan=1, parameter='CH1_S11')))
            self._mag_s22s.append(parse_float_list(self.mkr_read_measurement(chan=1, parameter='CH1_S22')))

            if not is_mock:
                time.sleep(0.1)

    def _phase_for_state(self, pattern):
        return sum([ph * pt for ph, pt in zip(self.phases, pattern)])

    # public API
    def connect(self):
        self._prepare_rig()

    def disconnect(self):
        self._pna.close()
        self._jerome.mkr_reset()

    def measure(self):
        self._clear()
        self._freqs = parse_float_list(self.mkr_read_freqs(chan=1, parameter='CH1_S21'))
        self._measure_s_params()

    def mkr_read_measurement(self, chan=1, parameter=''):
        self._pna.send(f'CALC{chan}:PAR:SEL "{parameter}"')
        self._pna.query('*OPC?')
        return self._pna.query(f'CALC{chan}:DATA? FDATA')

    def mkr_read_freqs(self, chan=1, parameter=''):
        self._pna.send(f'CALC{chan}:PAR:SEL "{parameter}"')
        self._pna.query(f'*OPC?')
        return self._pna.query(f'SENS{chan}:X?')

    def mkr_init(self):
        self._pna.send('SYST:PRES')
        self._pna.query('*OPC?')
        self._pna.send('CALC:PAR:DEL:ALL')

        self._pna.send('DISP:WIND2 ON')

        self._pna.send('CALC1:PAR:DEF "CH1_S21",S21')
        self._pna.send('CALC2:PAR:DEF "CH2_S21",S21')
        self._pna.send('CALC1:PAR:DEF "CH1_S11",S11')
        self._pna.send('CALC1:PAR:DEF "CH1_S22",S22')

        # c:\program files\agilent\newtowrk analyzer\UserCalSets
        self._pna.send('SENS1:CORR:CSET:ACT "-20dBm_1.1-1.4G",1')
        self._pna.send('SENS2:CORR:CSET:ACT "-20dBm_1.1-1.4G",1')

        # self._pna.send(f'SENS1:SWE:POIN 201')
        # self._pna.send(f'SENS2:SWE:POIN 201')

        self._pna.send('DISP:WIND1:TRAC1:FEED "CH1_S21"')
        self._pna.send('DISP:WIND2:TRAC1:FEED "CH2_S21"')
        self._pna.send('DISP:WIND1:TRAC2:FEED "CH1_S11"')
        self._pna.send('DISP:WIND1:TRAC3:FEED "CH1_S22"')

        self._pna.send('SENS1:SWE:MODE CONT')
        self._pna.send('SENS2:SWE:MODE CONT')

        self._pna.send('CALC1:FORM MLOG')
        self._pna.send('DISP:WIND1:TRAC1:Y:SCAL:AUTO')
        self._pna.send('CALC2:FORM UPH')
        self._pna.send('DISP:WIND2:TRAC1:Y:SCAL:AUTO')

        self._pna.send(f'FORM:DATA ASCII')


    @property
    def freqs(self):
        return self._freqs

    @property
    def mag_s21s(self):
        return self._mag_s21s

    @property
    def phs_s21s(self):
        return self._phs_s21s

    @property
    def mag_s11s(self):
        return self._mag_s11s

    @property
    def mag_s22s(self):
        return self._mag_s22s

    @property
    def phase_values(self):
        return self._phase_values

    @property
    def measurements(self):
        return self.freqs, self.mag_s21s, self.phs_s21s, self.mag_s11s, self.mag_s22s, self.phase_values

    @property
    def pna(self):
        return str(self._pna)

    @property
    def jerome(self):
        return str(self._jerome)

    @property
    def connected(self):
        return self._pna and self._jerome
