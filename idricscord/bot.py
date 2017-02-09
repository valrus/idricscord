import asyncio
import os
import sys

import discord
import sopel
import sopel.bot
import sopel.module


class SopelClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.content.startswith('!test'):
            counter = 0
            tmp = await self.send_message(message.channel, 'Calculating messages...')
            async for log in self.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1

            await self.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await self.send_message(message.channel, 'Done sleeping')


@sopel.module.commands('helloworld')
def helloworld(bot, trigger):
    bot.say('Hello, world!')


def main():
    irc_config = sopel.config.Config('irc.cfg')
    irc_client = sopel.bot.Sopel(irc_config)
    # irc_client needs to be run
    # one of the run() calls needs to happen in an executor, I think
    discord_client = SopelClient().run(os.environ.get('IDRICSCORD_TOKEN'))


if __name__ == '__main__':
    sys.exit(main())
