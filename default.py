# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs

Versao = "18.04.15"

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
cPageani = Addon.getSetting("cPageani")
cPagedes = Addon.getSetting("cPagedes")
if not cadulto:
	cPageleg = cPage
	cPagenac = cPage
	cPageser = cPage
	cPageani = cPage
	cPagedes = cPage
Cat = Addon.getSetting("Cat")
Clista=[ "todos",                     "acao", "animacao", "aventura", "comedia", "drama", "fantasia", "ficcao-cientifica", "romance", "suspense", "terror"]
Clista2=["Sem filtro (Mostrar Todos)","Acao", "Animacao", "Aventura", "Comedia", "Drama", "Fantasia", "Ficcao-Cientifica", "Romance", "Suspense", "Terror"]

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
playlistsFile = "http://localhost:8080/nc/tvshows.php"
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
historicFile = os.path.join(addon_data_dir, 'historic.txt')
if not (os.path.isfile(favoritesFile)):
	common.SaveList(favoritesFile, [])
if not (os.path.isfile(historicFile)):
	common.SaveList(historicFile, [])
	
makeGroups = "true"
URLP="http://buildtonywarlley.000webhostapp.com"
#URLP="http://localhost:8080/"
URLNC=URLP+"nc/"
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	#xbmcgui.Dialog().ok('Kodi', str(cPagenac))
	#AddDir("[B]!{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	AddDir("[B][COLOR lightgray]Canais -[/COLOR][/B][COLOR lime] Ao Vivo [/COLOR]" , "", 100, "http://i66.tinypic.com/fdsr2s.jpg", "http://i66.tinypic.com/fdsr2s.jpg")
	AddDir("[COLOR lightgray][B]Filmes Dublados[/B][/COLOR]" , cPage, 90, "http://i67.tinypic.com/2mnojkn.jpg", "http://i67.tinypic.com/2mnojkn.jpg", background="cPage")
	AddDir("[COLOR lightgray][B]Filmes Legendados[/B][/COLOR]" , cPageleg, 91, "http://i67.tinypic.com/34xg6s7.jpg", "http://i67.tinypic.com/34xg6s7.jpg", background="cPageleg")
	AddDir("[COLOR lightgray][B]Filmes Nacionais[/B][/COLOR]" , cPagenac, 92, "http://i68.tinypic.com/rvzp8l.jpg", "http://i68.tinypic.com/rvzp8l.jpg", background="cPagenac")
	AddDir("[COLOR lightgray][B]Séries[/B][/COLOR]" , cPageser, 130, "http://i67.tinypic.com/33ng6cl.jpg", "http://i67.tinypic.com/33ng6cl.jpg", background="cPageser")
	try:
		checa = urllib2.urlopen( URLNC + "version.txt" ).read()
		AddDir("[COLOR lightgray][B]Séries[/B][/COLOR]" , URLNC + "listTVshow.php", 60, "http://i67.tinypic.com/2cwx3it.jpg", "http://i67.tinypic.com/2cwx3it.jpg")
		AddDir("[COLOR lightgray][B]Filmes[/B][/COLOR]" , URLNC + "listMovies.php", 71, "http://i66.tinypic.com/2ezh8wj.jpg", "http://i66.tinypic.com/2ezh8wj.jpg")
	except urllib2.URLError, e:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "setting", 50, "", "", 0, cacheMin = "0", isFolder=False)
	#AddDir("[COLOR lightgray][B]Filmes por Gênero:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"http://i67.tinypic.com/ieibdw.jpg", "http://i67.tinypic.com/ieibdw.jpg", isFolder=False)
	AddDir("[COLOR lightgray][B]Animes[/B][/COLOR]" , cPageser, 140, "http://i66.tinypic.com/1112hc3.jpg", "http://i66.tinypic.com/1112hc3.jpg", background="cPageser")
	AddDir("[COLOR lightgray][B]Desenhos[/B][/COLOR]" , cPageani, 150, "http://i65.tinypic.com/1qqzgz.jpg", "http://i65.tinypic.com/1qqzgz.jpg", background="cPageser")
# --------------  NETCINE
def PlayS(): #62
	try:
		link = urllib2.urlopen(URLNC +  url).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		listau=[]
		listan=[]
		listai=[]
		for url2,img2,name2,info2 in match:
			listau.append(url2)
			listan.append(name2 + name)
			listai.append(info2)
		d = xbmcgui.Dialog().select("TONYWARLLEY", listan)
		if d!= -1:
			PlayUrl(listan[d], listau[d], iconimage, listai[d])
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok("TONYWARLLEY" , "Server error, tente novamente em alguns minutos")

