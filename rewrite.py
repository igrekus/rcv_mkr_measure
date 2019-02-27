import sys
import serial
import pyvisa


def com_port_init(port: str):

    serial_obj = serial.Serial(port=port, baudrate=115200, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS,
                               stopbits=serial.STOPBITS_ONE, timeout=0.2)
    try:
        serial_obj.open()
        serial_obj.write(b'$KE\r\n')
        ans = serial_obj.read_all()
        if '#OK' not in ans:
            print('error opening port')
            sys.exit(1)

    except Exception as ex:
        print(ex)

    print('port open')
    serial_obj.write(b'$KE,IO,SET,7,0')
    serial_obj.write(b'$KE,IO,SET,8,0')
    serial_obj.write(b'$KE,IO,SET,9,0')
    serial_obj.write(b'$KE,IO,SET,10,0')
    serial_obj.write(b'$KE,IO,SET,11,0')
    serial_obj.write(b'$KE,IO,SET,12,0')
    serial_obj.write(b'$KE,IO,SET,13,0')
    serial_obj.write(b'$KE,IO,SET,14,0')
    serial_obj.write(b'$KE,WRA,000000010101010000000000')

    return serial_obj


def com_port(port: str):

    serial_obj = serial.Serial(port=port, baudrate=115200, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS,
                               stopbits=serial.STOPBITS_ONE, timeout=0.2)
    try:
        serial_obj.open()
        serial_obj.write(b'$KE\r\n')
        ans = serial_obj.read_all()
        if '#OK' not in ans:
            print('error opening port')
            sys.exit(1)

    except Exception as ex:
        print(ex)

    return serial_obj


def receiver_control(bit_str: str, state: int):
    # для переключения выводов оснастки
    # bit_str {bit3,bit4,bit5,bit6}
    # /state {1, 0}

    port = 'COM7'

    if bit_str == '0':
        serial_obj = com_port_init(port)
        serial_obj.close()
        return

    code_pos, code_neg = 0, 0
    if bit_str == 'bit6':
        code_pos, code_neg = 7, 8
    elif bit_str == 'bit5':
        code_pos, code_neg = 9, 10
    elif bit_str == 'bit4':
        code_pos, code_neg = 13, 14
    elif bit_str == 'bit3':
        code_pos, code_neg = 11, 12

    if state == 1:
        state_pos = 1
        state_neg = 0
        state_str = 'on'
    elif state == 0:
        state_pos = 0
        state_neg = 1
        state_str = 'off'

    cmd_str_pos = f'$KE,WR,{code_pos},{state_pos}'
    cmd_str_neg = f'$KE,WR,{code_neg},{state_neg}'

    serial_obj = com_port(port)
    print(serial_obj, f'send: {cmd_str_pos}, {state_str}')
    print(serial_obj, f'send: {cmd_str_neg}, {state_str}')
    serial_obj.close()


def init_pna(preset: int):
    print('init pna')

    rm = pyvisa.ResourceManager()
    pna = rm.open_resource('TCPIP0::192.168.1.61::inst0::INSTR')

    if preset == 1:
        pna.write('SYST:PRES')
        pna.query('*OPC?')
        pna.write('CALC:PAR:DEL:ALL')

        pna.write('DISP:WIND2 ON')

        pna.write('CALC1:PAR:DEF "CH1_S21",S21')
        pna.write('CALC2:PAR:DEF "CH2_S21",S21')
        pna.write('CALC1:PAR:DEF "CH1_S11",S11')
        pna.write('CALC1:PAR:DEF "CH1_S22",S22')

        pna.write('SENS1:CORR:CSET:ACT "-20dBm_1.1-1.4G",1')
        pna.write('SENS2:CORR:CSET:ACT "-20dBm_1.1-1.4G",1')

        pna.write('DISP:WIND1:TRAC1:FEED "CH1_S21"')
        pna.write('DISP:WIND2:TRAC1:FEED "CH2_S21"')
        pna.write('DISP:WIND1:TRAC2:FEED "CH1_S11"')
        pna.write('DISP:WIND1:TRAC3:FEED "CH1_S22"')

        pna.write('SENS1:SWE:MODE CONT')
        pna.write('SENS2:SWE:MODE CONT')

        pna.write('CALC1:FORM MLOG')
        pna.write('CALC2:FORM UPH')
        pna.write('DISP:WIND1:TRAC1:Y:SCAL:AUTO')
        pna.write('DISP:WIND2:TRAC1:Y:SCAL:AUTO')

    return pna, 0


