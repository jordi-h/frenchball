import pygame
import time
import sys
from random import *

#--- Constentes
FENETRE_LARGEUR = 960
FENETRE_HAUTEUR = 720

FOND_LARGEUR = 960
FOND_HAUTEUR = 720
BALLON_LARGEUR = 79
BALLON_HAUTEUR = 79
MACARON_LARGEUR = 360
MACARON_HAUTEUR = 360

ROSE = (20, 0, 0)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

pygame.init()

fenetre = pygame.display.set_mode((FENETRE_LARGEUR, FENETRE_HAUTEUR))
pygame.display.set_caption("The French Ball")
temps = pygame.time.Clock()

#--- Images
image_ballon = pygame.image.load('images/Ballon.png').convert_alpha(fenetre)
image_ballon = pygame.transform.scale(image_ballon, (BALLON_LARGEUR, BALLON_HAUTEUR))

image_macaron1 = pygame.image.load('images/macaron1.png').convert_alpha(fenetre)
image_macaron1 = pygame.transform.scale(image_macaron1, (MACARON_LARGEUR, MACARON_HAUTEUR))
image_macaron2 = pygame.image.load('images/macaron2.png').convert_alpha(fenetre)
image_macaron2 = pygame.transform.scale(image_macaron2, (MACARON_LARGEUR, MACARON_HAUTEUR))
image_fond = pygame.image.load('images/Paris.jpg').convert_alpha(fenetre)
image_fond = pygame.transform.scale(image_fond, (FOND_LARGEUR, FOND_HAUTEUR))

#--- Son
son = pygame.mixer.Sound("musique/musique.wav")


#--- Définition Fonctions (ordre depuis GameOver)
def Texte(texte, Police):
    texteFenetre = Police.render(texte, True, BLANC)
    return texteFenetre, texteFenetre.get_rect()

def message(texte):
    Texte_1 = pygame.font.SysFont('monospace', 60)
    Texte_2 = pygame.font.SysFont('monospace', 40)

    Texte_1Fen, Texte_1Rect = Texte(texte, Texte_1)
    Texte_1Rect.center = FENETRE_LARGEUR/2, ((FENETRE_HAUTEUR/2) - 70)
    fenetre.blit(Texte_1Fen, Texte_1Rect)
    
    Texte_2Fen, Texte_2Rect = Texte("Press any key to retry", Texte_2)
    Texte_2Rect.center = FENETRE_LARGEUR/2, ((FENETRE_HAUTEUR/2) + 70)
    fenetre.blit(Texte_2Fen, Texte_2Rect)

    pygame.display.flip()
    time.sleep(1)
    
    while reset() == None:
        temps.tick()

    boucle()
    
def defaite():
    message("France has been defeated")

def reset ():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP:
            continue
        return event.key
    return None

def score(comptage):
    police = pygame.font.SysFont('monospace', 20)
    texte = police.render("Score: " + str(comptage), True, BLANC)
    fenetre.blit(texte, [840, 10])

def fond(x_fond, y_fond, image_fond):
    fenetre.blit(image_fond, (x_fond, y_fond))
                 
def ballon (x_ballon, y_ballon, image_ballon):
    fenetre.blit(image_ballon, (x_ballon, y_ballon))

def macaron(x_macaron, y_macaron, espace):
    fenetre.blit(image_macaron1, (x_macaron, y_macaron))
    fenetre.blit(image_macaron2, (x_macaron, y_macaron + MACARON_HAUTEUR + espace))
    
def boucle():
    x_ballon = 150
    y_ballon = 300
    V_ballon = 0

    x_macaron = FENETRE_LARGEUR
    y_macaron = randint(-300, 1)
    espace = BALLON_HAUTEUR * 3/2
    V_macaron = 6

    x_fond = 0
    y_fond = 0

    score_actuel = 0

    #--- Boucle principale
    fini = False
    while not fini:
        #--- Traiter entrées joueur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fini = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    V_ballon = -3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    V_ballon = 3
        y_ballon += V_ballon
        
                
        #--- Dessiner l'écran
        fenetre.fill(ROSE)

        fond(x_fond, y_fond, image_fond)
                 
        ballon(x_ballon, y_ballon, image_ballon)
        
        macaron(x_macaron, y_macaron, espace)
        x_macaron -= V_macaron

        score(score_actuel)
        
        #--- Collision
        if y_ballon > FENETRE_HAUTEUR - 60 or y_ballon < -5:
            defaite()

        if x_ballon + BALLON_LARGEUR > x_macaron + 70 and x_ballon + 70 < (x_macaron + MACARON_LARGEUR):
            if y_ballon + 80 < (y_macaron + MACARON_HAUTEUR) or y_ballon + BALLON_HAUTEUR > (y_macaron + MACARON_HAUTEUR + espace + 80):
                defaite()                    


        if x_macaron < (-MACARON_LARGEUR):
            x_macaron = FENETRE_LARGEUR
            y_macaron = randint(-300, 20)
            
        #--- Incrémentation du score
        if x_macaron < (x_ballon - MACARON_LARGEUR) < x_macaron + V_macaron + 1:
            score_actuel += 1

        #--- Son
        son.play()
        #--- Rafraichir l'écran
        pygame.display.flip()
        time.sleep(1./600) #fps


boucle()
#--- Quitter pygame
pygame.display.quit()
pygame.quit()
