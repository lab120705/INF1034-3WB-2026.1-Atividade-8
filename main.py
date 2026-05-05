import pygame
from pygame import *
import sys
import random

pygame.init()
mixer.init()

# FONTES
fonte_padrao = font.SysFont("Arial", 40)
fonte_pequena = font.SysFont("Arial", 25)


# FUNÇÕES PRINCIPAIS


def validar_email(email):
    return email.endswith("@puc.com")

def validar_senha(s):
    if len(s) < 8:
        return False

    temM = False
    temm = False
    temN = False

    for c in s:
        if 'A' <= c <= 'Z': temM = True
        if 'a' <= c <= 'z': temm = True
        if '0' <= c <= '9': temN = True

    return temM and temm and temN

def criptografar(txt):
    res = ""
    for c in txt:
        cod = ord(c)
        if 48 <= cod <= 122:
            novo = cod + 3
            if novo > 122:
                novo = 48 + (novo - 123)
            res += chr(novo)
        else:
            res += c
    return res

def descriptografar(txt):
    res = ""
    for c in txt:
        cod = ord(c)
        if 48 <= cod <= 122:
            novo = cod - 3
            if novo < 48:
                novo = 122 - (47 - novo)
            res += chr(novo)
        else:
            res += c
    return res


# CASINHA 


def casinha():
    largura, altura = 1200, 720
    screen = display.set_mode((largura, altura))
    clock = time.Clock()

    spiderman_png = image.load("spiderman.png")
    spiderman_png = transform.scale(spiderman_png, (300, 300))
    spider_font = font.Font("spiderfont.ttf", 40)

    sol_x, sol_y = 150, 150
    sol_raio = 50

    nuvem_x, nuvem_y = 800, 100
    vel_nuvem = 200 

    tamanho_raio = 30

    som_manha = mixer.Sound("som1.mp3")
    som_tarde = mixer.Sound("som2.mp3")
    som_noite = mixer.Sound("som3.mp3")

    running = True
    while running:
        clock.tick(60)
        dt = clock.get_time() / 1000 

        for ev in event.get():
            if ev.type == QUIT:
                running = False

            if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                running = False

            if ev.type == MOUSEMOTION:
                sol_x, sol_y = ev.pos

            if ev.type == MOUSEBUTTONDOWN:
                if sol_x < 400:
                    som_manha.play()
                elif sol_x < 800:
                    som_tarde.play()
                else:
                    som_noite.play()

        keys = key.get_pressed()

        if keys[K_a] or keys[K_LEFT]: sol_x -= 400 * dt
        if keys[K_d] or keys[K_RIGHT]: sol_x += 400 * dt
        if keys[K_w] or keys[K_UP]: sol_y -= 400 * dt
        if keys[K_s] or keys[K_DOWN]: sol_y += 400 * dt

        sol_x = max(sol_raio, min(largura - sol_raio, sol_x))
        sol_y = max(sol_raio, min(altura - sol_raio, sol_y))

        nuvem_x += vel_nuvem * dt
        if nuvem_x > largura - 150 or nuvem_x < 0:
            vel_nuvem *= -1

        percentual = sol_x / largura

        if percentual < 0.5:
            p = percentual * 2
            r = 135 + (245 - 135) * p
            g = 206 + (178 - 206) * p
            b = 235 + (64 - 235) * p
        else:
            p = (percentual - 0.5) * 2
            r = 245 + (13 - 245) * p
            g = 178 + (22 - 178) * p
            b = 64 + (100 - 64) * p

        background_color = (int(r), int(g), int(b))
        tamanho_raio = 50 - (percentual * 40)

        screen.fill(background_color)

        draw.rect(screen, (34,139,34),(0,550,largura,170))

        draw.circle(screen,(255,255,0),(int(sol_x),int(sol_y)),sol_raio)
        dist = sol_raio + 10

        draw.line(screen,(255,255,0),(sol_x,sol_y-dist),(sol_x,sol_y-dist-tamanho_raio),4)
        draw.line(screen,(255,255,0),(sol_x,sol_y+dist),(sol_x,sol_y+dist+tamanho_raio),4)
        draw.line(screen,(255,255,0),(sol_x-dist,sol_y),(sol_x-dist-tamanho_raio,sol_y),4)
        draw.line(screen,(255,255,0),(sol_x+dist,sol_y),(sol_x+dist+tamanho_raio,sol_y),4)

        draw.rect(screen,(105,105,105),(450,350,200,200))
        draw.polygon(screen,(210,105,30),[(450,350),(550,200),(650,350)])
        draw.rect(screen,(139,69,19),(560,430,60,120))

        draw.circle(screen,(255,255,255),(int(nuvem_x),nuvem_y),30)
        draw.circle(screen,(255,255,255),(int(nuvem_x)+30,nuvem_y-15),40)
        draw.circle(screen,(255,255,255),(int(nuvem_x)+60,nuvem_y),30)

        screen.blit(spiderman_png,(50,310))

        cor_txt = (255,255,255) if percentual > 0.7 else (0,0,0)
        msg = spider_font.render("Casa do Miranha",True,cor_txt)
        screen.blit(msg,(450,50))

        display.update()

    display.quit()


