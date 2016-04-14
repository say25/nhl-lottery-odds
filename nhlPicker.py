import urllib2
import json

odds = [0.20, 0.135, 0.115, 0.095, 0.085, 0.075, 0.065, 0.06, 0.05, 0.035, 0.03, 0.025, 0.02, 0.01]

class Team():
	def __init__(self, name, points, gamesPlayed, leagueRank):
		self.name = name
		self.points = points
		self.gamesPlayed = gamesPlayed
		self.pointPercentage = float(points)/float(gamesPlayed)
		self.leagueRank = int(leagueRank)
		self.index = -1
		self.pick1 = 0
		self.pick2 = 0
		self.pick3 = 0
		self.notTop3 = -1

	#Calculate the odds of winning the 2nd overall pick
	def calculate2(self):
		for team in teams:
			if team.index != self.index:
				self.pick2 += team.pick1 * (self.pick1/(1-team.pick1))

	#Calculate the odds of winning the 3rd overall pick
	def calculate3(self):
		for team1 in teams:
			for team2 in teams:
				if team1.index != self.index and team1.index != team2.index and team2.index != self.index:
					self.pick3 += team1.pick1 * team2.pick2 * (self.pick1/(1-team1.pick1-team2.pick2))

	#Calculate the odds of not ending up with the 1st, 2nd or 3rd overall pick
	def calculateNotTop3(self):
		self.notTop3 = 1 - (self.pick1 + self.pick2 + self.pick3)

	def display(self):
		print(str(self.index+1) + '. ' + self.name + ' - ' + str(self.points))
		print("1st - " + str(self.pick1))
		print("2nd - " + str(self.pick2))
		print("3rd - " + str(self.pick3))
		print("Not Top 3 - " + str(self.notTop3))

webUrl = urllib2.urlopen('https://statsapi.web.nhl.com/api/v1/standings')

if (webUrl.getcode() == 200):
	data = json.loads(webUrl.read())
	teams = []
	for record in data['records']:
		for teamRecord in record['teamRecords']:
			if int(teamRecord['wildCardRank']) > 2:
				teams.append(Team(teamRecord['team']['name'], teamRecord['points'], teamRecord['gamesPlayed'], teamRecord['leagueRank']))

	teams = sorted(teams, key=lambda team: (team.pointPercentage, -team.leagueRank))

	i = 0

	for team in teams:
		team.index = i
		team.pick1 = odds[i]
		i += 1

	for team in teams:
		team.calculate2()

	for team in teams:
		team.calculate3()
		team.calculateNotTop3()
		team.display()
else:
	print('Could not get data.')
