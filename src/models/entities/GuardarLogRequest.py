class GuardarLogRequest():

    def __init__(self, datetime = int, idUsuario = str, messageLog = str, messageId = str) -> None:
        self.datetime = datetime
        self.idUsuario = idUsuario
        self.messageLog = messageLog
        self.messageId = messageId
    
    def to_JSON(self):
        return {
            'datetime': self.datetime,
            'idUsuario': self.idUsuario,
            'messageLog': self.messageLog,
            'messageId': self.messageId
        }