from PyPaperBot.pbot import pbot
from os import system , path
from chemdataextractor import Document
from cd_lib.chose_para import cde_paras
from csv import reader
from gooey import Gooey, GooeyParser

with open('log.txt','w') as f:
    f.write("temp")
try:
    # pass
    Document.from_file('log.txt')
except:
    system("Cde data download")

def syndwn(query:str,results,pages:str,diri,yer,numlmt,tp,restrict,url):
    print("Execution Started!")
    pbot(query,pages,scholar_results=results,restrict=restrict,dwn_dir=diri,min_date=yer,num_limit=numlmt,num_limit_type=tp,SciHub_URL=url)
    with open(path.join(diri,"result.csv"),'r',encoding='utf-8')as f:
        cfile=reader(f)
        count=1
        for i in cfile:
            fname=i[4].split(".")[0]
            if fname !="PDF Name" and fname:
                item_html_cde = Document.from_file(path.join(diri,fname+'.pdf'))
                item = cde_paras(item_html_cde)

                if item.sny_sele():

                    sny_para_list = item.sny_para_str()
                    pot_sny_para_no = 0

                    print(f'We find {len(sny_para_list)} synthesis paragraph(s), which is (are):')
                    while pot_sny_para_no < len(sny_para_list):
                        print(f'{pot_sny_para_no+1})')
                        print(f'{sny_para_list[pot_sny_para_no]})'.encode("utf-8"))
                        with open(path.join(diri,'synthesis.txt'), 'a',encoding='utf-8') as f:
                            f.write(fname+"\n"+str(count)+") "+sny_para_list[pot_sny_para_no]+"\n\n")
                        with open(path.join(diri,fname + '.txt'), 'a',encoding='utf-8') as f:
                            f.write(str(pot_sny_para_no + 1)+") "+sny_para_list[pot_sny_para_no])
                            f.write("\n\n")
                        pot_sny_para_no += 1
                        count+=1
                        print()

@Gooey
def main():

    parser =GooeyParser(description='This is python tool to search, dwonload scientific papers and extract MOF synthesis paras from it, build using PyPaperBot and Tsotsalas-Group/MOF_Literature_Extraction ')
    parser.add_argument('Search', type=str, default=None, help='Query to make on Google Scholar or Google Scholar page link',gooey_options={'full_width':True})
    parser.add_argument('download_dir', type=str,default="/" ,help='Directory path in which to save the results',widget="DirChooser")
    # parser.add_argument('--doi', type=str, default=None, help='DOI of the paper to download (this option uses only SciHub to download)')
    # parser.add_argument('--doi-file', type=str, default=None, help='File .txt containing the list of paper\'s DOIs to download')
    parser.add_argument('--scholar_pages', default=1,type=int, help='Number of scholar pages to search, Each page has a maximum of 10 papers',widget="IntegerField",gooey_options={'min':1})
    parser.add_argument('--scholar_results', default=10, type=int, choices=[1,2,3,4,5,6,7,8,9,10], help='Downloads the first x results for each scholar page(default/max=10)',widget="IntegerField",gooey_options={'min':1,'max':10})
    parser.add_argument('--min-year', default=None, type=int, help='Minimal publication year of the paper to download')
    parser.add_argument('--max-dwn-year', default=None, type=int, help='Maximum number of papers to download sorted by year')
    parser.add_argument('--max-dwn-cites', default=None, type=int, help='Maximum number of papers to download sorted by number of citations')
    # parser.add_argument('--journal-filter', default=None, type=str ,help='CSV file path of the journal filter (More info on github)')
    parser.add_argument('--restrict', default=1, type=int ,choices=[0,1], help='0:Download only Bibtex - 1:Down load only papers PDF')
    parser.add_argument('--scihub-mirror', default=None, type=str, help='Mirror for downloading papers from sci-hub. If not set, it is selected automatically')
    # parser.add_argument('--proxy', nargs='+', default=[], help='Use proxychains, provide a seperated list of proxies to use.Please specify the argument al the end')
    args = parser.parse_args()
 
    max_dwn = None
    max_dwn_type = None
    if args.max_dwn_year != None:
        max_dwn = args.max_dwn_year
        max_dwn_type = 0
    if args.max_dwn_cites != None:
        max_dwn = args.max_dwn_cites
        max_dwn_type = 1
    syndwn(args.Search, args.scholar_results, str(args.scholar_pages), args.download_dir, args.min_year , max_dwn, max_dwn_type ,  args.restrict, args.scihub_mirror)


# syndwn("metal organic frameworks bismuth tdc",diri="./pdf",)
main()