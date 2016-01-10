import yaml, os

def get():
	# TODO: Give this file some efficiency
	return yaml.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.yml')).read())