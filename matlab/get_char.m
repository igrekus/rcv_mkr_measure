function [str] = get_char(num)
    str = '';
    %num = 53;
    ofs = 96;
    N = 26;
    celoe = fix(num ./ N);
    indx = num - celoe * N;

    if (indx == 0) && (celoe ~= 0)
        indx = N;
        celoe = celoe - 1;
        end;

        if celoe > 0
            str = char(celoe + ofs);
            end;

            str = strcat(str, char(indx + ofs));
            %fprintf('%s\n',str);
