from setuptools import setup, find_packages

setup(name="my_messenger_server",
      version="0.1",
      description="Server app with GUI to runa private messanger",
      author="Alexander Naumov",
      author_email="myMessenger@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
