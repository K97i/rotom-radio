from hitplayrun import rank as hprRank
from radioimaging import convert as riConvert

exitFlag = False

while not exitFlag:
    validFlag = False

    print("=== [ rotom-radio ] ===")
    print("by K97i")
    print("[1] Hit Play Run - Get final 40 songs for ranking")
    print("[2] Radio Imaging - Convert to final output format")
    print("[3] Exit")

    while not validFlag:
        choice = None

        try:
            choice = int(input())
        except:
            print("Invalid input.")
            continue

        match choice:
            case 1:
                validFlag = True
                hprRank()

            case 2:
                validFlag = True
                riConvert()

            case 3:
                validFlag = True
                exitFlag = True

            case _:
                print("Invalid input.")

        print("")

    