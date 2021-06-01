import pygame, sys, random

#Funções

def drawFloor():
    screen.blit(floorSurface, (floorXPosition,900))
    screen.blit(floorSurface, (floorXPosition + 576, 900))

def createPipe():
    randomPipePosition = random.choice(pipeHeight)
    bottomPipe = pipeSurface.get_rect(midtop = (700, randomPipePosition))
    topPipe = pipeSurface.get_rect(midbottom = (700, randomPipePosition - 300))
    return bottomPipe, topPipe

#Movimenta os canos na tela
def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5

    visiblePipes = [pipe for pipe in pipes if pipe.right > -50]
    
    return visiblePipes

def drawPipes(pipes):
    for pipe in pipes:
        #   Verifica se a parte de baixo do cano passa de 1024, se passar ele só poderá ser o bottomPipe
        #   então colocamos ele na tela normalmente
        if pipe.bottom >= 1024:
            screen.blit(pipeSurface, pipe)
        else:
            #   Caso não seja o bottomPipe será o topPipe, e precisamos rotacionar ele para que ele apareça
            #   normalmente.
            #   A função pygame.transform.flip() faz exatamente isso, nos passamos 3 parâmetros que são 
            #   respectivamente o objeto que queremos dar o flip, se queremos dar o flip no eixo X 
            #   e se queremos dar o flip no eixo Y
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flipPipe, pipe)

#   Verificando colisões com os canos, o teto e o chão
def checkCollision(pipes):
    for pipe in pipes:
        if characterRectangle.colliderect(pipe):
            canScore = True
            deathSound.play()
            return False
        
    if characterRectangle.top <= -100 or characterRectangle.bottom >= 900:
        canScore = True
        deathSound.play()
        return False

    return True

def rotateCharacter(character):
    newCharacter = pygame.transform.rotozoom(character, -characterMovement * 3, 1)
    return newCharacter

def characterAnimation(characterFrames, characterIndex, characterRectangle):
    newCharacter = characterFrames[characterIndex]
    newCharacterRectangle = newCharacter.get_rect(center = (100, characterRectangle.centery))
    return newCharacter, newCharacterRectangle

def scoreDisplay(gameState):
    if gameState == 'mainGame':
        scoreSurface = gameFont.render(str(int(score)), True, (255, 255, 255))
        scoreRectangle = scoreSurface.get_rect(center = (288, 100))
        screen.blit(scoreSurface, scoreRectangle)
    elif gameState == 'gameOver':
        scoreSurface = gameFont.render(f'Score:    {int(score)}', True, (255, 255, 255))
        scoreRectangle = scoreSurface.get_rect(center = (300, 460))
        screen.blit(scoreSurface, scoreRectangle)

        highScoreSurface = gameFont.render(f'High Score:    {int(highScore)}', True, (255, 255, 255))
        highScoreRectangle = highScoreSurface.get_rect(center = (300, 560))
        screen.blit(highScoreSurface, highScoreRectangle)

def updateScore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

def pipeScoreCheck():
    global score,canScore 
    if pipeList:
        for pipe in pipeList:
            if 95 < pipe.centerx < 105 and canScore:
                score += 1
                scoreSound.play()
                canScore = False
            if pipe.centerx < 0:
                canScore = True
        if checkCollision(pipeList) == False:
            canScore = True

pygame.mixer.pre_init()
#Inicio do jogo
pygame.init()

#   Configura um tamanho para tela semelhante ao size(576, 1024) do processing.
screen = pygame.display.set_mode((576, 1024))
#   Para controlar o Framerate/Fps do jogo chamamos pygame.time.Clock() e posteriormente clock.tick(120)
#   É importante controlar o framerate para não atualizar mais que o necessário 
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19.ttf',40)

#Variáveis do jogo
gravity = 0.25
characterMovement = 0
gameActive = True
gameOverActive = False
highScore = 0
score = 0
canScore = True
customizingCharacter = False
customizeCharacterX = 288
customizeCharacterIndex = 0
character1 = True
character2 = False
character3 = False 

#   Carregamento de imagem
#   Parece que o .convert otimiza o processamento do pygame, mas não muda nada visualmente.
bgSurface = pygame.image.load('./public/sprites/background-day.png').convert()
#   Esta função basicamente duplica o tamanho da imagem e para salva-la colocamos ela em uma variavel.
bgSurface = pygame.transform.scale2x(bgSurface)

