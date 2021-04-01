import tkinter
import random

#################################################################################
#
#  Parametres du jeu

canvas = None   # zone de dessin

#Grille[0][0] désigne la case en haut à gauche
#Grille[2][0] désigne la case en haut à droite
#Grille[0][2] désigne la case en bas à gauche


Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Scores = [0,0]   # score du joueur 1 (Humain) et 2 (IA)

#################################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

def Reset_Grille():
    for i in range(len(Grille)):
        for j in range(len(Grille[i])):
            Grille[i][j] = 0

def Cases_Possibles():
    cases = []
    for i in range(len(Grille)):
        for j in range(len(Grille[i])):
            if Grille[i][j] == 0:
                cases.append([i,j])
    return cases

def Player_won():
    won = False
    if (any(Grille[i] == [1,1,1] for i in range(len(Grille)))
    or all(Grille[i][0] == 1 for i in range(len(Grille)))
    or all(Grille[i][1] == 1 for i in range(len(Grille)))
    or all(Grille[i][2] == 1 for i in range(len(Grille)))
    or (Grille[0][0]==1 and Grille[1][1]==1 and Grille[2][2] ==1)
    or (Grille[0][2]==1 and Grille[1][1]==1 and Grille[2][0]==1)):
        won = True
    return won
    
def IA_won():
    won = False
    if (any(Grille[i] == [2,2,2] for i in range(len(Grille)))
    or all(Grille[i][0] == 2 for i in range(len(Grille)))
    or all(Grille[i][1] == 2 for i in range(len(Grille)))
    or all(Grille[i][2] == 2 for i in range(len(Grille)))
    or (Grille[0][0]==2 and Grille[1][1]==2 and Grille[2][2] ==2)
    or (Grille[0][2]==2 and Grille[1][1]==2 and Grille[2][0]==2)):
        won = True
    return won

def still_cases_left():
    return any(Grille[i][j] == 0 for i in range(len(Grille)) for j in range(len(Grille[i])))
    
def JoueurHumainSimule():
    simulated_scores = []
    L = Cases_Possibles()
    if Player_won() or IA_won() or not still_cases_left():
        return CalculScore()
    for coup in L:
        Grille[coup[0]][coup[1]] = 1
        Score = JoueurIA()
        simulated_scores.append(Score[0])
        Grille[coup[0]][coup[1]] = 0
    return min(simulated_scores), L[simulated_scores.index(min(simulated_scores))]

def JoueurIA():
    simulated_scores = []
    L = Cases_Possibles()
    if Player_won() or IA_won() or not still_cases_left():
        return CalculScore()
    for coup in L:
        Grille[coup[0]][coup[1]] = 2
        Score = JoueurHumainSimule()
        simulated_scores.append(Score[0])
        Grille[coup[0]][coup[1]] = 0
    return max(simulated_scores), L[simulated_scores.index(max(simulated_scores))]

def CalculScore():
    if IA_won():
        return 1, [0,0]
    elif Player_won():
        return -1, [0,0]
    else:
        return 0, [0,0]


def Play(x,y):
    Grille[x][y] = 1
    if Player_won():
        Scores[0]+=1
        Reset_Grille()
    elif not(still_cases_left()):
        Reset_Grille()
    _, CoupAJouer = JoueurIA()
    Grille[CoupAJouer[0]][CoupAJouer[1]] = 2
    if IA_won():
        Scores[1]+=1
        Reset_Grille()
    elif not(still_cases_left()):
        Reset_Grille()
    
################################################################################
#    
# Dessine la grille de jeu

def Affiche(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill="blue", width="4" )
            canvas.create_line(0,i*100,300,i*100,fill="blue", width="4" )
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        
        msg = 'SCORES : ' + str(Scores[0]) + '-' + str(Scores[1])
        fillcoul = 'gray'
        if (PartieGagnee) : fillcoul = 'red'
        canvas.create_text(150,400, font=('Helvetica', 30), text = msg, fill=fillcoul)  
        
    
        canvas.update()   #force la mise a jour de la zone de dessin
        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
   
    window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
     
    
    print("clicked at", x,y)
    
    Play(x,y)  # gestion du joueur humain et de l'IA
    
    Affiche()

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

# fenetre
window = tkinter.Tk()
window.geometry("300x500") 
window.title('Mon Super Jeu')
window.protocol("WM_DELETE_WINDOW", lambda : window.destroy())
window.bind("<Button-1>", MouseClick)

#zone de dessin
WIDTH = 300
HEIGHT = 500
canvas = tkinter.Canvas(window, width=WIDTH , height=HEIGHT, bg="#000000")
canvas.place(x=0,y=0)
Affiche()
 
# active la fenetre 
window.mainloop()


  


    
        

      
 

