from telegraph import Telegraph


def create_telegra_account(nickname):
    """
    Создание аккаунта и получение токена при помощи библиотеки telegraph
    """
    telegraph = Telegraph()
    result=telegraph.create_account(short_name=nickname)
    print(result)
    print('Your acces token is', result['access_token'])


nickname = ''

create_telegra_account(nickname)