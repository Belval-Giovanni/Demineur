import tuiles

def  afficherImage(x, y, colormap, image):
    
    #affiche une image au coordonnées x,y avec un panel de couleur issus de
    #colormap et image nous donne le numero de l'image dans un enregistrement
                                           
    for j in range(len(tuiles.images[0])): #j est l'indice donnant la ligne
                                               #de pixel dans une image
        
        for i in range(len(tuiles.images[0][0])): 
                                               #i est l'indice  de tout les 
                                              #éléments d'une ligne de pixel 
                                              #dans une image
            
               setPixel(x+i,y+j,colormap[tuiles.images[image][j][i]])
                
                #on parcours tout les élements d'une image 1 par 1 et on le 
                #représente sur notre écran
                                             
    return

def afficherTuile(x, y, tuile): #affiche une image sur une tuile dont la
                                #position est donné
    
    afficherImage(16*x,16*y,tuiles.colormap,tuile)
    
    return


def attendreClic():
    
    #La fonction retourne un enregistrement contenant les champs x et y qui 
    #indiquent la coordonnée de la tuile sur laquelle le joueur a cliqué, et un
    #champ drapeau qui indique avec un booléen si le clic correspond à une 
    #action pour ajouter/retirer un drapeau
    
    clic = 0
    
    while(clic==0):#on ne fait rien tant que le joueur ne clique pas sur une 
                   #tuile
        
        sleep(0.1)    #permet d'effectuer moins d'iteration pendant un temps
                      #imperceptible pour l'utilisateur
        Z = getMouse()   
        clic = Z.button   #on rafraichis
        
        if(clic!=0):#quand il clique on retourne les informations importante 
                #position de la tuile , drapeau ou non , etc
            
            X = Z.x//16     #represente l'absisse de la tuile
            Y = Z.y//16     #represente l'ordonné de la tuile
        
            while(True):#cette boucle permet d'attendre que l'utilisateur lache  
                  #la souris 
                
                sleep(0.1) 
                y = getMouse().button #permet de dire si l'utilisateur lache la 
                                  #souris
                if(y==0):
                    if(clic!=1):
                        return [X,Y,True]
            
                    else:
                        return [X,Y,getMouse().ctrl]
    
    return

def grilleDeBooleens(largeur, hauteur):
    
    #je cree un tableau qui va me dire si oui ou non j'ai un drapeau sur une
    #tuile quelquonque de mon espace de jeu
    
    tableau = []
     
    tableau = [None]*hauteur     
        
    for i in range(hauteur):
        
        tableau[i] = [False]*largeur
         
    
    return tableau

def placerMines(largeur, hauteur, nbMines, x, y):
    
     #La fonction placerMines retourne un tableau de hauteur tableaux de 
     #largeur booléens. Chaque élément de ce tableau à 2 dimensions indique 
     #s'il y a une mine sous la tuile à cette coordonnée. Tous les éléments 
     #sont False sauf pour nbMines éléments aléatoirement choisis qui sont True
     #L'élément qui correspond à la tuile à la coordonnée (x,y) est garantie 
     #False 
    
    jeu = grilleDeBooleens(largeur, hauteur) #represente l'etat de chaque
                                             #tuiles vis à vis des bombes  
    compteur = 0  #me sert a compter le nombre de bombe deja placé
    
    while(compteur!=nbMines):
        
        for i in range(hauteur):      #je parcours les tuiles  
            for j in range(largeur):  #une par une
                
                if(compteur!=nbMines):
                    
                    if(i==y) and (j==x) : #car la tuile xy est assuré False
                        continue
                    if(jeu[i][j] == True) :#la tuile à deja une bombe
                        continue
                    if(random()<0.5) :#1 chance sur deux de placé une bombe
                        jeu[i][j] = True
                        compteur+=1 
    
    return jeu

def nbMinesVoisinesBase(x,y,mines): 
    #determine le nombre de mine voisine si xy est en bordure haute de la 
    #grille , ou si xy est un élement qui n'est pas marginal
                                    
    compteur = 0  #stocke le nombre de bombe autour de xy
    hauteur = getHauteur(mines)
    largeur = getLargeur(mines)
    if(y==0):                        #calcul du nombrede bombe 
        if(x==0):                    #pour la tuile 0,0
            if(mines[y][x+1]==True):
                compteur+=1
            if(mines[y+1][x+1]==True):
                compteur+=1
            if(mines[y+1][x]==True):
                compteur+=1
                
        elif(x<getLargeur(mines)-1):#pour chaque tuile marginale haute sauf
                                     #la dernière
            if(mines[y][x+1]==True):
                compteur+=1
            if(mines[y][x-1]==True):
                compteur+=1
            if(mines[y+1][x]==True):
                compteur+=1
            if(mines[y+1][x-1]==True):
                compteur+=1
            if(mines[y+1][x+1]==True):
                compteur+=1
        else:                         #pour la derniere
            if(mines[y][x-1]==True):
                compteur+=1
            if(mines[y+1][x]==True):
                compteur+=1
            if(mines[y+1][x-1]==True):
                compteur+=1
                
    elif(x>0)and(x<largeur-1)and(y>0)and(y<hauteur-1):#non marginale
        
        if(mines[y-1][x-1]==True):
                compteur+=1
        if(mines[y-1][x]==True):
                compteur+=1
        if(mines[y-1][x+1]==True):
                compteur+=1 
        if(mines[y][x-1]==True):
                compteur+=1
        if(mines[y][x+1]==True):
                compteur+=1        
        if(mines[y+1][x-1]==True):
                compteur+=1 
        if(mines[y+1][x]==True):
                compteur+=1
        if(mines[y+1][x+1]==True):
                compteur+=1 
        
    return compteur

