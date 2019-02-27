%clc;
clear all;
fprintf('инициализаци€ com порта\n');
receiver_control('0', 0);
clc;


%{
receiver_control('bit3', 0);
receiver_control('bit4', 0);
receiver_control('bit5', 0);
receiver_control('bit6', 0);
%}
%{
for i = 1:1
    receiver_control('bit6', 0);
    %pause(1);
    receiver_control('bit6', 1);
    %pause(1);
end; 
receiver_control('bit6', 0);
%}
%index = [0 1 2 4 8];%основные состо€ни€
index = 0:15;%все состо€ни€
%index = [0 1];

 %fprintf('\n');
for i = 1:length(index)
    j = index(i);
    fprintf('состо€ние є ');
    fprintf('%s\n',num2str(j));
    fprintf('сдвиг фазы: ');

 switch j
        case 0
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            phs_state = 0;
        case 1
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            phs_state = 22.5;
        case 2
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            phs_state = 45;
        case 3
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            receiver_control('bit5', 0);
            receiver_control('bit6', 0);
            phs_state = 22.5+45;
        case 4
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            phs_state = 90;
        case 5
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            phs_state = 22.5+90;
        case 6
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            phs_state = 45+90;
        case 7
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            receiver_control('bit5', 1);
            receiver_control('bit6', 0);
            phs_state = 22.5+45+90;
        case 8
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            phs_state = 180;
        case 9
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            phs_state = 22.5+180;
        case 10
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            phs_state = 45+180;
        case 11
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            receiver_control('bit5', 0);
            receiver_control('bit6', 1);
            phs_state = 22.5+45+180;
        case 12
            receiver_control('bit3', 0);
            receiver_control('bit4', 0);
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            phs_state = 90+180;
        case 13
            receiver_control('bit3', 1);
            receiver_control('bit4', 0);
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            phs_state = 22.5+90+180;
        case 14
            receiver_control('bit3', 0);
            receiver_control('bit4', 1);
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            phs_state = 45+90+180;
        case 15
            receiver_control('bit3', 1);
            receiver_control('bit4', 1);
            receiver_control('bit5', 1);
            receiver_control('bit6', 1);
            phs_state = 22.5+45+90+180;
            fprintf('сдвиг фазы: ');
 end;
 fprintf('%3.2f',phs_state);
 fprintf(' град.\n');
 if i < length(index)
     fprintf('нажмите пробел\n');
     fprintf('\n');
     pause; 
 end;
 if i == length(index)
     fprintf('\n');
     fprintf('завершено\n');
 end;
 
end;
 





