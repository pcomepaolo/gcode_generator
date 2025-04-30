def set_position(
        plate_shape:str,
        plate_size:str,
        is_centered:bool,
        x_pos:float,
        y_pos:float,
        x_width:float,
        y_width:float,
        ) -> list[float]:
    """Function that sets the position of the first point of the serpentine depending on:
        - plate geometry 
        - nozzle home position
        If is_centered is True, the serpentine is centered in the printing plate.

    Args:
        plate_shape (str): shape of the printing plate (squared/rounded)
        plate_size (str): size of the printing plate (edge if squared, diameter if rounded)
        is_centered (bool): true if the serpentine must be centered in the printing plate
        x_pos (float): position of the serpentine along the x axis
        y_pos (float): position of the serpentine along the y axis
        x_width (float): maximum width of the serpentine along the x axis
        y_width (float): width of the serpentine along the y axis

    Returns:
        list[float]: x, y coordinate of the fist point of the serpentine
    """
    match plate_shape:
        case 'rounded':    
            if is_centered is True:
                x_pos = - x_width/2
                y_pos = - y_width/2
        case 'squared':
            if is_centered is True:
                x_pos = (plate_size - x_width)/2
                y_pos = (plate_size - y_width)/2


    return x_pos,y_pos