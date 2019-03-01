function com_port_close(serial_obj)
    % закрытие порта USB-модуля
    fclose(serial_obj);
    delete(serial_obj);
    clear serial_obj;
end;
