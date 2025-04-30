from itertools import accumulate

class Serpentine:

    def __init__(
            self,
            x_pos:float,
            y_pos:float,
            x_width:float,
            y_width:float,
            constant_pitch:bool,
            min_pitch:float,
            first_inlet_diameter:float,
            last_inlet_diameter:float,           
            ) -> None:
        """Class representing a serpentine.

        Args:
            x_pos (float): the position of the serpentine along the x axis
            y_pos (float):the position of the serpentine along the y axis
            x_width (float): the maximum width along the x axis
            y_width (float): the width along the y axis
            constant_pitch (bool): constant distance between adjacent segments
            min_pitch (float): minimum distance between adjacent segments
            first_inlet_diameter (float): inlet filament diameter of the first segment of the serpentine
            last_inlet_diameter (float): inlet filament diameter of the last segment of the serpentine
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_width = x_width
        self.y_width = y_width
        self.constant_pitch = constant_pitch
        self.min_pitch = min_pitch
        self.distances = []
        self.filament_diameters = []
        self._gen_x_coords()
        self._gen_y_coords()
        self._gen_filament_diameters(first_inlet_diameter,last_inlet_diameter)
    
    def _gen_distances(self) -> list[float]:
        """Generates the distances along the x axis between consecutive adjacent segments 

        Returns:
            list[float]: the distances along x
        """
        delta = []
        i=1
        while sum(delta) + self.min_pitch*i <= self.x_width:
            delta.append(self.min_pitch*i)
            if self.constant_pitch is False:
                i+=0.5
        if len(delta) % 2 == 0:
            # we want a serpentine that starts and ends at the same y position, so if the number of segments
            # is even, we just have to cut the last one
            _ = delta.pop()
        self.distances = list([*accumulate(list(reversed(delta)))])
        return self.distances

    def _gen_x_coords(self) -> None:
        """Generates the set of coordinates along the x axis
        """
        x_home = self.x_pos
        distances = self._gen_distances()
        self.x_coords = [x_home,x_home]
        self.x_coords += [round(i + x_home,2) for i in distances for _ in range(2)]

    def _gen_y_coords(self) -> None:
        """Generates the set of coordinates along the y axis
        """        
        coords = [self.y_width for i in range(len(self.x_coords))]
        mask = [0,1,1,0]
        self.y_coords = []
        for i in range(len(self.x_coords)):
            self.y_coords.append(self.y_pos + coords[i]*mask[i%4])
    
    def _gen_filament_diameters(self,first_inlet_diameter,last_inlet_diameter) -> None:
        diameter_increment = (last_inlet_diameter - first_inlet_diameter)/(self.number_of_segments-2)
        self.filament_diameters = [round(first_inlet_diameter + diameter_increment*i,3) for i in range(self.number_of_segments)]

    def save_serpentine_info(
            self,
            filename:str
            ) -> None:
        """Saves the serpentine information to a file named as {filename}_serpentine_info.csv

        Args:
            filename (str): the name of the  file to be saved
        """
        with open(f'{filename}_serpentine_info.csv', 'w') as file:
            file.write('Segment number,x position,inlet diameter,distance from previous\n')
            for info in self.vertical_segments_info:
                file.write(f"{info['n']},{info['x position']},{info['inlet diameter']},{info['distance from previous']}\n")


    @property
    def number_of_segments(self) -> int:
        """Return the number of segments of the serpentine

        Returns:
            int: the number of segments
        """
        
        return len(self.points)

    @property
    def points(self) -> list[tuple[float,float]]:
        """Returns the set of coodinates of the serpentine points

        Returns:
            list[tuple[float,float]]: (x, y) coordinates of the serpentine points
        """
        return list(zip(self.x_coords, self.y_coords))
    
    @property
    def trace_info(self) -> list[dict[float,float,float]]:
        """Return the coordinates and filament diameter of each serpentine point

        Returns:
            list[dict[float,float,float]]: List of dictionaries containing the 'x', 'y' and 'filament_diameter' value of each serpentine point
        """
        trace_info = []
        for i in range(len(self.x_coords)):
            trace_info.append(
                {
                    'n':i+1,
                    'x':self.x_coords[i],
                    'y':self.y_coords[i],
                    'filament_diameter':self.filament_diameters[i],
                }
            )
        return trace_info
    
    @property
    def vertical_segments_info(self) -> list[dict[float,float,float]]:
        """Returns the information about the vertical segments (filament diameter, distance from previous segment)

        Returns:
            list[dict[float,float,float,float]]: List of dictionaries indicating number, x position, filament diameter and distance from previous segment of each vertical segment
        """
        info = [
            {
                'n':1,
                'x position': self.x_coords[0],
                'inlet diameter': self.filament_diameters[0],
                'distance from previous':0,
                }
            ]
        for i in range(len(self.distances)):
            segment_index = i*2+2
            info.append(
                {
                    'n': i + 2,
                    'x position': self.x_coords[segment_index],
                    'inlet diameter': self.filament_diameters[segment_index],
                    'distance from previous': self.x_coords[segment_index]-self.x_coords[(i-1)*2+2],
                }
            )
        return info
    
    @property
    def width(self) -> float:
        """Returns the actual width of the serpentine

        Returns:
            float: the actual width of the serpentine
        """
        return round(self.x_coords[-1] - self.x_coords[0],2)