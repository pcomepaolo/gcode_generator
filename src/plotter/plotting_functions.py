from matplotlib import pyplot as plt
from math import pi, sin, cos

def gen_plate_shape(
        plate_shape:str,
        plate_size:int
        ) -> list[list[float],list[float]]:
    """generates the coordinates of the printing plate perimeter

    Args:
        plate_shape (str): the shape of the printing plate (squared/rounded)
        plate_size (int): the size of the printing plate (edge if squared, diameter if rounded)

    Returns:
        list[list[float],list[float]]: the list of x and y coordinates of the printing plate perimeter
    """
    match plate_shape:
        case 'squared':
            x_coords = [plate_size*i for i in [0,0,1,1,0]]
            y_coords = [plate_size*i for i in [0,1,1,0,0]]
        case 'rounded':
            angles = [2*pi*i/100 for i in range(101)]
            x_coords = [plate_size/2*cos(angle) for angle in angles]
            y_coords = [plate_size/2*sin(angle) for angle in angles]
    return x_coords,y_coords

def gen_serpentine_area(
        info:list[float]
        ) -> list[list[float],list[float]]:
    """generates the serpentine maximum area

    Args:
        info (list[float]): the x,y starting coordinates and x maximum width, y width of the serpentine

    Returns:
        list[list[float],list[float]]: the coordinates of the vertices of the rectangle describing the maximum area of the serpentine
    """
    x,y,x_width,y_width=info
    x_coords = [x+i for i in [0,0,x_width,x_width,0]]
    y_coords = [y+i for i in [0,y_width,y_width,0,0]]
    return x_coords,y_coords

def plot_data(
    plate:list[list[float]],
    nozzle_home:list[float],
    serpentine_area:list[float],
    serpentine:list[list[float]],
    segment:list[list[float]]=None,
    purge_segment:list[list[float]]=None,
    ):
    ax_min=min(plate[0])-25
    ax_max=max(plate[0])+25
    figure, axes = plt.subplots(nrows=1,ncols=1, figsize=(8,8))  
    axes.axvline((ax_max+ax_min)/2,c='g',lw=0.75)
    axes.axhline((ax_max+ax_min)/2,c='r',lw=0.75)
    axes.plot(plate[0],plate[1],ls='-.',c='xkcd:medium blue')
    axes.plot(*gen_serpentine_area(serpentine_area),ls='--',c='xkcd:light grey'),
    axes.plot(serpentine[0],serpentine[1],c='xkcd:purple',ls='-')
    if segment is not None:
        axes.plot(segment[0],segment[1],c='xkcd:purple',ls='-')
    if purge_segment is not None:
        axes.plot(purge_segment[0],purge_segment[1],c='xkcd:black',ls='-',lw=4)
    axes.plot(nozzle_home[0],nozzle_home[1],'+', mec='xkcd:leaf green',ms='20',mew=2)
    axes.set_xlabel('x',color='r')
    axes.set_ylabel('y',color='g')
    axes.set_xlim(ax_min,ax_max)
    axes.set_ylim(ax_min,ax_max)
    return figure, axes