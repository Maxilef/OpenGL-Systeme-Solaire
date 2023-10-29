#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# IL RESTE A FAIRE LES TEXTURE
# LA FONCTION A ÉTAIT IMPLENTER
# ON SE SERT D'UN DICO POUR CHARGER LES IMAGES AU PRÉALABLE DEDANS
# VOIR DANS INIT, RESTE A L'APPLIQUER A CHAQUE PLANETTE



###############################################################
from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time

from math import pi, cos, sin
from PIL import Image
import numpy as np




###############################################################
# variables globales
year, day = 0, 0
heure = 0
quadric = None
zoom = -25
x,y = 0,-4
u, i, o = 20,0,0

mercure = 0
venus = 0
mars = 0
jupiter,saturne,neptune,uranus = 0,0,0,0

vitesse = 4000

tmp = 0


###############################################################
#

def load_texture(image):
    """
    charge la texture de l'image donné
    """
    texture_data = image.tobytes()
    width = image.width
    height = image.height

    glEnable(GL_TEXTURE_2D)
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    return tex_id


def drawGrid():
    """
    dessine une grille de 15 par 15
    """
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5) # couleur des lignes
    size = 15 # nombre de lignes
    step = 1 # espace entre les lignes
    for i in range(-size, size+1, step):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_anneaux(a,b,c, taille1, taille2,incliner):
    """
    dessine anneaux des planette
    a,b,c = color anneaux
    taille1/2 = rayon de debut et fin de l'anneau
    """
    glDisable(GL_LIGHTING)

    glColor3f(a, b, c) # couleur des anneaux

    # rayon intérieur et extérieur des anneaux
    inner_radius = taille1
    outer_radius = taille2

    # nombre de segments de la bande rectangulaire
    num_segments = 64

    # angle de chaque segment
    segment_angle = 2*pi / num_segments

    glRotatef(incliner, 0, 0, 1)
    glBegin(GL_QUAD_STRIP)
    for i in range(num_segments+1):
        angle = i * segment_angle
        x = outer_radius * cos(angle)
        z = outer_radius * sin(angle)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(x, 0.0, z)

        x = inner_radius * cos(angle)
        z = inner_radius * sin(angle)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(x, 0.0, z)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_trajectoir():
    draw_anneaux(1, 1, 1, 1.99, 2, 0)
    draw_anneaux(1, 1, 1, 3.19, 3.2, 0)
    draw_anneaux(1, 1, 1, 4.39, 4.4, 0)
    draw_anneaux(1, 1, 1, 5.99, 6, 0)
    draw_anneaux(1, 1, 1, 7.79, 7.8, 0)
    draw_anneaux(1, 1, 1, 2+1.8+6-0.01, 2+1.8+6, 0)
    draw_anneaux(1, 1, 1, 2+1.8+6-0.01+2, 2+1.8+6+2, 0)
    draw_anneaux(1, 1, 1, 2+1.8+6-0.01+2+2, 2+1.8+6+2+2, 0)

##############
#   INIT

def luminous():
    """
    active la lumiére
    """
    # LUMIERE
    # Activer l'éclairage
    glEnable(GL_LIGHTING)

    # Définir la position et la couleur de la source lumineuse
    glLoadIdentity()
    glPushMatrix()

    glTranslatef(x ,y ,zoom)
    glRotatef(u, 1, 0.0, 0.0)
    glRotatef(i, 0.0, 1, 0.0)
    glRotatef(o, 0.0, 0.0, 1)


    glEnable(GL_LIGHT0) # Activer la source lumineuse 0
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1.0]) # Position de la source lumineuse
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0]) # Couleur de la source lumineuse
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0]) # Couleur de la réflexion spéculaire
    glPopMatrix()

def init_sun():
    """
    crée le soleil avec ces parametre de matiére ect...
    """
    glDisable(GL_LIGHTING)

    # SUN
    # Définir les propriétés de matériau pour l'astre
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    # L'ASTRE
    # couleur dessin
    glColor4f (1.0, 1.0, 0 , 1.0) #jaune

    # dessine une sphère de rayon 1.0 avec 40 méridiens et 40 parallèles,
    gluSphere(quadric, 1.0, 1000, 1000)

    glEnable(GL_LIGHTING)


def init_earth():
    # planette
    # Définir les propriétés de matériau pour la planette
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 0.4, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 0)


    # LA PLANETTE
    #glColor4f (0, 0, 1.0, 1.0) #bleu

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.2, 1000, 1000)

    # Dessiner l'atmosphère
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 0.2])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.2, 0.8, 0.2])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 0.2])
    glMaterialfv(GL_FRONT, GL_SHININESS, 5)

    glEnable(GL_BLEND)  # Activer le mélange de couleurs
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Définir la fonction de mélange
    glColor4f(0.2, 0.2, 0.8, 0.2)  # Définir la couleur de l'atmosphère
    gluSphere(quadric, 0.28, 1000, 1000)  # Dessiner l'atmosphère
    glDisable(GL_BLEND)  # Désactiver le mélange de couleurs



