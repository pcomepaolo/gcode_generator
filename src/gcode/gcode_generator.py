class GCodeGenerator:

    COMMAND_PRINT = 'G1'
    COMMANDS = ['X', 'Y', 'Z', 'E', 'F']
    gcode = ''

    def __init__(
            self,
            filename:str,
            gcode_head:str,
            gcode_tail:str
            ) -> None:
        """Class representing a g-code generator.
        The head and tail of the file are hardcoded in the gcode_head.ini and gcode_tail.ini files.


        Args:
            filename (str): the name of the gcode file that will be generated
            gcode_head (str): the name of the file containing the head of the g-code file
            gcode_tail (str): the name of the file containing the tail of the g-code file
        """
        self.head = gcode_head
        self.tail = gcode_tail
        self.filename = filename

    def gen_gcode(
            self,
            instructions:list
            ) -> None:
        """Generates the g-code from the set of instructions provided by the printer.

        Args:
            instructions (list): the set of instructions
        """
        self.gcode+=self.head
        if instructions is not None:
            for coordinate in instructions:
                self.gcode+=self.gen_gcode_line(coordinate)
        self.gcode+=self.tail

    def gen_gcode_line(
            self,
            instructions:dict
            ) -> str:
        """Generates a single g-code line from the printer instructions.

        Args:
            instructions (dict): the instructions

        Returns:
            str: the generated g-code line
        """
        gcode_line = 'G1 '
        for command in self.COMMANDS:
            if command in instructions:
                gcode_line+=f'{command}{instructions[command]} '
        gcode_line+='\n'
        return gcode_line

    def save_gcode(self) -> None:
        """Saves the g-code file.
        """
        with open(f'{self.filename}.gcode', 'w') as output_file:
            for line in self.gcode:
                output_file.write(line)        