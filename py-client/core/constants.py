from .fclasses import *


STD_SCR_SIZE = (960, 720)

# --- declare all engine events ---
_TRADITIONAL_1ST_ETYPE = 32866+1  # 32866 == pygame.USEREVENT

EngineEvTypes = PseudoEnum((
    'Quit',
    'Activation',
    'FocusGained',
    'FocusLost',
    'BasicTextinput',

    'Keydown',
    'Keyup',
    'Mousemotion',
    'Mousedown',
    'Mouseup',

    'Stickmotion',  # has event.axis; event.value
    'GamepadDir',
    'Gamepaddown',
    'Gamepadup',

    'Update',
    'Paint',

    'Gamestart',
    'Gameover',
    # (used in RPGs like niobepolis, conv<- conversation)
    'ConvStart',  # contains convo_obj, portrait
    'ConvFinish',
    'ConvStep',  # contains value

    'StateChange',  # contains code state_ident
    'StatePush',  # contains code state_ident
    'StatePop',

    'RpcReceive',  # two-level reception (->tunelling if we use the json-rpc). Has num and raw_rpc_resp attributes
    'RpcError',  # contains: code, msg

    'NetwSend',  # [num] un N°identification & [msg] un string (Async network comms)
    'NetwReceive'  # [num] un N°identification & [msg] un string (Async network comms)
), _TRADITIONAL_1ST_ETYPE)
