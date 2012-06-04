class ServerConstants:
    MSG_REGISTER_CLIENT = 0
    MSG_GET_GAME_STATE  = 1
    MSG_START_GAME      = 2
    
    MSG_CLIENT_ERROR    = 0
    MSG_CLIENT_OK       = 1

    MSG_START_ERROR     = 0
    MSG_START_OK        = 1
    MSG_START_INPROGRESS = 2
    MSG_START_WAITING   = 3
    
    PADDLE_WIDTH        = 0.2
    WINNING_SCORE       = 10

    DIRECTION_TOP       = 0
    DIRECTION_BOTTOM    = 1
    DIRECTION_LEFT      = 2
    DIRECTION_RIGHT     = 3

    TIME_STEP_SIZE      = 0.005
    MIN_SPEED           = 0.1 * TIME_STEP_SIZE
    MAX_SPEED           = 0.3 * TIME_STEP_SIZE