def init_moon():
    # LUNE
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    # LA PLANETTE
    glColor4f (1.0, 1.0, 1.0, 1.0) #bleu

    glRotatef(heure, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.08, 1000, 1000)

def init_mars():
    # LUNE
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    # LA PLANETTE
    glColor4f (1.0, 1.0, 1.0, 1.0) #bleu

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.35, 1000, 1000)


def init_mercure():
    # mercure
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0.5, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    # LA PLANETTE
    glColor4f (1.0, 1.0, 1.0, 1.0) #bleu

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.14, 1000, 1000)

def init_venus():
    # mercure
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.18, 180, 100)


def init_jupiter():
    # mercure
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 1, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.60, 180, 100)
    draw_anneaux(0.5, 0.5, 0.5, 0.5, 0.70,30)




def init_saturne():
    # mercure
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.5, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.50, 180, 100)

    glRotatef(day, 0.0, 1, 0.0)
    draw_anneaux(0.5, 0.5, 0.5, 0.5, 0.60,30)
    glRotatef(day, 0.0, 1, 0.0)
    draw_anneaux(0.5, 0.5, 0.5, 0.61, 0.67,30)
    glRotatef(day, 0.0, 1, 0.0)
    draw_anneaux(0.5, 0.5, 0.5, 0.68, 0.72,30)
    glRotatef(day, 0.0, 1, 0.0)
    draw_anneaux(0.5, 0.5, 0.5, 0.73, 0.74,30)



def init_uranus():
    # mercure
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 1, 1, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.42, 180, 100)

    draw_anneaux(0.5, 0.5, 0.5, 0.6, 0.64,30)
    glRotatef(day, 0.0, 1.0, 0.0)
    draw_anneaux(0.5, 0.5, 0.5, 0.65, 0.66,30)


def init_neptune():
    # mercure
    # Définir les propriétés de matériau pour la LUNE
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.6, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [100])

    glRotatef(day, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.42, 180, 100)
    draw_anneaux(0.5, 0.5, 0.5, 0.5, 0.55,30)


################
def init():
    """
    init fenetre d'affichage et parametre
    """
    global quadric
    # définir la couleur de fond de la fenêtre
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)

    # définir le modèle de rendu
    # GL_FLAT = couleur d'un triangle est uniforme pour tous ses pixels
    # glShadeModel(GL_FLAT)

    # objet quadrique, qui est une forme géométrique utilisée
    quadric = gluNewQuadric()

    # configure le style de dessin pour l'objet quadrique
    # GLU_LINE dessine avec des lignes
        #gluQuadricDrawStyle(quadric, GLU_LINE)

    glEnable(GL_DEPTH_TEST) #buffer
    glPolygonMode(GL_FRONT, GL_FILL)
    glShadeModel(GL_SMOOTH)
    luminous()


def display():
    """
    appelée à chaque fois que la fenêtre de rendu doit être mise à jour.
    Elle efface l'écran avec la couleur de fond, définit la couleur de dessin
    sur blanc, dessine la planète en utilisant l'objet quadrique, et effectue
    des rotations et des translations pour simuler la rotation de la planète autour
    de son étoile.
    Elle termine en échangeant les buffers de la fenêtre de rendu pour afficher l'image.
    """

    #ouverture image pour texture
    ouverture_earth = Image.open("earth.bmp")


    DICO_TEXTURES = {"earth" : ouverture_earth}



    # efface le tampon de couleur (couleur de fond)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    glTranslatef(x ,y ,zoom)
    glRotatef(u, 1, 0.0, 0.0)
    glRotatef(i, 0.0, 1, 0.0)
    glRotatef(o, 0.0, 0.0, 1)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1.0])

    #drawGrid()

    # enregistre la matrice de modèle courante
    glPushMatrix()

    #init du soleil
    tex_id = load_texture(DICO_TEXTURES["earth"])
    init_sun()

    draw_trajectoir()

    #########################
    glPushMatrix()
    glRotatef(mercure,0,1,0)
    glTranslatef(2.0, 0.0, 0.0)
    init_mercure()
    glPopMatrix()
    #########################


    #########################
    glPushMatrix()
    glRotatef(venus,0,1,0)
    glTranslatef(3.2, 0, 0.0)
    init_venus()
    glPopMatrix()
    #########################


    ########################
    glPushMatrix()
    glRotatef(year,0,1,0)
    glTranslatef(4.4, 0, 0.0)
    # init de la planette

    init_earth()
    glTranslatef(0.5, 0.0, 0.0)
    # init de la lune
    init_moon()

    glPopMatrix()
    #########################



    #########################
    glPushMatrix()
    glRotatef(mars,0,1,0)
    glTranslatef(6, 0.0, 0.0)
    init_mars()
    glPopMatrix()
    #########################



    #########################
    glPushMatrix()
    glRotatef(jupiter,0,1,0)
    glTranslatef(1.8+6, 0.0, 0.0)
    init_jupiter()
    glPopMatrix()
    #########################



    #########################
    glPushMatrix()
    glRotatef(saturne,0,1,0)
    glTranslatef(2+1.8+6, 0.0, 0.0)
    init_saturne()
    glPopMatrix()
    #########################

    #########################
    glPushMatrix()
    glRotatef(uranus,0,1,0)
    glTranslatef(2+1.8+6+2, 0.0, 0.0)
    init_uranus()
    glPopMatrix()
    #########################

    #########################
    glPushMatrix()
    glRotatef(neptune,0,1,0)
    glTranslatef(2+1.8+6+2+2, 0.0, 0.0)
    init_neptune()
    glPopMatrix()
    #########################"""

    glPopMatrix()

    # échange les buffers de la fenêtre de rendu pour afficher l'image
    glutSwapBuffers()


