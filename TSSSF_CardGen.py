import os, glob, shutil, traceback, random
import PIL_Helper

TYPE, PICTURE, SYMBOLS, TITLE, KEYWORDS, BODY, FLAVOR, EXPANSION = range(8)
DIRECTORY = "TSSSF"
ARTIST = "Pixel Prism"


LegacySymbolMode = True
PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH*PAGE_HEIGHT


workspace_path = os.path.dirname("workspace")
card_set = os.path.dirname("deck.cards")
CardSet = os.path.dirname("deck.cards")
CardPath = DIRECTORY+"/Card Art/"
ResourcePath = DIRECTORY+"/resources/"
BleedsPath = DIRECTORY+"/bleed-images/"
CropPath = DIRECTORY+"/cropped-images/"
VassalPath = DIRECTORY+"/vassal-images/"

VassalTemplatesPath = DIRECTORY+"/vassal templates/"
VassalWorkspacePath = DIRECTORY+"/vassal workspace/"
VassalImagesPath = os.path.join(VassalWorkspacePath, "images")
vassalscale=(260,359)

VassalCard = [0]
ART_WIDTH = 600
base_w = 889
base_h = 1215
base_w_center = base_w/2
base_h_center = base_h/2
w_marg = 31
h_marg = 36
baserect=[(w_marg,h_marg),(base_w-w_marg,base_h-h_marg)]
textmaxwidth = 689
# SymbolX = 58
# PonySymbolYs = [56, 160, 535]
# GoalSymbolYs = [86, 550]

#croprect=[(50,63),(788,1088)]
croprect=(50,63,788+50,1088+63)

TextHeightThresholds = [363, 378, 600]
TitleWidthThresholds = [50] #This is in #characters, fix later plox
BarTextThreshold = [500]

fonts = {
    "Title":PIL_Helper.BuildFont(ResourcePath+"TSSSFBartholomew-Bold.otf", 55),
    "TitleSmall":PIL_Helper.BuildFont(ResourcePath+"TSSSFBartholomew-Bold.otf", 45),
    "Body":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", 35),
    "BodySmall":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", 35),
    "BodyChangeling":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", 33),
    "Bar":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", 38),
    "BarSmall":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", 35),
    "Flavortext":PIL_Helper.BuildFont(ResourcePath+"KlinicSlabBookIt.otf", 28),
    "Copyright":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", 18)
}

Anchors = {
    "Blank": (base_w_center, 300),
    "PonyArt": (173, 225),
    "ShipArt": (173, 226),
    "GoalArt": (174, 224),
    "Symbol1": (58+50,56+63),
    "Symbol2": (58+50,160+63),
    "LoneSymbol": (108,153),
    "TimelineSymbol": (58+50,535+63),
    "GoalSymbol2": (108,613),
    "Title": (-65-50, 160),
    "TitleTwoLine": (-65-50, 159),
    "TitleSmall": (-65-50, 157),
    "Bar": (-68-50, 598+67),
    "Body": (base_w_center, 730),
    "BodyShiftedUp": (base_w_center, 720),
    "Flavor": (base_w_center, -110),
    "Expansion": (640+50, 525+63),
    "Copyright": (-38-50, -15-63)
}

ArtMissing = [
    PIL_Helper.LoadImage(CardPath+"/artmissing01.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing02.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing03.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing04.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing05.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing06.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing07.png"),
    ]

Frames = {
    "START": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Start.png"),
    "Warning": PIL_Helper.LoadImage(CardPath+"/BLEED_Card - Warning.png"),
    "Pony": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Pony.png"),
    "Ship": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Ship.png"),
    "Rules1": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules1.png"),
    "Rules3": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules3.png"),
    "Rules5": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules5.png"),
    "Goal": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Goal.png"),
    "Derpy": PIL_Helper.LoadImage(CardPath+"/BLEED_Card - Derpy Hooves.png"),
    "TestSubject": PIL_Helper.LoadImage(CardPath+"/BLEED_Card - OverlayTest Subject Cheerilee.png")
    }

