import time
import pygame

pygame.init()

window_width = 1400
window_height = 1400
margin = 200

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Crows and Vulture GAME")


original_image = pygame.image.load("board.jpeg")
image = pygame.transform.scale(original_image, (window_width - 2 * margin, window_height - 2 * margin))  # Resize the image

BLUE = (65, 105, 225)
PINK = (255, 20, 147)
BLACK = (0, 0, 0)

crowTokens = [(108, 400), (108, 500), (108, 600), (108, 700), (108, 800), (108, 900), (108, 1000)]
previousCrowPositions = [(108, 400), (108, 500), (108, 600), (108, 700), (108, 800), (108, 900), (108, 1000)]
vultureToken = (1280,1000)
previousVulturePosition = (1280,1000)
crows_placed = [-1,-1,-1,-1,-1,-1,-1]
vulture_placed = -1
placement = {
    1 : "empty",
    2 : "empty",
    3 : "empty",
    4 : "empty",
    5 : "empty",
    6 : "empty",
    7 : "empty",
    8 : "empty",
    9 : "empty",
    10 : "empty"        
}
intersections = {
    1 : (702, 292),
    2 : (258, 599),
    3 : (431, 1091),
    4 : (974, 1091),
    5 : (1146, 599),
    6 : (811, 597),
    7 : (594, 597),
    8 : (528, 789),
    9 : (703, 911),
    10 : (877, 790)
}
firstNeighbors = {
    1 : [7, 6],
    2 : [8, 7],
    3 : [9, 8],
    4 : [10, 9],
    5 : [6, 10],
    6 : [1, 7, 10, 5],
    7 : [1, 2, 8, 6],
    8 : [7, 2, 3, 9],
    9 : [8, 3, 4, 10],
    10 : [6, 9, 4, 5]
}
attackPossibilities = {
    (1, 6) : 10,
    (1, 7) : 8,
    (2, 7) : 6,
    (2, 8) : 9,
    (3, 8) : 7,
    (3, 9) : 10,
    (4, 9) : 8,
    (4, 10) : 6,
    (5, 10) : 9,
    (5, 6) : 7,
    (6, 7) : 2,
    (6, 10) : 4,
    (7, 8) : 3,
    (7, 6) : 5,
    (8, 9) : 4,
    (8, 7) : 1,
    (9, 10) : 5,
    (9, 8) : 2,
    (10, 9) : 3,
    (10, 6) : 1
} 
    
def alert (sentence,color,position,size,duration):
    alertFont = pygame.font.Font(None, 75)
    alert_text = alertFont.render(sentence, True, color)
    screen.blit(alert_text, position)
    pygame.display.flip() 
    pygame.time.delay(duration * 1000) 


def Text (sentence,color,position,size):
    font = pygame.font.Font(None, size)
    text_surface = font.render(sentence, True, color)
    screen.blit(text_surface, position)
    
drag = False
selected_crow = None
offset_x = 0
offset_y = 0
placedToken = False
turn = "crow"
show_welcome = True
exit_game = False
count = 0
count_for_vulture = 0
attack_can_be_done = False
crows_killed = 0
attack_done = False


