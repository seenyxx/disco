from nextcord.embeds import Embed

def error_embed(desc):
    return Embed(title='Error', description=desc, color=0xff5a52)

def error_too_many_args():
    return error_embed('Too many arguments were given!')

def error_help_menu_notfound():
    return error_embed('Command/Category not found!')

def success_embed(desc):
    return Embed(title='Success', description=desc, color=0x31d663)