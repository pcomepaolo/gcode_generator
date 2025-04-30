import marimo

__generated_with = "0.12.8"
app = marimo.App(
    width="medium",
    app_title="G-Code Generator",
    layout_file="layouts/gcode_generator.grid.json",
    css_file="src/style.css",
)


@app.cell
def import_libraries():
    import marimo as mo
    from src.sketch import Sketch
    from src.gcode import GCodeGenerator
    from src.plotter import plotting_functions
    from src.printer import Nozzle,Printer
    from src.settings import SettingsManager
    from src.shapes import Segment, Serpentine, set_position
    return (
        GCodeGenerator,
        Nozzle,
        Printer,
        Segment,
        Serpentine,
        SettingsManager,
        Sketch,
        mo,
        plotting_functions,
        set_position,
    )


@app.cell
def _(mo):
    mo.callout(
        mo.md("""#G-Code Generator"""),
        kind='info'
    )
    return


@app.cell
def settings_manager_instantiation(SettingsManager):
    settings = SettingsManager()
    return (settings,)


@app.cell
def sketch_settings(mo, settings):
    layer_width = mo.ui.number(
        label='trace width, mm',
        start= 0,
        value = settings.value('layer_width'),
        step=0.01
    )
    layer_height = mo.ui.number(
        label='trace height, mm',
        start= 0,
        value = settings.value('layer_height'),
        step=0.01
    )
    number_of_layers = mo.ui.number(
        label='number of layers',
        start = 1,
        value = settings.value('number_of_layers'),
        step=1
    )
    print_segment = mo.ui.checkbox(
        label = 'Print suspended segment',
        value = settings.value('print_segment')
    )
    sketch_settings = mo.md('''
    <table>
    <tr><td>{layer_width}</td></tr>
    <tr><td>{layer_height}</td></tr>
    <tr><td>{number_of_layers}</td></tr>
    <tr><td>{print_segment}</td></tr>
    </table>
    ''').batch(
        layer_width=layer_width,
        layer_height=layer_height,
        number_of_layers=number_of_layers,
        print_segment=print_segment
    )
    return (
        layer_height,
        layer_width,
        number_of_layers,
        print_segment,
        sketch_settings,
    )


@app.cell
def serpentine_settings(mo, settings):
    centered_serpentine = mo.ui.checkbox(
        label="centered serpentine", value=settings.value("centered_serpentine")
    )
    y_width = mo.ui.number(
        label="y width, mm",
        start=1,
        value=settings.value("y_width"),
        )
    x_width = mo.ui.number(
        label="x maximum width, mm",
        start=1,
        value=settings.value("x_width"),
    )
    constant_pitch = mo.ui.checkbox(
        label="constant pitch, mm",
        value=settings.value("constant_pitch"),
    )
    min_pitch = mo.ui.number(
        label="minimum pitch, mm",
        start=1,
        value=settings.value("min_pitch"),
    )
    x_pos = mo.ui.number(label="x position, mm", value=settings.value("x_pos"))
    y_pos = mo.ui.number(label="y position, mm", value=settings.value("y_pos"))

    serpentine_settings = mo.md("""
    <table>
    <tr><td>{y_width}</td></tr>
    <tr><td>{x_width}</td></tr>
    <tr><td>{constant_pitch}</td></tr>
    <tr><td>{min_pitch}</td></tr>
    <tr><td>{x_pos}</td></tr>
    <tr><td>{y_pos}</td></tr>
    <tr><td>{centered_serpentine}</td></tr>
    </table>

    """).batch(
        y_width=y_width,
        x_width=x_width,
        constant_pitch=constant_pitch,
        min_pitch=min_pitch,
        x_pos=x_pos,
        y_pos=y_pos,
        centered_serpentine=centered_serpentine,
    )
    return (
        centered_serpentine,
        constant_pitch,
        min_pitch,
        serpentine_settings,
        x_pos,
        x_width,
        y_pos,
        y_width,
    )


