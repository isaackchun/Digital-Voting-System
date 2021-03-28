import discord
import os
from replit import db
from discord.ext import commands

from queue import Queue
import reactionVote
import voteSys
import process

from random import randrange
import math
import voter
import time

client = commands.Bot(command_prefix = "$", case_insensitive = True)

#keeps track of all the channel
voteSys_list = []


# TODO: 
# 1. FIX $stop, doesn't work most of the time
# 2. (optional) Create embeds



def displayQuotesEmbed(newVote):
  embed = discord.Embed(
    title = '',
    description = '',
    colour = discord.Colour.green()
  )
  #embed.set_footer(text='xd')
  embed.set_thumbnail(url= 'https://s7d2.scene7.com/is/image/TWCNews/Getty_Vote_Ballot_Election')
  embed.set_author(name='🗳️ Digital Voting System')
  #embed.add_field(name="Number of Candidates: ", value = len(newVote.candidates), inline='False')

  counter = 1
  for candidate in newVote.candidates:
    embed.add_field(name="#" + str(counter) + ": " + str(candidate), value =  "\u200b", inline='True')
    counter += 1


  return embed

def initiateEmbed(newVote):
  embed = discord.Embed(
    title = 'Enter your candidates seperated by commas!',
    description = 'Good input: Iron Man, Thor, Captain America.\n\nBad input: Iron Man Thor Captain America\n\n\nTo view all available commands enter $help!',
    colour = discord.Colour.green()
  )
  return embed


#the voting process
def chooseWinner(new):
  #winner = process.Process(new.candidates,new.queueList)
  #winner.run()
  #-----------------------------------------------------------
  candidates = new.candidates

  #all votes
  votes = new.queueList

  def add_one(name,fin):
    for x in range(len(fin)):
      if fin[x].name == name:
        fin[x].count+=1

  def insertion_sort(array):
  
    for i in range(1, len(array)):
      
      key_item = array[i].count
      key_name = array[i].name
          
      j = i - 1

        
      while j >= 0 and array[j].count > key_item:
              
        array[j + 1].count = array[j].count
        array[j + 1].name = array[j].name
        j -= 1

          
      array[j + 1].count = key_item
      array[j + 1].name = key_name

    return array

  def insert(list, n):
    ind = 0
      # Searching for the position
    
    if len(list)==0:
      list.append(n);
      return list,0
    for i in range(len(list)):
      if list[i] > n:
      
        ind = i
        break
        
    # Inserting n in the list
    if i==len(list)-1:
    
      list.append(n)
      return list,i
    list = list[:i] + [n] + list[i:]
    return list, i

  #fake votes simulation
  '''
  for x in range(50):
    votes.append(Queue(maxsize=0))
    # random votes
    for i in range(len(candidates)):
      vote = candidates[randrange(0,len(candidates))]
      if vote not in votes[x].queue:

        votes[x].put(vote)
  '''




  #for x in range(50):
  #  print(votes[x].queue[0])

  #creating dictionary with values in them
  keyvotes = {}
  for x in range(len(candidates)):
    keyvotes[candidates[x]] = []
  for x in range(len(votes)):
    keyvotes[votes[x].queue[0]].append(votes[x])


  for x in range(len(keyvotes)):
    for y in range(len(keyvotes[candidates[x]])):
      print(keyvotes[candidates[x]][y].queue)



  #sorting lowest and highest values
  totals = []
  amt =	len(keyvotes[candidates[0]])

  amt=0


  vote_order=[]

  index = 0;
  vote_final=[]
  high = 0
  low = 0


  for x in range(len(candidates)):
    amt =	len(keyvotes[candidates[x]])
    p1 = voter.Voter(candidates[x],amt)
    vote_final.append(p1)
    

    
    index =0
  insertion_sort(vote_final)
  for x in range(0,len(vote_final)):
    print(vote_final[x].name +  " || "+ str(vote_final[x].count))


  lowest = vote_final[0].count
  lowestname = vote_final[0].name
  highest = vote_final[len(vote_final)-1].count
  highestname = vote_final[len(vote_final)-1].name

  total = len(votes)
  print("HEREtotal: " + str(total))
        
  disposed = 0
  vote_percent = float(highest/total)
  nextname= 0 
  n = 0
  #Getting final result
  while(vote_percent <= .5):
    print("lowest:" + lowestname)
    
    n = 0
    for x in range(len(keyvotes[lowestname])):

      keyvotes[lowestname][x].get()
      time.sleep(0)
      print(keyvotes[lowestname][x].empty())
      q = keyvotes[lowestname][x]
      print("remove: "+lowestname)
      if q.empty():
        total= total -1
        print("EMPTY")
        continue
      nextname = keyvotes[lowestname][x].queue[0]
      print("newvote: " +nextname)
      if nextname in keyvotes:
        keyvotes[nextname].append(keyvotes[lowestname][x])
        add_one(nextname,vote_final)
      else:
        total = total-1
          
    del keyvotes[lowestname]
    candidates.remove(lowestname)
      
    if vote_final[0].count == vote_final[1].count:
      lowestname = vote_final[n+1].name
      n+=1
      
    
    vote_order=[]
    index = 0;
    vote_final=[]
    high = 0
    low = 0

    for x in range(len(candidates)):

      amt =	len(keyvotes[candidates[x]])
      p1 = voter.Voter(candidates[x],amt)
      vote_final.append(p1)

      index =0
    insertion_sort(vote_final)
    for x in range(0,len(vote_final)):
      #print(vote_final[x].name +  " || "+ str(vote_final[x].count))
      print("|" + vote_final[x].name + ":" + str(vote_final[x].count)+ "|",end="")
      
    print()
    print(len(vote_final))
    lowest = vote_final[0].count
    lowestname = vote_final[0].name
    highest = vote_final[len(vote_final)-1].count
    highestname = vote_final[len(vote_final)-1].name
    disposed = 0
    
    vote_percent = float(highest/total)
    print(str(highest) + "/" + str(total) +  "percent : " + str(vote_percent) + "%")
    nextname= 0 
    
  print("winner:" + highestname)
  return highestname
      


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


