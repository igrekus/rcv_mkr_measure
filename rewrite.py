import datetime
import openpyxl
import pyvisa
import serial
import sys

from serialmock import SerialMock

ser = serial.Serial(port='COM10', baudrate=115200)
port = SerialMock()


def com_port_init(serial_obj):
    try:
        serial_obj.open()
        serial_obj.write(b'$KE\r\n')
        ans = serial_obj.read_all()
        if b'#OK' not in ans:
            print('error opening port')
            sys.exit(1)

    except Exception as ex:
        print(ex)

    serial_obj.write(b'$KE,IO,SET,7,0\r\n')
    serial_obj.write(b'$KE,IO,SET,8,0\r\n')
    serial_obj.write(b'$KE,IO,SET,9,0\r\n')
    serial_obj.write(b'$KE,IO,SET,10,0\r\n')
    serial_obj.write(b'$KE,IO,SET,11,0\r\n')
    serial_obj.write(b'$KE,IO,SET,12,0\r\n')
    serial_obj.write(b'$KE,IO,SET,13,0\r\n')
    serial_obj.write(b'$KE,IO,SET,14,0\r\n')
    serial_obj.write(b'$KE,WRA,000000010101010000000000\r\n')

    return serial_obj


def com_port(serial_obj):
    try:
        serial_obj.open()
        serial_obj.write(b'$KE\r\n')
        ans = serial_obj.read_all()
        if b'#OK' not in ans:
            print('error opening port')
            sys.exit(1)

    except Exception as ex:
        print(ex)

    return serial_obj


def receiver_control(bit_str: str, state: int, serial_obj):
    # для переключения выводов оснастки
    # bit_str {bit3,bit4,bit5,bit6}
    # /state {1, 0}

    if bit_str == '0':
        serial_obj = com_port_init(serial_obj=serial_obj)
        serial_obj.close()
        return 'init complete'

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
    elif state == 0:
        state_pos = 0
        state_neg = 1

    cmd_str_pos = f'$KE,WR,{code_pos},{state_pos}\r\n'
    cmd_str_neg = f'$KE,WR,{code_neg},{state_neg}\r\n'

    serial_obj = com_port(serial_obj=serial_obj)

    serial_obj.write(bytes(cmd_str_pos, encoding='ascii'))
    ans1 = serial_obj.read_all()
    serial_obj.write(bytes(cmd_str_neg, encoding='ascii'))
    ans2 = serial_obj.read_all()

    serial_obj.close()
    return ans1, ans2


def init_pna(preset: int, pna=None):
    if pna is None:
        try:
            rm = pyvisa.ResourceManager()
            pna = rm.open_resource('TCPIP0::192.168.1.61::inst0::INSTR')

        except Exception as ex:
            print('error connecting to pna:', ex)
            sys.exit(1)

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
    modS = list(map(lambda x: pow(10, x), tmp_inp_S))
    outp_G = map(lambda z: z[0] / z[1] if z[1] != 0 else 0.000001, zip(map(lambda x: 1 + x, modS), map(lambda x: 1 - x, modS)))

    return list(outp_G)


def init_file(file_path, freq, states, gamma_inp, gamma_outp, mS21, pS21):

    first_16_nonzero_elem_indices = [idx for idx, x in enumerate(states) if x != 0]

    num_states = len(first_16_nonzero_elem_indices) + 1

    N = len(freq)
    ofs = 2

    B = [[None] * (num_states + ofs)] * 4  # empty array to wipe xlsx-file header
    C = [[None] * (16 * 4 + 2)] * N + 10  # empty array to wipe xlsx-file

    sheet = 1
    xlRange = 'A1'

    wb = openpyxl.Workbook()
    ws = wb.active

    str_y, str_mth, str_d, str_h, str_m, *rest = datetime.datetime.now().timetuple()
    str_time = f'{str_h}:{str_m}'
    str_date = f'{str_d}.{str_mth}.{str_y}'

    title = 'приемный модуль МШУ'
    ws.cell(row=1, column=1, value=title)
    ws.cell(row=1, column=3, value=f'date:{str_date} time:{str_time}')
    ws.cell(row=3, column=1, value='пункт')
    ws.cell(row=3, column=2, value='частота, МГц')

    i = 3
    k = 1

    for j in range(1, num_states + 1):
        k = j * 4 - 3 + ofs
        ws.cell(row=3, column=k + 0, value='SWR_in')
        ws.cell(row=3, column=k + 1, value='SWR_out')
        ws.cell(row=3, column=k + 2, value='S21,дБ')
        ws.cell(row=3, column=k + 3, value='phase,гр.')

        ws.cell(row=4, column=k + 0, value=f'{states[j - 1]} гр.')
        ws.cell(row=4, column=k + 1, value=f'{states[j - 1]} гр.')
        ws.cell(row=4, column=k + 2, value=f'{states[j - 1]} гр.')
        ws.cell(row=4, column=k + 3, value=f'{states[j - 1]} гр.')

    wb.save('out.xlsx')

    for i in range(1, N + 1):
        ws.cell(row=i, column=2, value=freq[i - 1] * 1e-6)
        ws.cell(row=i, column=1, value=f'{i:03d}')

    pivot_row = 5
    pivot_col = 1

    for j in range(1, num_states + 1):
        k = j * 4 - 3 + ofs
        for i in range(1, N + 1):
            ws.cell(row=i + pivot_row, column=k + 0 + pivot_col, value=gamma_inp[j][i])
            ws.cell(row=i + pivot_row, column=k + 1 + pivot_col, value=gamma_outp[j][i])
            ws.cell(row=i + pivot_row, column=k + 2 + pivot_col, value=mS21[j][i])
            ws.cell(row=i + pivot_row, column=k + 3 + pivot_col, value=pS21[j][i])

    print('saved .xlsx:', file_path)


