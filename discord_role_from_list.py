
# region IMPORTS
import discord
import asyncio
from discord.errors import NotFound
import nest_asyncio
nest_asyncio.apply()
from discord.ext import commands, tasks
from discord.utils import get
import pandas as pd
import time

intents = discord.Intents.default()
intents.members = True

client=discord.Client(intents=intents)

@client.event
async def on_ready():
    #print('We have logged in as {0.user}'.format(client))
    usernames= ['tropoFarmer#0001', 'dylorr#0001']
    guild = client.get_guild(854127831047340066)
    role = discord.utils.get(guild.roles,name="SHAQ'S NICE LIST")

    # #using by name#1234 ----
    # import csv
    # prewhitelist_file= pd.read_csv('converted.csv')
    # prewhitelist_list = prewhitelist_file['usernames'].tolist()
    # #prewhitelist_list = [x for x in prewhitelist_list if '#' in x]
    # prewhitelist_list = [x.lstrip("!*@$") for x in prewhitelist_list]

    #      #loop through list of names
    # for x in prewhitelist_list:
    #     try: 
    #         user = discord.utils.get(guild.members, name= x[:-5], discriminator= x[-4:])
    #         await user.add_roles(role)
    #         print(f'✅ Succesfully added {user} to {role}')
    #         time.sleep(3)
    #     except AttributeError: 
    #         print(f'❌ {x} was unable to be added to the {role}') 


    #using by ids
    import csv
    # prewhitelist_file= pd.read_csv('premint_winners.csv')
    # prewhitelist_list = prewhitelist_file['discord id'].tolist()
    # prewhitelist_list = [int(x) for x in prewhitelist_list]

    # prewhitelist_list = prewhitelist_list[:100]
    #loop through list of names
    prewhitelist_file = pd.read_excel('all_ids.xlsx')
    
    prewhitelist_file.drop(index=prewhitelist_file.index[0], 
            axis=0, 
            inplace=True)

    prewhitelist_file = prewhitelist_file.fillna(0)
    import numpy
    prewhitelist_file['Table 1'] = prewhitelist_file['Table 1'].astype(numpy.int64)
    prewhitelist_list = prewhitelist_file['Table 1'].tolist()

    #merge previously added lists
    #
    #
    
    #new = [i for i in l if i not in l1]

    not_found = 0

    # record newly appended users to role
    newly_added = []
    from datetime import datetime
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for x in prewhitelist_list:
        try:
            print(x)
            username_convert = await client.fetch_user(x)
            discrim_1 = str(username_convert.discriminator)
            user_1 = str(username_convert.display_name)
            newstring = (user_1 + '#' + discrim_1)
            print(newstring)
            user = discord.utils.get(guild.members, name= newstring[:-5], discriminator= newstring[-4:])
            await user.add_roles(role)
            print(f'✅ Succesfully added {user} to {role}')
            # append newly added to list
            newly_added.append(x)
            time.sleep(3)

        except NotFound:
            print(f'{x} not found') 
            not_found = not_found + 1
        except AttributeError: 
            print(f'❌ {newstring} was unable to be added to the {role}') 
    print('Creating export for newly added to role ids....')
    new_adds = len(newly_added)
    print(f'New Adds: {new_adds}')
    print(f'Not Added: {not_found}')
    newly_added_df = pd.DataFrame(newly_added, columns =['discord id'])
    file_string = (f'newlyadded-{current_time}.csv')
    newly_added_df.to_csv(file_string)

    #converted = pd.DataFrame(discord_usernames_new, columns=['usernames'])
    #converted.to_csv('converted.csv') # relative position
    #print(f'total not found: {not_found}')
    # try: 
    #     user = discord.utils.get(guild.members, name= newstring[:-5], discriminator= newstring[-4:])
    #     print(newstring[:-5])
    #     print(newstring[-4:])
    #     print(user)
    #     await user.add_roles(role)
    #     print(f'✅ Succesfully added {user} to {role}')
    #     time.sleep(3)
    # except AttributeError: 
    #     print(f'❌ {newstring} was unable to be added to the {role}') 


client.run('[insert token here]')
