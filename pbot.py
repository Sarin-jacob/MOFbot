from .Paper import Paper
from .PapersFilters import filterJurnals, filter_min_date, similarStrings
from .Downloader import downloadPapers
from .Scholar import ScholarPapersInfo
from .Crossref import getPapersInfoFromDOIs
from .proxy import proxy
from os import path
proxy([])
def pbot(query, scholar_pages,scholar_results=10,  proxy=proxy, dwn_dir='./', min_date=None, num_limit=None, num_limit_type=None, filter_jurnal_file=None, restrict=None, DOIs=None, SciHub_URL=None):

    split = scholar_pages.split('-')
    if len(split) == 1:
        scholar_pages = range(1, int(split[0]) + 1)
    elif len(split) == 2:
        start_page, end_page = [int(x) for x in split]
        scholar_pages = range(start_page, end_page + 1)

    to_download = []
    if DOIs==None:
        print("Query: {}".format(query))
        to_download = ScholarPapersInfo(query, scholar_pages, restrict, min_date, scholar_results)
    else:
        print("Downloading papers from DOIs\n")
        num = 1
        i = 0
        while i<len(DOIs):
            DOI = DOIs[i]
            print("Searching paper {} of {} with DOI {}".format(num,len(DOIs),DOI))
            papersInfo = getPapersInfoFromDOIs(DOI, restrict)
            to_download.append(papersInfo)

            num += 1
            i +=  1


    if restrict!=0 and to_download:
        if filter_jurnal_file!=None:
           to_download = filterJurnals(to_download,filter_jurnal_file)

        if min_date!=None:
            to_download = filter_min_date(to_download,min_date)

        if num_limit_type!=None and num_limit_type==0:
            to_download.sort(key=lambda x: int(x.year) if x.year!=None else 0, reverse=True)

        if num_limit_type!=None and num_limit_type==1:
            to_download.sort(key=lambda x: int(x.cites_num) if x.cites_num!=None else 0, reverse=True)

        downloadPapers(to_download, dwn_dir, num_limit, SciHub_URL)


    Paper.generateReport(to_download,path.join(dwn_dir,"result.csv"))
    Paper.generateBibtex(to_download,path.join(dwn_dir,"bibtex.bib"))
