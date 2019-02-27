function [pointer] = com_port(str_com_port)

    serial_obj = serial(str_com_port);
    serial_obj.Baudrate = 115200;
    set(serial_obj, 'Parity', 'none');
    set(serial_obj, 'Databits', 8);
    set(serial_obj, 'StopBits', 1);
    set(serial_obj, 'Terminator', 'LF');
    set(serial_obj, 'InputBufferSize', 512);
    set(serial_obj, 'OutputBufferSize', 512);
    set(serial_obj, 'ReadAsyncMode', 'Continuous');
    set(serial_obj, 'Timeout', 10);
    fopen(serial_obj);
    %проверка соединения
    fprintf(serial_obj, '%s\r\n', '$KE');
    ret = fscanf(serial_obj, '%s');

    if (ret == '#OK')
        %fprintf('COM-порт открыт\n');
        pointer = serial_obj;
    else
        fprintf('ошибка при настройке связи с модулем\n');
        pointer = -1;
        %break;
        end;