Symbols = {
    "male": PIL_Helper.LoadImage(ResourcePath+"/Symbol-male.png"),
    "female": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Female.png"),
    "malefemale": PIL_Helper.LoadImage(ResourcePath+"/Symbol-MaleFemale.png"),
    "earth pony": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Earth-Pony.png"),
    "unicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Unicorn.png"),
    "uniearth": PIL_Helper.LoadImage(ResourcePath+"/symbol-uniearth.png"),
    "pegasus": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Pegasus.png"),
    "alicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Alicorn.png"),
    "changelingearthpony": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingEarthPony.png"),
    "changelingunicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingUnicorn.png"),
    "changelingpegasus": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingPegasus.png"),
    "changelingalicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingAlicorn.png"),
    "dystopian": PIL_Helper.LoadImage(ResourcePath+"/symbol-dystopian-future.png"),
    "ship": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Ship.png"),
    "goal": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Goal.png"),
    "0": PIL_Helper.LoadImage(ResourcePath+"/symbol-0.png"),
    "1": PIL_Helper.LoadImage(ResourcePath+"/symbol-1.png"),
    "2": PIL_Helper.LoadImage(ResourcePath+"/symbol-2.png"),
    "3": PIL_Helper.LoadImage(ResourcePath+"/symbol-3.png"),
    "4": PIL_Helper.LoadImage(ResourcePath+"/symbol-4.png"),
    "3-4": PIL_Helper.LoadImage(ResourcePath+"/symbol-34.png"),
    "2-3": PIL_Helper.LoadImage(ResourcePath+"/symbol-23.png")
    }
TIMELINE_SYMBOL_LIST = ["Dystopian"]

Expansions = {
    "Everfree14": PIL_Helper.LoadImage(ResourcePath+"/symbol-Everfree14.png"),
    "Indiegogo": PIL_Helper.LoadImage(ResourcePath+"/symbol-Indiegogo.png"),
    "Birthday": PIL_Helper.LoadImage(ResourcePath+"/symbol-birthday.png"),
    "Bronycon": PIL_Helper.LoadImage(ResourcePath+"/symbol-Bronycon14.png"),
    "Summer": PIL_Helper.LoadImage(ResourcePath+"/symbol-summer-lovin.png"),
    "Apricity": PIL_Helper.LoadImage(ResourcePath+"/symbol-apricity.png"),
    "BronyCAN": PIL_Helper.LoadImage(ResourcePath+"/symbol-Bronycan14.png"),
    "Xtra": PIL_Helper.LoadImage(ResourcePath+"/symbol-extracredit.png"),
    "Xtra-dark": PIL_Helper.LoadImage(ResourcePath+"/symbol-extracredit-black.png"),
    "NMND": PIL_Helper.LoadImage(ResourcePath+"/symbol-nightmarenights.png"),
    "Ciderfest": PIL_Helper.LoadImage(ResourcePath+"/symbol-ponyvilleciderfest.png"),
    "Adventure": PIL_Helper.LoadImage(ResourcePath+"/symbol-adventure.png"),
    "Custom": PIL_Helper.LoadImage(ResourcePath+"/symbol-custom.png"),
    "Power": PIL_Helper.LoadImage(ResourcePath+"/symbol-power.png"),
    "Multiplicity": PIL_Helper.LoadImage(ResourcePath+"/symbol-multiplicity.png"),
    "Canon": PIL_Helper.LoadImage(ResourcePath+"/symbol-canon.png"),
    "Dungeon": PIL_Helper.LoadImage(ResourcePath+"/symbol-dungeon.png"),
    "50": PIL_Helper.LoadImage(ResourcePath+"/symbol-50.png"),
    "2014": PIL_Helper.LoadImage(ResourcePath+"/symbol-2014.png"),
    "Hearthswarming": PIL_Helper.LoadImage(ResourcePath+"/symbol-hearthswarming.png")
    }

ColorDict={
    "START": (58, 50, 53),
    "START bar text": (237, 239, 239),
    "START flavor": (28, 20, 23),
    "Pony": (70, 44, 137),
    "Pony bar text": (234, 220, 236),
    "Pony flavor": (25, 2, 51),
    "Goal": (18, 57, 98),
    "Goal flavor": (7, 34, 62),
    "Shipwrecker": (8, 57, 98),
    "Shipwrecker flavor": (0, 34, 62),
    "Ship": (206, 27, 105),
    "Ship bar text": (234, 220, 236),
    "Ship flavor": (137, 22, 47),
    "Copyright": (255, 255, 255),
    "Blankfill": (200,200,200)
    }