@app.cell
def segment_settings(mo, settings):
    segment_y_pos = mo.ui.number(
        label='relative y position',
        value=settings.value('segment_y_pos'),
        start=0.1,
        stop=0.9,
        step=0.1,
    )
    centered_segment = mo.ui.checkbox(
        label='centered segment',
        value = settings.value('centered_segment')
    )
    segment_settings = mo.md('''
    <table>
    <tr><td>{segment_y_pos}</td></tr>
    <tr><td>{centered_segment}</td></tr>
    </table>
    ''').batch(
        segment_y_pos=segment_y_pos,
        centered_segment=centered_segment
    )
    return centered_segment, segment_settings, segment_y_pos


@app.cell
def printer_settings(mo, settings):
    plate_shape = mo.ui.radio(
        options=['rounded','squared'],
        value=settings.value('plate_shape'),
        label='shape of the printing plate',
    )
    plate_size = mo.ui.number(
        label='plate size, mm',
        value=settings.value('plate_size')
    )
    x_home = mo.ui.number(
        label='x home, mm',
        value=settings.value('x_home')
    )
    y_home = mo.ui.number(
        label='y home, mm',
        value=settings.value('y_home')
    )
    z_home = mo.ui.number(
        label='z home, mm',
        value=settings.value('z_home')
    )
    first_inlet_diameter = mo.ui.number(
        label='lower inlet diameter, mm',
        start=0.1,
        step=0.01,
        value=settings.value('first_inlet_diameter')
    )
    last_inlet_diameter = mo.ui.number(
        label='higher inlet diameter, mm',
        start=0.1,
        step=0.01,
        value=settings.value('last_inlet_diameter')
    )
    retraction = mo.ui.number(
        label='retraction, mm',
        value = settings.value('retraction')
    )
    lift_distance = mo.ui.number(
        label='lift distance, mm',
        value = settings.value('lift_distance')
    )
    moving_speed = mo.ui.number(
        label='moving speed, mm/min',
        value = settings.value('moving_speed')
    )
    printing_speed = mo.ui.number(
        label='printing speed, mm/min',
        value = settings.value('printing_speed')
    )
    purge_nozzle = mo.ui.checkbox(
        label='purge the nozzle',
        value=settings.value('purge_nozzle'),
    )
    printer_settings = mo.md('''
    <table>
    <tr><td>{plate_shape}</td></tr>
    <tr><td>{plate_size}</td></tr>
    <tr><td>{x_home}</td></tr>
    <tr><td>{y_home}</td></tr>
    <tr><td>{z_home}</td></tr>
    <tr><td>{first_inlet_diameter}</td></tr>
    <tr><td>{last_inlet_diameter}</td></tr>
    <tr><td>{retraction}</td></tr>
    <tr><td>{lift_distance}</td></tr>
    <tr><td>{moving_speed}</td></tr>
    <tr><td>{printing_speed}</td></tr>
    <tr><td>{purge_nozzle}</td></tr>
    </table>
    ''').batch(
        plate_shape=plate_shape,
        plate_size=plate_size,
        x_home=x_home,
        y_home=y_home,
        z_home=z_home,    
        retraction=retraction,
        lift_distance=lift_distance,
        moving_speed=moving_speed,
        printing_speed=printing_speed,
        first_inlet_diameter=first_inlet_diameter,
        last_inlet_diameter=last_inlet_diameter,
        purge_nozzle=purge_nozzle,
    )
    return (
        first_inlet_diameter,
        last_inlet_diameter,
        lift_distance,
        moving_speed,
        plate_shape,
        plate_size,
        printer_settings,
        printing_speed,
        purge_nozzle,
        retraction,
        x_home,
        y_home,
        z_home,
    )


