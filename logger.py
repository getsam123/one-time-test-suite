import logging
import sys
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=sys.argv[1],
                    filemode='w')
	logging.info(sys.argv[2]+' :')
	for i in sys.argv[3:]:
		logging.info(i)