RulesDict={
    "{replace}": "While in your hand, you may discard a Pony card from the grid and play this card in its place. This power cannot be copied.",
    "{swap}": "You may swap 2 Pony cards on the shipping grid. Neither of their powers activate.",
    "{draw}": "You may draw a card from the Ship or Pony deck.",
    "{goal}": "You may put 1 Goal at the bottom of the Goal deck and draw a new one to replace it.",
    "{search}": "You may search the Ship or Pony discard pile for a card of your choice and play it.",
    "{copy}": "You may copy the power of any Pony card currently on the shipping grid, except for Changelings.",
    "{love poison}": "Instead of playing this ship with a Pony card from your hand, or connecting two ponies already on the grid, take a Pony card from the shipping grid and reattach it elsewhere with this Ship. That card's power activates.",
    "{keyword change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as having any one keyword of your choice, except pony names."
    }

backs = {"START": PIL_Helper.LoadImage(ResourcePath + "Back-Start.png"),
         "Pony": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "Goal": PIL_Helper.LoadImage(ResourcePath + "Back-Goals.png"),
         "Ship": PIL_Helper.LoadImage(ResourcePath + "Back-Ships.png"),
         "Card": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "Shipwrecker": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "BLANK": PIL_Helper.LoadImage(ResourcePath + "Blank - Intentionally Left Blank.png"),
         "Rules1": PIL_Helper.LoadImage(CardPath + "Rules2.png"),
         "Rules3": PIL_Helper.LoadImage(CardPath + "Rules4.png"),
         "Rules5": PIL_Helper.LoadImage(CardPath + "Rules6.png"),
         "TestSubject": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "Warning": PIL_Helper.LoadImage(CardPath + "Card - Contact.png")
        }


def FixFileName(tagin):
    FileName = tagin.replace("\n", "")
    invalid_chars = [",", "?", '"', ":"]
    for c in invalid_chars:
        FileName = FileName.replace(c,"")
    FileName = u"{0}.png".format(FileName)
    #print FileName
    return FileName

def FixUnicode(text):
    text=text.replace(r'\n','\n')
    if LegacySymbolMode:
        text=text.replace(';', u"\u2642")
        text=text.replace('*', u"\u2640")
        text=text.replace('>', u"\u26A4")
        text=text.replace('#', u"\u2714")
        text=text.replace('<', u"\u2764")
        text=text.replace('%', u"\uE000")
        text=text.replace('8', u"\uE001")
        text=text.replace('9', u"\uE002")
        text=text.replace('@', u"\uE003")
        text=text.replace('$', u"\uE004")
    else:
        text=text.replace('{male}', u"\u2642")
        text=text.replace('{female}', u"\u2640")
        text=text.replace('{malefemale}', u"\u26A4")
        text=text.replace('{goal}', u"\u2714")
        text=text.replace('{ship}', u"\u2764")
        text=text.replace('{earthpony}', u"\uE000")
        text=text.replace('{unicorn}', u"\uE001")
        text=text.replace('{pegasus}', u"\uE002")
        text=text.replace('{alicorn}', u"\uE003")
        text=text.replace('{postapocalypse}', u"\uE004")
    return text

def BuildCard(linein):
    tags = linein.strip('\n').replace(r'\n', '\n').split('`')
    try:
        im = PickCardFunc(tags[TYPE], tags)
        if len(tags)>3:
            #print os.path.join(BleedsPath,FixFileName(tags[0]+"__"+tags[3]))
            im.save(os.path.join(BleedsPath,FixFileName(tags[0]+"__"+tags[3])))
            im_crop=im.crop(croprect)
            im_crop.save(os.path.join(CropPath,FixFileName(tags[0]+"__"+tags[3])))
            im_vassal=PIL_Helper.ResizeImage(im_crop,vassalscale)
            im_vassal.save(os.path.join(VassalPath,FixFileName(tags[0]+"__"+tags[3])))
        else:
            im_crop=im.crop(croprect)
        #MakeVassalCard(im_cropped)

    except Exception as e:
        print "Warning, Bad Card: {0}".format(tags)
        traceback.print_exc()
        im_crop = MakeBlankCard().crop(croprect)
    #im.show()  # TEST
    return im_crop