floorSurface = pygame.image.load('./public/sprites/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXPosition = 0

#   Carregamos os frames das animações do personagem, e colocamos em um array para chamar 
#   a imagem na hora certa. 
characterDownFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-downflap.png')).convert_alpha()
characterMidFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-midflap.png')).convert_alpha()
characterUpFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-upflap.png')).convert_alpha()
characterFrames = [characterDownFlap, characterMidFlap, characterUpFlap]
characterIndex = 0
characterSprite = characterFrames[characterIndex]
#   characterSprite.get_rect() faz com que a gente coloque um retângulo em volta do nosso personagem
#   facilitando a verificação de colisões
characterRectangle = characterSprite.get_rect(center = (100, 512))

CHARACTERANIMATION = pygame.USEREVENT + 1
pygame.time.set_timer(CHARACTERANIMATION, 200)

characterShowBirdAnimation01 = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-downflap.png')).convert_alpha()
characterShowBirdAnimation02 = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-midflap.png')).convert_alpha()
characterShowBirdAnimation03 = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-upflap.png')).convert_alpha()
characterShowBirdFrames = [characterShowBirdAnimation01, characterShowBirdAnimation02, characterShowBirdAnimation03]
characterShowBirdIndex = 0
characterShowBirdSprite = characterShowBirdFrames[characterShowBirdIndex]

showBirdRectangle = characterShowBirdSprite.get_rect(center = (288, 512))

characterShowRedBirdAnimation01 = pygame.transform.scale2x(pygame.image.load('./public/sprites/redbird-downflap.png')).convert_alpha()
characterShowRedBirdAnimation02 = pygame.transform.scale2x(pygame.image.load('./public/sprites/redbird-midflap.png')).convert_alpha()
characterShowRedBirdAnimation03 = pygame.transform.scale2x(pygame.image.load('./public/sprites/redbird-upflap.png')).convert_alpha()
characterShowRedBirdFrames = [characterShowRedBirdAnimation01, characterShowRedBirdAnimation02, characterShowRedBirdAnimation03]
characterShowRedBirdIndex = 0
characterShowRedBirdSprite = characterShowRedBirdFrames[characterShowRedBirdIndex]

showRedBirdRectangle = characterShowRedBirdSprite.get_rect(center = (288, 512))

characterShowYellowBirdAnimation01 = pygame.transform.scale2x(pygame.image.load('./public/sprites/yellowbird-downflap.png')).convert_alpha()
characterShowYellowBirdAnimation02 = pygame.transform.scale2x(pygame.image.load('./public/sprites/yellowbird-midflap.png')).convert_alpha()
characterShowYellowBirdAnimation03 = pygame.transform.scale2x(pygame.image.load('./public/sprites/yellowbird-upflap.png')).convert_alpha()
characterShowYellowBirdFrames = [characterShowYellowBirdAnimation01, characterShowYellowBirdAnimation02, characterShowYellowBirdAnimation03]
characterShowYellowBirdIndex = 0
characterShowYellowBirdSprite = characterShowYellowBirdFrames[characterShowYellowBirdIndex]

showYellowBirdRectangle = characterShowYellowBirdSprite.get_rect(center = (288, 512))


""" characterSprite = pygame.image.load('./public/sprites/bluebird-midflap.png').convert_alpha()
characterSprite = pygame.transform.scale2x(characterSprite)
 """

pipeSurface = pygame.image.load('./public/sprites/pipe-green.png')
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipeList = []
SPAWNPIPE = pygame.USEREVENT
#Contador de tempo
pygame.time.set_timer(SPAWNPIPE, 1200)
pipeHeight = [400, 600, 800]

gameOverSurface = pygame.image.load('./public/sprites/message.png').convert_alpha()
gameOverSurface = pygame.transform.scale2x(gameOverSurface)
gameOverRectangle = gameOverSurface.get_rect(center = (288, 512))

customizeCharacter = pygame.image.load('./public/sprites/customizeCharacterButton.png').convert_alpha()
customizeCharacterRectangle = customizeCharacter.get_rect(center = (50, 900))

scoreShow = pygame.image.load('./public/sprites/scoreScreen.png').convert_alpha()
scoreShow = pygame.transform.scale2x(scoreShow)
scoreShowRectangle = scoreShow.get_rect(center = (288, 512))

flapSound = pygame.mixer.Sound('./public/audio/wing.wav')
deathSound = pygame.mixer.Sound('./public/audio/hit.wav')
scoreSound = pygame.mixer.Sound('./public/audio/point.wav')
scoreSoundCountdown = 100

#   Laço while para manter o jogo aberto, caso não tenha o while o jogo fecha rapidamente.
while True:
    #For verifica eventos do pygame
    for event in pygame.event.get():
        #   If para possibiltiar o fechamento do jogo.
        #   Caso não tenha o if você não consegue fechar a janela do pygame.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #   Depois que o contador chega ao final ele executa a ação dentro do if.
        if event.type == SPAWNPIPE:
            #   Acrescenta ao pipeList mais um cano, depois de 1,2 segundos(1200 ms)
            pipeList.extend(createPipe())
            
        #   Verifica se uma tecla qualquer foi pressionada 
        if event.type == pygame.KEYDOWN:
            #   Verifica se uma tecla específica foi pressionada, no caso a
            #   a tecla espaço
            if event.key == pygame.K_SPACE and gameActive:
                #   Mecânica de pulo do personagem
                characterMovement = 0
                characterMovement -= 11
                flapSound.play()

            if event.key == pygame.K_SPACE and gameActive == False and gameOverActive == True and customizingCharacter == False:
                gameActive = True
                gameOverActive = True
                pipeList.clear()
                characterRectangle.center = (100, 512)
                characterMovement = 0
                score = 0

                if character1:
                    characterDownFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-downflap.png')).convert_alpha()
                    characterMidFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-midflap.png')).convert_alpha()
                    characterUpFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/bluebird-upflap.png')).convert_alpha()
                    
                    characterFrames.clear()
                    characterFrames = [characterDownFlap, characterMidFlap, characterUpFlap]
                    characterSprite = characterFrames[characterIndex]
                    #   characterSprite.get_rect() faz com que a gente coloque um retângulo em volta do nosso personagem
                    #   facilitando a verificação de colisões
                    characterRectangle = characterSprite.get_rect(center = (100, 512))

                elif character2:
                    characterDownFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/redbird-downflap.png')).convert_alpha()
                    characterMidFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/redbird-midflap.png')).convert_alpha()
                    characterUpFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/redbird-upflap.png')).convert_alpha()
                    characterFrames.clear()
                    characterFrames = [characterDownFlap, characterMidFlap, characterUpFlap]
                    characterSprite = characterFrames[characterIndex]
                    #   characterSprite.get_rect() faz com que a gente coloque um retângulo em volta do nosso personagem
                    #   facilitando a verificação de colisões
                    characterRectangle = characterSprite.get_rect(center = (100, 512)) 
                    
                elif character3:
                    characterDownFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/yellowbird-downflap.png')).convert_alpha()
                    characterMidFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/yellowbird-midflap.png')).convert_alpha()
                    characterUpFlap = pygame.transform.scale2x(pygame.image.load('./public/sprites/yellowbird-upflap.png')).convert_alpha()
                    characterFrames.clear()
                    characterFrames = [characterDownFlap, characterMidFlap, characterUpFlap]
                    characterSprite = characterFrames[characterIndex]
                    #   characterSprite.get_rect() faz com que a gente coloque um retângulo em volta do nosso personagem
                    #   facilitando a verificação de colisões
                    characterRectangle = characterSprite.get_rect(center = (100, 512)) 

            if event.key == pygame.K_SPACE and gameOverActive == False:
                gameOverActive = True

            if event.key == pygame.K_z and gameActive == False and gameOverActive == True:
                customizingCharacter = True
            
            if event.key == pygame.K_SPACE and gameActive == False and gameOverActive == True and customizingCharacter == True:
                customizingCharacter = False

            if event.key == pygame.K_RIGHT and gameActive == False and gameOverActive == True and customizingCharacter == True:
                if customizeCharacterIndex < 2:
                    customizeCharacterIndex += 1
                else: 
                    customizeCharacterIndex = 0

            if event.key == pygame.K_LEFT and gameActive == False and gameOverActive == True and customizingCharacter == True:
                if customizeCharacterIndex > 0:
                    customizeCharacterIndex -= 1
                else: 
                    customizeCharacterIndex = 2
                

        if event.type == CHARACTERANIMATION:
            if characterIndex < 2:
                characterIndex += 1
                characterShowBirdIndex += 1
                characterShowRedBirdIndex += 1
                characterShowYellowBirdIndex += 1
            else:
                characterIndex = 0
                characterShowBirdIndex = 0
                characterShowRedBirdIndex = 0
                characterShowYellowBirdIndex = 0

            characterSprite, characterRectangle = characterAnimation(characterFrames, characterIndex, characterRectangle)
            characterShowBirdSprite, showBirdRectangle = characterAnimation(characterShowBirdFrames, characterShowBirdIndex, showBirdRectangle)
            characterShowRedBirdSprite, showRedBirdRectangle = characterAnimation(characterShowRedBirdFrames, characterShowRedBirdIndex, showRedBirdRectangle)
            characterShowYellowBirdSprite, showYellowBirdRectangle = characterAnimation(characterShowYellowBirdFrames, characterShowYellowBirdIndex, showYellowBirdRectangle)
       

    #   Pelo que parece o .blit coloca um objeto em cima de outro.
    #   Os argumentos passados para o .blit são primeiramente o objeto/imagem que você quer que 
    #   ele coloque e posteriormente a posição (x, y) que ele será renderizado na tela.
    screen.blit(bgSurface, (0,0))
 
    if gameActive:
        #   Aqui acrescentamos a "gravidade" para a variavel characterMovement, e em seguida
        #   acrescentamos o valor de characterMovement para o eixo Y do retângulo que envolve
        #   o personagem.

        

        characterMovement += gravity
        rotatedCharacter = rotateCharacter(characterSprite)
        characterRectangle.centery += characterMovement
        screen.blit(rotatedCharacter, characterRectangle)
        
        gameActive = checkCollision(pipeList)
        gameOverActive = checkCollision(pipeList)

        pipeList = movePipes(pipeList)
        drawPipes(pipeList)

        pipeScoreCheck()
        scoreDisplay('mainGame')
    else:
        if gameOverActive == False:
            screen.blit(scoreShow, scoreShowRectangle)
            highScore = updateScore(score, highScore)
            scoreDisplay('gameOver')
        elif customizingCharacter == True:

            if customizeCharacterIndex == 0:
                showBirdRectangle = characterShowBirdSprite.get_rect(center = (customizeCharacterX, 512))
                screen.blit(characterShowBirdSprite, showBirdRectangle)

                character1 = True
                character2 = False
                character3 = False
            elif customizeCharacterIndex == 1:
                showRedBirdRectangle = characterShowRedBirdSprite.get_rect(center = (customizeCharacterX, 512))
                screen.blit(characterShowRedBirdSprite, showRedBirdRectangle)

                character1 = False
                character2 = True 
                character3 = False
            elif customizeCharacterIndex == 2:
                showYellowBirdRectangle = characterShowYellowBirdSprite.get_rect(center = (customizeCharacterX, 512))
                screen.blit(characterShowYellowBirdSprite, showYellowBirdRectangle)

                character1 = False
                character2 = False
                character3 = True
            




        else:
            screen.blit(gameOverSurface, gameOverRectangle)

            highScore = updateScore(score, highScore)


    #   Incrementamos a variavel floorXPosition para dar um efeito de movimento no chão.
    floorXPosition -= 1
    #   Uma função que renderiza o chão duas vezes para um efeito de continuidade.
    drawFloor()

    if gameActive == False and gameOverActive == True and customizingCharacter == False:
        screen.blit(customizeCharacter, customizeCharacterRectangle)
    
    #   Uma condição para que o chão se mantenha contínuo, como o width da tela é 576 quando 
    #   floorXPosition chegar a um valor igual a -576 o primeiro chão renderizado vai chegar ao fim, então
    #   igualamos o floorXPosition para 0, assim o chão volta e da um efeito de que o chão é infinito.
    if floorXPosition <= -576:
        floorXPosition = 0
    

    pygame.display.update()
    #Aqui configuramos o máximo de fps, nesse caso 120.
    clock.tick(120)