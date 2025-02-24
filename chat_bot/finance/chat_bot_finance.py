import json
import yfinance as yf
import openai
from dotenv import find_dotenv, load_dotenv
from .tools import tools

_ = load_dotenv(find_dotenv())

client = openai.Client()

def get_historical_cotation(ticker, period):
    try:
        print(f'Buscando histórico de cotação de {ticker} para o período de {period}')
        formatted_ticker = ticker.replace('.SA', '')
        ticker_obj = yf.Ticker(f'{formatted_ticker}.SA')
        hist = ticker_obj.history(period=period, auto_adjust=False)
        if len(hist) > 30:
            slice_size = int(len(hist) / 30)
            hist = hist.iloc[::-slice_size][::-1]
        
        hist.index = hist.index.strftime("%d-%m-%Y")
        return hist['Close'].to_json()
        
    except Exception as error:
        return json.dumps({"error": str(error)})
    

def ask_finance_bot(question):
    """
    Função principal que faz a pergunta para o modelo, verifica se ele
    solicitou alguma chamada de função (tool) e, caso sim, executa a tool
    correspondendo. Depois disso, retorna a resposta final do modelo.
    """
    messages = [{"role": "user", "content": question}]
    active_functions = {'get_historical_cotation': get_historical_cotation}
    
    # Primeira chamada ao modelo
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        tools=tools,
        tool_choice="auto",
    )
    
    # Verifica se houve chamadas de ferramenta na resposta
    tool_calls = response.choices[0].message.tool_calls
    
    if tool_calls:
        messages.append(response.choices[0].message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = active_functions.get(function_name)                
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })
        
        second_response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
        )

        messages.append(second_response.choices[0].message)

    print('Assistente: ', messages[-1].content)

    return messages


if __name__ == "__main__":
    print('Faça perguntas sobre cotaçoes e histórico de cotacoes de ações da bolsa de valores brasileira')

    while True:
        user_input = input("User: ")        
        final_answer = ask_finance_bot(user_input)