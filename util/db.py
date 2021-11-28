from sqlitedict import SqliteDict
from copy import deepcopy

def database():
    return SqliteDict('./data.sqlite', autocommit=True)

db = database()

def del_guild(guild_id):
    del db[guild_id]

def set_guild_vc_create_channel(guild_id, vc_id):
    db[f'guild_{guild_id}_create_channel'] = vc_id

def get_guild_vc_create_channel(guild_id):
    if f'guild_{guild_id}_create_channel' in db:
        return deepcopy(db[f'guild_{guild_id}_create_channel'])
    else:
        return None

def set_guild_current_channels(guild_id, list):
    db[f'guild_{guild_id}_current_channels'] = list

def get_guild_current_channels(guild_id):
    if f'guild_{guild_id}_current_channels' in db:
        return deepcopy(db[f'guild_{guild_id}_current_channels'])
    else:
        return None

def append_guild_current_channel(guild_id, id):
    current_channels = get_guild_current_channels(guild_id)

    if not current_channels:
        set_guild_current_channels(guild_id, [id])
    else:
        set_guild_current_channels(guild_id, current_channels + [id])

def remove_guild_current_channel(guild_id, id):
    current_channels = get_guild_current_channels(guild_id)

    if current_channels and id in current_channels:
        current_channels.remove(id)
        set_guild_current_channels(guild_id, current_channels)

def delete_guild_current_channels(guild_id):
    del db[f'guild_{guild_id}_current_channels']

def match_guild_current_channels(guild_id, id):
    current_channels = get_guild_current_channels(guild_id)
    return id in (current_channels if current_channels else [])

def get_guild(guild_id):
    """
    Get information for a discord server
    Should be in format:
    {
        'create_channel': 'Voice creation channel id'
        'current_channels': [channel_id, channel_id, ...]
    }
    """
    
    current_channels = get_guild_current_channels(guild_id)

    return {
        'create_channel': get_guild_vc_create_channel(guild_id),
        'current_channels': current_channels if current_channels else []
    }

def set_room_name(guild_id, room_name):
    db[f'guild_{guild_id}_room_name'] = room_name

def get_room_name(guild_id):
    if f'guild_{guild_id}_room_name' in db:
        return deepcopy(db[f'guild_{guild_id}_room_name'])
    else:
        return 'Room'