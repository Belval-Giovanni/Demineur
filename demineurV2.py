import tuiles

def  afficherImage(x, y, colormap, image):
    
    #affiche une image au coordonnées x,y couleur issus de colormap 
    #et image nous donne le numero de l'image un tableau d'image
    
                                           
    for j in range(len(tuiles.images[0])): #j est l'ordonné d'un pixel d'une
                                           #image
        
        for i in range(len(tuiles.images[0][0])): 
                                            #i est l'abssice d'un pixel d'une
                                            #image
            
               setPixel(x+i,y+j,colormap[tuiles.images[image][j][i]]) 
                                             
    return

def afficherTuile(x, y, tuile): #affiche une image sur une tuile dont la
                                #position (x,y) est donné
    
    afficherImage(16*x,16*y,tuiles.colormap,tuile)
    
    return


def attendreClic():
    
    #La fonction retourne un enregistrement contenant les champs x et y de 
    #la tuile cliqué, et un champ drapeau (booléen) qui indique si le clic 
    #ajoute ou retire un drapeau
    
    clic = 0   #indique avec quel bouton le joueur clique
    
    while(clic==0):
        
        sleep(0.1)    
        Z = getMouse()   
        clic = Z.button   #on rafraichis
        
        if(clic!=0):
            
            X = Z.x//16     #absisse de la tuile
            Y = Z.y//16     #ordonné de la tuile
        
            #attendre que l'utilisateur lache la souris
            while(True): 
                
                sleep(0.1) 
                y = getMouse().button 
                
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
    
     #retourne un tableau de dimension 2, largeur*hauteur , chaque élement 
     #indexé par x et y nous dit si il y a une mine à cette position (booleen)
    
    jeu = grilleDeBooleens(largeur, hauteur) #je cree un tableau vierge
    
    compteur = 0  #nombre de bombe deja placé
    
    surface = largeur*hauteur 
    
    while(compteur!=nbMines):
        
        for i in range(hauteur):      
            for j in range(largeur):    
                if(compteur!=nbMines):
                    
                    if(i==y) and (j==x) : #car la tuile xy est assuré False
                        continue
                    if(jeu[i][j] == True) :#la tuile à deja une bombe
                        continue
                    if(random()<1/(surface-compteur) :#placement des bombes équiprobables
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
    drapeau = grilleDeBooleens(largeur, hauteur) #drapeau sur le plateau
    grilleDevoiler = grilleDeBooleens(largeur, hauteur) #etat (devoilé/no) d'une case
    print(mines)
    afficherTuile(X,Y,nbMinesVoisines(X, Y, mines))
    while(jeu):
        Z = attendreClic()
        X = Z[0]
        Y = Z[1]
        clic = Z[2]
        if(clic == True):   #posage de drapeau
            if(drapeau[Y][X]==False):
                afficherTuile(X,Y,13)
            elif(drapeau[Y][X]==True):
                afficherTuile(X,Y,12)
        elif(mines[Y][X]==True):
            afficherTuile(X,Y,10)
            jeu = False
        else:   #liberation des cases alentours en cas de non mines
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

demineur(11, 7, 10)
#mines = placerMines(16,16,145,0,0)
#print(mines)
#for j in range(7):
    #for i in range(11):
        #print(nbMinesVoisines(i,j,mines))