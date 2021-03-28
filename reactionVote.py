import asyncio


class ReactionVote:
  def __init__(self, client):
    self._client = client
    self.voterList = []
    #default is false for anonymous

  
  async def rVote(self, ctx):
    channel = ctx.channel
    msg = await channel.send("React to join the vote!")
    await msg.add_reaction('👍')
    await asyncio.sleep(5)
    
    #getting list of users who reacted and adding it to array
    msg = await ctx.fetch_message(msg.id)

    for reaction in msg.reactions:
      if reaction.emoji == '👍':
        async for user in reaction.users():

          #ignoring bot reaction
          if user != self._client.user:
            #maybe right here we can start sending private message
            self.voterList.append(user)

    
    #for testing purpose
    #for x in self.voterList:
    #  await ctx.channel.send(x.mention)


    return self.voterList