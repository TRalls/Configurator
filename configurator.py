"""
	A simple class to streamline config file usage.
	Created by Thomas Ralls
	tralls@outlook.com
"""

import configparser
import os
from shutil import copyfile

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
		To set mutliple options at once, pass None as options and a dict as value.
	"""
	def set(self, section, option, value):
		# Set single option.
		if option:
			# Default retrun.
			return_details = 'Value has been set'

			# Creates section if needed.
			if not self.config.has_section(section):
				self.config.add_section(section)
				return_details += ' - Section was created'

			# Set value and save loaded config.
			self.config.set(section, option, value)
			self.save()

			return {
				'status': 'success',
				'details': return_details
			}
		# Set multiple options.
		else:
			for key in value.keys():
				if len(value[key]) > 0:
					self.set(section, key, value[key])
			return {
				'status': 'success',
				'details': 'All values have been set'
			}

	"""
		Get a value from the config. If no option is specified, all options
		are returned in the form of a dict.
	"""
	def get(self, section, option=None):
		# Check if section doesn't exist.
		if not self.config.has_section(section):
			return {
				'status': 'failure',
				'details': 'Section doesn\'t exist'
			}
		# If option is specified.
		if option:
			# Ensure option exists.
			if not self.config.has_option(section, option):
				return {
					'status': 'failure',
					'details': 'Option doesn\'t exist'
				}
			details = self.config.get(section, option)
		# No option specified, get all options.
		else:
			details = {}
			for key in self.list(section)['details']:
				details[key] = self.config.get(section, key)

		# Section exists.
		return {
			'status': 'success',
			'details': details
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

		# Success - save and return.
		if result:
			self.save()
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
		Write to config file.
	"""
	def save(self):
		with open(self.full_name, 'w') as configfile:
			self.config.write(configfile)

	"""
		Creates to and restores from back up.
		action should be either 'restore' or 'create'.
		While creating a backup, the current file is the copy_ee meaning
		it will be coppied to the copy_er, which in this case would be the 
		backup. When restoring, the roles are reversed.
		The backup config has the same full name as the current config with
		'.bak' appended.
	"""
	def backup(self, action): 
		backup_name = self.full_name + '.bak'
		
		# Determing which file is copy_er and which is copy_ee based on action
		if action == 'restore':
			copy_er, copy_ee = backup_name, self.full_name
		elif action == 'create':
			copy_er, copy_ee = self.full_name, backup_name
		else:
			return {
				'status': 'failure',
				'details': 'Invalid action'
			}

		# Ensure copy_er file exists.
		if not os.path.isfile(copy_er):
			return {
				'status': 'failure',
				'details': copy_er + ' doesn\'t exist'
			}
		
		# Preform copy
		copyfile(copy_er, copy_ee)
		return {
			'status': 'success',
			'details': 'Action "' + action + '" complete'
		}

