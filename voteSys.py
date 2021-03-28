class VoteSys:
  def __init__(self, client, channel):
    self.client = client
    self.channel = channel
    self.candidates = []
    self.voterList = []
    self.queueList = []
    self.anonymous = False
    self.starter = None