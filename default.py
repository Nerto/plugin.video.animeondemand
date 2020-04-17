import xbmc
import xbmcplugin

from resources.lib import util
from resources.lib import model
from resources.lib import view
from resources.lib import controller

def main(argv):
    args = model.parse(argv)
    if not (args._addon.getSetting("user") and args._addon.getSetting("pass")):
        args._addon.openSettings()
        return False
    else:
        util.login(args)
        xbmcplugin.setContent(int(args._argv[1]), "tvshows")              
        check_mode(args)

def check_mode(args):
    if hasattr(args, "mode"):
        mode = args.mode
    else:
        mode = None           
    if not mode:
        showMainMenue(args)
    elif mode == 'showNewEpisodes':
        controller.showNewEpisode(args)
    elif mode == 'showNewEpisodesSerie':
        controller.showNewEpisodesSerie(args)  
    elif mode == 'newSimulcasts':
        controller.showNewSimualcasts(args)    
    elif mode == 'showNewAnime':  
        controller.showNewAnime(args)    
    elif mode == 'top10':
        controller.showTop10(args)
    elif mode == 'top10':
        controller.showTop10(args)                      
    elif mode == 'All':
        controller.showAll(args)            
    elif mode == 'AZ':
        controller.showAtoZ(args)    
    elif mode == 'showCharacter':
        controller.showCharacter(args)      
    elif mode == 'list_episodes':
        controller.listEpisodes(args)
    elif mode == "videoplay":
        controller.startplayback(args)    
    else:
        showMainMenue(args)

def showMainMenue(args):    
    view.add_item(args,{"title": args._addon.getLocalizedString(30114),"mode":   "showNewEpisodes"})  
    view.add_item(args,{"title": args._addon.getLocalizedString(30118),"mode":   "showNewEpisodesSerie"})
    view.add_item(args,{"title": args._addon.getLocalizedString(30116),"mode":   "newSimulcasts"})
    view.add_item(args,{"title": args._addon.getLocalizedString(30117),"mode":   "showNewAnime"})    
    view.add_item(args,{"title": args._addon.getLocalizedString(30119),"mode":   "top10"})
    #view.add_item(args,{"title": args._addon.getLocalizedString(30105),"mode":   "Genre"})
    view.add_item(args,{"title": args._addon.getLocalizedString(30107),"mode":   "All"})
    view.add_item(args,{"title": args._addon.getLocalizedString(30104),"mode":   "AZ"})
    view.endofdirectory(args)

if __name__ == "__main__":    
    main(sys.argv)