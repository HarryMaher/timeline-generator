#!/usr/bin/env python
'''
# Animated Timeline Maker

For animated timeline map resumes. It's sort of a hack-job. 

Some things you gotta watch out for:
1. You can't put commas in the job descriptions because that gets messed up because of the .csv 
   part of things (duh) so use "&#44;" (no quotes) when you need to put a comma in the job 
   if things aren't working!
2. Use ctrl+f to find and edit javascript, html, and css things because everything is on a single 
   line so that makes it hard to edit.
3. My laptop screen is tiny so it'll probably not look so good on anything with decent resolution.
   That'll be fixed if I get a better laptop someday.

When editing the .csv to suit your own resume or whatever time series you wanna show:
1. title is the title of the job
2. title_pl should probably be called "employer"
3. start_d is what'll show up on the job description start date
4. end_d is the end date. the last one will be the end date of the timeline below. Ideally present.
5. measure is currently not in use
6. units is in use, so like keep your units the same. This decides how long the timeline bar will be.
7. Location is the whole employer, city, state, country type thing
8. x and y are the x,y coordinates. find these by right clicking on location in google map then
   clicking on "what's here" and copying the coordinates
9. zoom is how far you wanna zoom in. For rural things, zoom farther out to keep it interesting.
10. All the descriptions. I believe you need to fill all of them, which you should be able to do 
    with any job.

Requires:
python3
pandas

'''
import pandas as pd 

df = pd.read_table("example.csv", sep=",")

ids = []
titls = []
units = []
cords = [] #called "all" in javascript below for all two coords. oops. horrible var name... w/e
zoom = []
description = []
start_d = []
end_d = []
titl_pl = []

for i in range(len(df['x'])):
    lst = []
    lst.append(df['x'][i])
    lst.append(df['y'][i])
    cords.append(lst)
    ids.append(df['id'][i])
    start_d.append(df['start_d'][i])
    end_d.append(df['end_d'][i])
    titls.append(df['title'][i])
    titl_pl.append(df['title_pl'][i])
    units.append(df['units'][i])
    zoom.append(df['zoom'][i])

    
# job description....
d0 = "<div class=\"descr\"><div class=\"row\"><div class=\"col-xs-7\" style=\"\" id= \"title\"><h3>"
#title goes here
d1 = "</h3></div><div class=\"col-xs-5\" style=\"text-align:right;\" id= \"dates\"><h3><small>"
#start date - end date go here
d2 = "</small></div></div> <i>"
#location, written format, goes here
d3 = "</i><p><li>"
#descrip1 goes here
d4 = "</li></p><p><li>"
#descrip2 goes here
d5 = "</li></p><p><li>"
#descrip3 goes here
d6 = "</li></p>"
length = len(ids)

    
for d in range(len(df['descrip1'])):
    newdescrip = d0 + df['title'][d]+d1+str(df['start_d'][d])+ " - " +str(df['end_d'][d])+d2+str(df['location'][d])+d3+str(df['descrip1'][d])+d4+str(df['descrip2'][d])+d5+str(df['descrip3'][d])+d6
    description.append(newdescrip)
    
f = open('index.html' , 'w')
f.write("<!DOCTYPE html><html><head><title>Animated Timeline Map</title><meta charset=\"UTF-8\"><meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\"><meta name=\"description\" content=\"Animated timeline map created with python!\"><meta name=\"keywords\" content=\"Animated Timeline Map With Leaflet leaflet Harry\"><meta name=\"author\" content=\"Harry\"><!-- CSS --><link rel=\"stylesheet\" href=\"http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css\"><link rel=\"stylesheet\" href=\"style.css\"><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css\"></head><body><main><section><div id=\"map\"></div><div id=\"instructions\"><strong>Instructions:</strong> click the different colors on the timeline below to navigate!<br><br><a class=\"btn btn-info\"id=\"close\">OK!</a></div><div id=\"bigtitle\">&emsp;</div><div id=\"startdate\">start</div><div id=\"enddate\">end</div><div id=\"slider\"></div></section></main><script src=\"https://code.jquery.com/jquery-3.2.1.min.js\" integrity=\"sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=\" crossorigin=\"anonymous\"></script><script type=\"text/javascript\" src=\"https://unpkg.com/leaflet@1.0.3/dist/leaflet.js\"></script><script type=\"text/javascript\" src=\"script.js\"></script></body></html>")
f.close()