@app.cell
def purge_segment_settings(mo, settings):
    purge_x = mo.ui.number(
        label='x position, mm',
        value=settings.value('purge_x'),
        step=1,
    )
    purge_y = mo.ui.number(
        label='y position, mm',
        value=settings.value('purge_y'),
        step=1,
    )
    length = mo.ui.number(
        label='length, mm',
        value=settings.value('length'),
        start=0,
        step=1,
    )
    purge_inlet_diameter = mo.ui.number(
        label='inlet diameter, mm',
        start=0,
        step=0.1,
        value=settings.value('purge_inlet_diameter'),
    )
    is_vertical = mo.ui.checkbox(
        label='vertical segment',
        value=settings.value('is_vertical'),
    )
    purge_segment_settings = mo.md('''
    <table>
    <tr><td>{purge_x}</td></tr>
    <tr><td>{purge_y}</td></tr>
    <tr><td>{length}</td></tr>
    <tr><td>{purge_inlet_diameter}</td></tr>
    <tr><td>{is_vertical}</td></tr>
    </table>
    ''').batch(
        purge_x=purge_x,
        purge_y=purge_y,
        length=length,
        purge_inlet_diameter=purge_inlet_diameter,
        is_vertical=is_vertical,
    )
    return (
        is_vertical,
        length,
        purge_inlet_diameter,
        purge_segment_settings,
        purge_x,
        purge_y,
    )


@app.cell
def gcode_settings(mo, settings):
    gcode_head = mo.ui.text_area(
        label='G-Code head',
        value=settings.gcode_head,
        full_width=True,
        rows=10
    )
    gcode_tail = mo.ui.text_area(
        label='G-Code tail',
        value=settings.gcode_tail,
        full_width=True,
        rows=10
    )
    filename = mo.ui.text(
        label='G-Code filename',
        value=settings.value('filename'),
        full_width=True,
    )
    gcode_settings = mo.md('''
    {filename}</br>
    {gcode_head}</br>
    {gcode_tail}</br>
    ''').batch(
        filename=filename,
        gcode_head=gcode_head,
        gcode_tail=gcode_tail,
    )
    return filename, gcode_head, gcode_settings, gcode_tail


@app.cell
def input_cell(
    gcode_settings,
    mo,
    printer_settings,
    purge_segment_settings,
    segment_settings,
    serpentine_settings,
    sketch_settings,
):
    settings_tabs = mo.ui.tabs(
        tabs={
            'Sketch': sketch_settings,
            'Serpentine': serpentine_settings,
            'Segment': segment_settings,
            'Printer':printer_settings,
            'Purge':purge_segment_settings,
            'GCode': gcode_settings,
        },
        label='Settings'
    )
    settings_tabs
    return (settings_tabs,)


@app.cell
def plot_sketch(
    mo,
    plotting_functions,
    printer_settings,
    purge_segment,
    segment,
    serpentine,
    sketch_settings,
):
    plate_x,plate_y = plotting_functions.gen_plate_shape(
        plate_shape=printer_settings.value['plate_shape'],
        plate_size=printer_settings.value['plate_size'],
    )
    segment_coords = [segment.x_coords,segment.y_coords] if sketch_settings.value['print_segment'] else None
    purge_segment_coords = [purge_segment.x_coords,purge_segment.y_coords] if printer_settings.value['purge_nozzle'] else None
    plot = plotting_functions.plot_data(
        plate=[plate_x,plate_y],
        nozzle_home=[printer_settings.value['x_home'],printer_settings.value['y_home']],
        serpentine_area=[serpentine.x_pos,serpentine.y_pos,serpentine.x_width,serpentine.y_width],
        serpentine=[serpentine.x_coords,serpentine.y_coords],
        segment=segment_coords,
        purge_segment=purge_segment_coords,
            )
    plot_area = mo.vstack(
        [plot],
        align='stretch',
        justify='center',
    )
    return (
        plate_x,
        plate_y,
        plot,
        plot_area,
        purge_segment_coords,
        segment_coords,
    )


@app.cell
def _(mo, serpentine):
    segment_table = mo.ui.table(data=serpentine.vertical_segments_info, pagination=False)
    return (segment_table,)


@app.cell
def segments_info_area(mo, segment_table):
    segments_info_area = mo.vstack([
        mo.md("""**Segments**"""),
        segment_table,
    ])
    return (segments_info_area,)