def reshape(width, height):
    """
    appelée lorsque la taille de la fenêtre de rendu est modifiée.
    Elle ajuste la projection pour s'adapter à la nouvelle taille de la fenêtre.
    """


    global zoom, x, y
    global t, y, u
    fov = 45

    glViewport(0, 0, width, height) #définiton de la view port. 0, 0 en bas à gauche

    glMatrixMode(GL_PROJECTION) # mode d'affichage
    glLoadIdentity()
    gluPerspective(fov, width/height, 0.5, 100.0)

    glMatrixMode(GL_MODELVIEW) # matrice spécifique d'affichage
    glLoadIdentity()





def keyboard_up(key, x, y):
    """
    print la touche qui est relaché lors de l'event keyboard
    """
    up = key
    #print(up)


def keyboard(key, droite, gauche):
    """
    appelée lorsque l'utilisateur appuie sur une touche du clavier
    """
    global day, year, heure, zoom, x, y
    global u,i,o
    global vitesse
    global mercure,venus,mars,jupiter,saturne,neptune,uranus


    key = key.decode('utf-8')
    if key == 'd':
        day = (day + 5) % 360
        heure = (heure + 10 ) % 27

    elif key == 'a':
        year = (year + 2) % 360
        day = (day + 5 ) % 360

    elif key == 'h':
        heure = (heure + 1) % 27

    elif key == 's':
        rotation_all()

    ################
    #zoom
    elif key == '-':
        zoom -= 1

    elif key == '+':
        zoom += 1

    ################
    #deplacement
    elif key == '6':
        x += 0.1

    elif key == '4':
        x -= 0.1

    elif key == '8':
        y += 0.1

    elif key == '2':
        y -= 0.1

    ################
    #rotation
    elif key == 'u':
        u += 0.5

    elif key == 'j':
        u -= 0.5

    elif key == 'i':
        i += 0.5

    elif key == 'k':
        i -= 0.5

    elif key == 'o':
        o += 0.5

    elif key == 'l':
        o -= 0.5

    elif key == 'w':
        tmp = 0
        while tmp < 365:
            rotation_all()
            display()
            tmp = tmp +1
        print(tmp)

    elif key == '\033':
        # sys.exit( )  # Exception ignored
        glutLeaveMainLoop()

    #reshape(800, 800)
    glutPostRedisplay()  # indispensable en Python


def rotation_all() :
    """
    effectue simulation compléte de la rotation des planettes dans systeme solaire
    """

    global day, year, heure, zoom, x, y
    global u,i,o
    global vitesse

    global mercure,venus,mars,jupiter,saturne,neptune,uranus
    day = (day + 5) % 360
    year = (year + vitesse/365.0) % 360
    heure = ((heure +vitesse)/27.3) % 360

    mercure = (mercure + vitesse/88.0) % 360
    venus = (venus + vitesse/225.0) % 360
    mars = (mars + vitesse/687.0) % 360
    jupiter = (jupiter + vitesse/(12*365.0)) % 360
    saturne = (saturne + vitesse/(29*365.0)) % 360
    uranus = (uranus + vitesse/(84*365.0)) % 360
    neptune = (neptune + vitesse/(165*365.0)) % 360




###############################################################
# MAIN

# initialise la bibliothèque GLUT.
glutInit()

# définit les paramètres d'affichage pour la fenêtre de rendu.
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)


# crée une nouvelle fenêtre de rendu.et
# définit la taille initiale de la fenêtre de rendu.
glutCreateWindow('planet')
glutReshapeWindow(800,800)

# définit la fonction de rappel pour le redimensionnement de la fenêtre.
glutReshapeFunc(reshape)
# définit la fonction de rappel pour l'affichage de la fenêtre.
glutDisplayFunc(display)
# définit la fonction de rappel pour les événements de clavier.
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboard_up)


# appelée pour initialiser les paramètres de rendu.
init()

# lance la BOUCLE principale de GLUT pour gérer les événements.
glutMainLoop()