#to make sure channel that is in voting can't start another
def inVote(ctx):
  for x in voteSys_list:
    if x.channel == ctx.channel:
      return x
  return None


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  new = None
  for x in voteSys_list:
    if x.channel == message.channel:
      new = x
  

  if message.guild is None:
    for x in voteSys_list:
      if message.author in x.voterList:
        new = x

  if new != None:
    msg = message.content.lower()

    #private vote
    if message.author in new.voterList and new.anonymous == True and message.guild is None:
      votes = msg.split(',')
      for x in range(len(votes)):
        votes[x] = votes[x].strip()

      for x in votes:
        if x.lower() not in (name.lower() for name in new.candidates):
          return

        print(votes.count(x))
        if votes.count(x) > 1:
          return

      queue = Queue(maxsize=0)
      for x in votes:
        queue.put(x.strip())
        
      new.queueList.append(queue)
      
      new.voterList.remove(message.author)

      #proceed if all voters voted
      if len(new.voterList) == 0:
        winner = chooseWinner(new)
        await new.channel.send("Winner is: " + winner)
        voteSys_list.remove(new)


      for x in new.queueList:
        print(list(x.queue))
    
    
    #public vote
    elif message.author in new.voterList and message.channel == new.channel:
      votes = msg.split(',')
      #Makes sure that votes are valid
      #print("1")

      #RETURNS IF 1. 

      for x in range(len(votes)):
        votes[x] = votes[x].strip()

      for x in votes:
        if x.lower() not in (name.lower() for name in new.candidates):
          return

        print(votes.count(x))
        if votes.count(x) > 1:
          return

      queue = Queue(maxsize=0)
      for x in votes:
        queue.put(x.strip())
      new.queueList.append(queue)

      for x in new.queueList:
        print(list(x.queue))

      new.voterList.remove(message.author)

      #proceed if all voters voted
      if len(new.voterList) == 0:
        winner = chooseWinner(new)
        await new.channel.send("Winner is: " + winner)
        voteSys_list.remove(new)




  await client.process_commands(message)



#await message.channel.send(embed=displayHelpEmbed())

@client.command()
async def create(ctx):
  #if the channel is already in voting process don't start another one

  if inVote(ctx) == None:
    channel = ctx.channel
    #ask for candidate name input
    newVote = voteSys.VoteSys(client, ctx.channel)
    newVote.starter = ctx.author

    voteSys_list.append(newVote)




    #await ctx.send('🗳️ Digital Voting System')
    await ctx.send(embed = initiateEmbed(newVote))
    #FIXME inform user how to write candidate name

    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author

    msg = await client.wait_for('message', check=check)

    candidates = msg.content.split(',')
    for x in range(len(candidates)):
      candidates[x] = candidates[x].strip()
 
    newVote.candidates = candidates

    #add role voting

    #reaction voting    
    reacVote = reactionVote.ReactionVote(client)
    newVote.voterList = await reacVote.rVote(ctx)

    
    #ask self.anonymous or not
    await ctx.send("Would you like this vote to be annonymous process? [Y/N]")
    def check2(m):
      return (m.content.lower() == 'y' or m.content.lower() == 'n') and m.channel == channel and m.author == ctx.author

    msg = await client.wait_for('message', check = check2)

    #private voting
    if msg.content.lower() == 'y':
      newVote.anonymous = True
      await ctx.send ("Sending private message to every voters")

      for user in newVote.voterList:
        await user.send("Here is your candidates")
        for x in candidates:
          await user.send(x)

        await user.send("Enter your vote from most preferred to least preferred seperated by commas!") 

      await ctx.send("Enter your votes!")
      print('send embeds')
      await ctx.send(embed=displayQuotesEmbed(newVote))

    
    #public voting
    else:
      await ctx.send("Enter your vote from most preferred to least preferred seperated by commas!") 
      print('send embeds')
      await ctx.send(embed=displayQuotesEmbed(newVote))

    

  else:
    await ctx.send("This channel is already in voting process")



#FIXME stop doesn't work immediately
#this command stops current voting process
#only allow the starter to stop
@client.command()
async def stop(ctx):
  x = inVote(ctx)
  if x == None:
    await ctx.send("This server is currenlty not in voting process")
  else:
    if x.starter == ctx.author:
      await ctx.send("Ending voting process now")
      voteSys_list.remove(x)
      
    else:
      await ctx.send("Only the user who initiatied the vote can end")


@client.command()
async def proceed(ctx):
  x = inVote(ctx)
  if x == None:
    await ctx.send("This server is currenlty not in voting process\nStart Vote to use this command")
  else:
    if x.starter == ctx.author:
      await ctx.send("Force proceeding...")
      winner = chooseWinner(x)
      await x.channel.send("Winner is: " + winner)
      
    else:
      await ctx.send("Only the user who initiatied the vote can force proceed")



#to get count of how many people finished voting
@client.command()
async def currentCount(ctx):
  x = inVote(ctx)
  if x == None:
    await ctx.send("This server is currenlty not in voting process")
  else:
    count = len(x.voterList)
    await ctx.send("Currently there are " + count + " people who haven't voted yet")




#printing the queue
@client.command()
async def printQ(ctx):
  new = inVote(ctx)
  if new == None:
    await ctx.send("Initate vote to use this command!")
  else:
    for x in new.queueList:
      await ctx.send(list(x.queue))
      

#error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command!')



client.run(os.getenv('TOKEN'))