def EpisodioS(): #61
	try:
		link = urllib2.urlopen( URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		for url2,img2,name2,info2 in match:
			AddDir(name2 ,url2, 62, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)
	
def Series(): #60
	try:
		link = urllib2.urlopen(url).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		for url2,img2,name2 in match:
			AddDir(name2, url2, 61, img2, img2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)

def MoviesNC(): #70
	AddDir("[COLOR lightgray][B]Filmes por Gênero:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"http://i67.tinypic.com/ieibdw.jpg", "http://i67.tinypic.com/ieibdw.jpg", isFolder=False)
	try:
		link = urllib2.urlopen(url +"?cat=" + Clista[int(Cat)]).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		for url2,img2,name2 in match:
			AddDir(name2 ,url2, 79, img2, img2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)

def Generos(): #80
	xbmcgui.Dialog().notification('Movie Trailers', 'Finding Nemo download finished.', xbmcgui.NOTIFICATION_INFO, 5000)
	d = xbmcgui.Dialog().select("Escolha o Genero", Clista2)
	if d != -1:
		global Cat
		Addon.setSetting("Cat", str(d) )
		Cat = d
		Addon.setSetting("cPage", "0" )
		Addon.setSetting("cPageleg", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def PlayM(): #79
	try:
		link = urllib2.urlopen(URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		for url2,img2,name2,info2 in match:
			AddDir(name2 + name ,url2, 3, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2, background=url+";;;"+name)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)
# --------------  FIM NETCINE
# --------------  REDECANAIS FILMES
def MoviesRCD(): #90 Filme dublado
	AddDir("[COLOR lightgray][B]Filmes por Gênero:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"http://i67.tinypic.com/ieibdw.jpg", "http://i67.tinypic.com/ieibdw.jpg", isFolder=False)
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Página Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", cPage , 120 ,"http://i65.tinypic.com/70dmx4.jpg", isFolder=False, background="cPage")
		l= int(cPage)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-dublado-videos-"+str(l)+"-date.html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.info/browse-"+Clista2[int(Cat)]+"-Filmes-videos-"+str(l)+"-date.html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Próxima Página >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", cPage , 110 ,"http://i64.tinypic.com/9jiova.jpg", isFolder=False, background="cPage")
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def MoviesRCL(): #91 Filme Legendado
	AddDir("[COLOR lightgray][B]Filmes por Gênero:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"http://i67.tinypic.com/ieibdw.jpg", "http://i67.tinypic.com/ieibdw.jpg", isFolder=False)
	try:
		p= 1
		if int(cPageleg) > 0:
			AddDir("[COLOR blue][B]<< Página Anterior ["+ str( int(cPageleg) ) +"[/B]][/COLOR]", cPageleg , 120 ,"http://i65.tinypic.com/70dmx4.jpg", isFolder=False, background="cPageleg")
		l= int(cPageleg)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-legendado-videos-"+str(l)+"-date.html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.net/browse-"+Clista2[int(Cat)]+"-Filmes-Legendado-videos-"+str(l)+"-date.html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Próxima Página >> ["+ str( int(cPageleg) + 2) +"[/B]][/COLOR]", cPageleg , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPageleg")
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def MoviesRCN(): #92 Filmes Nacional
	try:
		p= 1
		if int(cPagenac) > 0:
			AddDir("[COLOR blue][B]<< Próxima Página ["+ str( int(cPagenac) ) +"[/B]][/COLOR]", cPagenac , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPagenac")
		l= int(cPagenac)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-nacional-videos-"+str(l)+"-date.html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Próxima Página >> ["+ str( int(cPagenac) + 2) +"[/B]][/COLOR]", cPagenac , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPagenac")
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
			AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , urlp[0] + "?play|Referer=http://www.redecanais.com/", 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info=desc, background=url+";;;"+name)
		else:
			AddDir("[B]Ocorreu um erro[/B]"  , "", 0, iconimage, iconimage, index=0, isFolder=False, IsPlayable=False, info="Erro")
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
# ----------------- FIM REDECANAIS
# --------------  REDECANAIS SERIES,ANIMES,DESENHOS
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
		else:
			xbmcgui.Dialog().ok('TONYWARLLEY', 'Erro, tente novamente em alguns minutos')
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def TemporadasRC(): #135 Temporadas
	link = common.OpenURL(url).replace('\n','').replace('\r','').replace('</html>','<span style="font')
	temps = re.compile('size: x-large;\">.+?<span style\=\"font').findall(link)
	if temps:
		i= 0
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(temps[0])
		temps = re.compile('(<span style="font-size: x-large;">(.+?)<\/span>)').findall(link)
		if temps:
			for a,tempname in temps:
				tempname = re.sub('<[\/]{0,1}strong>', "", tempname)
				try:
					tempname = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), tempname).encode('utf-8')
				except:
					tempname = tempname
				if not "ilme" in tempname:
					AddDir("[B]["+tempname+"][/B]" , url, 136, iconimage, iconimage, info="", isFolder=True, background=i)
				i+=1
	else:
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	#if not temps:
		for name2,url2,brp in epi:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
			else:
				name3=name2
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			try:
				namem = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), re.compile('([^\-]+)').findall(url2)[0] ).encode('utf-8')
			except:
				namem = re.compile('([^\-]+)').findall(url2)[0]
			namem = re.sub('<[\/]{0,1}strong>', "", namem)
			if "<" in namem:
				namem = ""
			if urlm:
				urlm[0] = "http://www.redecanais.net/" + urlm[0] if "http" not in urlm[0] else urlm[0]
			if len(urlm) > 1:
				urlm[1] = "http://www.redecanais.net/" + urlm[1] if "http" not in urlm[1] else urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] "+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] "+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir(name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
	#xbmcgui.Dialog().ok('Kodi', "1"))
def EpisodiosRC(x): #136 Episodios
	link = common.OpenURL(url).replace('\n','').replace('\r','').replace('</html>','<span style="font')
	temps = re.compile('size: x-large;\">.+?<span style\=\"font').findall(link)
	if temps:
		i= 0
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(temps[ int(x) ])
	else:
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if epi:
		for name2,url2,brp in epi:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
			else:
				name3=name2
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			try:
				namem = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), re.compile('([^\-]+)').findall(url2)[0] ).encode('utf-8')
			except:
				namem = re.compile('([^\-]+)').findall(url2)[0]
			namem = re.sub('<[\/]{0,1}strong>', "", namem)
			if "<" in namem:
				namem = ""
			if urlm:
				urlm[0] = "http://www.redecanais.net/" + urlm[0] if "http" not in urlm[0] else urlm[0]
			if len(urlm) > 1:
				urlm[1] = "http://www.redecanais.net/" + urlm[1] if "http" not in urlm[1] else urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] "+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] "+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir(name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)

