class Sketch:
    
    def __init__(
            self,
            layer_height:float,
            number_of_layers:float,
            ) -> None:
        """Class representing the sketch to be printed.

        Args:
            layer_height (float): the height of each layer of the sketch
            number_of_layers (float): number of serpetine to be stacked
        """
        self.layer_height=layer_height
        self.number_of_layers=number_of_layers
        self.layer_sequence = []
        self.coordinates = []

    def gen_coordinates(
            self
            ) -> dict[float,list[float,float,float]]:
        """Generates the coordinates and filament diameters of each point of the sketch

        Returns:
            dict[float,list[float,float,float]]: Dictionary containing the heigth and x,y,filament diameter of each sketch point
        """
        height = self.layer_height
        for layer in self.layer_sequence:
            self.coordinates.append(
                {
                    'z':height,
                    'trace':layer,
                }
            )
            height+=self.layer_height
    
    def gen_serpentine_layers(
            self,
            serpentine_trace_info
            ) -> None:
        """Generates the sequence of serpentines to be stacked

        Args:
            serpentine_trace_info (list[dict[float,float,float]]): List of dictionaries containing the 'x', 'y' and 'filament_diameter' value of each serpentine point
        """
        for i in range(self.number_of_layers):
            self.layer_sequence.append(serpentine_trace_info)
    
    def gen_segment_layer(
            self,
            segment_trace_info
            ) -> None:
        """Generates the segment to be printed on top of the stack of serpentines

        Args:
            segment_trace_info (list[dict[float,float,float]]): List of dictionaries containing the 'x', 'y' and 'filament_diameter' value of each segment point
        """
        self.layer_sequence.append(segment_trace_info)