f = open('script.js','w')
newdoc = "function addControlPlaceholders(t){function i(t,i){var n=e+t+\" \"+e+i;a[t+i]=L.DomUtil.create(\"div\",n,s)}var a=t._controlCorners,e=\"leaflet-\",s=t._controlContainer;i(\"verticalcenter\",\"left\"),i(\"verticalcenter\",\"right\")}function zoomer(t,i){return x=(t[0]+i[0])/2,y=(t[1]+i[1])/2,[x,y]}function zoomer2(t,i){var a=Math.abs(Math.max(t[0],i[0])-Math.min(t[0],i[0])),e=Math.abs(Math.max(t[1],i[1])-Math.min(t[1],i[1]));return a<2&&e<2?13:a<10&&e<10?6:a<30&&e<30?4:a<40&&e<40?5:3}function timer(t,i){var a=Math.abs(Math.max(t[0],i[0])-Math.min(t[0],i[0])),e=Math.abs(Math.max(t[1],i[1])-Math.min(t[1],i[1]));return a<2&&e<2?340:a<20&&e<20?1500:a<50&&e<50?2e3:2500}function timer2(t,i){var a=Math.abs(Math.max(t[0],i[0])-Math.min(t[0],i[0])),e=Math.abs(Math.max(t[1],i[1])-Math.min(t[1],i[1]));return a<2&&e<2?1300:a<20&&e<20?6e3:a<50&&e<50?8200:8600}function recenter(t,i,a,e){var s=t.project(i);s=new L.point(s.x+a,s.y+e);var n=t.unproject(s);t.panTo(n)}function mapmove(t,i){map.flyTo(zoomer(all[t],all[i]),zoomer2(all[t],all[i])),$(\".info\").hide(),setTimeout(function(){marker.closePopup(),marker.moveTo(all[i],timer(all[t],all[i]))},timer(all[t],all[i])),setTimeout(function(){map.flyTo(all[i],zoom[i])},2*timer(all[t],all[i])),setTimeout(function(){recenter(map,all[i],-200,0),$(\".info\").html(description[i]),$(\".info\").show(),marker.bindPopup(\"<span id='tooltip'>\"+titl_pl[i]+\"</span>\",{closeOnClick:!0}).openPopup(),i++},timer2(all[t],all[i])),setTimeout(function(){marker.closePopup()},timer2(all[t],all[i])+3e3)}L.interpolatePosition=function(t,i,a,e){var s=e/a;return s=s>0?s:0,s=s>1?1:s,L.latLng(t.lat+s*(i.lat-t.lat),t.lng+s*(i.lng-t.lng))},L.Marker.MovingMarker=L.Marker.extend({statics:{notStartedState:0,endedState:1,pausedState:2,runState:3},options:{autostart:!1,loop:!1},initialize:function(t,i,a){L.Marker.prototype.initialize.call(this,t[0],a),this._latlngs=t.map(function(t,i){return L.latLng(t)}),i instanceof Array?this._durations=i:this._durations=this._createDurations(this._latlngs,i),this._currentDuration=0,this._currentIndex=0,this._state=L.Marker.MovingMarker.notStartedState,this._startTime=0,this._startTimeStamp=0,this._pauseStartTime=0,this._animId=0,this._animRequested=!1,this._currentLine=[],this._stations={}},isRunning:function(){return this._state===L.Marker.MovingMarker.runState},isEnded:function(){return this._state===L.Marker.MovingMarker.endedState},isStarted:function(){return this._state!==L.Marker.MovingMarker.notStartedState},isPaused:function(){return this._state===L.Marker.MovingMarker.pausedState},start:function(){this.isRunning()||(this.isPaused()?this.resume():(this._loadLine(0),this._startAnimation(),this.fire(\"start\")))},resume:function(){this.isPaused()&&(this._currentLine[0]=this.getLatLng(),this._currentDuration-=this._pauseStartTime-this._startTime,this._startAnimation())},pause:function(){this.isRunning()&&(this._pauseStartTime=Date.now(),this._state=L.Marker.MovingMarker.pausedState,this._stopAnimation(),this._updatePosition())},stop:function(t){this.isEnded()||(this._stopAnimation(),void 0===t&&(t=0,this._updatePosition()),this._state=L.Marker.MovingMarker.endedState,this.fire(\"end\",{elapsedTime:t}))},addLatLng:function(t,i){this._latlngs.push(L.latLng(t)),this._durations.push(i)},moveTo:function(t,i){this._stopAnimation(),this._latlngs=[this.getLatLng(),L.latLng(t)],this._durations=[i],this._state=L.Marker.MovingMarker.notStartedState,this.start(),this.options.loop=!1},addStation:function(t,i){t>this._latlngs.length-2||t<1||(this._stations[t]=i)},onAdd:function(t){L.Marker.prototype.onAdd.call(this,t),!this.options.autostart||this.isStarted()?this.isRunning()&&this._resumeAnimation():this.start()},onRemove:function(t){L.Marker.prototype.onRemove.call(this,t),this._stopAnimation()},_createDurations:function(t,i){for(var a=t.length-1,e=[],s=0,n=0,o=0;o<a;o++)n=t[o+1].distanceTo(t[o]),e.push(n),s+=n;var r=i/s,l=[];for(o=0;o<e.length;o++)l.push(e[o]*r);return l},_startAnimation:function(){this._state=L.Marker.MovingMarker.runState,this._animId=L.Util.requestAnimFrame(function(t){this._startTime=Date.now(),this._startTimeStamp=t,this._animate(t)},this,!0),this._animRequested=!0},_resumeAnimation:function(){this._animRequested||(this._animRequested=!0,this._animId=L.Util.requestAnimFrame(function(t){this._animate(t)},this,!0))},_stopAnimation:function(){this._animRequested&&(L.Util.cancelAnimFrame(this._animId),this._animRequested=!1)},_updatePosition:function(){var t=Date.now()-this._startTime;this._animate(this._startTimeStamp+t,!0)},_loadLine:function(t){this._currentIndex=t,this._currentDuration=this._durations[t],this._currentLine=this._latlngs.slice(t,t+2)},_updateLine:function(t){var i=t-this._startTimeStamp;if(i<=this._currentDuration)return i;for(var a,e=this._currentIndex,s=this._currentDuration;i>s;){if(i-=s,void 0!==(a=this._stations[e+1])){if(i<a)return this.setLatLng(this._latlngs[e+1]),null;i-=a}if(++e>=this._latlngs.length-1){if(!this.options.loop)return this.setLatLng(this._latlngs[this._latlngs.length-1]),this.stop(i),null;e=0,this.fire(\"loop\",{elapsedTime:i})}s=this._durations[e]}return this._loadLine(e),this._startTimeStamp=t-i,this._startTime=Date.now()-i,i},_animate:function(t,i){this._animRequested=!1;var a=this._updateLine(t);if(!this.isEnded()){if(null!=a){var e=L.interpolatePosition(this._currentLine[0],this._currentLine[1],this._currentDuration,a);this.setLatLng(e)}i||(this._animId=L.Util.requestAnimFrame(this._animate,this,!1),this._animRequested=!0)}}}),L.Marker.movingMarker=function(t,i,a){return new L.Marker.MovingMarker(t,i,a)};var map=new L.Map(\"map\",{minZoom:2});map.zoomControl.setPosition(\"topright\");var tileUrl=\"http://c.tile.stamen.com/toner-lite/{z}/{x}/{y}.png\",layer=new L.TileLayer(tileUrl,{attribution:'Timeline map by <a href=\"http://harrymaher.github.io\" target=\"_blank\">Harry Maher</a> tiles by <a href=\"http://stamen.com\" target=\"_blank\">Stamen Design</a>, under <a target=\"_blank\" href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a>. Data by <a target=\"_blank\" href=\"http://openstreetmap.org\">OpenStreetMap</a>, under <a target=\"_blank\" href=\"http://creativecommons.org/licenses/by-sa/3.0\">CC BY SA</a>',maxZoom:17});map.addLayer(layer);var start=["+str(df["x"][length-1])+", "+str(df["y"][length-1])+"],all="+str(cords) +",zoom="+ str(zoom) +",units= "+ str(units) + ",titls="+ str(titls)+",start_d="+ str(start_d)+",end_d="+ str(end_d)+",titl_pl="+str(titl_pl)+",ids="+str(ids) +",previous=\"<div id='previous'>Previous</a>\",description="+str(description)+";map.setView(new L.LatLng(start[0],start[1]),13),addControlPlaceholders(map);var marker=L.Marker.movingMarker([start],{iconUrl:\"https://unpkg.com/leaflet@1.0.3/dist/images/marker-icon.png\"}).addTo(map),lasti=(ids.length-1);recenter(map,all[(ids.length-1)],-200,0);var info=L.control();info.onAdd=function(t){return this._div=L.DomUtil.create(\"div\",\"info\"),this.update(),this._div},info.update=function(t){this._div.innerHTML=description[lasti]},info.addTo(map),info.setPosition(\"verticalcenterleft\"),marker.bindPopup(\"<span id='tooltip'>\"+titl_pl[lasti]+\"</span>\",{closeOnClick:!0}).openPopup(),$(document).ready(function(){for(tot=0,count=0;count<units.length;count++)tot+=units[count];for(count=0;count<units.length;count++){var t=100*units[count]/tot;$(\"#slider\").append(\"<div id='\"+[count]+\"' class='\"+ ids[count] +\" box' ></div>\"),$(\"#\"+[count]).css(\"width\",t+\"%\"),$(\"#\"+[count]).css(\"background-color\",\"rgba(0,\"+(255-Math.round(30*ids[count]))+\",\"+(255-Math.round(ids[count]*8))+\", .8)\")}}),$(document).ready(function(){$(\"#close\").click(function(){$(\"#instructions\").hide()});$(\"#startdate\").html(start_d[0]);$(\"#enddate\").html(end_d[(end_d.length-1)]);$(\".box\").css(\"opacity\",.8),$(\".box\").mouseenter(function(){var highlightThis=$(this).attr(\"class\").split(\" \")[0];$(\".\"+highlightThis).css(\"opacity\",1);$(\"#bigtitle\").html(titl_pl[this.id]+\" - \"+titls[this.id])}).mouseleave(function(){var highlightThis=$(this).attr(\"class\").split(\" \")[0];$(\".\"+highlightThis).css(\"opacity\",.8);$(\"#bigtitle\").html(\"&emsp;\")}),$(\".box\").click(function(){mapmove(lasti,this.id),lasti=this.id})});$(document).ready(function(){$(\".leaflet-marker-icon\").attr(\"src\",\"https://unpkg.com/leaflet@1.0.3/dist/images/marker-icon.png\"),$(\".leaflet-marker-shadow\").attr(\"src\",\"https://unpkg.com/leaflet@1.0.3/dist/images/marker-shadow.png\")});"
f.write(newdoc)
f.close()