@app.cell
def _(mo, plot_area, segments_info_area):
    sketch_tabs = mo.ui.tabs(
        tabs={
            'Plot': plot_area,
            'Serpentine info': segments_info_area,
        },
        label='Sketch'
    )
    sketch_tabs
    return (sketch_tabs,)


@app.cell
def serpentine_instantiation(
    Serpentine,
    printer_settings,
    serpentine_settings,
    set_position,
):
    actual_serpentine_x_pos, actual_serpentine_y_pos = set_position(
        printer_settings.value['plate_shape'],
        printer_settings.value['plate_size'],
        serpentine_settings.value['centered_serpentine'],
        serpentine_settings.value['x_pos'],
        serpentine_settings.value['y_pos'],
        serpentine_settings.value['x_width'],
        serpentine_settings.value['y_width'],
        )

    serpentine = Serpentine(
        x_pos=actual_serpentine_x_pos,
        y_pos=actual_serpentine_y_pos,
        x_width=serpentine_settings.value['x_width'],
        y_width=serpentine_settings.value['y_width'],
        constant_pitch=serpentine_settings.value['constant_pitch'],
        min_pitch=serpentine_settings.value['min_pitch'],
        first_inlet_diameter=printer_settings.value['first_inlet_diameter'],
        last_inlet_diameter=printer_settings.value['last_inlet_diameter'],
        )
    return actual_serpentine_x_pos, actual_serpentine_y_pos, serpentine


@app.cell
def segment_instantiation(
    Segment,
    printer_settings,
    segment_settings,
    serpentine,
    serpentine_settings,
):
    shift = 0.5 if segment_settings.value['centered_segment'] is True else segment_settings.value['segment_y_pos']
    segment = Segment(
        x_position = serpentine.x_pos,
        y_position=serpentine.y_pos + serpentine_settings.value['y_width']*shift,
        length=serpentine.width,
        inlet_diameter=printer_settings.value['first_inlet_diameter']
    )
    return segment, shift


@app.cell
def purge_segment_instantiation(Segment, purge_segment_settings):
    purge_segment = Segment(
        x_position = purge_segment_settings.value['purge_x'],
        y_position = purge_segment_settings.value['purge_y'],
        length=purge_segment_settings.value['length'],
        inlet_diameter=purge_segment_settings.value['purge_inlet_diameter'],
        is_vertical=purge_segment_settings.value['is_vertical']
    )
    return (purge_segment,)


@app.cell
def purge_sketch_instantiation(Sketch, purge_segment, sketch_settings):
    purge_sketch = Sketch(
        layer_height=sketch_settings.value['layer_height'],
        number_of_layers=1,
        )
    purge_sketch.gen_segment_layer(purge_segment.trace_info)
    purge_sketch.gen_coordinates()
    return (purge_sketch,)


@app.cell
def sketch_instantiation(Sketch, sketch_settings):
    sketch = Sketch(
        layer_height=sketch_settings.value['layer_height'],
        number_of_layers=sketch_settings.value['number_of_layers'],
        )
    return (sketch,)


@app.cell
def gen_serpentine_layers(serpentine, sketch):
    sketch.gen_serpentine_layers(serpentine.trace_info)
    return


@app.cell
def gen_segment_layer(segment, sketch, sketch_settings):
    if sketch_settings.value['print_segment'] is True:
        sketch.gen_segment_layer(segment.trace_info)
    return


@app.cell
def gen_sketch_coordinates(sketch):
    sketch.gen_coordinates()
    return


@app.cell
def nozzle_instantiation(Nozzle, printer_settings, sketch_settings):
    nozzle = Nozzle(
            x_home=printer_settings.value['x_home'],
            y_home=printer_settings.value['y_home'],
            z_home=printer_settings.value['z_home'],
            layer_width=sketch_settings.value['layer_width'],
            layer_height=sketch_settings.value['layer_height'],
            retraction=printer_settings.value['retraction'],
            lift_distance=printer_settings.value['lift_distance'],
            moving_speed=printer_settings.value['moving_speed'],
            printing_speed=printer_settings.value['printing_speed'],
        )
    return (nozzle,)


