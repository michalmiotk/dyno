from cgitb import enable
import datetime
import queue
import threading

import serial
import serial.tools.list_ports
import pandas as pd

from parse_file import get_df_from_file, is_valid_csv
from data_from_df import add_to_df_with_wheel_torque, add_to_df_power_in_KM, add_to_df_engine_rot_speed

from df_from_uart import df_from_uart_rows
from gui import Gui
from print import print_file
from uart_preprocessing import convert_raw_serial_row_to_filtered_data

import time
import logging as l
l.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', level=l.INFO)

class Program():
    def __init__(self):
        self.gui = Gui(self.connect, self.disconnect, self.save_figure, self.select_file, self.get_coms_description, self.print_chart_method)
        self.serial_object = None
                
        self.uart_process_queue = queue.Queue()

        self.update_gui_enabled = False
        self.uart_df = pd.DataFrame()
        self.gui.mainloop()  

    def get_coms(self):
        return serial.tools.list_ports.comports()

    def get_coms_description(self):
        coms_names = []
        for com in serial.tools.list_ports.comports():
            coms_names.append(com.description)
        return coms_names

    def is_valid_gear_ratio(self):
        try:
            self.gui.get_gear_ratio()
        except ValueError as e:
            l.debug(e)
            l.debug("not valid gear_ratio")
        else:
            return True
    
        return False


    def is_valid_wheel_diameter(self):
        try:
            self.gui.get_wheel_diameter()
        except ValueError as e:
            l.debug(e)
            l.debug("not valid wheel_diameter")
        else:
            return True
        
        return False
    

    def select_file(self):
        
        if not self.is_valid_wheel_diameter():
            self.gui.set_communicates_label("bad wheel diameter format")
            return

        if not self.is_valid_gear_ratio():
            self.gui.set_communicates_label("bad gear ratio format")
            return
    
        filename = self.gui.choose_filename()

        if filename == '':
            self.gui.set_communicates_label("No choosen file")    
            return
        
        if not is_valid_csv(filename):
            self.gui.set_communicates_label("No valid csv")    
            return

        self.gui.clear_communicates_label()

        df = get_df_from_file(filename)
        add_to_df_with_wheel_torque(df, wheel_diameter_in_cm=self.gui.get_wheel_diameter())
        add_to_df_power_in_KM(df)
        add_to_df_engine_rot_speed(df, self.gui.get_wheel_diameter(), self.gui.get_gear_ratio())
        self.gui.figure.update_figure(df)
        self.gui.draw_figure(self.gui.figure.figure)

    def print_chart_method(self):
        if self.gui.figure.is_figure_empty():
            self.gui.set_communicates_label("No figure")
            return
        self.gui.clear_communicates_label()
        figure_filename = 'print.png'
        
        moto_name = self.gui.get_moto_name()
        if moto_name == '':
            self.gui.set_communicates_label("Empty moto name - needed for printing")    
            return
        
        self.gui.figure.add_moto_name_to_figure(moto_name)
        self.gui.figure.save_figure(figure_filename)
        print_file(figure_filename)

    def save_figure(self):
        moto_name = self.gui.get_moto_name()
        if moto_name == '':
            self.gui.set_communicates_label("Empty moto name")    
            return
    
        now_time = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        if self.gui.figure.is_figure_empty():
            self.gui.set_communicates_label("No figure")
            return

        self.gui.clear_communicates_label()
    
        self.gui.figure.save_figure(moto_name + '_' + now_time + '.png')

    
    def update_gui(self, uart_process_q):
        x = 0
        while (self.update_gui_enabled):
            l.debug("update")
            try:
                x += 1
                filter_data_list = []
                while not uart_process_q.empty():
                    raw_data =uart_process_q.get()
                    filter_data = convert_raw_serial_row_to_filtered_data(raw_data)
                    if filter_data[0] < 0 or filter_data[1] < 0:
                        l.info(filter_data)
                    filter_data_list.append(filter_data)
                if len(filter_data_list) == 0:
                    continue

                new_df = df_from_uart_rows(filter_data_list)
                add_to_df_with_wheel_torque(new_df, wheel_diameter_in_cm=self.gui.get_wheel_diameter())
                add_to_df_power_in_KM(new_df)
                add_to_df_engine_rot_speed(new_df, self.gui.get_wheel_diameter(), self.gui.get_gear_ratio())
                l.debug("adding to df done")
                power_in_KM_list = list(new_df['power_in_KM'])
                #assert len(power_in_KM_list) == 1
                self.gui.set_instant_power_label(power_in_KM_list[-1])
                torque_in_Nm_list = list(new_df['torque_on_wheel'])
                #assert len(torque_in_Nm_list) == 1
                self.gui.set_instant_torque_label(torque_in_Nm_list[-1])
                l.debug("setting instant done")
                if self.uart_df.empty:
                    l.info("empty")
                    self.uart_df = pd.concat([self.uart_df, new_df])
                else:
                    l.info("not empty")
                    self.uart_df = self.uart_df.append(new_df)
                l.debug("concat done")
                self.gui.figure.update_figure(self.uart_df)
                l.debug("update figure done")
                self.gui.draw_figure(self.gui.figure.figure)
                l.debug("draw figure done")
                time.sleep(2)
                l.info("update")
            except queue.Empty as e:
                l.debug(e)
            except UnicodeDecodeError as u:
                l.debug("unicode decode error" + str(u))
            except ValueError as v:
                l.debug("Value err" + str(v))

        l.debug("updating gui stopped")
    

    def start_update_gui_thread(self):
        t2 = threading.Thread(target=self.update_gui, args=(self.uart_process_queue,))
        t2.daemon = True
        t2.start()
    

    def get_data(self, queue, serial_obj):
        while serial_obj.isOpen():
            l.debug("begin of reading from serial")
            if serial_obj.inWaiting() > 0:
                try:
                    serial_data = serial_obj.readline()
                    l.debug("serial data" + str(serial_data))
                    
                    queue.put(serial_data)
                except TypeError as e:
                    l.debug("tajp error" + str(e))
                    pass
                

    def connect(self):
        self.uart_df = pd.DataFrame()
        com_description = self.gui.value_inside.get()
        port = self.found_com_path_in_available_coms(com_description) 
        if port is None:
            self.gui.set_communicates_label("can't find " + com_description)
            return
        baud = self.gui.get_baud() 
        try:
            self.serial_object = serial.Serial(port, baud)

        except ValueError:
            l.debug("Enter Baud and Port")
            return

        self.gui.disconnect_btn.state(["!disabled"])
        t1 = threading.Thread(target=self.get_data, args=(self.uart_process_queue, self.serial_object))
        t1.daemon = True
        t1.start()
        self.update_gui_enabled = True
        self.start_update_gui_thread()
        

    def disconnect(self):
        if self.serial_object is not None:
            self.uart_df = pd.DataFrame()
            self.serial_object.close()
            self.update_gui_enabled = False
            self.gui.disconnect_btn.state(["disabled"])
    
    def found_com_path_in_available_coms(self, com_description):
        for com in self.get_coms():
            if str(com.description) == com_description:
                return com.device

        return None

if __name__ == '__main__':
    program = Program()