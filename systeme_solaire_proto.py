#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
# portage de planet.c

from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
# from Image import open
from PIL import Image

###############################################################
# variables globales
year, day = 0, 0  # Terre
luna, periode = 0, 0  # Lune
quadric = None
SOLEIL, TERRE, ATERRE, LUNE = 1, 2, 3, 4  # ID astre, planete, satellite
texture_planete = [None for i in range(5)]

###############################################################
# chargement des textures

def LoadTexture(filename, ident):
    global texture_planete
    image = Image.open(filename)  # retourne une PIL.image

    ix = image.size[0]
    iy = image.size[1]
    # image = image.tostring("raw", "RGBX", 0, -1)
    image = image.tobytes("raw", "RGBX", 0, -1)

    # 2d texture (x and y size)
    # BUG (?)
    #glBindTexture(GL_TEXTURE_2D, glGenTextures(1, texture_planete[ident]))
    texture_planete[ident] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, int(texture_planete[ident]))

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # commente car alpha blinding (cf. atmosphere)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

###############################################################
# creation des composants du systeme

def CreerPlanete(rayon):
    ambient = (0.1, 0.1, 0.1, 1.0)
    diffuse = (0.8, 0.8, 0.8, 1.0)
    Black = (0.0, 0.0, 0.0, 1.0)
    sph1 = gluNewQuadric()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, Black)
    glMaterialfv(GL_FRONT, GL_EMISSION, ambient)
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0)

    gluQuadricDrawStyle(sph1, GLU_FILL)
    gluQuadricNormals(sph1, GLU_SMOOTH)
    gluQuadricTexture(sph1, GL_TRUE)
    gluSphere(sph1, rayon, 100, 80)

def CreerSoleil(rayon):
    pass

###############################################################
# affichage

def display_sun():
    pass

def display_earth():
    pass

def display_atmosphere():
    pass

def display_moon():
    pass

###############################################################
#

def init_texture():
    LoadTexture("sun.bmp", 1)
    LoadTexture("earth.bmp", 2)
    LoadTexture("earthcld.bmp", 3)
    LoadTexture("moon.bmp", 4)


def init():
    global quadric
    # définir la couleur de fond de la fenêtre
    glClearColor (0.0, 0.0, 0.0, 0.0)

    # définir le modèle de rendu
    # GL_FLAT = couleur d'un triangle est uniforme pour tous ses pixels
    #glShadeModel(GL_FLAT)

    # objet quadrique, qui est une forme géométrique utilisée
    # pour représenter des sphères etc...
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

    # efface le tampon de couleur (couleur de fond)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    glTranslatef(x ,y ,zoom)
    glRotatef(u, 1, 0.0, 0.0)
    glRotatef(i, 0.0, 1, 0.0)
    glRotatef(o, 0.0, 0.0, 1)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1.0])

    drawGrid()

    # enregistre la matrice de modèle courante
    glPushMatrix()

    #init du soleil
    init_sun()

    #on traslate le soleil
    glRotatef(year, 0.0, 1.0, 0.0)
    glTranslatef(2.0, 0.0, 0.0)

    # init de la planette
    init_earth()

    glTranslatef(0.5, 0.0, 0.0)

    # init de la lune
    init_moon()

    glPopMatrix()

    # échange les buffers de la fenêtre de rendu pour afficher l'image
    glutSwapBuffers()


def reshape(width, height):
    global zoom, x, y
    global t, y, u
    fov = 45
    """
    appelée lorsque la taille de la fenêtre de rendu est modifiée.
    Elle ajuste la projection pour s'adapter à la nouvelle taille de la fenêtre.
    """
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
        day = (day + 5) % 360
        year = (year + 2) % 360
        heure = (heure + 10) % 27


    #zoom
    elif key == '-':
        zoom -= 1

    elif key == '+':
        zoom += 1

    #deplacement
    elif key == '6':
        x += 0.1

    elif key == '4':
        x -= 0.1

    elif key == '8':
        y += 0.1

    elif key == '2':
        y -= 0.1

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

    elif key == '\033':
        # sys.exit( )  # Exception ignored
        glutLeaveMainLoop()

    #reshape(800, 800)
    glutPostRedisplay()  # indispensable en Python

###############################################################
# MAIN

glutInit(sys.argv)

glutMainLoop()
