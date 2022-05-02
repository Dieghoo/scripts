#!/usr/bin/python3
import sys
import subprocess
import os
from subprocess import run

path = "<your_path_here>"
os.chdir(path)

alvo = sys.argv[1]

# USING BBRF SCOPE AS ARGV[1]
useSCOPE = "bbrf use {0}".format(alvo)
os.system(useSCOPE)


# EXCLUDING OLD
excluirOLD = "rm -r {0} &".format(alvo)
os.system(excluirOLD)
mkdirAlvo = "mkdir /your/path/{0}".format(
    alvo)
os.system(mkdirAlvo)
cdAlvo = "/your/path/{0}".format(alvo)
os.chdir(cdAlvo)


# -> DOING RECON [Pt1 == OK!]
print("\n---> Extracting with ASSETFINDER...")
comandoAssetfinder = "bbrf scope in --wildcard | assetfinder -subs-only | anew assetfinder_{0}".format(
    alvo)
os.system(comandoAssetfinder)
print("\n---> Extracting with SUBFINDER...")
comandoSubfinder = "bbrf scope in --wildcard | subfinder -silent | anew subfinder_{0}".format(
    alvo)
os.system(comandoSubfinder)
print("\n---> Extracting with CHAOS...")
comandoChaos = "bbrf scope in --wildcard | chaos | anew chaos_{0}".format(
    alvo)
os.system(comandoChaos)
# END [Pt1]
# CREATING SCOPE FILE FOR XARGS
comandoESCOPO = "bbrf scope in --wildcard | anew escopo_{0}".format(
    alvo)
os.system(comandoESCOPO)
# FILE CREATED


# -> DOING RECON [Pt2 == OK!]
# EXTRACTING WITH GITHUB == OK
print("\n---> Extracting with GITHUB-SUBDOMAINS...")
comandoGithub = "xargs -a escopo_{0} -I@ bash -c 'github-subdomains.py -t <Your_Token_Here> -d @ | anew github_{1}'".format(
    alvo, alvo)
os.system(comandoGithub)
# END GITHUB
# EXTRACTING WITH CRT.SH == OK
print("\n---> Extracting with CRT.SH...")
comandoCrtsh = "xargs -a escopo_{0} -I@ bash -c 'curl -s \"https://crt.sh/?q=%25.@&output=json\" | jq -r '.[].name_value' | sed 's/\*\.//g' | anew crtSH_{1}\'".format(
    alvo, alvo)
os.system(comandoCrtsh)
# END CRT.SH
# EXTRACTING WITH FINDOMAIN == OK
print("\n---> Extracting with FINDOMAIN...")
comandoFindomain = "xargs -a escopo_{0} -I@ bash -c 'findomain-linux -t @ -q | anew findomain_{1}'".format(
    alvo, alvo)
os.system(comandoFindomain)


# END FINDOMAIN
# EXTRACTING WITH AMASS
print("\n---> Extracting with AMASS...")
comandoAMASS = "xargs -a escopo_{0} -I@ bash -c 'amass enum -d @ -o amass_{1}\'".format(
    alvo, alvo)
os.system(comandoAMASS)
# END AMASS
# END [Pt2]


# CONCATENATING RESULTS
print("\n___Concatenating results___")
os.system("cat * | anew subs_01")
# END CONCATENATING RESULTS


# # RESOLVING SUBDOMAINS [200,403,404]
os.system("clear")
comandoHTTPX = ("cat subs_01 | httpx -silent -mc 200,403,404 | anew httpResolved_1")
os.system(comandoHTTPX)
comandoSubs200 = "cat httpResolved_1 | cut -d \"/\" -f 3 | anew subResolved_1"
os.system(comandoSubs200)

