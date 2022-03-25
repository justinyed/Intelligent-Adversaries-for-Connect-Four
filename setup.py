#!/usr/bin/env python
from setuptools import setup
setup(name='capstone',
      version='0.7',
      author='Justin S, Yedinak',
      url='https://github.com/justinyed/Intelligent-Adversaries-for-Connect-Four',
      download_url='https://github.com/justinyed/Intelligent-Adversaries-for-Connect-Four.git',
      author_email='justin.yedinak.19@cnu.edu',
      description='Adversarial Agents with a Discord Bot Interface',
      packages=['main_package', 'intelligence', 'discord_bot'],
      package_dir={'game_components': 'game_components', 'intelligence': 'intelligence', 'discord_bot': 'discord_bot'}
)