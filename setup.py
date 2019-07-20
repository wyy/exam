from distutils.core import setup
setup(name='cs',
      version='1.0',
      py_modules=['cs', 'lol'],
      scripts=['scripts/cs', 'scripts/lol'],
      data_files=[('',['data.txt'])],
      )
