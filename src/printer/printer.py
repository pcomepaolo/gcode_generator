from .nozzle import Nozzle

class Printer:
    
    def __init__(
            self,
            nozzle:Nozzle
            ) -> None:
        """Class representing a printer

        Args:
            nozzle (Nozzle): the nozzle of the printer
        """
        self.nozzle = nozzle

    def print_cad(
            self,
            sketch_coordinates:dict[float,list[float,float,float]]
            ) -> list[dict]:
        """Prints the instruction contained in a sketch.

        Args:
            sketch_coordinates (dict[float,list[float,float,float]]): _description_Dictionary containing the heigth and x,y,filament diameter of each sketch point

        Returns:
            list[dict]: the instructions to be converted in g-code language
        """
        for layer in sketch_coordinates:
            layer_x_home = layer['trace'][0]['x']
            layer_y_home = layer['trace'][0]['y']
            self.nozzle.move_to(layer_x_home,layer_y_home,layer['z'])
            for point in layer['trace'][1:]:
                self.nozzle.print(point)
        return self.instructions
    
    @property
    def instructions(self):
        return self.nozzle.positions
    