#synarthsh gia na fortoso ta arxeia mou sthn mnhmh gia epeksergasia (ta grid.dir kai grid.grd )
def loadGrids(dirFile, grdFile):
    # fortono to arheio grid.grd gia na paro ta dedomena kai na ksanaftiakso tin tripleta opos sto meros 1o gia na kano ta window queries epeita.
    gridCells = {}
    with open(grdFile, 'r') as file:
        for line in file:
            # pernao kathe grammi tou arheiou sto parts gia na kano extract tis sintetagmenes kai epeita posa antikeimena yparhoun.
            parts = line.strip().split()
            
            cellCoords = tuple(map(int, parts[:2])) # cellCoords krataei sintetagmenes p.x 0,6 ktlp.
            
            numOfObjects = int(parts[2]) # kratao ola ta linestrings.
            
            objects = []
            for _ in range(numOfObjects):
                # edo kratame to roadID kai ta MBR me vash ta numOfObjects pou fortosame prin.
                parts = next(file).strip().split()
                roadID = int(parts[0]) # p.x to 35664,35665,35666 kai 35667
                roadMBR = tuple(map(float, parts[1:5])) # kratame ta MBR
                # kai edo kratame ta simeia ta linestring data
                roadPoints = []
                for i in range(5, len(parts), 2): #treho for loop kai kratao ana 2 tis syntetagmenes gia ta roads. 
                    #ftiahno ena tuple pou tha ehei ta epomena 2 parts (part(i) kai part (i+1) san floats kai ta pernao sta roadPoints
                
                    point = (float(parts[i]), float(parts[i+1]))
                    roadPoints.append(point)
                
                objects.append((roadID, roadMBR, roadPoints)) # opote to object ehei tin tripleta mas ksanaftiagmeni gia epeksergasia.
            
            gridCells[cellCoords] = objects # kai ta vazoume sto gridCells me vasi to keli.
            #epeita apo ayto to stadio ehoume ksana ftiagmena oti ftiaksame sto proto meros ksana sthn mnhmh mas gia na kanoume ta queries.

    # edo fortono to .dir arheio
    with open(dirFile, 'r') as file:
        # sthn proti grammi diavazo to global min,max gia X,Y
        minX, maxX, minY, maxY = map(float, next(file).strip().split())
        # ftiahnoume to dictionary mas me vasi to arheio.
        gridData = {
            'min_x': minX,
            'max_x': maxX,
            'min_y': minY,
            'max_y': maxY,
            'cellsX': 10,
            'cellsY': 10
        }

    return gridData, gridCells

#gridData, gridCells = load_grid('grid.dir', 'grid.grd')



# synarthsh opou ektelo ta window selection queries me vasi to arheio queries.txt
#pernao san orizmata to gridData kai to Gridcells pou fortosame prohgoumenos sthn mnhmh + tis syntetagmenes apo to arxeio queries.txt
def windowSelectionQuery(gridData, gridCells, winCoords):
    # pernoume ta winCoords apo to arheio queries.txt
    qMinX, qMaxX, qMinY, qMaxY = winCoords

    # vriskoume poia kelia kanoun intersect me to parathiro.
    cell_width = (gridData['max_x'] - gridData['min_x']) / gridData['cellsX'] #cell width kai height opou meta tha prostethoun sta cell_mix_x me vash thn eikona sthn ekfonisi
    cell_height = (gridData['max_y'] - gridData['min_y']) / gridData['cellsY']
    cells = [] #sto cells tha kratisoume poia kelia kanoun interscet me ena for loop kai na ta printaroume argotera sto apotelesma mas.
    for x in range(gridData['cellsX']):
        for y in range(gridData['cellsY']):
            cellMinX =gridData['min_x'] + x * cell_width
            cellMinY =gridData['min_y'] + y * cell_height
            cellMaxX =cellMinX + cell_width
            cellMaxY =cellMinY + cell_height
            if max(cellMinX, qMinX) < min(cellMaxX, qMaxX) and max(cellMinY, qMinY) < min(cellMaxY, qMaxY):
                cells.append((x, y)) #an kanoun interesct tote kratame to sygkekrimeno cell sto cells gia na to kanoume print argotera .

    # tora tha psaksoume sta objects tou kathe  cell pou kratisame poia kanoun intersect. tha ta kratisoume sto results.
    results = []
    doubleRoads = set() # tsekaro gia diplotipies sto teliko apotelesma. se aytin tin lista tha elegho an eho diplotypia.
    for cellX, cellY in cells:
        if (cellX, cellY) in gridCells:
            for roadId, roadMbr, roadPoints in gridCells[(cellX, cellY)]:
                # elegho an to MBR kanei intersect kai tote prostheto sta results afou tsekaro an ehei ksanaperastei.
                if max(roadMbr[0], qMinX) < min(roadMbr[2], qMaxX) and max(roadMbr[1], qMinY) < min(roadMbr[3], qMaxY):
                    if roadId not in doubleRoads:
                            results.append((roadId))
                            doubleRoads.add(roadId)

    return results, cells


# telos forono ta arheia grid.dir kai gid.grd me thn synarthsh load_grid kai kratao sta gridData kai gridCells.
gridData, gridCells = loadGrids('grid.dir', 'grid.grd')
with open('queries.txt', 'r') as file:
    for i, line in enumerate(file): # gia kathe queri (i) sto arheio treho to for loop kai printaro ta apotelesmata.
        # perno tis syntetagmenes apo to arxeio queries pou diahorizonte me komma
        query = line.strip().split(',')[1]
        # epeita spao tis syntetagmenes kai lista apo floats.
        queryC = list(map(float, query.split()))
        #  treho thn synarthsh gia na paro ta results kai cells .
        results, cells = windowSelectionQuery(gridData, gridCells, queryC)
        print(f'Query {i+1} results: ')
        print(' '.join(map(str, results)))
        print(f'Cells: {len(cells)}')
        print(f'Results: {len(results)}')
        print('----------')

