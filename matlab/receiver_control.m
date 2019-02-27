%программа для переключения выводов оснастки
function receiver_control(bit_str, state)
    %bit_str {bit3,bit4,bit5,bit6} /state: {вкл - 1; выкл - 0}
    if bit_str == '0'
        %фазовращатель включен на проход
        serial_obj = com_port_init('COM7');
        com_port_close(serial_obj);
    else

        if bit_str ~= '0'
            %кодировщик команд
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

                    %задаём состояние битов,
                    %не забывая об инверсии выходным буфером
                    if state == 1
                        state_pos = 1;
                        state_neg = 0;
                        state_str = 'вкл';
                        end;

                        if state == 0
                            state_pos = 0;
                            state_neg = 1;
                            state_str = 'выкл';
                            end;
                            %{
                            fprintf('\nсигнал ');
                            fprintf('%s', bit_str);
                            fprintf(' переключен в состояние:');
                            fprintf(' %s\n', state_str);
                            %}
                            cmd_str_pos = strcat('$KE,WR,', num2str(code_pos), ',', num2str(state_pos));
                            cmd_str_neg = strcat('$KE,WR,', num2str(code_neg), ',', num2str(state_neg));
                            %fprintf('%s\n',cmd_str_pos);
                            %fprintf('%s\n',cmd_str_neg);
                            serial_obj = com_port('COM7');
                            fprintf(serial_obj, '%s\r\n', cmd_str_pos);
                            fprintf(serial_obj, '%s\r\n', cmd_str_neg);
                            com_port_close(serial_obj);
                            end;
                            end;

                            clear all;

                        end

                        %EOF
