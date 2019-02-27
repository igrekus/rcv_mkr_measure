function [pointer] = com_port_init(str_com_port)

 serial_obj = serial(str_com_port) ;
 serial_obj.Baudrate = 115200;
 set(serial_obj, 'Parity', 'none') ;
 set(serial_obj, 'Databits', 8) ;
 set(serial_obj, 'StopBits', 1) ;
 set(serial_obj, 'Terminator', 'LF') ;
 set(serial_obj, 'InputBufferSize', 512) ;
 set(serial_obj, 'OutputBufferSize', 512) ;  
 set(serial_obj, 'ReadAsyncMode', 'Continuous') ;
 set(serial_obj, 'Timeout', 10) ;
 fopen(serial_obj) ;
 %проверка соединения
 fprintf(serial_obj, '%s\r\n','$KE');
 ret = fscanf(serial_obj, '%s') ;              
 if (ret=='#OK') 
      fprintf('COM-порт открыт\n'); 
      pointer = serial_obj;
     %настройка выходов
     %OPEN COLLECTOR INVERT.
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,7,0');
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,8,0');
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,9,0');
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,10,0');
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,11,0');
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,12,0');
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,13,0');
     fprintf(serial_obj, '%s\r\n','$KE,IO,SET,14,0');
     fprintf(serial_obj, '%s\r\n','$KE,WRA,000000010101010000000000');
 else
     fprintf('ошибка при настройке связи с модулем\n'); 
     %break;
     %аварийное завершение программы при условии, что 
     %соединение не установлено
 end;