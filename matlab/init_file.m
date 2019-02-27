function init_file(file_path, freq, states, ...
        gamma_inp, gamma_outp, mS21, pS21)

    num_states = (length(find(states, 16, 'first')) + 1);

    N = length(freq);
    ofs = 2;
    %структура заголовков
    B = cell(4, num_states + ofs); %структура для инициализации заголовков файла
    C = cell(N + 10, 16 * 4 + 2); %структура для очистки файла
    sheet = 1;
    xlRange = 'A1';
    xlswrite(file_path, C, sheet, xlRange);
    clear C;

    t = clock;
    str_d = num2str(t(3));
    str_mth = num2str(t(2));
    str_y = num2str(t(1));
    str_h = num2str(t(4));
    str_m = num2str(t(5));
    str_time = strcat(str_h, ':', str_m);
    str_data = strcat(str_d, '.', str_mth, '.', str_y, 'г.');
    clear str_d str_mth str_y str_h str_m t;

    title = 'приёмный модуль МШУ';
    B{1, 1} = title;
    B{1, 3} = strcat('дата: ', str_data, ' время: ', str_time);
    B{3, 1} = 'пункт';
    B{3, 2} = 'частота, МГц';
    i = 3;
    k = 1;

    for j = 1:num_states %столбцы
        k = j * 4 - 3 + ofs;
        B{3, k} = 'SWR_in';
        B{3, k + 1} = 'SWR_out';
        B{3, k + 2} = 'S21,дБ';
        B{3, k + 3} = 'phase,гр.';
        B{4, k} = strcat(num2str(states(j)), ' гр.');
        B{4, k + 1} = strcat(num2str(states(j)), ' гр.');
        B{4, k + 2} = strcat(num2str(states(j)), ' гр.');
        B{4, k + 3} = strcat(num2str(states(j)), ' гр.');
    end;

    xlswrite(file_path, B, sheet, xlRange);

    D = cell(N, 4 * num_states + 2);

    for i = 1:N
        D{i, 2} = freq(i) * 1e-6;
        D{i, 1} = num2str(i, '%3.0d');
    end;

    for j = 1:(num_states)
        k = j * 4 - 3 + ofs;

    for i = 1:N
        D{i, k} = gamma_inp(j, i);
        D{i, k + 1} = gamma_outp(j, i);
        D{i, k + 2} = mS21(j, i);
        D{i, k + 3} = pS21(j, i);
        end;
        end;
        xlRange = 'A5';
        xlswrite(file_path, D, sheet, xlRange);

        fprintf('данные сохранены в файле:\n');
        fprintf('%s\n', file_path);

    end

                %EOF
