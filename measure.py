import matplotlib
from attr import attrs, attrib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plot

import glfw
import OpenGL.GL as GL

# import imgui
from imgui.integrations.glfw import GlfwRenderer

from instumentcontroller import InstrumentController
from measurementresult import MeasurementResult

import numpy as np

from imgui_datascience import *

COLOR_DISABLED = (0.2, 0.2, 0.2)


@attrs
class UiState:
    clicked_quit = attrib(default=False)
    clicked_connect = attrib(default=False)
    clicked_measure = attrib(default=False)
    clicked_export = attrib(default=False)


def main():
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    pna_addr = 'TCPIP0::192.168.0.102::inst0::INSTR'

    ui = UiState()
    instrs = InstrumentController(pna_address=pna_addr)
    result = MeasurementResult()

    # io = imgui.get_io()
    # font_new = io.fonts.add_font_from_file_ttf("segoeuil.ttf", 20)
    # impl.refresh_font_texture()

    figure = plot.figure()
    x = np.arange(0.1, 100, 0.1)
    y = np.sin(x) / x
    plot.plot(x, y)

    current_raw_state = 0

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        ui.clicked_quit, _ = draw_main_menu()

        ui.pna_addr, ui.clicked_connect, ui.clicked_measure, ui.clicked_export = draw_instruments_windows(instrs, pna_addr, result)

        imgui.set_next_window_position(500, 50, imgui.ONCE)
        imgui.set_next_window_size(500, 500, imgui.ONCE)

        imgui.begin('Raw data', False)

        _, current_raw_state = imgui.combo('States', current_raw_state, list(map(str, result._states)))

        imgui.columns(6, border=False)
        imgui.separator()
        imgui.text('#')
        imgui.next_column()
        imgui.text('F')
        imgui.next_column()
        imgui.text('S21_mag')
        imgui.next_column()
        imgui.text('S21_phs')
        imgui.next_column()
        imgui.text('S11_mag')
        imgui.next_column()
        imgui.text('S22_mag')
        imgui.next_column()
        imgui.columns(1)

        if result.datasets:
            imgui.begin_child('RawScrollRegion', 0.0, 0.0, False)
            imgui.columns(6, border=False)
            s21_mags, s21_phs, s11_mags, s22_mags = result.datasets[list(result.datasets)[current_raw_state]]
            for index, frq in enumerate(result._freqs):
                imgui.text(str(index + 1))
                imgui.next_column()
                imgui.text(str(frq))
                imgui.next_column()
                imgui.text(str(s21_mags[index]))
                imgui.next_column()
                imgui.text(str(s21_phs[index]))
                imgui.next_column()
                imgui.text(str(s11_mags[index]))
                imgui.next_column()
                imgui.text(str(s22_mags[index]))
                imgui.next_column()
            imgui.end_child()

        imgui.columns(1)
        imgui.end()

        imgui.set_next_window_position(50, 200, imgui.ONCE)
        imgui.set_next_window_size(500, 500, imgui.ONCE)

        # imgui.begin('Stats', False, 0)
        #
        # imgui.end()

        # imgui.begin('S21/f')

        if result.datasets:
            imgui.begin('Plots')

            img = np.array([result._freqs, s21_mags], dtype=np.float64)

            imgui_fig.fig(figure, 500, 500, 'S21')

            imgui.end()

        # imgui.end()

        imgui.show_metrics_window()
        # imgui.show_demo_window()
        # 1st plot - freq x swr_in
        # 2nd plot - freq x s21_mag
        # 3rd plot - freq x swr_out
        # 4th plot - freq x phase
        # 5th plot - freq x ph_err

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        imgui.render()

        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

        if ui.clicked_connect:
            instrs.connect()

        if ui.clicked_measure:
            result.invalidate()
            instrs.measure()
            result.raw_data = instrs.measurements
            result.process()

        if ui.clicked_export:
            print('export')

        if ui.clicked_quit:
            exit(0)

    impl.shutdown()
    glfw.terminate()


def draw_instruments_windows(instrs, pna_addr, result):
    imgui.begin('Instruments', False, imgui.WINDOW_NO_COLLAPSE)
    _, new_addr = imgui.input_text('PNA address', pna_addr, 50)
    imgui.input_text('PNA', instrs.pna, 50)
    imgui.input_text('Jerome', instrs.jerome, 50)
    clicked_connect = imgui.button('Connect')
    clicked_measure = False
    clicked_export = False
    if instrs.connected:
        imgui.same_line()
        clicked_measure = imgui.button('Measure')
    if result:
        imgui.same_line()
        clicked_export = imgui.button('Export')
    imgui.end()

    return new_addr, clicked_connect, clicked_measure, clicked_export


def draw_main_menu():
    clicked_quit, selected_quit = False, False

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu('File', True):

            clicked_quit, selected_quit = imgui.menu_item(
                'Quit', 'Ctrl+Q', False, True
            )

            if clicked_quit:
                exit(10)

            imgui.end_menu()

        imgui.end_main_menu_bar()

    return clicked_quit, selected_quit


def impl_glfw_init():
    width, height = 1280, 720
    window_name = 'Receiver measure'

    if not glfw.init():
        print('Could not initialize OpenGL context')
        exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)

    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print('Could not initialize Window')
        exit(1)

    return window


if __name__ == '__main__':
    main()