def save_file(file_path, freq, gamma_inp, gamma_outp, mS21, pS21, s21_min, s21_max, delta_s21, delta_Kp, states):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    xls_str_start = 6  # перва¤ строка для записи значений
    xls_cln_start = 3  # первый столбец для записи значений

    N = len(freq)
    temp = [0] * N

    first_16_nonzero_elem_indices = [idx for idx, x in enumerate(states) if x != 0]
    num_states = len(first_16_nonzero_elem_indices) + 1

    indx = 0  # индекс смещения по колонкам

    for j in range(1, num_states + 1):
        ptr_cln = indx + xls_cln_start
        temp[:] = gamma_inp[j - 1][:]
        for row, value in enumerate(temp):
            ws.cell(row=xls_str_start + row, column=ptr_cln, value=value)
        indx += 4

    indx = 1

    for j in range(1, num_states + 1):
        ptr_cln = indx + xls_cln_start
        temp[:] = gamma_outp(j - 1)[:]
        for row, value in enumerate(temp):
            ws.cell(row=xls_str_start + row, column=ptr_cln, value=value)
        indx += 4

    indx = 2

    for j in range(1, num_states + 1):
        ptr_cln = indx + xls_cln_start
        temp[:] = mS21[j - 1][:]
        for row, value in enumerate(temp):
            ws.cell(row=xls_str_start + row, column=ptr_cln, value=value)
        indx += 4

    indx = 3

    for j in range(1, num_states + 1):
        ptr_cln = indx + xls_cln_start
        temp[:] = pS21[j - 1][:]
        for row, value in enumerate(temp):
            ws.cell(row=xls_str_start + row, column=ptr_cln, value=value)
        indx += 4

    temp = [0] * 3
    indx = 0

    for j in range(1, num_states + 1):
        ptr_cln1 = indx + xls_cln_start
        ptr_cln2 = indx + xls_cln_start + 2
        temp[1] = s21_max[j]
        temp[2] = s21_min[j]
        temp[3] = delta_s21[j]
        for col, value in enumerate(temp):
            ws.cell(row=xls_str_start - 3, column=ptr_cln1 + col, value=value)
        indx += 4

    data2str = delta_Kp
    ptr_cln = 2
    ws.cell(row=xls_str_start - 3, column=ptr_cln, value=delta_Kp)

    wb.save(file_path)

    print('data saved to:', file_path)


def measure():
    receiver_control('0', 0, serial_obj=ser)

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
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 0
        elif j == 1:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 22.5
        elif j == 2:
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 45
        elif j == 3:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 22.5 + 45
        elif j == 4:
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 90
        elif j == 5:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 22.5 + 90
        elif j == 6:
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 45 + 90
        elif j == 7:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 0, serial_obj=ser)
            phs_state = 22.5 + 45 + 90
        elif j == 8:
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 180
        elif j == 9:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 22.5 + 180
        elif j == 10:
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 45 + 180
        elif j == 11:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 0, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 22.5 + 45 + 180
        elif j == 12:
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 90 + 180
        elif j == 13:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 0, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 22.5 + 90 + 180
        elif j == 14:
            receiver_control('bit5', 0, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 45 + 90 + 180
        elif j == 15:
            receiver_control('bit5', 1, serial_obj=ser)
            receiver_control('bit6', 1, serial_obj=ser)
            receiver_control('bit3', 1, serial_obj=ser)
            receiver_control('bit4', 1, serial_obj=ser)
            phs_state = 22.5 + 45 + 90 + 180

        st_arr[i - 1] = phs_state

        # magS21
        pna.write('CALC1:PAR:SEL "CH1_S21"')
        s_data = pna.query('CALC1:DATA? FDATA')
        mag_s21_arr[i - 1][:] = s_data[:]

        # phsS21
        pna.write(pna, 'CALC2:PAR:SEL "CH2_S21"')
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

    receiver_control('bit3', 1, serial_obj=ser)
    receiver_control('bit4', 1, serial_obj=ser)
    receiver_control('bit5', 1, serial_obj=ser)
    receiver_control('bit6', 1, serial_obj=ser)

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
    sred_Kp = (s21_MAX + s21_MIN) / 2

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
