function [device_pointer,error_flag] = init_pna(preset)
%запуск процедуры инициализации PNA
%fprintf('\n подключение к анализатору цепей...\n');
pna = tcpip('192.168.1.61',5025);
set(pna,'InputBufferSize',10000000);
fopen(pna);

if preset==1
    %сброс параметров
    fprintf(pna,'SYST:PRES');
    query(pna,'*OPC?');
    %удалить все каналы измерений
    fprintf(pna,'CALC:PAR:DEL:ALL');
   
    fprintf(pna,'DISP:WIND2 ON');
    
    %создать измерение S21
    fprintf(pna,'CALC1:PAR:DEF "CH1_S21",S21');
    fprintf(pna,'CALC2:PAR:DEF "CH2_S21",S21');
    fprintf(pna,'CALC1:PAR:DEF "CH1_S11",S11');
    fprintf(pna,'CALC1:PAR:DEF "CH1_S22",S22');

    %загрузка калибровки
    %fprintf(pna,'SENS1:CORR:CSET:ACT "-20dbm_0.9_1.7G_S",1');
    %fprintf(pna,'SENS2:CORR:CSET:ACT "-20dbm_0.9_1.7G_S",1');
    fprintf(pna,'SENS1:CORR:CSET:ACT "-20dBm_1.1-1.4G",1');
    fprintf(pna,'SENS2:CORR:CSET:ACT "-20dBm_1.1-1.4G",1');

   
    %создать график TRACe1 S21 1го измерительного канала
    fprintf(pna,'DISP:WIND1:TRAC1:FEED "CH1_S21"');
    fprintf(pna,'DISP:WIND2:TRAC1:FEED "CH2_S21"');
    fprintf(pna,'DISP:WIND1:TRAC2:FEED "CH1_S11"');
    fprintf(pna,'DISP:WIND1:TRAC3:FEED "CH1_S22"');
 
    fprintf(pna,'SENS1:SWE:MODE CONT');
    fprintf(pna,'SENS2:SWE:MODE CONT');
    
end;


fprintf(pna,'CALC1:FORM MLOG');
fprintf(pna,'DISP:WIND1:TRAC1:Y:SCAL:AUTO');
fprintf(pna,'CALC2:FORM UPH');
fprintf(pna,'DISP:WIND2:TRAC1:Y:SCAL:AUTO');




%fprintf(pna,'CALC3:PAR:SEL "CH1_S11"');
%fprintf(pna,'CALC2:PAR:SEL "CH2_S21"');



%установка частотного диапазона
%fprintf(pna,'SENS1:FREQ:STAR 900.0E6');
%query(pna,'*OPC?');
%fprintf(pna,'SENS1:FREQ:STOP 1700.0E6');
%query(pna,'*OPC?');

%запрос сетки частот, используемой при измерении
%fprintf(pna,'FORM:DATA REAL,32');
%query(pna,'*OPC?');
%fprintf(pna,'SENS1:X?');
%frq = binblockread(pna, 'float32');

%автомасштаб
%fprintf(pna,'DISP:WIND1:TRAC1:Y:SCAL:AUTO');
%query(pna,'*OPC?');
%{
%установка параметров сглаживания
fprintf(pna,'CALC1:SMO:APER 1');
query(pna,'*OPC?');
fprintf(pna,'CALC1:SMO:POIN 20');
query(pna,'*OPC?');
fprintf(pna,'CALC1:SMO OFF');
query(pna,'*OPC?');
%}

%установка параметров усреднения
%fprintf(pna,'SENS1:AVER:CLE');
%query(pna,'*OPC?');
%fprintf(pna,'SENS:AVER:COUN 5');
%query(pna,'*OPC?');
%fprintf(pna,'SENS1:AVER:STAT ON');
%query(pna,'*OPC?');

device_pointer = pna;
error_flag = 0;
