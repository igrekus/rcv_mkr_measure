function init_file (file_path, freq, states)
%freq, gamma_inp, gamma_outp, mS21, pS21
  xls_str_start = 6;%перва€ строка дл€ записи значений
  %xls_cln_start = 1;%первый столбец дл€ записи значений
  indx = 0;%индекс смещени€ по колонкам

  N = length(freq);
  freq = freq*1e-6;
  data2str = {'N' 'freq,MHz'};
  ptr_cln1 = get_char(1);
  ptr_cln2 = get_char(2);
  strs = strcat(ptr_cln1,num2str(xls_str_start-1),':',ptr_cln2,num2str(xls_str_start-1));
  xlswrite(file_path,data2str,strs); 
  
  data2str = freq;
  ptr_cln1 = get_char(2);
  strs = strcat(ptr_cln1,num2str(xls_str_start),':',ptr_cln1,num2str(xls_str_start+N-1));
  xlswrite(file_path,data2str,strs); 
  
  num = 1:1:N;
  data2str = num(:);
  ptr_cln1 = get_char(1);
  strs = strcat(ptr_cln1,num2str(xls_str_start),':',ptr_cln1,num2str(xls_str_start+N-1));
  xlswrite(file_path,data2str,strs); 
        
  num_states  = length(find(states,16,'first'))+1;
  indx = 3;
  for i = 1:num_states
    data2str = states(i);
    ptr_cln1 = get_char(indx);
    ptr_cln2 = get_char(indx + 3);
    strs = strcat(ptr_cln1,num2str(xls_str_start-2),...
              ':',ptr_cln2,num2str(xls_str_start-2));
    indx = indx + 4;
    xlswrite(file_path,data2str,strs);    
  end;
  
  indx = 3;
  data2str = {'gamma_inp' 'gamma_outp' 'mag(S21),dB' 'arg(S21),grad'};
  for i = 1:num_states
    ptr_cln1 = get_char(indx);
    ptr_cln2 = get_char(indx+3);
    strs = strcat(ptr_cln1,num2str(xls_str_start-1),...
        ':',ptr_cln2,num2str(xls_str_start-1));
    indx = indx + 4;
    xlswrite(file_path,data2str,strs);    
  end;
   
  indx = 3;
  data2str = {'maxS21,дЅ' 'minS21,дЅ' 'max(S21)-min(S21),дЅ'};
  for i = 1:num_states
    ptr_cln1 = get_char(indx);
    ptr_cln2 = get_char(indx+2);
    strs = strcat(ptr_cln1,num2str(xls_str_start-4),...
        ':',ptr_cln2,num2str(xls_str_start-4));
    indx = indx + 4;
    xlswrite(file_path,data2str,strs);    
  end;
  
  data2str = {'delta_Kp, дЅ'};
  ptr_cln1 = get_char(2);
  strs = strcat(ptr_cln1,num2str(xls_str_start-4),...
        ':',ptr_cln1,num2str(xls_str_start-4));
  xlswrite(file_path,data2str,strs);    
  
  data2str = {'сдвиг фазы, град.'};
  ptr_cln1 = get_char(2);
  strs = strcat(ptr_cln1,num2str(xls_str_start-2),...
        ':',ptr_cln1,num2str(xls_str_start-2));
  xlswrite(file_path,data2str,strs);    
  
        
      fprintf('файл инициализирован:\n');
      fprintf('%s\n',file_path);
      clear all;
end
%EOF