class SelectableChoices():

	choice = {'James Mclean': 'U1EGXCR63', 'Scott Magnuson':'U1EGNU4J2', 'Slackbot': 'USLACKBOT'}
	def __init__(self, selectedChoices):
		self.selectedChoices = selectedChoices

	def setChoice(self):
		choice = self.selectedChoices