# # # RECON OF RECON
# # REMOVE OLD FILES
# ASSETFINDER XARGS == OK
removeAssetfinder = "rm assetfinder_{0}".format(alvo)
os.system(removeAssetfinder)
xargsAssetfinder = "xargs -a subResolved_1 -I@ bash -c 'assetfinder -subs-only @ | anew assetfinder_{0}'".format(alvo)
os.system(xargsAssetfinder)

# SUBFINDER XARGS == OK
removeSubfinder = "rm subfinder_{0}".format(alvo)
os.system(removeSubfinder)
xargsSubfinder = "xargs -a subResolved_1 -I@ bash -c 'subfinder -d @ -silent | anew subfinder_{0}'".format(alvo)
os.system(xargsSubfinder)

# # GITHUB XARGS
print("\n---> Extracting with GITHUB-SUBDOMAINS")
removeGithub = "rm github_{0}".format(alvo)
os.system(removeGithub)
xargsGithub = "xargs -a subResolved_1 -I@ bash -c 'github-subdomains.py -t <Your_Token_Here> -d @ | anew github_{0}'".format(alvo)
os.system(xargsGithub)
# # END GITHUB XARGS

# # CRT.SH XARGS
print("\n---> Extracting with CRT.SH")
removeCRTSH = "rm crtSH_{0}".format(
    alvo)
os.system(removeCRTSH)
xargsCRTSH = "xargs -a subResolved_1 -I@ bash -c 'curl -s \"https://crt.sh/?q=%25.@&output=json\" | jq -r '.[].name_value' | sed 's/\*\.//g' | anew crtSH_{0}\'".format(alvo)
os.system(xargsCRTSH)
# # END CRT.SH XARGS

# # FINDOMAIN XARGS
print("\n---> Extracting with FINDOMAIN")
removeFindomain = "rm findomain_{0}".format(alvo)
os.system(removeFindomain)
xargsFindomain = "xargs -a subResolved_1 -I@ bash -c 'findomain-linux -t @ -q | anew findomain_{0}'".format(alvo)
os.system(xargsFindomain)
# # END FINDOMAIN XARGS

# # AMASS XARGS
print("\n---> Extracting withAMASS")
removeAMASS = "rm amass_{0}".format(
    alvo)
os.system(removeAMASS)
xargsAMASS = "xargs -a subResolved_1 -I@ bash -c 'amass enum -d @ -o amass_{0}'".format(alvo)
os.system(xargsAMASS)
# # END AMASS XARGS

# # CONCATENATING RECON OF RECON
print("___Concatenando resultados___")
concatenar_recon_recon = "cat amass_{0} findomain_{1} crtSH_{2} github_{3} chaos_{4} subfinder_{5} assetfinder_{6} | anew subFINAL".format(alvo, alvo, alvo, alvo, alvo, alvo, alvo)
os.system(concatenar_recon_recon)
# # END CONCAT REC REC

# # RESOLVING SUBDOMAINS
os.system("clear")
print("\n***RESOLVING SUBDOMAINS 200,403,404***")

httpx_recon_recon = "cat subFINAL | httpx -silent -mc 200 | anew http200"
os.system(httpx_recon_recon)
httpx_recon_recon403 = "cat subFINAL | httpx -silent -mc 403 | anew http403"
os.system(httpx_recon_recon403)
httpx_recon_recon404 = "cat subFINAL | httpx -silent -mc 404 | anew http404"
os.system(httpx_recon_recon404)

sub200_recon_recon = "cat http200 | cut -d \"/\" -f 3 | anew sub200"
os.system(sub200_recon_recon)

os.system("rm httpResolved_1")
os.system("rm escopo_*")
os.system("rm subResolved_1")
os.system("rm subs_01")
os.system("rm assetfinder_*")
os.system("rm subfinder_*")
os.system("rm chaos_*")
os.system("rm github_*")
os.system("rm crtSH_*")
os.system("rm amass_*")
os.system("rm findomain_*")

os.system("echo \"[SUBDOMAIN ENUMERATION ==> OK!!]\" | notify")
