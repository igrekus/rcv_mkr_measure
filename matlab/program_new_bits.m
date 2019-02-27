clc;
clear all;
fprintf('инициализация com порта\n');
receiver_control('0', 0);

[pna, err] = init_pna(1); % <- только для 1го запуска
%[pna,err] = init_pna(0);
%запрос сетки частот, используемой при измерении

%index = [0 1 2 4 8];%основные состояния
%index = [0 1];%основные состояния
index = 0:15; %все состояния
%index = [0 1];

%сохранение результатов измерений в файл
flag_save_on = 1;
%размещение файла для записи результатов измерений
dir = 'D:\Martynov\MatLab\receiver_module_otd7_v3\meas_27_feb_2019';
file_name = '-20dBm_#2_withUV8_Standart.xlsx';
num_pts = str2double(query(pna, 'SENS1:SWE:POINts?'));
num_ph = length(index); %количество состояний ФВ
mag_s11_arr = zeros(num_ph, num_pts);
mag_s22_arr = zeros(num_ph, num_pts);
mag_s21_arr = zeros(num_ph, num_pts);
phs_s21_arr = zeros(num_ph, num_pts);
gamma_inp = zeros(num_ph, num_pts);
gamma_outp = zeros(num_ph, num_pts);
st_arr = zeros(1, num_ph);

fprintf(pna, 'CALC1:PAR:SEL "CH1_S21"');
fprintf(pna, 'FORM:DATA REAL,32');
fprintf(pna, 'SENS1:X?');
frq = binblockread(pna, 'float32');

