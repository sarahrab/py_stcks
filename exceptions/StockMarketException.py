from ViewManager import Model


class StockMarketException(Exception):
    def _init_(self, message: str):
        self.message = message if Model().error_messages is None else Model().error_messages.get_error_message(message)