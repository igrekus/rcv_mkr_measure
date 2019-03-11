function receiver_control(bit_str, state)
    if bit_str == '0'
        com_port_init('COM7');
    else

        if bit_str ~= '0'
            switch bit_str
                case 'bit6'
                    code_pos = 7;
                    code_neg = 8;
                case 'bit5'
                    code_pos = 9;
                    code_neg = 10;
                case 'bit4'
                    code_pos = 13;
                    code_neg = 14;
                case 'bit3'
                    code_pos = 11;
                    code_neg = 12;
                    end;

                    if state == 1
                        state_pos = 1;
                        state_neg = 0;
                    end;

                    if state == 0
                        state_pos = 0;
                        state_neg = 1;
                    end;
                    cmd_str_pos = strcat('$KE,WR,', num2str(code_pos), ',', num2str(state_pos), '\r\n');
                    cmd_str_neg = strcat('$KE,WR,', num2str(code_neg), ',', num2str(state_neg), '\r\n');
                    disp(cmd_str_pos);
                    disp(cmd_str_neg);
                end;
            end;
end;

function com_port_init(str_com_port)
    disp('$KE,IO,SET,7,0\r\n');
    disp('$KE,IO,SET,8,0\r\n');
    disp('$KE,IO,SET,9,0\r\n');
    disp('$KE,IO,SET,10,0\r\n');
    disp('$KE,IO,SET,11,0\r\n');
    disp('$KE,IO,SET,12,0\r\n');
    disp('$KE,IO,SET,13,0\r\n');
    disp('$KE,IO,SET,14,0\r\n');
    disp('$KE,WRA,000000010101010000000000\r\n');
end;

receiver_control('0', 0);
index = 0:15;
for i = 1:length(index)
    j = index(i);

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
end;

            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
