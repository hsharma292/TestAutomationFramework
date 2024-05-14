import logging
import os


# class LogGen:
#     @staticmethod
#     def loggen():
#         logging.basicConfig(filename=".\\Logs\\automation.log",
#                             format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%y %I:%M:%S: %p')
#         logger = logging.getLogger()
#         logger.setLevel(logging.INFO)
#         return logger
class LogGen:
    # we added the static method so that we dont need to use the "self" keyword in the below fucntion
    @staticmethod
    # now create one object for logging
    def loggen():
        # Set up a logger
        logger = logging.getLogger('myLogger')

        # If logger already has handlers configured, return it to avoid duplicate handlers
        if logger.handlers:
            return logger

        # Set logging level
        logger.setLevel(logging.DEBUG)

        # Create handlers
        dir_path = os.path.dirname(os.path.realpath(__file__))  # Current file path
        base_dir = os.path.dirname(dir_path)  # This assumes LogGen is in the testCases folder, adjust if needed
        log_file_path = os.path.join(base_dir, 'Logs', 'automation.log')

        # Check if Logs directory exists, if not create it
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))

        # Set up file handler with formatting
        fh = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger
