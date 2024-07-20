from core.events import game_events_enum


gevents = game_events_enum((
    'BoardChanges',  # contains a "board" attribute
    'ActivePlayerChanges'  # contains "curr_player"
))