def BuildBack(linein):
    tags = linein.strip('\n').replace(r'\n', '\n').split('`')
    #print("Back type: " + tags[TYPE])
    return backs[tags[TYPE]]
  

def PickCardFunc(card_type, tags):
    if tags[TYPE] == "START":
        return MakePonyCard(tags)
    elif tags[TYPE] == "Pony":
        return MakePonyCard(tags)
    elif tags[TYPE] == "Ship":
        return MakeShipCard(tags)
    elif tags[TYPE] == "Goal":
        return MakeGoalCard(tags)
    elif tags[TYPE] == "BLANK":
        return MakeBlankCard()
    elif tags[TYPE] == "Warning":
        return MakeSpecialCard("Warning")
    elif tags[TYPE] == "Rules1":
        return MakeSpecialCard("Rules1")
    elif tags[TYPE] == "Rules3":
        return MakeSpecialCard("Rules3")
    elif tags[TYPE] == "Rules5":
        return MakeSpecialCard("Rules5")
    elif tags[TYPE] == "TestSubject":
        return MakePonyCard(tags)
    elif tags[TYPE] == "Card":
        return MakeSpecialCard(tags[PICTURE])
    else:
        raise Exception("No card of type {0}".format(tags[TYPE]))
def GetFrame(card_type):
    return Frames[card_type].copy()

def AddCardArt(image, filename, anchor):
    if filename == "NOART":
        return
    if os.path.exists(os.path.join(CardPath, filename)):
        art = PIL_Helper.LoadImage(os.path.join(CardPath, filename))
    else:
        art = random.choice(ArtMissing)
    # Find desired height of image based on width of 600 px
    w, h = art.size
    h = int((float(ART_WIDTH)/w)*h)
    # Resize image to fit in frame
    art = PIL_Helper.ResizeImage(art, (ART_WIDTH,h))
    image.paste(art, anchor)

def AddSymbols(image, symbols, card_type=""):
    # Remove any timeline symbols from the symbols list
    pruned_symbols = set(symbols)-set(TIMELINE_SYMBOL_LIST)
    if card_type == "Goal":
        positions = [Anchors["LoneSymbol"], Anchors["GoalSymbol2"]]
    else:
        # If there's only one non-timeline symbol in the list,
        # Set it right on the corner of the picture.
        # Otherwise, adjust so the symbols share the space
        if len(pruned_symbols) == 1:
            positions = [Anchors["LoneSymbol"]]
        else:
            positions = [Anchors["Symbol1"], Anchors["Symbol2"]]

    for index,s in enumerate(symbols):
        sym = Symbols.get(s.lower(), None)
        if sym:
            if s in TIMELINE_SYMBOL_LIST:
                image.paste(sym, Anchors["TimelineSymbol"], sym)
            else:
                image.paste(sym, positions[index], sym)

def TitleText(image, text, color):
    font = fonts["Title"]
    anchor = Anchors["Title"]
    leading = -9
    if text.count('\n') > 0:
        anchor = Anchors["TitleTwoLine"]
        leading = -15
    if len(text)>TitleWidthThresholds[0]:
        anchor = Anchors["TitleSmall"]
        font = fonts["TitleSmall"]
    print repr(text)
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        valign = "center",
        halign = "right",
        leading_offset = leading
        )
def BarText(image, text, color):
    bar_text_size = PIL_Helper.GetTextBlockSize(text,fonts["Bar"],textmaxwidth)
    if bar_text_size[0] > BarTextThreshold[0]:
        font = fonts["BarSmall"]
    else:
        font = fonts["Bar"]
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = Anchors["Bar"],
        halign = "right"
        )
def BodyText(image, text, color, flavor_text_size=0):
    # Replacement of keywords with symbols
    for keyword in RulesDict:
        if keyword in text:
            text = text.replace(keyword, RulesDict[keyword])
    text = FixUnicode(text)
    font = fonts["Body"]
    anchor = Anchors["Body"]
    leading = -1
    # Get the size of the body text as (w,h)
    body_text_size = PIL_Helper.GetTextBlockSize(
        text, fonts["Body"], textmaxwidth
        )
    # If the height of the body text plus the height of the flavor text
    # doesn't fit in on the card in the normal position, move the body text up
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[0]:
        anchor = Anchors["BodyShiftedUp"]
    # If they still don't fit, makes the body text smaller
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
        font = fonts["BodySmall"]
        body_text_size = PIL_Helper.GetTextBlockSize(
            text, font, textmaxwidth
            )
        # If they still don't fit, make it smaller again. They're probably
        # the changeling cards
        if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
            font = fonts["BodyChangeling"]
            leading = -5
            print "changeling bodytext"
    Anchors["BodyShiftedUp"]
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        halign = "center",
        max_width = textmaxwidth,
        leading_offset=leading
        )
def FlavorText(image, text, color):
    return PIL_Helper.AddText(
        image = image,
        text = text,
        font = fonts["Flavortext"],
        fill = color,
        anchor = Anchors["Flavor"],
        valign = "bottom",
        halign = "center",
        leading_offset=+1,
        max_width = textmaxwidth,
        )
def AddExpansion(image, expansion):
    expansion_symbol = Expansions.get(expansion, None)
    if expansion_symbol:
        image.paste(expansion_symbol, Anchors["Expansion"], expansion_symbol)
def CopyrightText(image, color):
    text = "{}; TSSSF (C) Horrible People Productions. Art by {}.".format(
        CardSet.replace('_',' '),
        ARTIST
        )
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = fonts["Copyright"],
        fill = color,
        anchor = Anchors["Copyright"],
        valign = "bottom",
        halign = "right",
        )
def MakeBlankCard():
    image = PIL_Helper.BlankImage(base_w, base_h)
    
    PIL_Helper.AddText(
        image = image,
        text = "This Card Intentionally Left Blank",
        font = fonts["Title"],
        fill = ColorDict["Blankfill"],
        anchor = Anchors["Blank"],
        max_width = textmaxwidth
        )    
    return image

def MakeStartCard(tags):
    image = PIL_Helper.BlankImage(base_w, base_h,color=ColorDict[tags[TYPE]])

    return image
def MakePonyCard(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["PonyArt"])
    TitleText(image, tags[TITLE], ColorDict["Pony"])
    AddSymbols(image, tags[SYMBOLS].split('!'))
    BarText(image, tags[KEYWORDS], ColorDict["Pony bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Pony flavor"])
    BodyText(image, tags[BODY], ColorDict["Pony"], text_size)
    AddExpansion(image, tags[EXPANSION])
    CopyrightText(image, ColorDict["Copyright"])
    return image
def MakeShipCard(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["ShipArt"])
    TitleText(image, tags[TITLE], ColorDict["Ship"])
    AddSymbols(image, tags[SYMBOLS].split('!'), "Ship")
    #AddSymbols(image, "Ship")
    BarText(image, tags[KEYWORDS], ColorDict["Ship bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Ship flavor"])
    BodyText(image, tags[BODY], ColorDict["Ship"], text_size)
    AddExpansion(image, tags[EXPANSION])
    CopyrightText(image, ColorDict["Copyright"])
    return image
def MakeGoalCard(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["GoalArt"])
    TitleText(image, tags[TITLE], ColorDict["Goal"])
    AddSymbols(image, tags[SYMBOLS].split('!'), card_type="Goal")
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Goal flavor"])
    BodyText(image, tags[BODY], ColorDict["Goal"], text_size)
    AddExpansion(image, tags[EXPANSION])
    CopyrightText(image, ColorDict["Copyright"])
    return image
def MakeSpecialCard(cardtype):
    return GetFrame(cardtype)

def InitVassalModule():
    pass

def MakeVassalCard(im):
    VassalCard[0]+=1
    #BuildCard(line).save(VassalImagesPath + "/" + str(VassalCard) + ".png")
    im.save(VassalImagesPath + "/" + str(VassalCard[0]) + ".png")
    
def CompileVassalModule():
    pass

if __name__ == "__main__":
    print "Not a main module. Run GameGen.py"