def SeriesRC(urlrc,pagina2): #130 Lista as Series RC
	try:
		pagina=eval(pagina2)
		p= 1
		if int(pagina) > 0:
			AddDir("[COLOR blue][B]<< Próxima Página ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
		l= int(pagina)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-"+urlrc+"-videos-"+str(l)+"-title.html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 135, img2, img2, info="")
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Próxima Página >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , url, 0, "", "", 0, cacheMin = "0")
# ----------------- FIM REDECANAIS SERIES,ANIMES,DESENHOS
# ----------------- BUSCA
def Busca(): # 160
	AddDir("[COLOR pink][B][Nova Busca][/B][/COLOR]", "" , 50 ,"", isFolder=False)
	d = xbmcgui.Dialog().input("Busca (poder demorar a carregar os resultados)").replace(" ", "+")
	try:
		p= 1
		AddDir("[COLOR blue][B][RedeCanais.com][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		l= 0
		for x in range(0, 10):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/search.php?keywords="+d+"&page="+str(l))
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			if match:
				for url2,img2,name2 in match:
					if re.compile('\d+p').findall(name2):
						AddDir(name2 ,url2, 95, img2, img2)
					elif "Lista" in name2:
						AddDir(name2 ,url2, 135, img2, img2)
	except urllib2.URLError, e:
		AddDir("Nada encontrado" , "", 0, "", "", 0)
	try:
		AddDir("[COLOR yellow][B][NetCine.us][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		link = urllib2.urlopen(URLNC+"listBusca.php?b="+d).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?ode="(.+?)"').findall(link)
		for url2,img2,name2,mode2 in match:
			AddDir(name2 ,url2, int(mode2), img2, img2)
	except urllib2.URLError, e:
		AddDir("Nada encontrado" , "", 0, "", "", 0)
# ----------------- FIM BUSCA
# ----------------- REDECANAIS TV
def TVRC(): # 100
	try:
		l= 0
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/browse-canais-videos-"+str(l)+"-title.html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					try:
						name2 = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), name2.replace("Assistir ", "").replace(" - Online - 24 Horas - Ao Vivo", "") ).encode('utf-8')
					except:
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
	#xbmcgui.Dialog().ok(background, url + " " +background)
	if background != "None":
		b = background.split(";;;")
		if "redecanais" in background:
			AddFavorites(b[0], iconimage, b[1], "95", "historic.txt")
		else:
			AddFavorites(b[0], iconimage, b[1], "79", "historic.txt")
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
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage )
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
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode== 61 or info=="series nc":
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
	
