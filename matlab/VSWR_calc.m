function [ outp_G ] = VSWR_calc(inp_S)

modS = power(10,inp_S./20);
outp_G = (1+modS)./(1-modS);
clear modS;

end

