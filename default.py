# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs

Versao = "1.0"

AddonID = 'plugin.video.TONYWARLLEY'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path').decode("utf-8")
iconsDir = os.path.join(addonDir, "resources", "images")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

addon_data_dir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
cacheDir = os.path.join(addon_data_dir, "cache")
if not os.path.exists(cacheDir):
	os.makedirs(cacheDir)

cadulto = Addon.getSetting("cadulto")
cPage = Addon.getSetting("cPage") # dublado redecanais
cPageleg = Addon.getSetting("cPageleg")
cPagenac = Addon.getSetting("cPagenac")
cPageser = Addon.getSetting("cPageser")
if not cPageleg:
	cPageleg = cPage
	cPagenac = cPage
	cPageser = cPage
Cat = Addon.getSetting("Cat")
Clista=[ "todos",                     "acao", "animacao", "aventura", "comedia", "drama", "fantasia", "ficcao-cientifica", "romance", "suspense", "terror"]
Clista2=["Sem filtro (Mostrar Todos)","Acao", "Animacao", "Aventura", "Comedia", "Drama", "Fantasia", "Ficcao-Cientifica", "Romance", "Suspense", "Terror"]

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
playlistsFile = "http://localhost:8080/nc/tvshows.php"
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
if not (os.path.isfile(favoritesFile)):
	common.SaveList(favoritesFile, [])
	
