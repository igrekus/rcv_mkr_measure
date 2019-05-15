import matplotlib
matplotlib.use('TkAgg')

from matplotlib import pyplot as plot
from matplotlib.figure import Figure

import glfw
import OpenGL.GL as GL
from imgui.integrations.glfw import GlfwRenderer
from imgui_datascience import *

from attr import attrs, attrib

from excelresultfinal import ExcelResultFinal
from instumentcontroller import InstrumentController
from measurementresult import MeasurementResult


@attrs
class UiState:
    clicked_quit = attrib(default=False)
    clicked_connect = attrib(default=False)
    clicked_measure = attrib(default=False)
    clicked_export = attrib(default=False)


def main():
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    # pna_addr = 'TCPIP0::192.168.0.102::5025::SOCKET'
    pna_addr = 'GPIB0::10::INSTR'

    ui = UiState()
    instrs = InstrumentController(pna_address=pna_addr)
    result = MeasurementResult()

    # io = imgui.get_io()
    # font_new = io.fonts.add_font_from_file_ttf("segoeuil.ttf", 20)
    # impl.refresh_font_texture()

    figure_s21: Figure = plot.figure()
    figure_swr_in: Figure = plot.figure()
    figure_swr_out: Figure = plot.figure()
    figure_phases: Figure = plot.figure()
    figure_phase_err: Figure = plot.figure()

    current_raw_state = 0
    current_plot_data_state = 0

    plots_ready = False

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        ui.clicked_quit, _ = draw_main_menu()

        ui.pna_addr, ui.clicked_connect, ui.clicked_measure, ui.clicked_export = draw_instruments_windows(instrs, pna_addr, result)

        current_raw_state = draw_raw_data_window(current_raw_state, result)

        if plots_ready:
            imgui.begin('Pow plots')

            imgui_fig.fig(figure_swr_in, 500, 350, 'SWR in')
            imgui.same_line()
            imgui_fig.fig(figure_s21, 500, 350, 'S21')
            imgui_fig.fig(figure_swr_out, 500, 350, 'SWR out')

            imgui.end()

            imgui.begin('Phase plots')

            imgui_fig.fig(figure_phases, 500, 350, 'Phase')
            imgui_fig.fig(figure_phase_err, 500, 350, 'Phase err')

            imgui.end()

        if result:
            imgui.begin('Stats')

            imgui.text(f'delta Kp = {result._delta_Kp:.02f}')
            imgui.text(f'SWR max in = {result._swr_in_max:.02f}')
            imgui.text(f'SWR max out = {result._swr_out_max:.02f}')
            imgui.text(f'phase err = {result._phase_err_min}..{result._phase_err_max}')
            imgui.text(f'S21 max = {result._s21_MAX:.02f}')
            imgui.text(f'S21 delta max = {result._s21_delta_max:.02f}')

            imgui.text(f'S21 deltas')
            imgui.columns(16)
            for state in result._states:
                imgui.text(f'{state:.01f}')
                imgui.next_column()
            for delta in result._s21_deltas:
                imgui.text(f'{delta:.02f}')
                imgui.next_column()
            imgui.columns(1)

            imgui.end()

            current_plot_data_state = draw_plot_data_window(current_plot_data_state, result)

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

            plot_data(figure_s21, result.freqs, result._mag_s21s, 'F, GHz', 'S21')
            plot_data(figure_swr_in, result.freqs, result._gamma_input, 'F, GHz', 'SWR in, dB')
            plot_data(figure_swr_out, result.freqs, result._gamma_output, 'F, GHz', 'SWR out, dB')
            plot_data(figure_phases, result.freqs, result._phases, 'F, GHz', 'Phase, deg')
            plot_data(figure_phase_err, result.freqs, result._phase_errs, 'F, GHz', 'Phase err, deg')

            plots_ready = True

        if ui.clicked_export:
            excel = ExcelResultFinal(result)
            excel.save()

        if ui.clicked_quit:
            exit(0)

    impl.shutdown()
    glfw.terminate()


def plot_data(figure, xs, yss, xlabel, ylabel):
    # ax.set_facecolor((1.0, 0.47, 0.42))
    figure.clear()
    ax = figure.gca()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(b=True, which='major', color='0.5', linestyle='--')
    for ys in yss:
        ax.plot(xs, ys)


def draw_raw_data_window(current_raw_state, result):
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
    if result:
        draw_raw_table(result.freqs, result.raw_datasets[list(result.raw_datasets)[current_raw_state]], 5)
    imgui.end()
    return current_raw_state


def draw_plot_data_window(current_plot_data_state, result):
    imgui.begin('Plot data', False)
    _, current_plot_data_state = imgui.combo('States##1', current_plot_data_state, list(map(str, result._states))[1:])
    imgui.columns(7, border=False)
    imgui.separator()
    imgui.text('#')
    imgui.next_column()
    imgui.text('F')
    imgui.next_column()
    imgui.text('S21')
    imgui.next_column()
    imgui.text('SWR in')
    imgui.next_column()
    imgui.text('SWR out')
    imgui.next_column()
    imgui.text('Phase')
    imgui.next_column()
    imgui.text('Ph err')
    imgui.next_column()
    imgui.columns(1)
    if result:
        draw_table(result.freqs, result.datasets[list(result.datasets)[current_plot_data_state]], 6)
    imgui.end()
    return current_plot_data_state


def draw_raw_table(freqs, dataset, cols):
    s21_mags, s21_phs, s11_mags, s22_mags = dataset
    imgui.begin_child('RawScrollRegion', 0.0, 0.0, False)
    imgui.columns(cols + 1, border=False)
    for index, frq in enumerate(freqs):
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


def draw_table(freqs, dataset, cols):
    s21s, swr_ins, swr_outs, phases, phase_errs = dataset
    imgui.begin_child('ScrollRegion', 0.0, 0.0, False)
    imgui.columns(cols + 1, border=False)
    for index, frq in enumerate(freqs):
        imgui.text(str(index + 1))
        imgui.next_column()
        imgui.text(str(frq))
        imgui.next_column()
        imgui.text(str(s21s[index]))
        imgui.next_column()
        imgui.text(str(swr_ins[index]))
        imgui.next_column()
        imgui.text(str(swr_outs[index]))
        imgui.next_column()
        imgui.text(str(phases[index]))
        imgui.next_column()
        imgui.text(str(phase_errs[index]))
        imgui.next_column()
    imgui.end_child()
    imgui.columns(1)


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


def draw_plot():
    draw_list = imgui.get_window_draw_list()

    win_x, win_y = imgui.get_window_position()

    rgba_color = imgui.get_color_u32_rgba(1, 1, 1, 1)
    draw_list.add_line(win_x + 10, win_y + 10, win_x + 200, win_y + 200, rgba_color)


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
