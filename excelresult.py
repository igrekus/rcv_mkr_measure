import datetime
import openpyxl


class ExcelResult:

    def __init__(self, freqs, st_arr, gamma_inp, gamma_outp, mag_s21_arr, phs_s21_arr):
        self._freqs = freqs
        self._states = st_arr
        self._gamma_in = gamma_inp
        self._gamma_out = gamma_outp
        self._s21_mags = mag_s21_arr
        self._s21_phs = phs_s21_arr

    @property
    def file_path(self):
        year, month, day, hour, minute, *rest = datetime.datetime.now().timetuple()
        return f'.\\xlsx\\VSWR-{year}-{month:02d}-{day:02d}-{hour:02d}.{minute:02d}.xlsx'

    def save(self):
        year, month, day, hour, minute, *rest = datetime.datetime.now().timetuple()

        wb = openpyxl.Workbook()
        ws = wb.active

        wb_header_cell = ws['A1']
        wb_header_cell.value = 'приемный модуль МШУ'
        wb_header_cell.offset(0, 3).value = f'дата: {day:02d}.{month:02d}.{year}   время: {hour:02d}:{minute:02d}'

        table_header_cell = wb_header_cell.offset(2, 0)
        table_header_cell.value = 'пункт'
        table_header_cell.offset(0, 1).value = 'частота, МГц'

        for i, state in enumerate(self._states):
            batch_offset = 4 * i
            table_header_cell.offset(0, 2 + batch_offset).value = 'КСВ вх.'
            table_header_cell.offset(0, 3 + batch_offset).value = 'КСВ вых.'
            table_header_cell.offset(0, 4 + batch_offset).value = 'S21, дБ'
            table_header_cell.offset(0, 5 + batch_offset).value = 'фаза, гр.'

            table_header_cell.offset(1, 2 + batch_offset).value = f'{state} гр.'
            table_header_cell.offset(1, 3 + batch_offset).value = f'{state} гр.'
            table_header_cell.offset(1, 4 + batch_offset).value = f'{state} гр.'
            table_header_cell.offset(1, 5 + batch_offset).value = f'{state} гр.'

        table_data_cell = wb_header_cell.offset(4, 0)
        for i, freq in enumerate(self._freqs):
            table_data_cell.offset(i, 0).value = f'{i:04d}'
            table_data_cell.offset(i, 1).value = f'{freq * 1e-6:.2f}'

        for i in range(len(self._states)):
            batch_offset = 4 * i
            for j in range(len(self._freqs)):
                table_data_cell.offset(j, 2 + batch_offset).value = self._gamma_in[i][j]
                table_data_cell.offset(j, 3 + batch_offset).value = self._gamma_out[i][j]
                table_data_cell.offset(j, 4 + batch_offset).value = self._s21_mags[i][j]
                table_data_cell.offset(j, 5 + batch_offset).value = self._s21_phs[i][j]

        wb.save(self.file_path)
        print('\nsaved .xlsx:', self.file_path)

