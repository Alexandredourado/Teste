import logging

def configurar_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:%(message)s'
    )
    return logging.getLogger(__name__)