while exit_game != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            show_welcome = False
            if turn == "crow":
                if count < 7:
                    for i, crow in enumerate(crowTokens):
                        crow_x, crow_y = crow
                        mouse_x, mouse_y = event.pos
                        if abs(crow_x - mouse_x) < 32 and abs(crow_y - mouse_y) < 32:
                            selected_crow = i
                            drag = True
                            offset_x = crow_x - mouse_x
                            offset_y = crow_y - mouse_y
                            break
                else:
                    for i, crow in enumerate(crowTokens):
                        crow_x, crow_y = crow
                        mouse_x, mouse_y = event.pos
                        if abs(crow_x - mouse_x) < 32 and abs(crow_y - mouse_y) < 32:
                            selected_crow = i
                            drag = True
                            offset_x = crow_x - mouse_x
                            offset_y = crow_y - mouse_y
                            for key,value in intersections.items():
                                if value[0] == crow_x and value[1] == crow_y:
                                    placement[key] = "empty"
                                    break
            elif turn == "vulture":
                mouse_x, mouse_y = event.pos
                if abs(vultureToken[0] - mouse_x) < 32 and abs(vultureToken[1] - mouse_y) < 32:
                    drag = True
                    offset_x = vultureToken[0] - mouse_x
                    offset_y = vultureToken[1] - mouse_y
                    if count_for_vulture >= 1:
                        for key,value in intersections.items():
                            if value[0] == vultureToken[0] and value[1] == vultureToken[1]:
                                placement[key] = "empty"
                                break
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_crow == None:
                break
            if turn == "crow":
                if count < 7:
                    if crows_placed[selected_crow] == -1:
                        for key,value in intersections.items():
                            if abs(crowTokens[selected_crow][0] - value[0]) < 40 and abs(crowTokens[selected_crow][1] - value[1]) < 40 and placement[key] == "empty":
                                crowTokens[selected_crow] = value   
                                placement[key] = "crow"
                                placedToken = True
                                count = count + 1
                                crows_placed[selected_crow] = key
                                turn = "vulture"    
                                previousCrowPositions[selected_crow] = crowTokens[selected_crow]
                        if placedToken == False:
                            crowTokens[selected_crow] = previousCrowPositions[selected_crow]
                            alert("Kindly Place the Token on the Allowed Circles!",BLACK,(137,1250),75,3)
                    else:
                        crowTokens[selected_crow] = previousCrowPositions[selected_crow]
                        alert("All the crows are not placed yet!",BLACK,(320,1250),75,2)
                    drag = False
                    placedToken = False
                else:
                    for neighbor in firstNeighbors[crows_placed[selected_crow]]:
                        for key,value in intersections.items():
                            if abs(crowTokens[selected_crow][0] - value[0]) < 40 and abs(crowTokens[selected_crow][1] - value[1]) < 40 and placement[key] == "empty":
                                if(neighbor == key):
                                    crowTokens[selected_crow] = value   
                                    placement[key] = "crow"
                                    placedToken = True
                                    count = count + 1
                                    crows_placed[selected_crow] = key
                                    turn = "vulture"    
                                    previousCrowPositions[selected_crow] = crowTokens[selected_crow]
                                    break
                        if placedToken == True:
                            break
                    if placedToken == False:
                        crowTokens[selected_crow] = previousCrowPositions[selected_crow]
                        alert('Invalid Move!',BLACK,(550,1250),75,2)
                                     
                    for i,j in attackPossibilities.items():
                        if i[0] == vulture_placed and placement[j] == "empty":
                            if placement[i[1]] == "crow":
                                attack_can_be_done = True
                                break             
                    if attack_can_be_done == False:
                        won = 1
                        for neighbor in firstNeighbors[vulture_placed]:
                            if placement[neighbor] == "empty":
                                won = 0
                                break
                        if won == 1:
                            alert("Crow WON!",BLACK,(550,1250),150,3)
                            exit_game = 1
                            time.sleep(2)
                            break
                    attack_can_be_done = False
                    drag = False
                    placedToken = False
            elif turn == "vulture":
                if count_for_vulture < 1:
                    for key,value in intersections.items():
                        if abs(vultureToken[0] - value[0]) < 40 and abs(vultureToken[1] - value[1]) < 40 and placement[key] == "empty":
                            vultureToken = value   
                            placement[key] = "vulture"
                            placedToken = True
                            count_for_vulture = count_for_vulture + 1
                            turn = "crow"
                            vulture_placed = key
                            previousVulturePosition = vultureToken
                    if placedToken == False:
                        vultureToken = previousVulturePosition
                        alert('Kindly Place the Token on the Allowed Circles!',BLACK,(137,1250),75,3)
                    drag = False
                    placedToken = False
                else:
                    for i,j in attackPossibilities.items():
                        if i[0] == vulture_placed and placement[j] == "empty":
                            if placement[i[1]] == "crow":
                                attack_can_be_done = True
                                break             
                    if attack_can_be_done == True:
                        for i,j in attackPossibilities.items():
                            if i[0] == vulture_placed and placement[j] == "empty" and placement[i[1]] == "crow":
                                if  abs(vultureToken[0] - intersections[j][0]) < 40 and abs(vultureToken[1] - intersections[j][1]) < 40:   
                                    k = 0
                                    for k in range(0,7):
                                        if crows_placed[k] == i[1]:
                                            break
                                    crowTokens[k] = (2000,2000)
                                    previousCrowPositions[k] = (2000,2000)
                                    crows_placed[k] = -2                                
                                    placement[i[1]] = "empty"  
                                    vultureToken = intersections[j]
                                    placement[j] = "vulture"
                                    count_for_vulture = count_for_vulture + 1
                                    turn = "crow"
                                    vulture_placed = j
                                    previousVulturePosition = vultureToken    
                                    attack_can_be_done = False 
                                    crows_killed = crows_killed + 1
                                    attack_done = True
                                    break
                        if attack_done == False and attack_can_be_done == True:
                            vultureToken = previousVulturePosition
                            alert('Vulture has to KILL the Crow!',BLACK,(340,1250),75,2)     
                        if crows_killed == 4:
                            alert("Vulture WON!",BLACK,(545,1250),150,3)
                            exit_game = 1
                            time.sleep(2)
                            break
                        attack_done = False
                    else:
                        for neighbor in firstNeighbors[vulture_placed]:
                            for key,value in intersections.items():
                                if abs(vultureToken[0] - value[0]) < 40 and abs(vultureToken[1] - value[1]) < 40 and placement[key] == "empty":
                                    if(neighbor == key):
                                        vultureToken = value   
                                        placement[key] = "vulture"
                                        placedToken = True
                                        vulture_placed = key
                                        turn = "crow"    
                                        previousVulturePosition = vultureToken
                                        break
                            if placedToken == True:
                                break
                        if placedToken == False:
                            vultureToken = previousVulturePosition
                            alert('Invalid Move!',BLACK,(550,1250),75,2)
                    drag = False
                    placedToken = False
        elif event.type == pygame.MOUSEMOTION:
            if drag:
                if turn == "crow":
                    crowTokens[selected_crow] = (event.pos[0] + offset_x, event.pos[1] + offset_y)
                elif turn == "vulture":
                    vultureToken = (event.pos[0] + offset_x, event.pos[1] + offset_y)

    screen.fill((255, 255, 255))
    screen.blit(image, (margin, margin))

    Text('Crows',BLACK,(40,1100),65)
    Text('Vulture',BLACK,(1200,1100),65)
    Text("Crows Killed: " + str(crows_killed),BLACK,(1020,300),65)
    for crow in crowTokens:
        pygame.draw.circle(screen, BLUE, crow, 32)  
    if turn == "crow":
        Text("Crow's turn", BLACK, (550,100), 75)
    else:
        Text("Vulture's turn", BLACK, (540,100), 75)
    pygame.draw.circle(screen, PINK, vultureToken, 32)
    if show_welcome:
        Text("Welcome! It's Crow's turn to begin with", BLACK, (220,1250), 75)
        
    pygame.display.update()

pygame.quit()
