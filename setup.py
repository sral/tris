from setuptools import setup, find_packages

setup(name="tris",
      version="0.1",
      description="Another shitty Tetris clone.",
      license="GPLv3",
      author="Lars Djerf",
      author_email="lars.djerf@gmail.com",
      url="http://github.com/sral/tris",
      packages=find_packages(),
      scripts=["tris/tris.py"],
      include_package_data=True,
      test_suite="tris.tests",
      install_requires=["pygame"])
