%программа для переключения выводов оснастки
function receiver_control_test

serial_obj = com_port('COM7');

clc;
%{
fprintf('IDC pin1\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,8,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,8,0');

fprintf('IDC pin2\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,7,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,7,0');

fprintf('IDC pin3\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,10,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,10,0');

fprintf('IDC pin4\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,9,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,9,0');

fprintf('IDC pin5\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,14,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,14,0');

fprintf('IDC pin6\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,13,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,13,0');

fprintf('IDC pin7\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,12,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,12,0');

fprintf('IDC pin8\n');  
fprintf(serial_obj, '%s\r\n','$KE,WR,11,1');
pause;
fprintf(serial_obj, '%s\r\n','$KE,WR,11,0');
%}

com_port_close(serial_obj);
end
%EOF
