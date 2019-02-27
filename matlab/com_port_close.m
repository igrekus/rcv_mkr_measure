%закрытие порта USB-модуля
function com_port_close(serial_obj)
%fprintf('закрытие COM-порта\n');
%fprintf(serial_obj, '%s\r\n','$KE,WRA,000000000000000000000000');
fclose(serial_obj) ;
delete(serial_obj);
clear serial_obj;