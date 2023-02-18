import requests
import re
from bs4 import BeautifulSoup
import telebot


class email:
    token = "6127497230:AAGxMBQoa60BMdFVmUtW92a4mQ1bPatL48A"
    bot = telebot.TeleBot(token)
    message = bot.get_updates()[-1].message
    
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        email.bot.send_message(chat_id=message.chat.id, text="Digite seu nome de usuário:")

    @bot.message_handler(func=lambda message: True)
    def handle_username(message):
        username = message.text
        email.criarEmail(username)

    def enviarMensagemTelegram(mensagem, message):
        email.bot.send_message(chat_id=message.chat.id, text=mensagem, parse_mode="HTML")
    
    def enviarMensagemMarkdown(mensagem, message):
        email.bot.send_message(chat_id=message.chat.id, text=mensagem, parse_mode="Markdown")
    
    def criarEmail(usuario):
        mail_url = "https://www.invertexto.com/gerador-email-temporario?email="+usuario+"@uorak.com"    
        r = requests.get(mail_url)
        if r.status_code == 200:
            email.enviarMensagemTelegram("Conta criada com sucesso, aguardando código!", email.message)
            email.enviarMensagemMarkdown(f"Seu e-mail é: `{usuario}@uorak.com`", email.message)
            email.receberToken(r.text)
        else:
            email.enviarMensagemTelegram("Houve uma falha ao criar a conta, tente novamente!", email.message)
    
    def receberToken(resposta):
        soup = BeautifulSoup(resposta, 'html.parser')
        script = soup.find("script", string=re.compile("https://uorak.com/tempmail.php\?token="))

        if script:
            result = re.search("https://uorak.com/tempmail.php\?token=\w+", script.text)
            if result:
                token = result.group().split("=")[-1]

                email.enviarMensagemTelegram(f"Token recebido com sucesso: + {token}", email.message)
                token_url = "https://uorak.com:443/tempmail.php?token="+token
                email.receberCodigo(token_url)
            else:
                email.enviarMensagemTelegram("Token não encontrado, refaça a operaçao!", email.message)
        else:
            email.enviarMensagemTelegram("Script não encontrado, refaça a operaçao!", email.message)

    def receberCodigo(token_url):
        while True:
            resultado = requests.get(token_url)
            pattern = re.compile("\d{6}")
            matches = pattern.findall(resultado.text)

            if matches:
                email.enviarMensagemMarkdown(f"Código de ativação é: `{matches[2]}`", email.message)
                break
            else:
                pass

if __name__ == "__main__":
    email.bot.polling()