import colorlog

"""
LOGGING CONFIG
"""
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s: %(message)s',
    #datefmt = '%d/%b/%Y %H:%M:%S',
    reset = True,
    log_colors={
		'DEBUG':    'blue',
		'INFO':     'green',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
	    },
    )
)

logger = colorlog.getLogger('ibnrisen')
logger.addHandler(handler)
logger.setLevel('DEBUG')