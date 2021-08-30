import os

DATABASE = os.getenv('DATABASE', 'sqlite:///local.db')
