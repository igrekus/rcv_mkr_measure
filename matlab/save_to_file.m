function save_to_file(file_path, freq, gamma_inp, gamma_outp, mS21, pS21, ...
        s21_min, s21_max, delta_s21, delta_Kp, states)
    %freq, gamma_inp, gamma_outp, mS21, pS21

    xls_str_start = 6; %перва¤ строка дл¤ записи значений
    xls_cln_start = 3; %первый столбец дл¤ записи значений

    N = length(freq);
    temp = zeros(N, 1);
    clear freq;

    num_states = (length(find(states, 16, 'first')) + 1);
    indx = 0; %индекс смещени¤ по колонкам

    for j = 1:(num_states)
        ptr_cln = get_char(indx + xls_cln_start);
        temp(:) = gamma_inp(j, :);
        data2str = temp;
        strs = strcat(ptr_cln, num2str(xls_str_start), ...
            ':', ptr_cln, num2str(xls_str_start + N - 1));
        indx = indx + 4;
        xlswrite(file_path, data2str, strs);
        end;

        indx = 1;

        for j = 1:(num_states)
            ptr_cln = get_char(indx + xls_cln_start);
            temp(:) = gamma_outp(j, :);
            data2str = temp;
            strs = strcat(ptr_cln, num2str(xls_str_start), ...
                ':', ptr_cln, num2str(xls_str_start + N - 1));
            indx = indx + 4;
            xlswrite(file_path, data2str, strs);
            end;

            indx = 2;

            for j = 1:(num_states)
                ptr_cln = get_char(indx + xls_cln_start);
                temp(:) = mS21(j, :);
                data2str = temp;
                strs = strcat(ptr_cln, num2str(xls_str_start), ...
                    ':', ptr_cln, num2str(xls_str_start + N - 1));
                indx = indx + 4;
                xlswrite(file_path, data2str, strs);
                end;

                indx = 3;

                for j = 1:(num_states)
                    ptr_cln = get_char(indx + xls_cln_start);
                    temp(:) = pS21(j, :);
                    data2str = temp;
                    strs = strcat(ptr_cln, num2str(xls_str_start), ...
                        ':', ptr_cln, num2str(xls_str_start + N - 1));
                    indx = indx + 4;
                    xlswrite(file_path, data2str, strs);
                    end;

                    clear temp;
                    temp = zeros(1, 3);
                    indx = 0;

                    for j = 1:(num_states)
                        ptr_cln1 = get_char(indx + xls_cln_start);
                        ptr_cln2 = get_char(indx + xls_cln_start + 2);
                        temp(1) = s21_max(j);
                        temp(2) = s21_min(j);
                        temp(3) = delta_s21(j);
                        data2str = temp;
                        strs = strcat(ptr_cln1, num2str(xls_str_start - 3), ...
                            ':', ptr_cln2, num2str(xls_str_start - 3));
                        indx = indx + 4;
                        xlswrite(file_path, data2str, strs);
                        end;

                        data2str = delta_Kp;
                        ptr_cln = get_char(2);
                        strs = strcat(ptr_cln, num2str(xls_str_start - 3), ...
                            ':', ptr_cln, num2str(xls_str_start - 3));
                        xlswrite(file_path, data2str, strs);

                        fprintf('данные сохранены в файле:\n');
                        fprintf('%s\n', file_path);

                    end

                    %EOF