makeGroups = "true"
URLP="http://buildtonywarlley.000webhostapp.com"
#URLP="http://localhost:8080/"
URLNC=URLP+"nc/"
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	#xbmcgui.Dialog().ok('Kodi', str(cPagenac))
	#AddDir("[B]!{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	AddDir("[B][COLOR lightgray]Canais -[/COLOR][/B][COLOR lime] Ao Vivo [/COLOR]" , "", 100, "http://i66.tinypic.com/fdsr2s.jpg", "http://i66.tinypic.com/fdsr2s.jpg", index=0)
	AddDir("[COLOR lightgray][B]Filmes Dublados[/B][/COLOR]" , cPage, 90, "http://i67.tinypic.com/2mnojkn.jpg", "http://i67.tinypic.com/2mnojkn.jpg", background="cPage")
	AddDir("[COLOR lightgray][B]Filmes Legendados[/B][/COLOR]" , cPageleg, 91, "http://i67.tinypic.com/34xg6s7.jpg", "http://i67.tinypic.com/34xg6s7.jpg", background="cPageleg")
	AddDir("[COLOR lightgray][B]Filmes Nacionais[/B][/COLOR]" , cPagenac, 92, "http://i68.tinypic.com/rvzp8l.jpg", "http://i68.tinypic.com/rvzp8l.jpg", background="cPagenac")
	AddDir("[COLOR lightgray][B]Séries[/B][/COLOR]" , cPageser, 130, "http://i67.tinypic.com/33ng6cl.jpg", "http://i67.tinypic.com/33ng6cl.jpg", background="cPageser")
	try:
		checa = urllib2.urlopen( URLNC + "version.txt" ).read()
		AddDir("[COLOR lightgray][B]Séries[/B][/COLOR]" , URLNC + "listTVshow.php", 60, "http://i67.tinypic.com/2cwx3it.jpg", "http://i67.tinypic.com/2cwx3it.jpg", index=0, cacheMin = "0")
		AddDir("[COLOR lightgray][B]Filmes[/B][/COLOR]" , URLNC + "listMovies.php", 71, "http://i66.tinypic.com/2ezh8wj.jpg", "http://i66.tinypic.com/2ezh8wj.jpg", index=0, cacheMin = "0")
	except urllib2.URLError, e:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "setting", 50, "", "", 0, cacheMin = "0", isFolder=False)
	AddDir("[COLOR lughtgray][B][Filmes por genero]:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		uversao = urllib2.urlopen( "https://raw.githubusercontent.com/BUILDTONYWARLLEY/TONYWARLLEY/master/version.txt" ).read().replace('\n','').replace('\r','')
		if uversao != Versao:
			Update()
			xbmc.executebuiltin("XBMC.Container.Refresh()")
	except urllib2.URLError, e:
		uversao = ""
	# --------------  NETCINE
def PlayS(): #62
	try:
		link = urllib2.urlopen(URLNC +  url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2,info2 in match:
			AddDir(name2 + name ,url2, 3, iconimage, iconimage, index=i, isFolder=False, IsPlayable=True, info=info2)
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")

def EpisodioS(): #61
	try:
		link = urllib2.urlopen( URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2,info2 in match:
			AddDir(name2 ,url2, 62, iconimage, iconimage, index=i, cacheMin = "0", info=info2)
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
	
def Series(): #60
	try:
		link = urllib2.urlopen(url).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2 in match:
			AddDir(name2, url2, 61, img2, img2, index=i, cacheMin = "0")
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")

def MoviesNC(): #70
	AddDir("[COLOR red][B]Filtro: " + Clista2[int(Cat)] + "[/B][/COLOR]", "setting" ,90 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		link = urllib2.urlopen( url +"?cat=" + Clista[int(Cat)]).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2 in match:
			AddDir(name2 ,url2, 79, img2, img2, index=i, cacheMin = "0", info="")
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")

def Generos(): #80
	dialog = xbmcgui.Dialog()
	d = dialog.select("Escolha o Genero", Clista2)
	if d != -1:
		global Cat
		Addon.setSetting("Cat", str(d) )
		Cat = d
		#xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, str(Cat) , "Cat", ""))
		Addon.setSetting("cPage", "0" )
		Addon.setSetting("cPageleg", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def PlayM(): #79
	try:
		link = urllib2.urlopen(URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2,info2 in match:
			AddDir(name2 + name ,url2, 3, iconimage, iconimage, index=i, isFolder=False, IsPlayable=True, info=info2)
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
# --------------  FIM NETCINE
# --------------  REDECANAIS FILMES
def MoviesRCD(): #90 Filme dublado
	AddDir("[COLOR red][B]Filtro: " + Clista2[int(Cat)] + "[/B][/COLOR]", "setting" ,90 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", cPage , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPage")
		l= int(cPage)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-dublado-videos-"+str(l)+"-date.html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.info/browse-"+Clista2[int(Cat)]+"-Filmes-videos-"+str(l)+"-date.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", cPage , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPage")
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def MoviesRCL(): #91 Filme Legendado
	AddDir("[COLOR red][B]Filtro: " + Clista2[int(Cat)] + "[/B][/COLOR]", "setting" ,90 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		p= 1
		if int(cPageleg) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPageleg) ) +"[/B]][/COLOR]", cPageleg , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageleg")
		l= int(cPageleg)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-legendado-videos-"+str(l)+"-date.html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.net/browse-"+Clista2[int(Cat)]+"-Filmes-Legendado-videos-"+str(l)+"-date.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPageleg) + 2) +"[/B]][/COLOR]", cPageleg , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPageleg")
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def MoviesRCN(): #92 Filmes Nacional
	try:
		p= 1
		if int(cPagenac) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPagenac) ) +"[/B]][/COLOR]", cPagenac , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPagenac")
		l= int(cPagenac)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-nacional-videos-"+str(l)+"-date.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPagenac) + 2) +"[/B]][/COLOR]", cPagenac , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPagenac")
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def PlayMRC(): #95 Play filmes
	try:
		link = common.OpenURL(url)
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		if player:
			link2 = common.OpenURL(player[0])
			urlp = re.compile('file: \"([^\"]+)\"').findall(link2)
			AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , urlp[0] + "?play|Referer=http://www.redecanais.com/", 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info=desc)
		else:
			AddDir("[B]Ocorreu um erro[/B]"  , "", 0, iconimage, iconimage, index=0, isFolder=False, IsPlayable=False, info="Erro")
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
# ----------------- FIM REDECANAIS
# --------------  REDECANAIS SERIES
def PlaySRC(): #131 Play series
	try:
		link = common.OpenURL(url)
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		if player:
			link2 = common.OpenURL(player[0])
			urlp = re.compile('file: \"([^\"]+)\"').findall(link2)
			PlayUrl(name, urlp[0] + "?play|Referer=http://www.redecanais.com/", iconimage, name)
			#AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , urlp[0] + "?play|Referer=http://www.redecanais.com/", 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info=desc)
		else:
			xbmcgui.Dialog().ok('TONYWARLLEY', 'Erro, tente novamente em alguns minutos')
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def EpisodiosRC(): #135 Play filmes
	link = common.OpenURL(url)
	match = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if match:
		for name2,url2,brp in match:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
				if int(name3) == 1:
					S = S + 1
			else:
				name3=name2

			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			namem = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), re.compile('([^\-]+)').findall(url2)[0] ).encode('utf-8')
			if "<" in namem:
				namem = ""
			if urlm:
				if "http" not in urlm[0]:
					urlm[0] = "http://www.redecanais.net/" + urlm[0]
			if len(urlm) > 1:
				if "http" not in urlm[1]:
					urlm[1] = "http://www.redecanais.net/" + urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir("[COLOR red][???][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
	#xbmcgui.Dialog().ok('Kodi', str(match[0][1]))


def SeriesRC(): #130 Lista as Series RC
	try:
		p= 1
		if int(cPageser) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPageser) ) +"[/B]][/COLOR]", cPageser , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageser")
		l= int(cPageser)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-series-videos-"+str(l)+"-title.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 135, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPageser) + 2) +"[/B]][/COLOR]", cPageser , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPageser")
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , url, 0, "", "", 0, cacheMin = "0")
# ----------------- REDECANAIS TV
def TVRC(): # 100
	#AddDir("[B]{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	try:
		l= 0
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/browse-canais-videos-"+str(l)+"-title.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					name2 = name2.replace("Assistir ", "").replace(" - Online - 24 Horas - Ao Vivo", "")
					#name2 = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), name2).encode('utf-8')
					if cadulto=="8080":
						AddDir(name2 ,url2, 101, img2, img2, index=i, cacheMin = "0", info="", isFolder=False, IsPlayable=True)
					elif not "sex" in url2 and not "playboy" in url2:
						AddDir(name2 ,url2, 101, img2, img2, index=i, cacheMin = "0", info="", isFolder=False, IsPlayable=True)
					i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def PlayTVRC(): # 101
	try:
		link = common.OpenURL(url)
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		link2 = common.OpenURL(player[0])
		urlp = re.compile('\"source\"\: \"([^\"]+)').findall(link2)
		PlayUrl(name, urlp[0] + "?play|Referer=http://www.redecanais.com/", iconimage, name)
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('TONYWARLLEY', 'Erro, tente novamente em alguns minutos')
# ----------------- FIM REDECANAIS TV
def AddNewList():
	listName = GetKeyboardText(getLocaleString(30004)).strip()
	if len(listName) < 1:
		return
	listUrl = GetChoice(30002, 30005, 30006, 30016, 30017, fileType=1, fileMask='.plx|.m3u|.m3u8')
	if len(listUrl) < 1:
		return
	image = GetChoice(30022, 30022, 30022, 30024, 30025, 30021, fileType=2)
	logosUrl = '' if listUrl.endswith('.plx') else GetChoice(30018, 30019, 30020, 30019, 30020, 30021, fileType=0)
	if logosUrl.startswith('http') and not logosUrl.endswith('/'):
		logosUrl += '/'
	cacheInMinutes = GetNumFromUser(getLocaleString(30034), '0') if listUrl.startswith('http') else 0
	if cacheInMinutes is None:
		cacheInMinutes = 0
	chList = common.ReadURL(playlistsFile)
	for item in chList:
		if item["url"].lower() == listUrl.lower():
			xbmc.executebuiltin('Notification({0}, "{1}" {2}, 5000, {3})'.format(AddonName, item["name"].encode("utf-8"), getLocaleString(30007), icon))
			return
	chList.append({"name": listName.decode("utf-8"), "url": listUrl, "image": image, "logos": logosUrl, "cache": cacheInMinutes})
	if common.SaveList(playlistsFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None, defaultText=""):
	choice = ''
	choiceList = [getLocaleString(choiceFile), getLocaleString(choiceUrl)]
	if choiceNone is not None:
		choiceList = [getLocaleString(choiceNone)] + choiceList
	method = GetSourceLocation(getLocaleString(choiceTitle), choiceList)	
	if choiceNone is None and method == 0 or choiceNone is not None and method == 1:
		if not defaultText.startswith('http'):
			defaultText = ""
		choice = GetKeyboardText(getLocaleString(fileTitle), defaultText).strip().decode("utf-8")
	elif choiceNone is None and method == 1 or choiceNone is not None and method == 2:
		if defaultText.startswith('http'):
			defaultText = ""
		choice = xbmcgui.Dialog().browse(fileType, getLocaleString(urlTitle), 'files', fileMask, False, False, defaultText).decode("utf-8")
	return choice
	
