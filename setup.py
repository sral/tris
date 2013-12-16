from setuptools import setup

setup(name="tris",
      version="0.1",
      description="Another shitty Tetris clone.",
      license="GPLv3",
      author="Lars Djerf",
      author_email="lars.djerf@gmail.com",
      url="http://github.com/sral/tris",
      install_requires=["pygame"],
      packages=["tris", "tris.tests"],
      test_suite="tris.tests",
      include_package_data=True,
      package_data={
          "tris": ["data/*.gif"],
      },
      entry_points={
          "gui_scripts": ["tris = tris.tris:main_func"]
      })