for i = 1:length(index)% i = [1..16]
    j = index(i); % j = [0..15]

    switch j
        case 0
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            phs_state = 0;
        case 1
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            phs_state = 22.5;
        case 2
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            phs_state = 45;
        case 3
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            phs_state = 22.5 + 45;
        case 4
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            phs_state = 90;
        case 5
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            phs_state = 22.5 + 90;
        case 6
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            phs_state = 45 + 90;
        case 7
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            phs_state = 22.5 + 45 + 90;
        case 8
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            phs_state = 180;
        case 9
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            phs_state = 22.5 + 180;
        case 10
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            phs_state = 45 + 180;
        case 11
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            phs_state = 22.5 + 45 + 180;
        case 12
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            phs_state = 90 + 180;
        case 13
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            phs_state = 22.5 + 90 + 180;
        case 14
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            phs_state = 45 + 90 + 180;
        case 15
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            phs_state = 22.5 + 45 + 90 + 180;
            end;
            st_arr(i) = phs_state;

            %magS21
            fprintf(pna, 'CALC1:PAR:SEL "CH1_S21"');
            %fprintf(pna,'DISP:WIND1:TRAC1:Y:SCAL:AUTO');
            %pause(time_delay);
            fprintf(pna, 'CALC1:DATA? FDATA');
            s_data = binblockread(pna, 'float32');
            mag_s21_arr(i, :) = s_data(:);
            clear s_data;

            %phsS21
            fprintf(pna, 'CALC2:PAR:SEL "CH2_S21"');
            %fprintf(pna,'DISP:WIND2:TRAC1:Y:SCAL:AUTO');
            %pause(time_delay);
            fprintf(pna, 'CALC2:DATA? FDATA');
            s_data = binblockread(pna, 'float32');
            phs_s21_arr(i, :) = s_data(:);
            clear s_data;

            %magS11
            fprintf(pna, 'CALC1:PAR:SEL "CH1_S11"');
            %fprintf(pna,'DISP:WIND1:TRAC2:Y:SCAL:AUTO');
            %pause(time_delay);
            fprintf(pna, 'CALC1:DATA? FDATA');
            s_data = binblockread(pna, 'float32');
            mag_s11_arr(i, :) = s_data(:);
            clear s_data;

            %magS22
            fprintf(pna, 'CALC1:PAR:SEL "CH1_S22"');
            %fprintf(pna,'DISP:WIND1:TRAC3:Y:SCAL:AUTO');
            %pause(time_delay);
            fprintf(pna, 'CALC1:DATA? FDATA');
            s_data = binblockread(pna, 'float32');
            mag_s22_arr(i, :) = s_data(:);
            clear s_data;

            end;
            fclose(pna);
            delete(pna);
            clear pna;

            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);

            for i = 1:length(index)
                gamma_inp(i, :) = VSWR_calc(mag_s11_arr(i, :));
                gamma_outp(i, :) = VSWR_calc(mag_s22_arr(i, :));
                end;

                if flag_save_on == 1
                    file_path = strcat(dir, '\', file_name);
                    init_file(file_path, frq, st_arr, gamma_inp, gamma_outp, mag_s21_arr, phs_s21_arr);
                    end;

                    df = frq(2) - frq(1);

                    for i = num_pts:-1:1

                        if (frq(i) < (1.32e9 + df)) && (frq(i) > (1.32e9 - df))
                            ind_up_frq = i;
                            end;
                            end;

                            for i = 1:1:num_pts

                                if (frq(i) < (1.21e9 + df)) && (frq(i) > (1.21e9 - df))
                                    ind_dn_frq = i;
                                    end;
                                    end;

                                    clc;
                                    %максимум для фиксированного состояния
                                    s21_max = zeros(1, length(index));
                                    s21_min = zeros(1, length(index));
                                    delta_s21 = zeros(1, length(index));

                                    for j = 1:length(index)
                                        temp = mag_s21_arr(j, ind_dn_frq:ind_up_frq);
                                        s21_max(j) = max(temp);
                                        s21_min(j) = min(temp);
                                        delta_s21(j) = s21_max(j) - s21_min(j);
                                        fprintf('Фаза ');
                                        fprintf('%3.1f\n', st_arr(j));
                                        fprintf('s21_max = ');
                                        fprintf('%3.1f\n', s21_max(j));
                                        fprintf('s21_min = ');
                                        fprintf('%3.1f\n', s21_min(j));
                                        fprintf('delta_s21 = ');
                                        fprintf('%3.1f\n', delta_s21(j));
                                        end;

                                        s21_MAX = max(s21_max);
                                        s21_MIN = min(s21_min);
                                        delta_Kp = abs(s21_MAX) - abs(s21_MIN);
                                        sred_Kp = (s21_MAX + s21_MIN) / 2;
                                        fprintf('delta_Kp = ');
                                        fprintf('%3.1f\n', delta_Kp);
                                        fprintf('Примерное среднее усиление = %4.2f\n', sred_Kp);
                                        fprintf('Max_S21 = %3.1f\n', s21_MAX);
                                        fprintf('Min_S21 = %3.1f\n', s21_MIN);

                                        eps = 1e-1;
                                        ref_pnt_inp = zeros(num_ph, (ind_up_frq - ind_dn_frq));
                                        ref_pnt_outp = zeros(num_ph, (ind_up_frq - ind_dn_frq));
                                        summ_inp = zeros(1, num_ph);
                                        summ_outp = zeros(1, num_ph);
                                        l = 1;
                                        k = 1;

                                        for j = 1:num_ph

                                            for i = ind_dn_frq:ind_up_frq

                                                if gamma_inp(j, i) > (1.5 + eps)
                                                    ref_pnt_inp(j, l) = 1;
                                                    l = l + 1;
                                                    end;

                                                    if gamma_outp(j, i) > (1.5 + eps)
                                                        ref_pnt_outp(j, k) = 1;
                                                        k = k + 1;
                                                        end;
                                                        end;
                                                        end;

                                                        for j = 1:num_ph
                                                            summ_inp(j) = sum(ref_pnt_inp(j, :));
                                                            summ_outp(j) = sum(ref_pnt_outp(j, :));
                                                            end;

                                                            if sum(summ_inp) == 0
                                                                fprintf('КСВ по входу менее 1.5\n');
                                                            else
                                                                fprintf('!!! КСВ по входу превышает 1.5\n');
                                                                end;

                                                                if sum(summ_outp) == 0
                                                                    fprintf('КСВ по выходу менее 1.5\n');
                                                                else
                                                                    fprintf('!!! КСВ по выходу превышает 1.5\n');
                                                                    end;

                                                                    % clear all;
                                                                    %EOF
