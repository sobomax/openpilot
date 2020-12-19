class COLORS:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  CBLUE = '\33[44m'
  BOLD = '\033[1m'
  CITALIC = '\33[3m'
  OKGREEN = '\033[92m'
  CWHITE = '\33[37m'
  ENDC = '\033[0m' + CWHITE
  UNDERLINE = '\033[4m'
  PINK = '\33[38;5;207m'
  PRETTY_YELLOW = BASE(220)

  RED = '\033[91m'
  PURPLE_BG = '\33[45m'
  YELLOW = '\033[93m'
  BLUE_GREEN = BASE(85)

  FAIL = RED
  INFO = PURPLE_BG
  SUCCESS = OKGREEN
  PROMPT = YELLOW
  DBLUE = '\033[36m'
  CYAN = BASE(39)
  WARNING = '\033[33m'

  def BASE(self, col):  # seems to support more colors
    return '\33[38;5;{}m'.format(col)

  def BASEBG(self, col):  # seems to support more colors
    return '\33[48;5;{}m'.format(col)


COLORS = COLORS()


def opParams_warning(msg):
  print('{}opParams WARNING: {}{}'.format(COLORS.WARNING, msg, COLORS.ENDC))


def opParams_error(msg):
  print('{}opParams ERROR: {}{}'.format(COLORS.FAIL, msg, COLORS.ENDC))