def VSWR_calc(inp_S: list):
    tmp_inp_S = map(lambda x: x/20, inp_S)
    modS = map(lambda x: pow(10, x), tmp_inp_S)
    outp_G = map(lambda x, y: x / y, zip(map(lambda x: 1 + x, modS), map(lambda x: 1 - x, modS)))

    return list(outp_G)


def init_file(file_path, freq, states, gamma_inp, gamma_outp, mS21, pS21):
    pass


def measure():
    receiver_control('0', 0)

    pna, err = init_pna(1)

    index = list(range(16))

    flag_save_on = 1

    file_name = 'xlsx\\out.xlsx'

    num_pts = pna.query('SENS1:SWE:POINts?')
    num_ph = len(index)

    tmp = [[0] * num_pts] * num_ph

    mag_s11_arr = [[0] * num_pts] * num_ph
    mag_s22_arr = [[0] * num_pts] * num_ph
    mag_s21_arr = [[0] * num_pts] * num_ph
    phs_s21_arr = [[0] * num_pts] * num_ph
    gamma_inp = [[0] * num_pts] * num_ph
    gamma_outp = [[0] * num_pts] * num_ph
    st_arr = [0] * num_ph

    pna.write('CALC1:PAR:SEL "CH1_S21"')
    pna.write('FORM:DATA REAL,32')
    frq = pna.query('SENS1:X?')

    phs_state = 0

    for i in range(1, len(index) + 1):
        j = i - 1
        if j == 0:
            receiver_control('bit5', 0)
            receiver_control('bit6', 0)
            receiver_control('bit3', 0)
            receiver_control('bit4', 0)
            phs_state = 0
        elif j == 1:
            receiver_control('bit5', 1)
            receiver_control('bit6', 0)
            receiver_control('bit3', 0)
            receiver_control('bit4', 0)
            phs_state = 22.5
        elif j == 2:
            receiver_control('bit5', 0)
            receiver_control('bit6', 1)
            receiver_control('bit3', 0)
            receiver_control('bit4', 0)
            phs_state = 45
        elif j == 3:
            receiver_control('bit5', 1)
            receiver_control('bit6', 1)
            receiver_control('bit3', 0)
            receiver_control('bit4', 0)
            phs_state = 22.5+45
        elif j == 4:
            receiver_control('bit5', 0)
            receiver_control('bit6', 0)
            receiver_control('bit3', 1)
            receiver_control('bit4', 0)
            phs_state = 90
        elif j == 5:
            receiver_control('bit5', 1)
            receiver_control('bit6', 0)
            receiver_control('bit3', 1)
            receiver_control('bit4', 0)
            phs_state = 22.5+90
        elif j == 6:
            receiver_control('bit5', 0)
            receiver_control('bit6', 1)
            receiver_control('bit3', 1)
            receiver_control('bit4', 0)
            phs_state = 45+90
        elif j == 7:
            receiver_control('bit5', 1)
            receiver_control('bit6', 1)
            receiver_control('bit3', 1)
            receiver_control('bit4', 0)
            phs_state = 22.5+45+90
        elif j == 8:
            receiver_control('bit5', 0)
            receiver_control('bit6', 0)
            receiver_control('bit3', 0)
            receiver_control('bit4', 1)
            phs_state = 180
        elif j == 9:
            receiver_control('bit5', 1)
            receiver_control('bit6', 0)
            receiver_control('bit3', 0)
            receiver_control('bit4', 1)
            phs_state = 22.5+180
        elif j == 10:
            receiver_control('bit5', 0)
            receiver_control('bit6', 1)
            receiver_control('bit3', 0)
            receiver_control('bit4', 1)
            phs_state = 45+180
        elif j == 11:
            receiver_control('bit5', 1)
            receiver_control('bit6', 1)
            receiver_control('bit3', 0)
            receiver_control('bit4', 1)
            phs_state = 22.5+45+180
        elif j == 12:
            receiver_control('bit5', 0)
            receiver_control('bit6', 0)
            receiver_control('bit3', 1)
            receiver_control('bit4', 1)
            phs_state = 90+180
        elif j == 13:
            receiver_control('bit5', 1)
            receiver_control('bit6', 0)
            receiver_control('bit3', 1)
            receiver_control('bit4', 1)
            phs_state = 22.5+90+180
        elif j == 14:
            receiver_control('bit5', 0)
            receiver_control('bit6', 1)
            receiver_control('bit3', 1)
            receiver_control('bit4', 1)
            phs_state = 45+90+180
        elif j == 15:
            receiver_control('bit5', 1)
            receiver_control('bit6', 1)
            receiver_control('bit3', 1)
            receiver_control('bit4', 1)
            phs_state = 22.5+45+90+180

        st_arr[i - 1] = phs_state

        # magS21
        pna.write('CALC1:PAR:SEL "CH1_S21"')
        s_data = pna.query('CALC1:DATA? FDATA')
        mag_s21_arr[i - 1][:] = s_data[:]

        # phsS21
        pna.write(pna,'CALC2:PAR:SEL "CH2_S21"')
        s_data = pna.query('CALC2:DATA? FDATA')
        phs_s21_arr[i - 1][:] = s_data[:]

        # magS11
        pna.write('CALC1:PAR:SEL "CH1_S11"')
        s_data = pna.query('CALC1:DATA? FDATA')
        mag_s11_arr[i - 1][:] = s_data[:]

        # magS22
        pna.write('CALC1:PAR:SEL "CH1_S22"')
        s_data = pna.query('CALC1:DATA? FDATA')
        mag_s22_arr[i - 1][:] = s_data[:]

    pna.close()

    receiver_control('bit3', 1)
    receiver_control('bit4', 1)
    receiver_control('bit5', 1)
    receiver_control('bit6', 1)

    gamma_inp = list()
    gamma_outp = list()
    for i in range(1, len(index) + 1):
        gamma_inp.append(VSWR_calc(mag_s11_arr[i]))
        gamma_outp.append(VSWR_calc(mag_s22_arr[i]))

    if flag_save_on == 1:
        # TODO write save func
        init_file(file_name, frq, st_arr, gamma_inp, gamma_outp, mag_s21_arr, phs_s21_arr)

    df = frq[1] - frq[0]

    ind_up_frq = 0
    for i in range(num_pts - 1, -1, -1):
        if (1.32e9 - df) < frq[i] < (1.32e9 + df):
            ind_up_frq = i

    ind_dn_frq = 0
    for i in range(num_pts):
        if (1.21e9 - df) < frq[i] < (1.21e9 + df):
            ind_dn_frq = i

    # максимум для фиксированного состояния
    s21_max = [0] * len(index)
    s21_min = [0] * len(index)
    delta_s21 = [0] * len(index)

    for j in range(len(index)):
        temp = mag_s21_arr[j][ind_dn_frq:ind_up_frq]
        s21_max[j] = max(temp)
        s21_min[j] = min(temp)
        delta_s21[j] = s21_max[j] - s21_min[j]

        print('phase:', st_arr[j])
        print('s21_max=', s21_max[j])
        print('s21_min=', s21_min[j])
        print('delta_s21=', delta_s21[j])

    s21_MAX = max(s21_max)
    s21_MIN = min(s21_min)
    delta_Kp = abs(s21_MAX) - abs(s21_MIN)
    sred_Kp = (s21_MAX + s21_MIN)/2

    print('delta_Kp=', delta_Kp)
    print('approx median amp=', sred_Kp)
    print('Max_S21 = %3.1f\n', s21_MAX)
    print('Min_S21 = %3.1f\n', s21_MIN)

    eps = 1e-1

    ref_pnt_inp = [[0] * (ind_up_frq - ind_dn_frq)] * num_ph
    ref_pnt_outp = [[0] * (ind_up_frq - ind_dn_frq)] * num_ph

    summ_inp = [0] * num_ph
    summ_outp = [0] * num_ph

    l = 0
    k = 0

    for j in range(num_ph):
        for i in range(ind_dn_frq, ind_up_frq + 1):
            if gamma_inp[j][i] > (1.5 + eps):
                ref_pnt_inp[j][l] = 1
                l += 1
            if gamma_outp[j][i] > (1.5 + eps):
                ref_pnt_outp[j][k] = 1
                k += 1

    for j in range(num_ph):
        summ_inp[j] = sum(ref_pnt_inp[j])
        summ_outp[j] = sum(ref_pnt_outp[j])

    if summ_inp == 0:
        print('WSVR in < 1.5')
    else:
        print('!!! WSVR in > 1.5 !!!')

    if summ_outp == 0:
        print('WSVR out < 1.5')
    else:
        print('!!! WS?VR out > 1.5 !!!')


if __name__ == '__main__':

    measure()