def getLargeur(grilleDeBoolean):
    return len(grilleDeBoolean[0])
                
def getHauteur(grilleDeBoolean):
    return len(grilleDeBoolean)

def matriceTranspose(matrice): # retourne la matrice transposé
    
    hauteur = getHauteur(matrice)
    largeur = getLargeur(matrice)
    
    transpose = grilleDeBooleens(hauteur, largeur) #dimension inversé
    
    for i in range(largeur):
        for j in range(hauteur):
            transpose[i][j]=matrice[j][i]
            
    return transpose

def matriceTransform(matrice):
    
    hauteur = getHauteur(matrice)
    largeur = getLargeur(matrice)
    
    transform = grilleDeBooleens(largeur, hauteur)
    
    for i in range(hauteur):
        for j in range(largeur):
            transform[i][j]=matrice[hauteur-1-i][largeur-1-j]
    return transform

def nbMinesVoisines(x, y, mines):
    
    largeur = getLargeur(mines)
    hauteur = getHauteur(mines)
    
    if(y==0): #sur la ligne margine haute de la grille 
        return nbMinesVoisinesBase(x,y,mines)
    
    elif(x==0):#sur la ligne marginale gauche / cela représente la ligne 
               #marginale haute de la grille transposé ( au sens matriciel )
            
        return nbMinesVoisinesBase(y,x,matriceTranspose(mines))
    
    elif(y==hauteur-1):#ligne marginale basse de la grille / cela représente 
                       #la ligne marginale haute de la transformé de la grille
                       #au sens matriciel
                       #( transformation y = (hauteur-1)-y , x = (largeur-1)-x)
                    
        return nbMinesVoisinesBase(largeur-1-x,hauteur-1-y,\
                                   matriceTransform(mines))
    
    elif(x==largeur-1):#ligne marginale droite / represente la ligne marginale
                       #haute de la transposé de la transformé de la grille
            
        return nbMinesVoisinesBase(hauteur-1-y,largeur-1-x,\
                                   matriceTranspose(matriceTransform(mines)))
    
    else:              #ligne non marginale
        return nbMinesVoisinesBase(x,y,mines)
        
    return

def afficherGrille(largeur,hauteur):
    setScreenMode(largeur*16,hauteur*16)
    for j in range(hauteur):
        for i in range(largeur):
            afficherTuile(i,j,12)
    return



def demineur(largeur, hauteur, nbMines):
    afficherGrille(largeur,hauteur)
    jeu = True
    Z = attendreClic()
    X = Z[0]
    Y = Z[1]
    mines = placerMines(largeur,hauteur,nbMines,X,Y)
    print(mines)
    afficherTuile(X,Y,nbMinesVoisines(X, Y, mines))
    while(jeu):
        Z = attendreClic()
        X = Z[0]
        Y = Z[1]
        clic = Z[2]
        if(clic == True):
            afficherTuile(X,Y,13)
        elif(mines[Y][X]==True):
            afficherTuile(X,Y,10)
            #jeu = False
        else:
            if(nbMinesVoisines(X, Y, mines)==0):
                afficherTuile(X,Y,0)
                if(X==0)and(Y==0):
                    for i in [0,1]:
                        for j in [0,1]:
                            if(j+i==0):
                                continue
                            afficherTuile(i,j,\
                                          nbMinesVoisines(X+i,Y+j, mines))
                elif(Y==0)and(X!=largeur-1):
                    for i in [-1,0,1]:
                        for j in [0,1]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
                elif(X==0)and(Y!=hauteur-1):
                    for j in [-1,0,1]:
                        for i in [0,1]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
                elif(X==0)and(Y==hauteur-1):
                    for j in [-1,0]:
                        for i in [0,1]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
                elif(X==largeur-1)and(Y==0):
                    for j in [1,0]:
                        for i in [-1,0]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
                elif(X!=largeur-1)and(Y==hauteur-1):
                    for j in [-1,0]:
                        for i in [-1,0,1]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
                elif(X==largeur-1)and(Y==hauteur-1):
                    for j in [-1,0]:
                        for i in [0,-1]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
                elif(X==largeur-1)and(Y!=hauteur-1):
                    for j in [-1,0,1]:
                        for i in [0,-1]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
                else:
                    for j in [-1,0,1]:
                        for i in [1,0,-1]:
                            if(i==0)and(j==0):continue
                            afficherTuile(X+i,Y+j,\
                                              nbMinesVoisines(X+i,Y+j, mines))
            else:
                afficherTuile(X,Y,nbMinesVoisines(X, Y, mines))
    return

demineur(11, 7, 30)
#mines = placerMines(16,16,145,0,0)
#print(mines)
#for j in range(7):
    #for i in range(11):
        #print(nbMinesVoisines(i,j,mines))






            
 




    
