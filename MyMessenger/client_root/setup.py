from setuptools import setup, find_packages

setup(name="my_messenger_client",
      version="0.1",
      description="Client app with GUI to connect to private messenger server",
      author="Alexander Naumov",
      author_email="myMessenger@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
