from kafka_consumer import KafkaConsumerClient


class MainUserView:

    def show(self):
        msgs = KafkaConsumerClient.massages
        if len(msgs) > 0:
            for m in msgs:
                if self.check_message(m):
                    print(m)
                    KafkaConsumerClient.massages.remove(m)

        # show choices

    def check_message(self, message: str) -> bool:
        return True