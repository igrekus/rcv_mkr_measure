import sys

import glfw
import OpenGL.GL as GL

import imgui
from imgui.integrations.glfw import GlfwRenderer

from instumentcontroller import InstrumentController
from measurementresult import MeasurementResult

COLOR_DISABLED = (0.2, 0.2, 0.2)


def main():
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    pna_addr = 'TCPIP0::192.168.0.102::inst0::INSTR'

    instrs = InstrumentController(pna_address=pna_addr)
    result = MeasurementResult(list(), list(), list(), list(), list(), list())

    # io = imgui.get_io()
    # font_new = io.fonts.add_font_from_file_ttf("segoeuil.ttf", 20)
    # impl.refresh_font_texture()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu('File', True):

                clicked_quit, selected_quit = imgui.menu_item(
                    'Quit', 'Ctrl+Q', False, True
                )

                if clicked_quit:
                    exit(10)

                imgui.end_menu()

            imgui.end_main_menu_bar()

        imgui.begin('Instruments', True, imgui.WINDOW_NO_COLLAPSE)

        _, pna_addr = imgui.input_text('PNA address', pna_addr, 50)
        _ = imgui.input_text('PNA', instrs.pna, 50)
        _ = imgui.input_text('Jerome', instrs.jerome, 50)

        connect_clicked = imgui.button('Connect')
        imgui.same_line()

        if not instrs.connected:
            imgui.push_style_color(imgui.COLOR_BUTTON, *COLOR_DISABLED)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *COLOR_DISABLED)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *COLOR_DISABLED)

        measure_clicked = imgui.button('Measure')
        measure_clicked = measure_clicked and instrs.connected

        if not instrs.connected:
            imgui.pop_style_color(3)

        if not result:
            imgui.push_style_color(imgui.COLOR_BUTTON, *COLOR_DISABLED)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *COLOR_DISABLED)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *COLOR_DISABLED)

        imgui.same_line()
        export_clicked = imgui.button('Export')
        export_clicked = export_clicked and result

        if not result:
            imgui.pop_style_color(3)

        imgui.end()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        imgui.render()

        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

        if connect_clicked:
            instrs.connect()

        if measure_clicked:
            instrs.measure()
            result.ready = True

        if export_clicked:
            print('export')

    impl.shutdown()
    glfw.terminate()


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
