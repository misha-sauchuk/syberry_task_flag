import argparse

WIDTH_COEF = 3
HIGH_COEF = 2
VERT_SHIFT = 0.5
HORIZ_SHIFT = 1
BORDER_TYPE = '#'
CIRCLE_BORDER = '*'
CIRCLE_INNER = 'o'


def arg_parser():
    """
    This function gather parameter of the flag from users,
    and call function clean to check the input parameter
    :return: clear input parameter as integer
    """
    parser = argparse.ArgumentParser(description='generate Japanese flag')
    input_arg = parser.add_argument('N', type=int, help='parameter N should be integer, positive and even')
    parameter = parser.parse_args().N
    clean_parameter = clear(parameter, input_arg)
    return clean_parameter


def clear(parameter: int, input_arg):
    """
    This function check if the input parameter is integer, even and positive,
    and raise an Exception if it is not
    :param parameter: input data from user
    :param input_arg: argument to raise an Exception
    :return: clear input parameter as integer
    """
    if parameter > 0 and parameter % 2 == 0:
        return parameter
    raise argparse.ArgumentError(input_arg, 'ArgumentError: parameter N should be integer, positive and even')


def mirror_update(lst: list):
    """
    This function change the second half-part of the list like a mirror reflection
    of the first half-part of the list
    """
    for i in range(0, len(lst) // 2):
        lst[len(lst)-i-1] = lst[i]


class Flag:
    """
    Parent class for every type of flags
    """
    def __init__(self, parameter):
        """
        Initialization of the class, create an empty flag with border as an matrix (list of lists)
        :param parameter: clean_data from user
        """
        self.width = WIDTH_COEF * parameter
        self.high = HIGH_COEF * parameter
        self.horizontal_border = [[BORDER_TYPE] + [BORDER_TYPE] * self.width + [BORDER_TYPE]]
        self.empy_body = [[BORDER_TYPE] + [" "] * self.width + [BORDER_TYPE] for i in range(self.high)]
        self.flag = self.horizontal_border + self.empy_body + self.horizontal_border

    def __str__(self):
        """
        reload of the method __str__
        transform self.flag as a list of lists into string with "\n" separator between lists
        """
        string_flag = ''
        for line in self.flag:
            string_flag += ''.join(line) + '\n'
        return string_flag


class JapaneseFlag(Flag):
    """
    Child class of the class Flag
    """
    def __init__(self, parameter):
        """
        Initialization of the class, use the parent __init__
        self.horizontal_pic_border and self.vertical_pic_border are used
        to define the border of the high left quarter of the picture(circle)
        :param parameter: clean_data from user
        """
        super(JapaneseFlag, self).__init__(parameter)
        self.parameter = parameter
        self.horizontal_pic_border = (int(parameter * VERT_SHIFT + 1), len(self.flag) // 2)
        self.vertical_pic_border = (int(parameter * HORIZ_SHIFT + 1), len(self.flag[0]) // 2)

    def create_half_pic(self):
        """
        create the top part of the circle
        by going line by line from top horizontal_pic_border to the middle of the high of the flag
        and from left vertical_pic_border to the meddle of current line and after make mirror_update for this line
        """
        number_of_line = 0
        for i in range(*self.horizontal_pic_border):
            number_of_column = self.parameter//2
            for j in range(*self.vertical_pic_border):
                if number_of_column > (number_of_line + 1):
                    self.flag[i][j] = ' '
                elif number_of_column == (number_of_line + 1):
                    self.flag[i][j] = CIRCLE_BORDER
                else:
                    self.flag[i][j] = CIRCLE_INNER
                number_of_column -= 1
            mirror_update(self.flag[i])
            number_of_line += 1

    def create_full_pic(self):
        """
        create a full picture of the circle by making a mirror_update for whole flag
        """
        self.create_half_pic()
        mirror_update(self.flag)


def flag():
    """
    create a Japanese flag like ASCII art
    """
    try:
        flag_parameter = arg_parser()
        flag = JapaneseFlag(flag_parameter)
        flag.create_full_pic()
        return flag
    except argparse.ArgumentError as err:
        print(err)
    except Exception as err:
        print('Application error: {}!\n Please, contact support'.format(err))


if __name__ == '__main__':
    japan_flag = flag()
    print(japan_flag)
