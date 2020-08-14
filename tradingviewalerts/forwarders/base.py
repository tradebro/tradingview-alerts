from abc import abstractmethod


class BaseForwarder:
    @abstractmethod
    async def send_notification(self, message: dict):
        pass

    @staticmethod
    def is_valid_message(message: dict) -> bool:
        check = map(lambda x: x in message, [
            'close',
            'indicator',
            'exchange',
            'pair',
            'action'
        ])

        return not (False in check)
