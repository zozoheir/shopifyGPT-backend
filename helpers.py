import logging


def getLogger(name, save_to_path=None):
    logging.basicConfig(format='%(levelname)s | %(name)s | %(asctime)s : %(message)s ', level=logging.INFO)
    logger = logging.getLogger(name)
    if save_to_path:
        fh = logging.FileHandler(save_to_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger