import re 
import urllib2
#from HTMLParser import HTMLParser


from bs4 import BeautifulSoup as Soup
#from BeautifulSoup import BeautifulSoup as Soup
#from soupselect import select


from time import gmtime, strftime

from pyquery import PyQuery as pq 
from lxml import etree

def crawl( q ):
	
	#url ="http://tw.dictionary.search.yahoo.com/search?p=%s" % ( q )
	url ="http://tw.dictionary.yahoo.com/dictionary?p=%s" % q 
	print url
	page = urllib2.urlopen( url )
	#return page 
	return page.read()  


def parse_test( page ):
	query_reg = "<span class=\"yschttl\"[^>]*>([^<]+)</span>"
	tmp_query_re = re.findall( query_reg, page ) 
	if( len( tmp_query_re ) == 0):
		return ("null",["not found" ])
	query = tmp_query_re[0]

def parse( page ):
	page = page.decode("utf8")
	d = pq( page ) 
	#query_tmp = d(".title_term .yschttl")
	query_tmp = d(".summary h2")
	if len( query_tmp) == 0:
		return( None, [] )
	query = query_tmp.text()

	#kk_proun = d(".proun_wrapper .proun_value") 
	kk_proun = d(".pronun dd") 
	proun = kk_proun.eq(0).text()

	ret_explains = [] 
	
#	for exp_html in d(".result_cluster_first ul.explanation_wrapper li.explanation_pos_wrapper"):
	for exp_html in d("ul.explanations li.type-item"):	 
		exp = pq( exp_html ) 
#		if len( exp(".pos_abbr") ) > 0:
		if len( exp("div.type") ) > 0:
			pos = exp("div.type").text() 
			
		else:
			pos = ""
		
		#exp_text = "; ".join( [ pq(exp_line).text() for exp_line in exp("ol.explanation_ol li") ] )
		exp_text = "; ".join( [ pq(exp_line).text() for exp_line in exp("ol.exp-list li.exp-item") ] )
		
		ret_explains.append( "%s   %s"%( pos, exp_text ) ) 
	return ( "%s\n%s" %( query, proun ) , ret_explains )

def parse_old( page  ):
	soup = Soup( page )
	query_tmp_soup_list = soup.select( ".title_term .yschttl")
	#query_tmp_soup_list = soup.select( ".yschttl" )
	print query_tmp_soup_list 
	if len( query_tmp_soup_list ) == 0:
		return ("null",["not found" ])

	query = soup.select( ".title_term .yschttl")[0].get_text() 
	
	kk_proun  = soup.select(".proun_wrapper .proun_value") 
	if len( kk_proun ) > 0 :
		proun = kk_proun[0].get_text() 
	else:
		proun = ""

	ret_explains = []
	for exp in soup.select( ".result_cluster_first  ul.explanation_wrapper li.explanation_pos_wrapper"):
		if len( exp.select(".pos_abbr") )>0: 
			pos =  exp.select(".pos_abbr")[0].get_text()
		else:
			pos = " "
		exp_text =  "; ".join( [ exp_line.get_text() for exp_line in exp.select("ol.explanation_ol li")  ] )
		ret_explains.append( "%s    %s"%( pos, exp_text )) 

	return  ("%s %s" %  ( query, proun ) , ret_explains )
		#print exp.get_text()
	#exp = soup.select( "ul.explanation_wrapper")[0].get_text()
	#print exp

	#word_reg = '<span class="yschttl"[^>]*>([^<]+)</span>'
	#tmp = re.search( word_reg , page )
	#q = tmp.group(1) 
	#print q 



def main( out_dir ):
	#parser = MyHTMLParser()
	time_str = strftime("%m-%d-%H-%M-%S", gmtime())
	outf = open( "%s/%s.csv" % ( out_dir, time_str ) , "w")

	while True: 
		try:
			q = raw_input("Q: ")
			page  = crawl( q )
			query , explains  = parse( page )
			if query == None:
				print "Not found %s" % q 
				continue 
			aggregate_text = "\"%s\",\"%s\""%( query, ("\n".join( explains)).replace('"',"'") ) 
			print aggregate_text 
			isAdd= raw_input("add? [y/n]")
			if ( isAdd == "y" or isAdd.strip() =="" ):
				print >> outf, aggregate_text.encode("utf8","ignore")
				print "Add [%s]" % q 
		except KeyboardInterrupt: 
			outf.close()
			break


main("data/")
