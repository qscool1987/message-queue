#publish message error define

MSG_OK = 0
MSG_NOT_JSON = 1
MSG_NO_OWNER = 2
MSG_BODY_ERR = 3

errorDict = {
        MSG_OK : "successful",
        MSG_NOT_JSON : "message is not json",
        MSG_NO_OWNER : "message has no owner",
        MSG_BODY_ERR : "message body error",
        }
