import ollama

def main():
    modelfile='''
    FROM llama3.2
    SYSTEM You are a financial sentiment analyzer. The only metric you care about is the S&P 500. You recieve news headlines as input and you respond with a score from -1 to 1. -1 represents a headline that will have an extremely negative impact on the S&P 500. 1 represents a headline that will have extremely positive impact on the S&P 500. 0 represents a headline that does not affect the S&P 500 in any meaningful way. Utilize decimals to represent headlines that fall somewhere in this spectrum. Be very precise. Do not respond anything other than a number ever. Numbers can have up to 16 digits. Be extremely precise. There are many things that affect the S&P 500. Some items likely to have a large impact positive or negative: changes in GDP, tax cuts or raises, major innovations, wars, inflation, job market, unemployment, interest rates, risk of bank failure, etc. Growth in certain industries may have a much larger impact on the S&P 500. Bullish is a very positive term and bearish is a very negative term for the position one is referring to. Many headlines will be completely irrelevent to movements in the S&P 500
    '''
    
    ollama.create(model='sentiment', modelfile=modelfile)
    
    f = open("llama-sent-scores.txt", "a")
    try:
        with open('input.txt', 'r') as file:
            for line in file:
                headline = line.strip()

                if headline.lower() == 'quit':
                    break

                response = ollama.chat(model='sentiment', messages=[
                    {
                        'role': 'You are a financial sentiment analyzer. The only metric you care about is the S&P 500. You recieve news headlines as input and you respond with a score from -1 to 1. -1 represents a headline that will have an extremely negative impact on the S&P 500. 1 represents a headline that will have extremely positive impact on the S&P 500. 0 represents a headline that does not affect the S&P 500 in any meaningful way. Utilize decimals to represent headlines that fall somewhere in this spectrum. ONLY EVER RESPOND IN THE FORMAT:  {"Score": {"label": "neutral","score": VALUE},"Datetime": "DATETIME"}. DO NOT RESPOND IF USER INPUT IS EMPTY OR NOT A HEADLINE. Items likely to have a large impact: changes in GDP, tax cuts or raises, major innovations, wars, inflation, job market, unemployment, interest rates, risk of bank failure, etc. Growth in certain industries may have a much larger impact on the S&P 500. Bullish is a very positive term and bearish is a very negative term for the position one is referring to. Many headlines will be completely irrelevent to movements in the S&P 500',
                        'content': 'Respond with code to fix user issues',
                    },
                    {
                        'role': 'user',
                        'content': headline,
                    },
                ])
                f.write(f"{response['message']['content']}\n")
                print(response['message']['content'])
    except FileNotFoundError:
        print("The file 'input.txt' was not found.")
    
    f.close()

if __name__ == "__main__":
    main()