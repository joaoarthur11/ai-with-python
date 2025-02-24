tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_historical_cotation',
            'description': 'Get historical cotation of a stock ticker on Yahoo Finance - BOVESPA',
            'parameters': {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker on Yahoo Finance - BOVESPA. Exemplo: PETR4 para Petrobras, ABEV3 para Ambev, VALE3 para Vale"
                    },
                    "period": {
                        "type": "string",
                        "description": "Período de histórico de cotação. Exemplo: 1d para 1 dia, 5d para 5 dias, 1mo para 1 mês, 1y para 1 ano",
                        "enum": ["1d", "5d", "1mo", "6mo", "1y", "5y", "10y", "ytd", "max"]
                    }
                },
                "required": ["ticker", "period"]
            }
        }
    }
]
