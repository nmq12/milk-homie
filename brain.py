from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import JaccardSimilarity


class ChatterBot:
    def __init__(self):
        self.bot = ChatBot(
            'Milk Homie',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///one_pickled_brain.db',
            preprocessors=[
                'chatterbot.preprocessors.clean_whitespace'
            ],
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    "statement_comparison_function": JaccardSimilarity,
                    "response_selection_method": get_random_response
                }
            ]
        )
        self.trainer = ListTrainer(self.bot)

    def train(self, data):
        self.trainer.train(data)

    def get_response(self, msg):
        return self.bot.get_response(msg)
