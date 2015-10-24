#!/usr/bin/env python
# Name:     nocommonssidslous.py
# Purpose:  Removes Common SSID's From OSX. 
# By:       Jerry Gamblin
# Date:     23.10.15
# Modified  23.10.15
# Rev Level 0.5
# -----------------------------------------------

from contextlib import closing
from urllib import urlopen
import os
import re
import time
import sys
from time import sleep


def color(text, color_code):
    if sys.platform == "win32" and os.getenv("TERM") != "xterm":
        return text

    return '\x1b[%dm%s\x1b[0m' % (color_code, text)

def red(text):
    return color(text, 31)

def blue(text):
    return color(text, 34)
    

ssids=['"SSID"', '"linksys"', '"xfinitywifi"', '"NETGEAR"', '"BTWiFi-with-FON"', '"dlink"', '"default"', '"hpsetup"', '"Ziggo"', '"FreeWifi"', '"BTWIFI"', '"FreeWifi_secure"', '"BTWifi-X"', '"TELENETHOMESPOT"', '"eduroam"', '"UPC Wi-Free"', '"optimumwifi"', '"AndroidAP"', '"belkin54g"', '"SFR WiFi Mobile"', '"cablewifi"', '"wireless"', '"Home"', '"asus"', '"SFR WiFi FON"', '"KPN Fon"', '"orange"', '"BTOpenzone"', '"UPC WifiSpots"', '"BTFON"', '"TelenetWiFree"', '"Fritz!Box Fon WLAN 7390"', '"no_ssid"', '"Guest"', '"WLAN"', '"KD WLAN Hotspot+"', '"attwifi"', '"setup"', '"TWCWiFi"', '"SFR WiFi Public"', '"FRITZ!Box Fon WLAN 7170"', '"FRITZ!Box Fon WLAN 7270"', '"FRITZ!Box Fon WLAN 7112"', '"portthru"', '"0001softbank"', '"FON_BELGACOM"', '"Bouygues Telecom Wi-Fi"', '"FRITZ!Box 7312"', '"internet"', '"SWS1day"', '"BTOpenzone-H"', '"ZyXEL"', '"FON_ZON_FREE_INTERNET"', '"Free Public WiFi"', '"Tp-link"', '"FRITZ!Box 6360 Cable"', '"FRITZ!Box 7362 SL"', '"ACTIONTEC"', '"FON_FREE_INTERNET"', '"FRITZ!Box Fon WLAN 7360"', '"hhonors"', '"freephonie"', '"SMC"', '"FRITZ!Box Fon WLAN 7113"', '"BTOpenzone-B"', '"VOIP"', '"_AUTO_ONOWiFi"', '"PROXIMUS_FON"', '"iPhone"', '"FRITZ!Box 7490"', '"BELTELECOM WIFI"', '"U+zone"', '"PROXIMUS_AUTO_FON"', '"au_Wi-Fi"', '"MyPlace"', '"Motorola"', '"Sitecom"', '"TWCWiFi-Passpoint"', '"iptime"', '"FON_NETIA_FREE_INTERNET"', '"Wi2premium"', '"airportthru"', '"FRITZ!Box 7330 SL"', '"Telekom_FON"', '"wifi"', '"orange12"', '"Wi2premium_club"', '"wlan-ap"', '"D-LINK"', '"dd-wrt"', '"FRITZ!Box WLAN 3170"', '"Orange_FunSpot"', '"ollehWiFi"', '"FRITZ!Box Fon WLAN 7320"', '"Concrete"', '"ShawOpen"', '"rebar"', '"FRITZ!Box Fon WLAN 7240"', '"Netcomm Wireless"', '"au_Wi-Fi2"', '"o2DSL"', '"MSHOME"', '"101"', '"HomeNet"', '"FRITZ!Box Fon WLAN 7141"', '"logitecuser"', '"logitecgameuser"', '"DIR-300NRU"', '"3Com"', '"0000docomo"', '"skynet"', '"FRITZ!Box WLAN 3270"', '"HTC Portable Hotspot"', '"Neuf WiFi"', '"Telekom"', '"Gastzugang"', '"netgear-guest"', '"office"', '"Casa"', '"tsunami"', '"TrendNET"', '"bandsaw"', '"Speedport W 501V"', '"CMCC"', '"_The Cloud"', '"DIR-615"', '"Bright House Networks"', '"EAGLE"', '"myLGNet"', '"THOMSON"', '"Dom"', '"FRITZ!Box 6340 Cable"', '"Philips WiFi"', '"airport"', '"0002softbank"', '"A9F1BDF1DAB1NVT4F4F59"', '"ALICE-WLAN"', '"tmobile"', '"Lowes-Guest-WiFi"', '"ZTE"', '"FRITZ!Box Gastzugang"', '"FRITZ!Box WLAN 3131"', '"TENDA"', '"Target Guest Wi-Fi"', '"0001docomo"', '"guestnet"', '"test"', '"public"', '"Linksys-G"', '"docomo"', '"Fon"', '"FRITZ!Box Fon WLAN 7050"', '"mobile"', '"FRITZ!Box 7330"', '"WWM_P2P"', '"swisscom"', '"XFBSECA7HE6H"', '"CMCC-AUTO"', '"ConnectionPoint"', '"virus"', '"Home Network"', '"Wayport_Access"', '"Alex"', '"FRITZ!Box 6490 Cable"', '"Marriott_Guest"', '"WirelessNet"', '"T wifi zone"', '"Voice"', '"Private"', '"NetWork"', '"cisco"', '"EdiMAX"', '"Zoom"', '"NETGEAR-2.4-G"', '"DIR-300"', '"USR8054"', '"YOTA"', '"KPN"', '"HOL ALU WLAN"', '"RSS-351540"', '"O2 WIFI"', '"MEO-WIFI"', '"NETGEAR_EXT"', '"str241xipv"', '"vodafone-WiFi"', '"HomeDepot Public Wi-Fi"', '"T wifi zone_secure"', '"admin"', '"FON_FREE_EAP"', '"Darmowe_Orange_WiFi"', '"TELE2"', '"DSL_2640NRU"', '"Horizon Wi-Free"', '"NETGEAR1"', '"VOO_HOMESPOT"', '"FRITZ!Box Fon WLAN 7340"', '"belkin"', '"Homenetwork"', '"Tele2-modem"', '"_ONOWiFi"', '"DIR-620"', '"CG-Guest"', '"FRITZ!Box 7272"', '"pretty fly for a wifi"', '"SYNC_00000000"', '"Draytek"', '"coxwifi"', '"dge"', '"freebox"', '"WebSTAR"', '"ASUS_5G"', '"Connectify-me"', '"plusnetwireless"', '"david"', '"M4m786iA"', '"NETGEAR_Guest1"', '"DSLWLANModem200"', '"FRITZ!Box WLAN 3370"', '"ANY"', '"Apple"', '"FRITZ!Box 6320 Cable"', '"Hotspot"', '"planexuser"', '"byfly WIFI"', '"backup"', '"router"', '"staff"', '"steel"', '"xerox"', '"hol - NetFasteR WLAN 3"', '"Visitor"', '"BHN Secure"', '"My Network"', '"Gateway"', '"Student"', '"Tiscali"', '"Wi-Fi"', '"GDS VCI 01"', '"NETGEAR01"', '"netgear12"', '"DLINK_WIRELESS"', '"Airlive"', '"Swisscom_Auto_Login"', '"InfostradaWiFi"', '"netgear11"', '"Wireless Network"', '"NETGEAR24"', '"DIR-320NRU"', '"demopool1"', '"OTE WiFi Fon"', '"DIRECT-"', '"NETGEAR13"', '"NETGEAR22"', '"NETGEAR10"', '"net"', '"Home1"', '"CHT Wi-Fi Auto"', '"NETGEAR23"', '"Customer ID"', '"NETGEAR28"', '"FRITZ!Box SL WLAN"', '"NETGEAR55"', '"NETGEAR19"', '"Netgear88"', '"NETGEAR77"', '"NETGEAR75"', '"NETGEAR21"', '"NETGEAR15"', '"NETGEAR41"', '"NETGEAR45"', '"NETGEAR-24-G"', '"NETGEAR51"', '"NETGEAR25"', '"NETGEAR07"', '"Netgear18"', '"NETGEAR16"', '"NETGEAR46"', '"NETGEAR35"', '"DIR-300NRUB7"', '"NETGEAR85"', '"NETGEAR47"', '"netgear44"', '"NETGEAR40"', '"NETGEAR26"', '"House"', '"netgear69"', '"NETGEAR92"', '"NETGEAR74"', '"NETGEAR50"', '"Netgear09"', '"netgear27"', '"NETGEAR71"', '"NETGEAR05"', '"Netgear30"', '"netgear31"', '"NETGEAR04"', '"NETGEAR99"', '"NETGEAR33"', '"NETGEAR20"', '"NETGEAR53"', '"NETGEAR63"', '"NETGEAR17"', '"NETGEAR32"', '"NETGEAR60"', '"NETGEAR43"', '"NETGEAR52"', '"NETGEAR81"', '"NETGEAR80"', '"NETGEAR08"', '"NETGEAR37"', '"NETGEAR36"', '"Netgear91"', '"NETGEAR42"', '"NETGEAR95"', '"Sweex LW050v2"', '"NETGEAR38"', '"Netgear61"', '"NETGEAR70"', '"NETGEAR65"', '"NETGEAR79"', '"Netgear57"', '"NETGEAR97"', '"SpeedStream"', '"NETGEAR90"', '"NETGEAR86"', '"NETGEAR93"', '"NETGEAR62"', '"NETGEAR64"', '"NETGEAR82"', '"netgear76"', '"NETGEAR84"', '"NETGEAR67"', '"netgear02"', '"NETGEAR00"', '"NETGEAR49"', '"netgear83"', '"NETGEAR48"', '"NETGEAR89"', '"NETGEAR73"', '"NETGEAR78"', '"NETGEAR68"', '"NETGEAR87"', '"NETGEAR03"', '"NETGEAR96"', '"NETGEAR94"', '"NETGEAR58"', '"netgear54"', '"NETGEAR72"', '"ADSL-WIFI"', '"NETGEAR34"', '"NETGEAR59"', '"NETGEAR56"', '"netgear29"', '"NETGEAR98"', '"NETGEAR39"', '"MOBILE-EAPSIM"', '"NETGEAR14"', '"NETGEAR66"', '"NETGEAR06"', '"mycloud"', '"Dynex"', '"Courtyard_Guest"', '"FON_FREE_ssid"', '"Mywlan"', '"WirelessICC"', '"Pod"', '"Wi2"', '"ChinaNet"', '"Virgin Broadband"', '"WiFi-Repeater1"', '"kabelinternet"', '"SST-PR-1"', '"ibahn"', '"martin"', '"Maria"', '"mike"', '"FRITZ!Box 3272"', '"FRITZ!Box 6320 v2 Cable"', '"orange14"', '"7357asM"', '"HOMERUN"', '"DIR-300NRUB6"', '"myhome"', '"Matrix"', '"onlime"', '"EMINENT"', '"thuis"', '"john"', '"Oi WiFi Fon"', '"NTT-SPOT"', '"OWNER-PC_Network"', '"vizio"', '"maison"', '"0"', '"[unknown]"', '"Buffalo"', '"netis"', '"mywifi"', '"Pentagram"', '"NETGEAR-5G"', '"chris"', '"TRENDnet652"', '"Gast"', '"Apple Network"', '"Wi2_club"', '"pocwyg7swean"', '"homewifi"', '".wifisfera_telecable"', '"PT-WIFI"', '"draadloos"', '"SMITH"', '"Max"', '"Beeline_WiFi_WPA"', '"FBI Surveillance Van"', '"Guest Network"', '"FON_MTS"', '"ICIDU"', '"Michael"', '"DANIEL"', '"serviceswifi"', '"Hyatt"', '"devolo"', '"IPAD"', '"BTWi-fi"', '"UBNT"', '"anna"', '"BLUE"', '"DV201AM"', '"Auto-BTWiFi"', '"thomas"', '"Vodafone Hotspot"', '"USR5461"', '"GuestWiFi"', '"PJ-WIRELESS5"', '"MyNetwork"', '"corega"', '"WLAN-TWDC"', '"WirelessSGF"', '"Johnson"', '"Beeline_WiFi"', '"Green"', '"Guest_Access"', '"Robert"', '"alpha"', '"samsung"', '"walmartwifi"', '"laQuinta"', '"TRENDnet651"', '"@Home"', '"AirLink89300"', '"wireless1"', '"University of Washington"', '"APTG Wi-Fi"', '"HOL_ZTE_4"', '"family"', '"george"', '"doma"', '"Home Wireless"', '"james"', '"HCSC"', '"wirelessmobile"', '"c2_free"', '"WiFi-Repeater"', '"orange13"', '"??"', '"GVT"', '"@wifi.id"', '"Macysfreewifi"', '"dell_device"', '"3210 Phone WLAN SL"', '"AndroidTether"', '"ciscosb"', '"LDSAccess"', '"bob"', '"airlink59300"', '"philips"', '"SSID"', '"arris54g"', '"goesh"', '"comcast"', '"pccw"', '"Peter"', '"Boingo Hotspot"', '"WaveLAN Network"', '"SHC-RF-DS-3"', '"scandic_easy"', '"Sunshine"', '"MINE"', '"Angel"', '"HomeWireless"', '"XLNBusinessServices"', '"megahoc.v24"', '"Wireless-N"', '"Williams"', '"Paul"', '"ABC"', '"demo"', '"megahoc.v22"', '"???"', '"mark"', '"DSL-2640U"', '".FREE_Wi-Fi_PASSPORT"', '"Anygate"', '"Domek"', '"Print Server"', '"NESPOT"', '"kt_wlan"', '"nomad5"', '"DM-HHT"', '".@ TRUEWIFI"', '"wireless2"', '"Sam"', '"Free Internet Access"', '"docomo_eap_roaming"', '"MyNet"', '"FDS020"', '"linksys1"', '"Link"', '"IWIFI"', '"GlobalSuiteWireless"', '"homebase"', '"Wi-Fi Arnet"', '"vpnator"', '"PrettyFlyForAWiFi"', '"INTERMEC"', '"5ECUR3w3p5TOR3"', '"AP"', '"CORP"', '"steve"', '"Charlie"', '"MO1975"', '"CyfrowyPolsat"', '"scout"', '"HomeSweetHome"', '"Marina"', '"ASUS_Guest1"', '"KEVIN"', '"myTouch 4G Hotspot"', '"LWL-M"', '"jones"', '"redwood"', '"brown"', '"ResidenceInn_GUEST"', '"ATT128"', '"MO1875"', '"USER-PC_Network"', '"Orcon-Wireless"', '"ATT144"', '"ATT688"', '"ATT032"', '"ATT768"', '"ATT472"', '"ATT024"', '"FRITZ!Box Fon WLAN"', '"ATT504"', '"ATT424"', '"ATT256"', '"ATT320"', '"ATT240"', '"P874"', '"ATT056"', '"ATT336"', '"ATT216"', '"ATT968"', '"ATT544"', '"FREE_U+zone"', '"ATT624"', '"ATT936"', '"ATT200"', '"ATT248"', '"ATT464"', '"ATT880"', '"ATT888"', '"Miller"', '"ATT304"', '"ATT800"', '"ATT344"', '"ATT560"', '"ATT176"', '"ATT584"', '"ATT824"', '"ATT400"', '"ATT392"', '"ATT088"', '"ATT136"', '"ATT432"', '"ATT104"', '"att728"', '"ATT480"', '"ATT280"', '"att296"', '"ATT120"', '"ATT080"', '"Fullrate"', '"att328"', '"ATT648"', '"beeline-router"', '"ATT856"', '"ATT760"', '"ATT912"', '"ATT488"', '"ATT976"', '"ATT840"', '"ATT744"', '"ATT960"', '"ATT952"', '"wilson"', '"ATT784"', '"ATT096"', '"ATT288"', '"ATT408"', '"ATT008"', '"ATT696"', '"ATT416"', '"ATT440"', '"Motel 6"', '"ATT192"', '"ATT384"', '"ATT928"', '"ATT456"', '"ATT072"', '"ATT048"', '"VIVACOM_NET"', '"att112"', '"ATT672"', '"home2"', '"ATT664"', '"yrneh09"', '"ATT552"', '"ZyXEL_ABGN_1"', '"ATT808"', '"ATT576"', '"ATT712"', '"ATT232"', '"ATT896"', '"att360"', '"ATT512"', '"ATT720"', '"ATT520"', '"ATT992"', '"ATT656"', '"ATT496"', '"ATT904"', '"ATT224"', '"ATT792"', '"ATT680"', '"ATT616"', '"ATT864"', '"ATT448"', '"ATT920"', '"ATT872"', '"ATT376"', '"ATT600"', '"ATT208"', '"ATT816"', '"ATT592"', '"ATT160"', '"DOVADO"', '"ATT832"', '"ATT640"', '"ATT536"', '"ATT016"', '"ATT184"', '"ATT776"', '"ATT272"', '"ATT264"', '"ATT064"', '"ATT752"', '"ATT528"', '"ATT944"', '"ATT848"', '"ATT352"', '"ATT632"', '"ATT736"', '"ATT608"', '"FRITZ!Box 3390"', '"ATT168"', '"ATT152"', '"ATT000"', '"scott"', '"ATT984"', '"ATT312"', '"SHC-RF-DS-Vendor"', '"ATT368"', '"MIT"', '"ATT568"', '"ATT704"', '"ATT040"', '"megahoc.v29"', '"NETGEAR2"', '"XLNTelecom"', '"????"', '"laura"', '"BeBox"', '"ArcorWirelessLAN"', '"Frank"', '"TDPJ"', '"WLI"', '"mprotek"', '"BLIZZARD"', '"unknown"', '"repeater"', '"lee"', '"XFINITY"', '"Guests"', '"PCCW1x"', '"yournetworkname"', '"vendcust"', '"Linda"', '"elena"', '"CSL"', '"fritz"', '"richard"', '"123"', '"GIGABYTE"', '"WIS"', '"Panasonic Display1"', '"OutOfService"', '"1234"', '"wlan1"', '"asu"', '"RGIS"', '"Inet"', '"HTC network"', '"jason"', '"Tony"', '"Carlos"', '"DATA"', '"cWiFi"', '"Google Starbucks"', '"jack"', '"FRITZ!Box"', '"Untitled"', '"TPLINK"', '"olga"', '"ChinaUnicom"', '"Linksys2"', '"IBM"', '"homerun1x"', '"LISA"', '"SMARTSIGHT"', '"King"', '"str241xvce"', '"taylor"', '"Hotel"', '"BYOD"', '"tom"', '"NetCore"', '"ethostream"', '"vodafone"', '"anderson"', '"p2pkoer"', '"188"', '"dd-wrt_vap"', '"G604T_WIRELESS"', '"MSI"', '"fred"', '"mary"', '"Siemenswlan"', '"RegusNETWiFi"', '"mywireless"', '"WEST"', '"HG520b"', '"sandra"', '"jackson"', '"asu guest"', '"SHC-RF-ID-2"', '"andy"', '"dlink1"', '"Tiger"', '"speedywifi"', '"zuhause"', '"AMD_IBSS"', '"SMCWBR14S-N4_AP"', '"Bella"', '"Adam"', '"arq_wifi"', '"sweethome"', '"Universities via PCCW"', '"NETGEAR-DualBand-N"', '"FRITZ!Box o2 DSL"', '"D35Broadband"', '"DIRECT-xyPhilips TV"', '"quality"', '"Edimax AP"', '"DLinkVWR"', '"corporate"', '"Fibertel WiFi"', '"ONTelecoms"', '"ICT free WIFI by TRUE"', '"Employee"', '"AirPort Extreme"', '"Kelly"', '"Tele2-2"', '"eBOS"', '"secure"', '"Fairfield_Guest"', '"BATCAVE"', '"HG520s"', '"meijer-corp"', '"GoogleGuest"', '"AirLink29150"', '"msftwlan"', '"hp"', '"IU SECURE"', '"davis"', '"timewarnercablewifi"', '"GoldenTree"', '"FBI"', '"verizon"', '"AlwaysOn"', '"brian"', '"QEBHW"', '"subway"', '"Enterprise"', '"eduSTAR"', '"Michelle"', '"wirelesslan"', '"studio"', '"rose"', '"FritzBox"', '"m3connect"', '"CSL Auto Connect"', '"BESTBUY"', '"Andrea"', '"0000FLETS-SPOT"', '"RED"', '"@TRUEWIFI"', '"tele2-1"', '"GuestAccess"', '"simon"', '"Netgear123"', '"Home WiFi"', '"PHOENIX"', '"GABLE"', '"sarah"', '"Joe"', '"1"', '"0000FLETS-PORTAL"', '"Engenius1"', '"BBUser"', '"orion"', '"Oscar"', '"DG1670A02"', '"upstairs"', '"TalkTalk520"','"Leo"', '"ShawGuest"', '"Julia"', '"Medialink"', '"Kim"', '"PLDTMyDSL"', '"IVAN"', '"paris"', '"Broadcom"', '"20dealer08"', '"dave"', '"FDS210"', '"google"', '"Pretty Fly for a Wi-Fi"', '"Andrew"', '"monkey"', '"Ikea WiFi"', '"jessica"', '"Apple Store"', '"AMX"', '"Eric"', '"megahoc.v25"', '"sasha"', '"Diana"', '"Red5"', '"mario"', '"planexuser-wps"', '"Mac"', '"Intellinet"', '"0001_Secured_Wi-Fi"', '"detnsw"', '"karen"', '"RYAN"', '"swaaa"', '"DSL-2640R"', '"ZIO"', '"rjjrjg14"', '"VICTOR"', '"Nordstrom_Wi-Fi"', '"Harvard University"', '"p27x1c2"', '"DRAGON"', '"privat"', '"My ASUS"', '"SSID1"', '"TitWpA23VfS"', '"TitLeP22VfS"', '"DGC"', '"Irina"', '".@ truemoveH"', '"TG1672GD2"', '"holidayinn"', '"TG1672G62"', '"Speedy"', '"fanTM"', '"ask4 Wireless"', '"TG1672G12"', '"TG1672G92"', '"Y5ZONE"', '"TG1672GF2"', '"TG1672G32"', '"TG1672G02"', '"CONNX"', '"TG1672G82"', '"prn"', '"TG1672GE2"', '"TG1672GB2"', '"TG1672GA2"', '"TG1672G22"', '"TG1672G52"', '"TG1672GC2"', '"Wireless@SG"', '"tardis"', '"TG1672G72"', '"a"', '"INTELBRAS"', '"TG1672G42"', '"Renaissance_GUEST"', '"lucky"', '"uofm"', '"PANAREA"', '"meins"', '"freedom"', '"xxx"', '"local"', '"Alice"', '"MM"', '"pi07490509x09"', '"topcom"', '"eo"', '"thompson"', '"cobra"', '"kubi"', '"FRITZ!WLAN REPEATER N/G"', '"nelson"', '"BATMAN"', '"patrick"', '"innflux"', '"unicorn"', '"WORKGROUP"', '"conference"', '"megahoc"', '"SCN"', '"BAILEY"', '"2WIRE631"', '"jeff"', '"My Place"', '"pi07490509x"', '"beltelecom"', '"Amped_SR"', '"Telenor"', '"Shadow"', '"Garcia"', '"PCCW Free"', '"LevelOne"', '"nick"', '"Belkin_G_Wireless_"', '"jennifer"', '"AP1"', '"DRI_vista"', '"apollo"', '"students"', '"princess"', '"OSUWIRELESS"', '"BETA"', '"luna"', '"jose"', '"Time Capsule"', '"mobilepoint"', '"MU-Wireless"', '"meijer-vendor"','"AUS Free WiFi"']
count=0
print (blue("Your MAC Autoconnects To Following Wireless Networks:"))
os.system("networksetup -listpreferredwirelessnetworks en0")	
print "\n"
print (blue("Removing Common SSIDS. This Could Take A While."))
for ssid in ssids: 
	os.system("networksetup -removepreferredwirelessnetwork en0 %s" % (ssid) )
	count += 1
print "\n"
print (blue("Removed %s Common SSIDs from your system." % count))
print "\n"
print (blue("Your MAC Now Autoconnects To Following Wireless Networks:"))
os.system("networksetup -listpreferredwirelessnetworks en0")	
