"""
	A simple class to streamline config file usage.
	Created by Thomas Ralls
	tralls@outlook.com
"""

import configparser
import os

class Configurator():
	"""
		Constructor - Takes the following:
			path: Full dir name that the file is (or should be) stored in.
			name: name of the config file without extention.
	"""
	def __init__(self, path, name):
		# Full path to file and name.
		self.full_name = os.path.join(path, name + '.cfg')
		
		# File iscreated if it doesn't exist.
		if not os.path.isfile(self.full_name):
			with open(self.full_name, 'w'): pass
		
		# Load config file.
		self.config = configparser.RawConfigParser()
		self.config.read(self.full_name)
	
	"""
		Sets a value in the config file.
		If the specified section doesn't exist, it is created.
	"""
	def set(self, section, option, value):
		# Default retrun.
		return_details = 'Value has been set'

		# Creates section if needed.
		if not self.config.has_section(section):
			self.config.add_section(section)
			return_details += ' - Section was created'

		# Set value and save_refresh loaded config.
		self.config.set(section, option, value)
		self.save_refresh()

		return {
			'status': 'success',
			'details': return_details
		}

	"""
		Get a value from the config.
	"""
	def get(self, section, option):
		# Check if section doesn't exist.
		if not self.config.has_option(section, option):
			return {
				'status': 'failure',
				'details': 'Section or Option doesn\'t exist'
			}
		# Section exists.
		return {
			'status': 'success',
			'details': self.config.get(section, option)
		}
	
	"""
		List items in config file.
		If section is specifies, its options will be listed.
		Else, available sections will be lists.
	"""
	def list(self, section=None):
		# List sections.
		if section == None:
			result = self.config.sections()
		# List options in section.
		else:
			# Return failure if section doesn't exist.
			if not self.config.has_section(section):
				return {
					'status': 'failure',
					'details': 'Section does not exist'
				}
			result = self.config.options(section)

		return {
			'status': 'success',
			'details': result
		}

	"""
		Removes option if specifies, else, section is removed.
	"""
	def remove(self, section, option=None):
		# Remove section.
		if option == None:
			result = self.config.remove_section(section)
		# Remove option.
		else:
			result = self.config.remove_option(section, option)

		# Success - save_refresh and return.
		if result:
			self.save_refresh()
			return {
				'status': 'success',
				'details': 'Removed item'
			}

		# Failure.
		return {
			'status': 'failure',
			'details': 'Item didn\'t exist to be removed'
		}

	"""
		Return all contents in config file.
	"""
	def get_all(self):
		with open(self.full_name) as f:
			return {
				'status': 'success',
				'details': f.read()
			}
	
	"""
		Write to config file and load fresh contents.
	"""
	def save_refresh(self):
		with open(self.full_name, 'w') as configfile:
			self.config.write(configfile)
		self.config.read(self.config.read(self.full_name))
