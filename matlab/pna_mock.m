function init_pna(preset)
    if preset == 1
		disp('SYST:PRES');        
		disp('*OPC?');
		disp('CALC:PAR:DEL:ALL');
		disp('DISP:WIND2 ON');
		disp('CALC1:PAR:DEF "CH1_S21",S21');
		disp('CALC2:PAR:DEF "CH2_S21",S21');
		disp('CALC1:PAR:DEF "CH1_S11",S11');
		disp('CALC1:PAR:DEF "CH1_S22",S22');
		disp('SENS1:CORR:CSET:ACT "-20dBm_1.1-1.4G",1');
		disp('SENS2:CORR:CSET:ACT "-20dBm_1.1-1.4G",1');
		disp('DISP:WIND1:TRAC1:FEED "CH1_S21"');
		disp('DISP:WIND2:TRAC1:FEED "CH2_S21"');
		disp('DISP:WIND1:TRAC2:FEED "CH1_S11"');
		disp('DISP:WIND1:TRAC3:FEED "CH1_S22"');
		disp('SENS1:SWE:MODE CONT');
		disp('SENS2:SWE:MODE CONT');
    end;
	disp('CALC1:FORM MLOG');
	disp('DISP:WIND1:TRAC1:Y:SCAL:AUTO');
	disp('CALC2:FORM UPH');
	disp('DISP:WIND2:TRAC1:Y:SCAL:AUTO');
end;

init_pna(1);

disp('CALC1:PAR:SEL "CH1_S21"');
disp('FORM:DATA REAL,32');
disp('SENS1:X?');

index = 0:15;
for i = 1:length(index)% i = [1..16]
    j = index(i); % j = [0..15]
	disp('CALC1:PAR:SEL "CH1_S21"');
	disp('CALC1:DATA? FDATA');
	disp('CALC2:PAR:SEL "CH2_S21"');
	disp('CALC2:DATA? FDATA');
	disp('CALC1:PAR:SEL "CH1_S11"');
	disp('CALC1:DATA? FDATA');
	disp('CALC1:PAR:SEL "CH1_S22"');
	disp('CALC1:DATA? FDATA');
end;
