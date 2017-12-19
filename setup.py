from setuptools import setup

setup(
   name='simple_cnlp',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['simple_cnlp'],  #same as name
   install_requires=["requests"], #['bar', 'greek'],
)