def RemoveFromLists(index, listFile):
	chList = common.ReadList(listFile) 
	if index < 0 or index >= len(chList):
		return
	del chList[index]
	common.SaveList(listFile, chList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")
			
def PlxCategory(url, cache):
	tmpList = []
	chList = common.plx2list(url, cache)
	background = chList[0]["background"]
	for channel in chList[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("{0}".format(name) ,channel["url"].encode("utf-8"), 1, iconimage, background=background.encode("utf-8"))
		else:
			AddDir(name, channel["url"].encode("utf-8"), 3, iconimage, isFolder=False, IsPlayable=True, background=background)
			tmpList.append({"url": channel["url"], "image": iconimage.decode("utf-8"), "name": name.decode("utf-8")})
			
def m3uCategory(url, logos, cache, gListIndex=-1):	
	tmpList = []
	chList = common.m3u2list(url, cache)
	groupChannels = []
	for channel in chList:
		if makeGroups:
			matches = [groupChannels.index(x) for x in groupChannels if len(x) > 0 and x[0].get("group_title", x[0]["display_name"]) == channel.get("group_title", channel["display_name"])]
		if makeGroups and len(matches) == 1:
			groupChannels[matches[0]].append(channel)
		else:
			groupChannels.append([channel])
	for channels in groupChannels:
		idx = groupChannels.index(channels)
		if gListIndex > -1 and gListIndex != idx:
			continue
		isGroupChannel = gListIndex < 0 and len(channels) >= 1
		chs = [channels[0]] if isGroupChannel else channels
		for channel in chs:
			chUrl = common.GetEncodeString(channel["url"])
			name = common.GetEncodeString(channel["display_name"]) if not isGroupChannel else common.GetEncodeString(channel.get("group_title", channel["display_name"]))
			if isGroupChannel:
				name = '{0}'.format(name)
				chUrl = url
				image = channel.get("tvg_logo", channel.get("logo", ""))
				AddDir(name ,url, 10, image, index=idx)
			elif chUrl == "http://127.0.0.0":
				image = channel.get("tvg_logo", channel.get("logo", ""))
				if logos is not None and logos != ''  and image != "" and not image.startswith('http'):
					image = logos + image
			else:
				image = channel.get("tvg_logo", channel.get("logo", ""))
				if logos is not None and logos != ''  and image != "" and not image.startswith('http'):
					image = logos + image
				AddDir(name, chUrl, 60, image, index=-1, isFolder=True, IsPlayable=False)
			tmpList.append({"url": chUrl.decode("utf-8"), "image": image.decode("utf-8"), "name": name.decode("utf-8")})
		
def PlayUrl(name, url, iconimage=None, info=''):
	if url.startswith('acestream://'):
		url = 'plugin://program.plexus/?mode=1&url={0}&name={1}&iconimage={2}'.format(url, name, iconimage)
	else:
		url = common.getFinalUrl(url)
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	if iconimage is not None:
		try:
			listitem.setArt({'thumb' : iconimage})
		except:
			listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage='', logos='', index=-1, move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'info': info, 'background': background}
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, )
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
	#liz.setProperty("Fanart_Image", logos)
	liz.setArt({
	"poster": iconimage,
	"banner": logos,
	"fanart": logos
        })
	listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	#if background != None:
	#	liz.setProperty('fanart_image', background)
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode== 61:
		liz.addContextMenuItems(items = [("Add ao fav. do TONYWARLLEY", 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 79:
		liz.addContextMenuItems(items = [("Add ao fav. do TONYWARLLEY", 'XBMC.RunPlugin({0}?url={1}&mode=72&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 95:
		liz.addContextMenuItems(items = [("Add ao fav. do TONYWARLLEY", 'XBMC.RunPlugin({0}?url={1}&mode=93&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 135:
		liz.addContextMenuItems(items = [("Add ao fav. do TONYWARLLEY", 'XBMC.RunPlugin({0}?url={1}&mode=131&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	if info=="Favoritos":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=33)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 38)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 38)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 38))]
		liz.addContextMenuItems(items)
	if mode == 10:
		urlParams['index'] = index
	u = '{0}?{1}'.format(sys.argv[0], urllib.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, chList):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, chList)
	return answer
	
def AddFavorites(url, iconimage, name, mode):
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30011), icon))
			return
	chList = []	
	for channel in chList:
		if channel["name"].lower() == name.decode("utf-8").lower():
			url = channel["url"].encode("utf-8")
			iconimage = channel["image"].encode("utf-8")
			break
	if not iconimage:
		iconimage = ""
	data = {"url": url.decode("utf-8"), "image": iconimage.decode("utf-8"), "name": name.decode("utf-8"), "mode": mode}
	favList.append(data)
	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30012), icon))
	
def ListFavorites():
	chList = common.ReadList(favoritesFile)
	i = 0
	for channel in chList:
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), index=i, isFolder=True, IsPlayable=False, info="Favoritos")
		i += 1
		
def AddNewFavorite():
	chName = GetKeyboardText(getLocaleString(30014))
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText(getLocaleString(30015))
	if len(chUrl) < 1:
		return
	image = GetChoice(30023, 30023, 30023, 30024, 30025, 30021, fileType=2)
		
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == chUrl.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, getLocaleString(30011), icon))
			return
			
	data = {"url": chUrl.decode("utf-8"), "image": image, "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(favoritesFile, favList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def ChangeKey(index, listFile, key, title):
	chList = common.ReadList(listFile)
	str = GetKeyboardText(getLocaleString(title), chList[index][key].encode("utf-8"))
	if len(str) < 1:
		return
	chList[index][key] = str.decode("utf-8")
	if common.SaveList(listFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def ChangeChoice(index, listFile, key, choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None):
	chList = common.ReadList(listFile)
	defaultText = chList[index].get(key, "")
	str = GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone, fileType, fileMask, defaultText.encode("utf-8"))
	if key == "url" and len(str) < 1:
		return
	elif key == "logos" and str.startswith('http') and not str.endswith('/'):
		str += '/'
	chList[index][key] = str.decode("utf-8")
	if common.SaveList(listFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")
	
def MoveInList(index, step, listFile):
	theList = common.ReadList(listFile)
	if index + step >= len(theList) or index + step < 0:
		return
	if step == 0:
		step = GetIndexFromUser(len(theList), index)
	if step < 0:
		tempList = theList[0:index + step] + [theList[index]] + theList[index + step:index] + theList[index + 1:]
	elif step > 0:
		tempList = theList[0:index] + theList[index +  1:index + 1 + step] + [theList[index]] + theList[index + 1 + step:]
	else:
		return
	common.SaveList(listFile, tempList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetNumFromUser(title, defaultt=''):
	dialog = xbmcgui.Dialog()
	choice = dialog.input(title, defaultt=defaultt, type=xbmcgui.INPUT_NUMERIC)
	return None if choice == '' else int(choice)

def GetIndexFromUser(listLen, index):
	dialog = xbmcgui.Dialog()
	location = GetNumFromUser('{0} (1-{1})'.format(getLocaleString(30033), listLen))
	return 0 if location is None or location > listLen or location <= 0 else location - 1 - index

def ChangeCache(index, listFile):
	chList = common.ReadList(listFile)
	defaultText = chList[index].get('cache', 0)
	cacheInMinutes = GetNumFromUser(getLocaleString(30034), str(defaultText)) if chList[index].get('url', '0').startswith('http') else 0
	if cacheInMinutes is None:
		return
	chList[index]['cache'] = cacheInMinutes
	if common.SaveList(listFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def ToggleGroups():
	notMakeGroups = "false" if makeGroups else "true"
	Addon.setSetting("makeGroups", notMakeGroups)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def TogglePrevious(url, background):
	Addon.setSetting(background, str(int(url) - 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def ToggleNext(url, background):
	#xbmcgui.Dialog().ok('TONYWARLLEY', url + " " +background)
	Addon.setSetting(background, str(int(url) + 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def CheckUpdate(): #200
	try:
		uversao = urllib2.urlopen( "https://raw.githubusercontent.com/BUILDTONYWARLLEY/TONYWARLLEY/master/version.txt" ).read().replace('\n','').replace('\r','')
		if uversao != Versao:
			Update()
			xbmc.executebuiltin("XBMC.Container.Refresh()")
		else:
			xbmcgui.Dialog().ok('TONYWARLLEY', "O addon ja esta na ultima versao: "+Versao+"\nAs atualizacoes normalmente sao automaticas\nUse esse recurso caso nao esteja recebendo automaticamente")
			xbmc.executebuiltin("XBMC.Container.Refresh()")
	except urllib2.URLError, e:
		uversao = ""

def Update():
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	try:
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/BUILDTONYWARLLEY/TONYWARLLEY/master/default.py" ).read().replace('\n','')
		prog = re.compile('#checkintegrity25852').findall(fonte)
		if prog:
			#dialog.ok('TONYWARLLEY', str( prog ))
			py = os.path.join( Path, "default.py")
			file = open(py, "w")
			file.write(fonte)
			file.close()
	except urllib2.URLError, e:
		fonte = ""
	try:
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/BUILDTONYWARLLEY/TONYWARLLEY/master/resources/settings.xml" ).read().replace('\n','')
		prog = re.compile('</settings>').findall(fonte)
		if prog:
			py = os.path.join( Path, "resources/settings.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
	except urllib2.URLError, e:
		fonte = ""
	xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "Atualizando o addon. Aguarde um momento!", icon))
	xbmc.sleep(2000)
#	xbmc.executebuiltin("XBMC.Container.Refresh()")
#	xbmcgui.Dialog().ok('TONYWARLLEY', 'Addon atualizado para a ultima versao')
#	xbmc.executebuiltin("XBMC.Container.Refresh()")
#	dialog = xbmcgui.Dialog()
#	ret = xbmcgui.Dialog().ok('TONYWARLLEY', 'Addon atualizado para a ultima versao')
#	if ret:
#		zip = os.path.join( Path, "default.py")
#		f = urllib.urlopen("https://raw.githubusercontent.com/BUILDTONYWARLLEY/TONYWARLLEY/master/default.py")
#		with open(zip, "wb") as subFile:
#			subFile.write(f.read())
#			subFile.close()

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
url = params.get('url')
logos = params.get('logos', '')
name = params.get('name')
iconimage = params.get('iconimage')
cache = int(params.get('cache', '0'))
index = int(params.get('index', '-1'))
move = int(params.get('move', '0'))
mode = int(params.get('mode', '0'))
info = params.get('info')
background = params.get('background')

if mode == 0:
	Categories()
	setViewM()
elif mode == 1:
	PlxCategory(url, cache)
elif mode == 2 or mode == 10:
	m3uCategory(url, logos, cache, index)
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage, info)
	#xbmc.executebuiltin('Notification({0}, "{1}", {2}, {3})'.format( str( info ) , str(info), 20000, ""))
elif mode == 20:
	AddNewList()
elif mode == 21:
	MoveInList(index, move, playlistsFile)
elif mode == 22:
	RemoveFromLists(index, playlistsFile)
elif mode == 23:
	ChangeKey(index, playlistsFile, "name", 30004)
elif mode == 24:
	ChangeChoice(index, playlistsFile, "url", 30002, 30005, 30006, 30016, 30017, None, 1, '.plx|.m3u|.m3u8')
elif mode == 25:
	ChangeChoice(index, playlistsFile, "image", 30022, 30022, 30022, 30024, 30025, 30021, 2)
elif mode == 26:
	ChangeChoice(index, playlistsFile, "logos", 30018, 30019, 30020, 30019, 30020, 30021, 0)
elif mode == 27:
	common.DelFile(playlistsFile)
	sys.exit()
elif mode == 28:
	ChangeCache(index, playlistsFile)
elif mode == 30:
	ListFavorites()
	setViewS()
elif mode == 31: 
	AddFavorites(url, iconimage, name, "61") 
elif mode == 72: 
	AddFavorites(url, iconimage, name, "79") 
elif mode == 93: 
	AddFavorites(url, iconimage, name, "95") 
elif mode == 131: 
	AddFavorites(url, iconimage, name, "135") 
elif mode == 33:
	RemoveFromLists(index, favoritesFile)
elif mode == 34:
	AddNewFavorite()
elif mode == 35:
	ChangeKey(index, favoritesFile, "name", 30014)
elif mode == 36:
	ChangeKey(index, favoritesFile, "url", 30015)
elif mode == 37:
	ChangeChoice(index, favoritesFile, "image", 30023, 30023, 30023, 30024, 30025, 30021, 2)
elif mode == 38:
	MoveInList(index, move, favoritesFile)
elif mode == 39:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('TONYWARLLEY', 'Deseja mesmo deletar todos os favoritos?')
	if ret:
		common.DelFile(favoritesFile)
		sys.exit()
elif mode == 50:
	ToggleGroups()
elif mode == 60:
	Series()
	setViewS()
elif mode == 61:
	EpisodioS()
	setViewS()
elif mode == 62:
	PlayS()
	setViewS()
elif mode == 71:
	MoviesNC()
	setViewM()
elif mode == 79:
	PlayM()
	setViewS()
elif mode == 80:
	Generos()
elif mode == 90:
	MoviesRCD()
	setViewM()
elif mode == 91:
	MoviesRCL()
	setViewM()
elif mode == 92:
	MoviesRCN()
	setViewM()
elif mode == 95:
	PlayMRC()
	setViewM()
elif mode == 100:
	TVRC()
	setViewM()
elif mode == 101:
	PlayTVRC()
	#setViewM()
elif mode == 110:
	ToggleNext(url, background)
elif mode == 120:
	TogglePrevious(url, background)
elif mode == 130:
	SeriesRC()
	setViewS()
elif mode == 135:
	EpisodiosRC()
	setViewS()
elif mode == 133:
	PlaySRC()
	setViewS()
elif mode == 200:
	CheckUpdate()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegrity25852
