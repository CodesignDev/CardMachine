'''
Master Game Gen 
1.0b
'''
import os, glob
import PIL_Helper
from OS_Helper import *

#TSSSF Migration TODO:
#automagickally create vassal module :D
#individual artist naming
#.pon files have symbols like {ALICORN} and so on.

def main(folder=".", filepath="deck.cards"):

    CardFile = open(os.path.join(folder, filepath))
    card_set = os.path.dirname(filepath)

    # Read first line of file to determine module
    first_line = CardFile.readline()
    try:
        module=(__import__(first_line.strip()))
    except ValueError:
        print "Failed to load module: " + str(ValueError)
        return
    module.CardSet = card_set

    # Create workspace for card images
    workspace_path = CleanDirectory(path=folder, mkdir="workspace", rmstring="*.*")

    # Create image directories
    bleed_path = CleanDirectory(path=folder+"/"+card_set, mkdir="bleed-images",rmstring="*.*")
    module.BleedsPath = bleed_path
    cropped_path = CleanDirectory(path=folder+"/"+card_set, mkdir="cropped-images",rmstring="*.*")
    module.CropPath = cropped_path
    vassal_path = CleanDirectory(path=folder+"/"+card_set, mkdir="vassal-images",rmstring="*.*")
    module.VassalPath = vassal_path

    # Create output directory
    output_folder = CleanDirectory(path=folder, mkdir=card_set,rmstring="*.pdf")

    # Load Card File and strip out comments
    cardlines = [line for line in CardFile if not line[0] in ('#', ';', '/')]
    CardFile.close()

    # Make a list of lists of cards, each one page in scale
    cardpages=[]
    cardlines+=["BLANK" for i in range(1,module.TOTAL_CARDS)]
    cardlines.reverse()
    while len(cardlines)>module.TOTAL_CARDS:
        cardpages.append([cardlines.pop() for i in range(0,module.TOTAL_CARDS)])

    # Make pages
    card_list=[]
    back_list=[]
    for i,page in enumerate(cardpages):
        for line in page:
            card_list.append(module.BuildCard(line))
            back_list.append(module.BuildBack(line))
        BuildPage(card_list,i,module.PAGE_WIDTH,module.PAGE_HEIGHT,workspace_path)
        BuildBack(back_list,i,module.PAGE_WIDTH,module.PAGE_HEIGHT,workspace_path)
        card_list=[]
        back_list=[]

    #Build Vassal
    module.CompileVassalModule()

    print "\nCreating PDF..."
    os.system(r'convert "{}/page_*.png" "{}/{}.pdf"'.format(workspace_path, output_folder, card_set))
    print "\nCreating PDF of backs..."
    os.system(r'convert "{}/backs_*.png" "{}/backs_{}.pdf"'.format(workspace_path, output_folder, card_set))
    print "Done!"

if __name__ == '__main__':
    #main('TSSSF', 'Ponyville University 0.0.2/cards.pon')
    #main('TSSSF', 'Ponyville University 1.0.1/cards.pon')
    main('TSSSF', 'Core 1.0.5/cards.pon')
    #main('TSSSF', '2014 Con Exclusives/cards.pon')
    #main('TSSSF', 'Extra Credit 0.10.4/cards.pon')
    #main('BaBOC', 'BaBOC_0.0.1/deck.cards')
