#anoigo to arxeio tiger_roads.csv kai sto fileData apothikeyo ksehorista kathe grammi 
with open('tiger_roads.csv', 'r') as file:
    fileData = file.read().splitlines()

# arithmos linestrings pou einai mesa sto arxeio.
numberOfLinestrings = int(fileData[0])
print(numberOfLinestrings)
# kano initialize gia min kai max values. vazontas infinity gia poly megales times.

minX = float('inf')
minY = float('inf')
maxX = float('-inf')
maxY = float('-inf')

# lista gia na kratao ta roads 
roadData = []

# treho se loop ta linestrings mesa sto arheio File
for i in range(1, numberOfLinestrings+1):
    # diahorizo me komma kai perno tis syntetagmenes.
    rCoords = fileData[i].split(',')
    #kano metatropi tis syntetagmenes mou se float kai ftiaxno mia lista me points.
    rPoints = []
    for point in rCoords:
        coords = []
        for coord in point.split():
            coords.append(float(coord))
        rPoints.append(coords)

    # ypologizo ta min max gia tis syntetagmenes sthn lista me ta rPoints.
    rMinX = min(point[0] for point in rPoints)
    rMinY = min(point[1] for point in rPoints)
    rMaxX = max(point[0] for point in rPoints)
    rMaxY = max(point[1] for point in rPoints)
    # ananeono tis global metavlites me ta nea min , max 
    minX = min(minX, rMinX)
    minY = min(minY, rMinY)
    maxX = max(maxX, rMaxX)
    maxY = max(maxY, rMaxY)
    # ftiaxno tin tripleta opos zhtaei h ekfonisi me i anagnoristiko , ta mbr , kai ta linestrings me tis syntetagmenes
    roadData.append([i, [[rMinX, rMinY], [rMaxX, rMaxY]], rPoints])

# ypologizo to megethos ton kelion gia to grid symfona me tin ekfonisi 
sizeX = (maxX - minX) / 10
sizeY = (maxY - minY) / 10

# ftiaxno dictionary gia na kratiso ta grid cells
gridCells = {}

#treho loop mesa sto roadData kai kano assign sta gridcells (to roadData pou eftiaksa pio pano me tin tripleta)
for roadId, roadMbr, roadPoints in roadData:

    for i in range(10):
        for j in range(10):
            # ypologizo to min kai max gia tis syntetagmenes gia to kathe keli.
            cellMinX = minX + i*sizeX
            cellMinY = minY + j*sizeY
            cellMaxX = cellMinX + sizeX
            cellMaxY = cellMinY + sizeY
            # tsekaro an to MBR tou road kanei interscet me to keli.
            if roadMbr[0][0] <= cellMaxX and roadMbr[1][0] >= cellMinX and roadMbr[0][1] <= cellMaxY and roadMbr[1][1] >= cellMinY:
                # an den einai mesa tote na perasei sto gridCells dictionary.
                if (i,j) not in gridCells:
                    gridCells[(i,j)] = []

                gridCells[(i,j)].append(roadId)

#synarthsh gia na ftiakso to grid.grd opou pernei san orismata tin tripleta roadData , ta gridCells dictionary , kai to onoma tou arheiou pou tha dhmiourghsei 
def makeGridGrd(roadData, gridCells, fileName):
    with open(fileName, 'w') as file: #anoigo to arheio me 'w' gia eggrafi
        # treho to loop se kathe cell kai ta kano taksinomisi kai ta pernao sto arheio mou grid.grd
        for i in range(10):
            for j in range(10):
                if (i,j) in gridCells:
                    # sortaro ta cells tis syntetagmenes.
                    cellsSorted = sorted(gridCells[(i,j)])
                    
                    cellCoords = f'{i} {j}'
                    numOfObjects = len(cellsSorted)
                    file.write(f'{cellCoords} {numOfObjects}\n')
                    # grafo sto arheio to MBR kai to linestring (apo ton sortarismeno pinaka aythn thn fora )
                    
                    for roadId in cellsSorted:
                        
                        roadInfo = roadData[roadId-1]
                        
                        roadMbr = roadInfo[1]
                        
                        roadPoints = roadInfo[2]
                        
                        file.write(f'{roadId} {roadMbr[0][0]} {roadMbr[0][1]} {roadMbr[1][0]} {roadMbr[1][1]} ')
                        file.write(' '.join([f'{coord[0]} {coord[1]}' for coord in roadPoints]))
                        file.write('\n')
                

#synarthsh gia thn dhmiourgia tou grid.dir arxeiou 
def makeGridDir(roadData, gridCells, fileName):
    with open(fileName, 'w') as file:
        # sthn proti grammi tou arheiou grafo to min kai to max gia tis syntetagmenes
        
        file.write(f'{minX} {maxX} {minY} {maxY}\n')

        # treho pali me loop ta cells (gridCells) kai pernao sto arxeio tis syntetagmenes tou kathe kelio p.x (0,6) (0,1) ktlp
        #kai epeita posa objects yparhoun mesa se kathe keli.
        for i in range(10):
            for j in range(10):
                cellCoords = f'{i} {j}'
                if (i,j) in gridCells:
                    numOfObjects = len(gridCells[(i,j)])
                else:
                    numOfObjects = 0
                file.write(f'{cellCoords} {numOfObjects}\n')


# kalo tis synarthseis gia na dhmiourghso ta arxeia mou.
makeGridGrd(roadData, gridCells, 'grid.grd')
makeGridDir(roadData, gridCells, 'grid.dir')




