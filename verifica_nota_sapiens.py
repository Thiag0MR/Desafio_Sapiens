# coding: utf-8

# Programa entra no sapiens e extrai as notas finais do usuário, as quais são comparadas com as notas salvas em um arquivo
# Necessário phantomjs e yagmail (para enviar email)

# Thiago Mendes 5959
# Gabriel Alves 5988

from selenium import webdriver
import time
import os.path
import yagmail

MATRICULA = "matricula aqui"
SENHA =  "senha aqui"

LOGIN_URL = "https://sapiens.dti.ufv.br/sapiens_crp/CheckLogin.asp"

PATH = '/home/thiago/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

# connect to smtp server.
yag_smtp_connection = yagmail.SMTP( user="email.teste.sapiens@gmail.com", password="emailtester01", host='smtp.gmail.com')

enviar_email_para = "email aqui"

disciplina_nomes = []
notas_atualizadas = []
notas_antigas = []

#---------------------------------------

# Função responsável por verificar a existência do arquivo notas.txt
# Se o arquivo existir, guarda o conteudo do arquivo em uma lista e chama a função comparaNotas
# Caso não exista, o arquivo é criado com as notas atuais do sapiens

def verificaArquivo (nome_arquivo):
    if (os.path.exists(nome_arquivo)):
        f = open(nome_arquivo, "r")

        f1 = f.read().splitlines()
        for x in f1:
            notas_antigas.append (x)

        f.close ()

        comparaNotas (notas_antigas, notas_atualizadas)

    else:
        f = open(nome_arquivo, "w+")

        for x in notas_atualizadas:
            f.write (x + '\n')

        f.close ()
#---------------------------------------

# Função responsável por comparar as notas
# Se existir uma nota diferente, um email é enviado informando alteração na nota

def comparaNotas (n_antigas, n_atualizadas):

    for i in range(len(n_antigas)):
        if (n_antigas[i] != n_atualizadas[i]):
            #print ("Nota " + disciplina_nomes[i] + " atualizada !")


            # email subject
            subject = 'Nota Sapiens Atualizada'
            # email content with attached file path.
            contents = 'Sua nota na disciplina ' + disciplina_nomes[i] + ' foi atualizada !'
            # send the email
            yag_smtp_connection.send(enviar_email_para, subject, contents)

#---------------------------------------

def main ():

    driver = webdriver.PhantomJS(executable_path=PATH)

    time.sleep(1)

    driver.get(LOGIN_URL)

    time.sleep(3)

    username = driver.find_element_by_id("Usuario")
    password = driver.find_element_by_id("Senha")

    username.clear ()
    username.send_keys(MATRICULA)

    password.clear ()
    password.send_keys(SENHA)

    time.sleep(1)

    driver.find_element_by_name("Login").click()

    time.sleep(3)

    driver.switch_to.frame ("cabecalho")

    driver.find_element_by_link_text ("Avaliações").click ()

    time.sleep(3)

    driver.switch_to.default_content()

    driver.switch_to.frame ("principal")

    time.sleep(1)

    elements = driver.find_elements_by_tag_name ('p')

    for element in elements :
        nota = element.find_element_by_xpath ('table/tbody/tr[5]/td[13]/font/b').text
        disciplina = element.find_element_by_xpath ('table/tbody/tr[1]/td/b').text
        notas_atualizadas.append (nota)
        disciplina_nomes.append (disciplina)


    verificaArquivo ("notas.txt")


    driver.close()
    driver.quit()

if __name__== "__main__" :
    main()
