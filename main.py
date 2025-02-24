from chat_bot.default.conversation import start_chat
from chat_bot.finance.chat_bot_finance import ask_finance_bot


if __name__ == "__main__":
    print('Faça perguntas sobre cotaçoes e histórico de cotacoes de ações da bolsa de valores brasileira')

    while True:
        user_input = input("User: ")        
        final_answer = ask_finance_bot(user_input)