# FORCA 


def forca_pygame():
    tela = display.set_mode((800, 600))
    display.set_caption("Forca - PyGame")
    clock = time.Clock()
    
    palavras = ["MACA","BANANA","LARANJA","MELANCIA","UVA"]
    palavra = random.choice(palavras)
    letras = []
    vidas = 6
    estado = "JOGANDO"
    modo_palavra = False
    chute = ""

    running = True
    while running:
        clock.tick(30)
        tela.fill((255,255,255))

        for ev in event.get():
            if ev.type == QUIT:
                running = False

            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    running = False

                if estado == "JOGANDO":
                    if ev.key == K_RETURN:
                        if modo_palavra:
                            if chute == palavra:
                                letras = list(palavra)
                            else:
                                vidas -= 1
                            chute = ""
                            modo_palavra = False
                        else:
                            modo_palavra = True

                    elif modo_palavra:
                        if ev.key == K_BACKSPACE:
                            chute = chute[:-1]
                        elif K_a <= ev.key <= K_z:
                            chute += chr(ev.key).upper()

                    elif K_a <= ev.key <= K_z:
                        l = chr(ev.key).upper()
                        if l in palavra:
                            if l not in letras:
                                letras.append(l)
                        else:
                            vidas -= 1

                else:
                    if ev.key == K_SPACE:
                        palavra = random.choice(palavras)
                        letras = []
                        vidas = 6
                        estado = "JOGANDO"

        # desenho boneco
        draw.line(tela,(0,0,0),(100,500),(300,500),5)
        draw.line(tela,(0,0,0),(200,500),(200,100),5)
        draw.line(tela,(0,0,0),(200,100),(400,100),5)
        draw.line(tela,(0,0,0),(400,100),(400,150),5)

        if vidas <= 5: draw.circle(tela,(0,0,0),(400,180),30,5)
        if vidas <= 4: draw.line(tela,(0,0,0),(400,210),(400,350),5)
        if vidas <= 3: draw.line(tela,(0,0,0),(400,230),(350,300),5)
        if vidas <= 2: draw.line(tela,(0,0,0),(400,230),(450,300),5)
        if vidas <= 1: draw.line(tela,(0,0,0),(400,350),(350,450),5)
        if vidas <= 0:
            draw.line(tela,(0,0,0),(400,350),(450,450),5)
            estado = "PERDEU"

        texto = ""
        venceu = True
        for l in palavra:
            if l in letras:
                texto += l+" "
            else:
                texto += "_ "
                venceu = False

        if venceu and estado == "JOGANDO":
            estado = "VENCEU"

        tela.blit(fonte_padrao.render(texto,True,(0,0,0)),(350,500))

        if modo_palavra:
            tela.blit(fonte_pequena.render("CHUTE: "+chute,True,(0,0,255)),(350,450))

        if estado == "VENCEU":
            tela.blit(fonte_padrao.render("VENCEU! ESPACO",True,(0,255,0)),(100,50))
        elif estado == "PERDEU":
            tela.blit(fonte_padrao.render("PERDEU!",True,(255,0,0)),(100,50))

        display.update()

    display.quit()


# PPT 


