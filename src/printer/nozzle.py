from math import sqrt, pi

class Nozzle:   
    def __init__(
            self,
            x_home:float,
            y_home:float,
            z_home:float,
            layer_width:float,
            layer_height:float,
            retraction:float,
            lift_distance:float,
            moving_speed:float,
            printing_speed:float,
            ) -> None:
        """Class representing the nozzle of a printer

        Args:
            x_home (float): the home position of the nozzle along the x axis
            y_home (float): the home position of the nozzle along the y axis
            z_home (float): the home position of the nozzle along the z axis
            layer_width (float): the width of the trace to be printed
            layer_height (float): the height of the trace to be printed
            retraction (float): the filament retraction after printing a trace
            lift_distance (float): the distance to lift when moving without printing
            moving_speed (float): the speed the nozzle moves when not printing
            printing_speed (float): the speed the nozzle moves when printing
        """

        self.layer_width=layer_width
        self.layer_height=layer_height
        self.retraction=retraction
        self.lift_distance=lift_distance
        self.moving_speed=moving_speed
        self.printing_speed=printing_speed
        self._current_x = x_home
        self._current_y = y_home
        self._current_z = z_home
        self._extruded_volume = 0.0
        self.positions = [
            {
                'X': self._current_x,
                'Y': self._current_x,
                'Z': self._current_x,
                'E': 0,
                'F': 0,
            },
        ]

    @property
    def current_x(self):
        return round(self._current_x,2)

    @property
    def current_y(self):
        return round(self._current_y,2)

    @property
    def current_z(self):
        return round(self._current_z,2)
    
    @property
    def extruded_volume(self):
        return round(self._extruded_volume,3)

    def length_to_extrude(
            self,
            x:float,
            y:float
            ) -> float:
        """Calculates the length of the segment to be extruded.

        Args:
            x (float): x coordinate of the new position of the nozzle
            y (float): y coordinate of the new position of the nozzle

        Returns:
            float: the lenght of the segment to extrude
        """
        x_shift = x - self.current_x
        y_shift = y - self.current_y
        return round(sqrt((x_shift)**2 + (y_shift)**2),3)

    def move_to(
            self,
            x:float,
            y:float,
            z:float
            ) -> None:
        """Move the nozzle to the specified coordinates


        Args:
            x (float): x coordinate
            y (float): y coordinate
            z (float): z coordinate
        """
        self.extrude(self.retraction)
        self.positions.append({'Z': self.current_z + self.lift_distance, 'E': self.extruded_volume, 'F': self.moving_speed,})
        self.positions.append({'X': x,'Y': y,'F': self.moving_speed,})
        self.positions.append({'Z': z, 'F': self.moving_speed,})
        self._current_x = x
        self._current_y = y 
        self._current_z = z

    def print(
            self,
            point:dict[float]
            ) -> None:
        """Generate the instruction to print a segment

        Args:
            point (dict[float]): the end coordinates and filament diameter of the segment to be printed
        """
        volume = self.volume_to_extrude(point)
        self.extrude(volume)
        self.positions.append(
                        {
                'X': point['x'],
                'Y': point['y'],
                'E': self.extruded_volume,
                'F': self.printing_speed,
            }
        )
        self._current_x = point['x']
        self._current_y = point['y']

    def extrude(
            self,
            amount:float
            ) -> None:
        """Increase the current total extruded volume

        Args:
            amount (float): the amount of material extruded
        """
        self._extruded_volume += amount

    def volume_to_extrude(
            self,
            point:dict
            ) -> float:
        """Calculates the volume of the segment to print.

        Args:
            point (dict): the end coordinates and filament diameter of the segment to be printed

        Returns:
            float: the volume of the segment to print
        """
        lenght = self.length_to_extrude(point['x'],point['y'])
        inlet_area=pi*(point['filament_diameter'])**2/4
        return lenght*self.layer_width*self.layer_height/inlet_area