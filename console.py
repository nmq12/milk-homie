import brain

bot = brain.ChatterBot()

while True:
    request = input('You: ')
    if request == 'OK' or request == 'ok':
        print('Bot: bye')
        break
    else:
        response = bot.get_response(request)
        print('Bot:', response)