f = open('style.css' , 'w')
f.write("#map{height:100%}main{position:relative}h1{display:none}html,body{height:100%;margin:0}main{height:100%}section{height:100%}.info{padding:6px 8px;font:14px/16px Arial,Helvetica,sans-serif;background:rgba(255,255,255,.90);box-shadow:none;border-radius:4px;border:2px solid rgba(0,0,0,0.2);text-align:left;max-width:45%;min-width:400px;max-height:300px}.leftbar a{background:rgba(255,255,255,.8)!important}.info h4{margin:0 0 5px;color:#777}.leaflet-verticalcenter{position:absolute;top:35%;transform:translateY(-35%);padding-top:10px;padding-left:15px}.leaflet-verticalcenter .leaflet-control{margin-bottom:10px}#slider{width:98%;background-color:#fff;height:30px;position:absolute;z-index:9999;margin-left:1%;margin-right:1%;bottom:18px;border-radius:4px;border:2px solid rgba(0,0,0,0.2)}div .box{height:26px;float:left;width:30px}#bigtitle{position:absolute;left:0;right:0;margin-left:auto;margin-right:auto;max-width:500px;text-align:center;z-index:9999;bottom:55px;font-size:140%;color:#004fff;text-shadow:1px 1px 0 #FFF,-1px 1px 0 #FFF,1px -1px 0 #FFF,-1px -1px 0 #FFF,0 1px 0 #FFF,0 -1px 0 #FFF,-1px 0 0 #FFF,1px 0 0 #FFF}.descr{color:#0050c8!important;padding-left:10px}small{color:rgba(0,80,200,.8)!important}#tooltip{text-align:center;font-size:1.3em;color:#0050c8}.leaflet-control-zoom-in,.leaflet-control-zoom-out{background-color:rgba(255,255,255,.8)!important;}#instructions{background-color:rgba(255,255,255,.95);left:0;right:0;max-width:370px;text-align:center;color:rgba(0,80,200,.8)!important;z-index:99999;position:absolute;top:30%;margin-left:auto;margin-right:auto;padding:10px;border:2px solid rgba(0,0,0,.2);border-radius:4px;}.leaflet-popup-content-wrapper{border-radius: 4px;box-shadow: none;background-color: rgba(255,255,255,.8);}.leaflet-popup-tip{background-color:rgba(255,255,255,.8);box-shadow:none;}#enddate,#startdate{position:absolute;max-width:100px;text-align:center;z-index:9999;bottom:55px;font-size:110%;color:#004fff;padding:0 10px;text-shadow:1px 1px 0 #FFF,-1px 1px 0 #FFF,1px -1px 0 #FFF,-1px -1px 0 #FFF,0 1px 0 #FFF,0 -1px 0 #FFF,-1px 0 0 #FFF,1px 0 0 #FFF}#startdate{float:left;left:0}#enddate{right:0;float:right}")
f.close()

