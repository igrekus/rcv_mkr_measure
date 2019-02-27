%function Untitled
  clc;
  clear all;
  states = 0:2;
  N_set = 100;
  num_states  = (length(find(states,16,'first'))+1);
  freq = zeros(1,N_set);
  gamma_inp = zeros(num_states,N_set);
  gamma_outp = zeros(num_states,N_set);
  ms21 = zeros(num_states,N_set);
  ps21 = zeros(num_states,N_set);
 
  dir = 'D:\Martynov\MatLab\receiver_module_otd7_v2';
  file_name = 'results2.xlsx';
  file_path = strcat(dir,'\',file_name);
  
  N = length(freq);
  ofs = 2;    
  
  %��������� ����������
 
  B = cell(4,num_states+ofs);%��������� ��� ������������� ���������� �����

  C = cell(N+10,16*4+2);%��������� ��� ������� �����
  sheet = 1;
  xlRange = 'A1';
  xlswrite(file_path,C,sheet,xlRange);
  clear C;
  
  t = clock;
  str_d = num2str(t(3));
  str_mth = num2str(t(2));
  str_y = num2str(t(1));
  str_h = num2str(t(4));
  str_m = num2str(t(5));
  str_time = strcat(str_h,':',str_m);
  str_data = strcat(str_d,'.',str_mth,'.',str_y,'�.');
  clear str_d str_mth str_y str_h str_m t;
        
 title = '������� ������ ���';
 B{1,1} = title;
 B{1,3} = strcat('����: ',str_data,' �����: ',str_time);
 B{3,1} = '�����';
 B{3,2} = '�������, ���';
 i = 3;
 k = 1;
 for j = 1:num_states%�������
      k = j*4-3+ofs;
      B{3,k} = 'gamma_inp';
      B{3,k+1} = 'gamma_outp';
      B{3,k+2} = 'mag(S21),��';
      B{3,k+3} = 'arg(S21),��.';
      B{4,k} = strcat(num2str(states(j)),' ��.');
      B{4,k+1} = strcat(num2str(states(j)),' ��.');
      B{4,k+2} = strcat(num2str(states(j)),' ��.');
      B{4,k+3} = strcat(num2str(states(j)),' ��.');
 end;

xlswrite(file_path,B,sheet,xlRange);

D = cell(N,4*num_states + 2);
for i = 1:N
    D{i,2} = freq(i)*1e-6; 
    D{i,1} = num2str(i,'%3.0d');
end;
for j = 1:(num_states)
    k = j*4-3 + ofs;
    for i = 1:N
        D{i,k} = gamma_inp(j,i);   
        D{i,k+1} = gamma_outp(j,i);   
        D{i,k+2} = ms21(j,i);   
        D{i,k+3} = ps21(j,i);   
    end;
end;
xlRange = 'A5';
xlswrite(file_path,D,sheet,xlRange);
       
fprintf('������ ��������� � �����:\n');
fprintf('%s\n',file_path);
      
%end
%EOF