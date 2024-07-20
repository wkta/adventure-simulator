from core.events import game_events_enum


BG_COLOR = (225, 225, 225)

gevents = game_events_enum((
    'NetwExit',  # to stop network comms
    'GameEnds',  # contains : soundname

    'BoardChanges',  # contains a "board" attribute
    'ActivePlayerChanges'  # contains "curr_player"
))