def ppt_pygame():
    tela = display.set_mode((800,600))
    pontos = 0
    escolha_jogador = ""
    escolha_pc = ""
    resultado = "Escolha sua jogada!"

    opcoes = ["PEDRA","PAPEL","TESOURA"]

    running = True
    while running:
        tela.fill((200,200,200))

        for ev in event.get():
            if ev.type == QUIT:
                running = False

            if ev.type == MOUSEBUTTONDOWN:
                mx,my = ev.pos

                if 400 < my < 550:
                    if 100 < mx < 250: escolha_jogador = "PEDRA"
                    elif 325 < mx < 475: escolha_jogador = "PAPEL"
                    elif 550 < mx < 700: escolha_jogador = "TESOURA"

                    if escolha_jogador:
                        escolha_pc = random.choice(opcoes)

                        if escolha_jogador == escolha_pc:
                            resultado = "EMPATE!"
                        elif (escolha_jogador == "PEDRA" and escolha_pc == "TESOURA") or \
                             (escolha_jogador == "TESOURA" and escolha_pc == "PAPEL") or \
                             (escolha_jogador == "PAPEL" and escolha_pc == "PEDRA"):
                            resultado = "VOCÊ VENCEU!"
                            pontos += 1
                        else:
                            resultado = "VOCÊ PERDEU!"

        draw.rect(tela,(100,100,100),(100,400,150,150))
        tela.blit(fonte_padrao.render("PEDRA",True,(255,255,255)),(120,460))

        draw.rect(tela,(200,200,200),(325,400,150,150),5)
        tela.blit(fonte_padrao.render("PAPEL",True,(0,0,0)),(350,460))

        draw.rect(tela,(255,100,100),(550,400,150,150))
        tela.blit(fonte_pequena.render("TESOURA",True,(0,0,0)),(580,460))

        tela.blit(fonte_padrao.render("Pontos: "+str(pontos),True,(0,0,0)),(50,50))
        tela.blit(fonte_padrao.render("PC: "+escolha_pc,True,(255,0,0)),(400,150))
        tela.blit(fonte_padrao.render("Você: "+escolha_jogador,True,(0,0,255)),(100,150))
        tela.blit(fonte_padrao.render(resultado,True,(0,0,0)),(250,250))

        display.update()

    display.quit()


# MENU


def menu():
    tela = display.set_mode((1200,720))
    fonte = font.SysFont("Arial",40)

    while True:
        tela.fill((30,30,30))

        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == MOUSEBUTTONDOWN:
                x,y = ev.pos

                if 100 < y < 150:
                    casinha()
                elif 200 < y < 250:
                    forca_pygame()
                elif 300 < y < 350:
                    ppt_pygame()
                elif 400 < y < 450:
                    pygame.quit()
                    sys.exit()

        tela.blit(fonte.render("1 - Casinha",True,(255,255,255)),(100,100))
        tela.blit(fonte.render("2 - Forca",True,(255,255,255)),(100,200))
        tela.blit(fonte.render("3 - PPT",True,(255,255,255)),(100,300))
        tela.blit(fonte.render("4 - Sair",True,(255,255,255)),(100,400))

        display.update()


# LOGIN


def login():
    tela = display.set_mode((1200,720))
    fonte = font.SysFont("Arial",30)

    email = ""
    senha = ""
    etapa = "email"
    msg = ""

    while True:
        tela.fill((50,50,50))

        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == KEYDOWN:
                if ev.key == K_BACKSPACE:
                    if etapa == "email":
                        email = email[:-1]
                    else:
                        senha = senha[:-1]

                elif ev.key == K_RETURN:
                    if etapa == "email":
                        if validar_email(email):
                            etapa = "senha"
                            msg = ""
                        else:
                            msg = "email invalido"
                            email = ""
                    else:
                        if validar_senha(senha):
                            menu()
                        else:
                            msg = "senha fraca"
                            senha = ""

                else:
                    if etapa == "email":
                        email += ev.unicode
                    else:
                        senha += ev.unicode

        tela.blit(fonte.render("Email:",True,(255,255,255)),(100,100))
        tela.blit(fonte.render(email,True,(255,255,255)),(100,150))

        tela.blit(fonte.render("Senha:",True,(255,255,255)),(100,250))
        tela.blit(fonte.render("*"*len(senha),True,(255,255,255)),(100,300))

        if senha:
            c = criptografar(senha)
            d = descriptografar(c)
            tela.blit(fonte.render("Cripto: "+c,True,(200,200,0)),(100,400))
            tela.blit(fonte.render("Decripto: "+d,True,(0,200,200)),(100,450))

        tela.blit(fonte.render(msg,True,(255,0,0)),(100,500))

        display.update()



login()