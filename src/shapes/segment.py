class Segment:

    def __init__(
            self,
            x_position:float,
            y_position:float,
            length:float,
            inlet_diameter:float,
            is_vertical:bool=False,
            ) -> None:
        """Class representing a segment

        Args:
            x_position (float): the position of the segment along the x axis
            y_position (float): the position of the segment along the y axis
            length (float): the lenght of the segment
            inlet_diameter (float): inlet filament diameter of the  segment
            is_vertical (bool): vertical (True) or horizontal (False) segment
        """
        if is_vertical is True:
            self.x_coords = [x_position, x_position]
            self.y_coords = [y_position, y_position + length]
        else:
            self.x_coords = [x_position, x_position + length]
            self.y_coords = [y_position, y_position]
        self.inlet_diameter = inlet_diameter

    @property
    def points(self) -> list[tuple[float,float]]:
        """Returns the set of coodinates of the segment points

        Returns:
            list[tuple[float,float]]: (x, y) coordinates of the segment points
        """
        return list(zip(self.x_coords,self.y_coords))
    
    @property
    def trace_info(self) -> list[dict[float,float,float]]:
        """Return the coordinates and filament diameter of each segment point

        Returns:
            list[dict[float,float,float]]: List of dictionaries containing the 'x', 'y' and 'filament_diameter' value of each segment point
        """        
        trace_info = []
        for i in range(len(self.x_coords)):
            trace_info.append(
                {
                    'x':self.x_coords[i],
                    'y':self.y_coords[i],
                    'filament_diameter':self.inlet_diameter,
                }
            )
        return trace_info