def AddFavorites(url, iconimage, name, mode, file):
	file = os.path.join(addon_data_dir, file)
	favList = common.ReadList(file)
	for item in favList:
		if item["url"].lower() == url.decode("utf-8").lower():
			if "favorites" in file:
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
	common.SaveList(file, favList)
	if "favorites" in file:
		xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30012), icon))
	
def ListFavorites(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = common.ReadList(file)
	i = 0
	for channel in chList:
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), index=i, isFolder=True, IsPlayable=False, info=info)
		i += 1
		
def ListHistoric(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = common.ReadList(file)
	for channel in reversed(chList):
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), isFolder=True, IsPlayable=False, info=info)
		
def AddNewFavorite(file):
	file = os.path.join(addon_data_dir, file)
	chName = GetKeyboardText(getLocaleString(30014))
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText(getLocaleString(30015))
	if len(chUrl) < 1:
		return
	image = GetChoice(30023, 30023, 30023, 30024, 30025, 30021, fileType=2)
		
	favList = common.ReadList(file)
	for item in favList:
		if item["url"].lower() == chUrl.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, getLocaleString(30011), icon))
			return
			
	data = {"url": chUrl.decode("utf-8"), "image": image, "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(file, favList):
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
	#notMakeGroups = "false" if makeGroups else "true"
	#Addon.setSetting("makeGroups", notMakeGroups)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def TogglePrevious(url, background):
	Addon.setSetting(background, str(int(url) - 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def ToggleNext(url, background):
	#xbmcgui.Dialog().ok('TONYWARLLEY', url + " " +background)
	Addon.setSetting(background, str(int(url) + 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def CheckUpdate(msg): #200
	try:
		uversao = urllib2.urlopen( "https://raw.githubusercontent.com/BUILDTONYWARLLEY/TONYWARLLEY/master/version.txt" ).read().replace('\n','').replace('\r','')
		if uversao != Versao or not cadulto:
			Update()
			xbmc.executebuiltin("XBMC.Container.Refresh()")
		elif msg==True:
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
	xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "EM BREVE, Addon em Fase de Teste...", icon))
	xbmc.sleep(2000)

def study(x):
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	py = os.path.join( Path, "study.txt")
	file = open(py, "w")
	file.write(x)
	file.close()

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
	CheckUpdate(False)
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
	ListFavorites('favorites.txt', "Favoritos")
	setViewS()
elif mode == 333:
	ListHistoric('historic.txt', "Historico")
	setViewM()
elif mode == 31: 
	AddFavorites(url, iconimage, name, "61", 'favorites.txt') 
elif mode == 72: 
	AddFavorites(url, iconimage, name, "79", 'favorites.txt') 
elif mode == 93: 
	AddFavorites(url, iconimage, name, "95", 'favorites.txt') 
elif mode == 131: 
	AddFavorites(url, iconimage, name, "135", 'favorites.txt') 
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
elif mode == 40:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('TONYWARLLEY', 'Deseja mesmo deletar todo o historico?')
	if ret:
		common.DelFile(historicFile)
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
	SeriesRC("series","cPageser")
	setViewS()
elif mode == 135:
	TemporadasRC()
	setViewS()
elif mode == 136:
	EpisodiosRC(background)
	setViewS()
elif mode == 133:
	PlaySRC()
	setViewS()
elif mode == 140:
	SeriesRC("animes","cPageani")
	setViewS()
elif mode == 150:
	SeriesRC("desenhos","cPagedes")
	setViewS()
elif mode == 160:
	Busca()
	setViewM()
elif mode == 200:
	CheckUpdate(True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegrity25852