@app.cell
def printer_instantiation(Printer, nozzle):
    printer = Printer(nozzle)
    return (printer,)


@app.cell
def save_gcode_file_button(mo):
    save_file_button = mo.ui.run_button(
        label='SAVE G-CODE FILE',
        kind='success',
        full_width=True,
    )
    mo.left(save_file_button)
    return (save_file_button,)


@app.cell
def _(
    GCodeGenerator,
    Nozzle,
    Printer,
    gcode_settings,
    printer_settings,
    purge_sketch,
    sketch,
    sketch_settings,
):
    def save_gcode_function():
        nozzle = Nozzle(
            x_home=printer_settings.value['x_home'],
            y_home=printer_settings.value['y_home'],
            z_home=printer_settings.value['z_home'],
            layer_width=sketch_settings.value['layer_width'],
            layer_height=sketch_settings.value['layer_height'],
            retraction=printer_settings.value['retraction'],
            lift_distance=printer_settings.value['lift_distance'],
            moving_speed=printer_settings.value['moving_speed'],
            printing_speed=printer_settings.value['printing_speed'],
        )
        printer = Printer(nozzle)
        instructions = []
        if printer_settings.value['purge_nozzle'] is True:
            instructions.append(printer.print_cad(purge_sketch.coordinates))
        instructions = printer.print_cad(sketch.coordinates)
        gcode_generator = GCodeGenerator(
            filename=gcode_settings.value['filename'],
            gcode_head=gcode_settings.value['gcode_head'],
            gcode_tail=gcode_settings.value['gcode_tail'],
        )
        gcode_generator.gen_gcode(instructions)
        gcode_generator.save_gcode()
    return (save_gcode_function,)


@app.cell
def save_gcode(mo, save_file_button, save_gcode_function):
    mo.stop(not save_file_button.value)
    save_gcode_function()
    mo.md('G-Code file saved')
    return


@app.cell
def save_serpentine_info_button(mo):
    save_serpentine_info_button = mo.ui.run_button(
        label='SAVE SERPENTINE INFO',
        kind='success',
        full_width=True,
    )
    mo.left(save_serpentine_info_button)
    return (save_serpentine_info_button,)


@app.cell
def save_serpentine_info(
    gcode_settings,
    mo,
    save_serpentine_info_button,
    serpentine,
):
    mo.stop(not save_serpentine_info_button.value)
    serpentine.save_serpentine_info(gcode_settings.value['filename'])
    mo.md('Serpentine info file saved.')
    return


@app.cell
def save_settings_button(mo):
    save_settings_button = mo.ui.run_button(
        label='SAVE SETTINGS FILE',
        kind='success',
        full_width=True,
    )
    mo.left(save_settings_button)
    return (save_settings_button,)


@app.cell
def save_settings(
    gcode_settings,
    printer_settings,
    purge_segment_settings,
    segment_settings,
    serpentine_settings,
    settings,
    sketch_settings,
):
    def save_settings():
        for section in settings.settings_model:
            match section:
                case 'GCODE':
                    marimo_settings = gcode_settings
                case 'PURGE SEGMENT':
                    marimo_settings = purge_segment_settings
                case 'SERPENTINE':
                    marimo_settings = serpentine_settings
                case 'SEGMENT':
                    marimo_settings = segment_settings
                case 'PRINTER':
                    marimo_settings = printer_settings
                case 'SKETCH':
                    marimo_settings = sketch_settings
            for option in settings.settings_model[section]:
                settings.set(section,option,str(marimo_settings.value[option]))
        with open(settings.SETTINGS_FILE_NAME,'w') as file:
            settings.write(file)
    return (save_settings,)


@app.cell
def save_settings(mo, save_settings, save_settings_button):
    mo.stop(not save_settings_button.value)
    save_settings()
    mo.md('Settings file saved.')
    return


if __name__ == "__main__":
    app.run()
