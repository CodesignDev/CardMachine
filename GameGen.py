'''
Master Game Gen
1.1
'''
import os, glob
import PIL_Helper
import argparse
from OS_Helper import Delete, CleanDirectory, BuildPage, BuildBack
from PIL import Image
from sys import exit
import json


def main(folder="TSSSF", filepath="Core Deck 1.1.6/cards.json", watermark="", generate_pdf=True):
    '''
    @param folder: The base game folder where we'll be working.
        E.g. TSSSF, BaBOC
    @param filepath: The filepath (relative to the base folder) where the
        file that defines the different cards in the game are stored.
    '''

    CardFile = open(os.path.join(folder, filepath))

    # Read first line of file to determine format and/or module
    first_line = CardFile.readline()
    seond_line = ''
    third_line = ''
    if first_line == "{\n":
        file_type = 'json'
        # Load Card File
        CardFile.seek(0)
        data = json.load(CardFile)
        CardFile.close()
        module_name = data['deck']['module']
        cards = data['cards']
    else:
        file_type = 'pon'
        if first_line == "TSSSF_CardGen":
            print 'Warning: .pon files are DEPRECATED for TSSSF. Support for this format may be removed soon. Please use the pontojson.py converter to convert this file to JSON format.'
        module_name = first_line
        pos = CardFile.tell()
        # Attempt to read extra metadata
        metadata = CardFile.readline()
        CardFile.seek(pos)
        # Load Card File and strip out comments
        cards = [line for line in CardFile if not line[0] in ('#', ';', '/')]
        CardFile.close()

    try:
        module = __import__(module_name.strip())
    except ValueError:
        print "Failed to load module: " + str(ValueError)
        return
    card_set = os.path.dirname(filepath)
    if file_type == 'json':
        if data['deck'].get('version', '') != '':
            card_set_text = '{} {}'.format(data['deck']['name'], data['deck']['version'])
        else:
            card_set_text = data['deck']['name']
        module.CardSet = card_set_text
        module.DEFAULT_ARTIST = data['deck'].get('defaultArtist', module.DEFAULT_ARTIST)
        if 'symbol' in data['deck']:
            module.GlobalExpansionIcon = data['deck']['symbol']

    else:

        if metadata[0] == '#':
            metadata_dict = metadata[1:].strip('\n').strip('\r').replace(r'\n', '\n').split('`')
            card_set_name = metadata_dict[0]
            card_set_version = metadata_dict[1] or ''
            default_artist_name = metadata_dict[2] or module.DEFAULT_ARTIST
            expansion_symbol = metadata_dict[3] or None
            if card_set_version != '':
                card_set_text = '{} {}'.format(card_set_name, card_set_version)
            else:
                card_set_text = card_set_name
            module.CardSet = card_set_text
            module.DEFAULT_ARTIST = default_artist_name
            if expansion_symbol is not None:
                module.GlobalExpansionIcon = expansion_symbol
        else:
            module.CardSet = os.path.dirname(filepath)

    module.card_set = module.CardSet

    module.CardPath = os.path.join(folder, card_set, "art")
    module.OverlayPath = os.path.join(folder, card_set, "overlay")
    module.ExpansionIconsPath = os.path.join(folder, card_set, "expansion-icon")

    if watermark != "":
        module.WatermarkImage = os.path.join(folder, "watermarks", watermark)

    # Create workspace for card images
    workspace_path = CleanDirectory(path=folder, mkdir="workspace", rmstring="*.*")

    # Create image directories
    bleed_path = CleanDirectory(path=folder + "/" + card_set, mkdir="bleed-images", rmstring="*.*")
    module.BleedsPath = bleed_path
    cropped_path = CleanDirectory(path=folder + "/" + card_set, mkdir="cropped-images", rmstring="*.*")
    module.CropPath = cropped_path
    vassal_path = CleanDirectory(path=folder + "/" + card_set, mkdir="vassal-images", rmstring="*.*")
    module.VassalPath = vassal_path

    # Create output directory
    output_folder = CleanDirectory(path=folder, mkdir=card_set, rmstring="*.pdf")

    # Make pages
    card_list = []
    back_list = []
    bleed_cards = []
    page_num = 0
    for line in cards:
        card = module.BuildCard(line)
        back = module.BuildBack(line)

        card_list.append(card['cropped'])
        back_list.append(back['cropped'])

        # card_list.append(module.BuildCard(line))
        # back_list.append(module.BuildBack(line))
        # card_list.append(card)
        # back_list.append(back)

        bleed_cards.append(back['bleed'])
        bleed_cards.append(card['bleed'])

        # If the card_list is big enough to make a page
        # do that now, and set the card list to empty again
        #
        if len(card_list) >= module.TOTAL_CARDS and generate_pdf:
            page_num += 1
            print "Building Page {}...".format(page_num)
            BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
            BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
            card_list = []
            back_list = []

    # If there are leftover cards, fill in the remaining
    # card slots with blanks and gen the last page
    if len(card_list) > 0 and generate_pdf:
        # Fill in the missing slots with blanks
        while len(card_list) < module.TOTAL_CARDS:
            card_list.append(module.BuildCard("BLANK")['cropped'])
            back_list.append(module.BuildCard("BLANK")['cropped'])
        page_num += 1
        print "Building Page {}...".format(page_num)
        # print card_list
        BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)
        BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, workspace_path)

    # w,h = bleed_cards[0].size
    # card_num = 0
    # for x in xrange(len(bleed_cards)):
    #     card_num += 1
    #     card_to_paste = Image.new("RGB", (w, h))
    #     card = bleed_cards.pop(0)
    #     card_to_paste.paste(card, (0, 0))
    #     card_to_paste.save(
    #         os.path.join(
    #             workspace_path,
    #             "card_{0:>03}.png".format(card_num)
    #         ), dpi=(300, 300))



    # Build Vassal
    # module.CompileVassalModule()

    # Generate PDF files if required
    if generate_pdf:
        print "\nCreating PDF..."
        # os.system(r'convert "{}/card_*.png" "{}/{} Cards.pdf"'.format(workspace_path, output_folder, card_set))
        os.system(r'convert "{}/page_*.png" "{}/{}.pdf"'.format(workspace_path, output_folder, card_set))
        #print "\nCreating PDF of backs..."
        os.system(r'convert "{}/backs_*.png" "{}/backs_{}.pdf"'.format(workspace_path, output_folder, card_set))
        print "Done!"


if __name__ == '__main__':
    # To run this script, you have two options:
    # 1) Run it from the command line with arguments. E.g.:
    #       python GameGen -b TSSSF -f "Core 1.0.3/cards.pon"
    # 2) Comment out "main(args.basedir, args.set_file)" in this file
    #       and add a new line with the proper folder and card set
    #       in the arguments.
    # See the main() docstring for more info on the use of the arguments
    parser = argparse.ArgumentParser(prog="GameGen")

    parser.add_argument('-f', '--set-file', \
                        help="Location of set file to be parsed",
                        default="cards.json")
    parser.add_argument('-b', '--basedir',
                        help="Workspace base directory with resources output directory",
                        default="TSSSF")
    parser.add_argument('-w', '--watermark', \
                        help="Specify the watermark to apply to all generated cards",
                        default="")
    parser.add_argument('--no-pdf',
                        help="Do not generate PDF files",
                        action="store_false")

    args = parser.parse_args()

    main(args.basedir, args.set_file, args.watermark, args.no_pdf)
