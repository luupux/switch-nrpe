#!/usr/bin/python -t
from optparse import OptionParser
import string
import commands
import re
import sys

__author__="Mauro Ferrigno"
BASECOMMAND="/usr/lib/nagios/plugins/check_nrpe"




class nrpecmd:
	def __init__(self,fhost,fcmd,fargs,fhop):
		self.fhost=" -H "+fhost
		self.fhop=" -H "+fhop
		self.fcmd=" -c "+ fcmd
		self.fargs = fargs
		if  fargs:
			self.fargs = " -a "+fargs

	def nrpe_simple(self):
		command=self.fhost+" "+self.fcmd+" "+self.fargs
		return command

	def nrpe_hop(self):
		command=self.fhop+" -c check_nrpe -a '"+self.nrpe_simple()+"'"
		return command


class parseinput:
	def __init__(self,options=None,args=None):
		parser = OptionParser()
		parser.add_option("--fhop",dest="fhop",default="None",help="Ip o Hostname per hop check")
		parser.add_option("--fhost",dest="fhost",nargs=1,default="None",help="Ip o Hostname su cui eseguire i check")
		parser.add_option("--fcmd",dest="fcmd",nargs=1,default="None",help="Ip o Hostname su cui eseguire i check")
		(options, args) = parser.parse_args()
		self.options=options
		self.args=args
		options.fargs=' '.join(args)
		self.fargs = options.fargs

		if len(sys.argv)==1:
			parser.error("-h for help")

		if options.fhost == "None":
			parser.error("options --fhost not found")

		if options.fcmd == "None":
			parser.error("options --fcmd not found")



### DA SISTEMARE GESTIONE MESSAGGI PER FUNZIONE STATUSCODE
def excmd(BASECOMMAND,fcommand):
	endcmd=BASECOMMAND+" "+fcommand
	print endcmd
	comdc=commands.getstatusoutput(endcmd)
	rescmd = comdc[1].replace('(','').replace(')','')
	print rescmd
	sys.exit(statuscode(rescmd))

def statuscode(checkval):
	if re.match(r'^.*OK',checkval,re.IGNORECASE):
		return 0
	elif re.match(r'^.*WARNING',checkval,re.IGNORECASE):
		return 1
	elif re.match(r'^.*CRITICAL',checkval,re.IGNORECASE):
		return 2
	else:
		return 3

def main():
	pi=parseinput()
	nrpe=nrpecmd(pi.options.fhost,pi.options.fcmd,pi.options.fargs,pi.options.fhop)
	print pi.options.fhop
	if  pi.options.fhop != "None":
		print "NRPE HOP"
		fcommand = nrpe.nrpe_hop()
#		print fcommand
		excmd(BASECOMMAND,fcommand)
			
	else:
		print "NRPE DIRECT"
		fcommand = nrpe.nrpe_simple()
#		print fcommand
		excmd(BASECOMMAND,fcommand)


if __name__=="__main__":
	main()





	
