from nextcord.embeds import Embed
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from nextcord.guild import Guild
from nextcord.member import Member, VoiceState
from util.db import append_guild_current_channel, del_guild, delete_guild_current_channels, get_guild_current_channels, get_guild_vc_create_channel, get_room_name, match_guild_current_channels, remove_guild_current_channel, set_guild_current_channels, set_guild_vc_create_channel, set_room_name
from util.messages import error_embed, success_embed


class Voicerooms(commands.Cog):
    """ Voice Room commands """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        del_guild(guild.id)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if not member:
            return

        if before.channel and after.channel:
            if before.channel.id == after.channel.id:
                return

        if not before.channel and after.channel:
            if after.channel:
                for c in after.channel.guild.voice_channels:
                    try:
                        if len(c.voice_states) < 1 and match_guild_current_channels(after.channel.guild.id, c.id):
                            await c.delete()
                            remove_guild_current_channel(after.channel.guild.id, c.id)
                    except Exception as e:
                        e

                ccs = get_guild_current_channels(after.channel.guild.id)

                if ccs:
                    guild_vcs = after.channel.guild.voice_channels
                    guild_vc_ids = list(filter(lambda vc: vc.id in ccs, guild_vcs))

                    set_guild_current_channels(after.channel.guild.id, [d.id for d in guild_vc_ids])

                if after.channel.id == get_guild_vc_create_channel(after.channel.guild.id):
                    
                    if after.channel.category:
                        try:
                            room = await after.channel.category.create_voice_channel(f'{member.name}\'s {get_room_name(after.channel.guild.id)}')
                            await member.move_to(room)
                            append_guild_current_channel(after.channel.guild.id, room.id)
                        except Exception as e:
                            e
        
        if before.channel and not after.channel:
            if before.channel:
                for c in before.channel.guild.voice_channels:
                    try:
                        if len(c.voice_states) < 1 and match_guild_current_channels(before.channel.guild.id, c.id):
                            await c.delete()
                            remove_guild_current_channel(before.channel.guild.id, c.id)
                    except Exception as e:
                        e
                
                
                ccs = get_guild_current_channels(before.channel.guild.id)
                if ccs:
                    guild_vcs = before.channel.guild.voice_channels
                    guild_vc_ids = list(filter(lambda vc: vc.id in ccs, guild_vcs))

                    set_guild_current_channels(before.channel.guild.id, [d.id for d in guild_vc_ids])

                try:
                    if len(before.channel.voice_states) < 1 and match_guild_current_channels(before.channel.guild.id, before.channel.id):
                        await before.channel.delete()
                        remove_guild_current_channel(before.channel.guild.id, before.channel.id)
                except Exception as e:
                    e
    
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True, manage_channels=True)
    @commands.bot_has_guild_permissions(manage_guild=True, manage_channels=True)
    @commands.command('room-setup')
    async def room_setup(self, ctx: Context):
        """ Uses the current channel that you are in as the channel that users join to create a room """
        if not ctx.author.voice:
            await ctx.reply(embed=error_embed('You are not in a voice channel!'))
            return

        set_guild_vc_create_channel(ctx.guild.id, ctx.author.voice.channel.id)
        await ctx.reply(embed=success_embed('Successfully set your current voice channel to the voice room creation channel!'))

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True, manage_channels=True)
    @commands.bot_has_guild_permissions(manage_guild=True, manage_channels=True)
    @commands.command('remove-rooms')
    async def room_setup(self, ctx: Context):
        """ Removes the current channel that you join to create a room """

        delete_guild_current_channels(ctx.guild.id, ctx.author.voice.channel.id)
        await ctx.reply(embed=success_embed('Successfully set your current voice channel to the voice room creation channel!'))

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.command('set-room-name')
    async def set_room_name(self, ctx: Context, *room_name):
        """ Sets the name of the rooms that are created """
        name = ' '.join(room_name)
        set_room_name(ctx.guild.id, name.strip())
        await ctx.reply(embed=success_embed(f'Successfully changed the name of the rooms that are created to `{name}`.'))

def setup(bot):
    """ Setup voice room commands """
    bot.add_cog(Voicerooms(bot))