import requests
import json
import pysolr
import time

class IndexSearch:
    def __init__(self,ip,port):
        self.params = {"boost":1.0,"overwrite":"true","commitwhin":10000}
        self.post_url = 'http://{ip}:{port}/solr/TechDaily/'.format(ip = ip,port = port)
        self.headers = {"Content-Type":"application/json"}
        self.session = requests.session()
        self.url = 'http://10.144.5.127/external_data_access/'
        login_url = 'http://10.144.5.127/account/login/'
        payload = {
            'username': 'TechDailyGroup',
            'password': 'curidemo'
        }
        response = self.session.post(login_url, json.dumps(payload))

    def read_data(self,datasource,params):
        data_url = self.url + datasource
        while True:
            try:
                response = self.session.get(data_url,params = params)
                break
            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 60 seconds')
                time.sleep(60)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 60 seconds')
                time.sleep(60)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 60 seconds')
                time.sleep(60)
        return response

    def index_data_to_solr(self,data):
        solr = pysolr.Solr(self.post_url, timeout=10)
        # How you'd index data.
        try:
            result = solr.add(data)
        except Exception as e:
            print(e)
            pass

    def search_from_solr(self,url):
        r = requests.get(url,verify = False)
        print(r.json())
        r = r.json()['response']['numFound']
        print(r)

    def index_articles_to_solr(self):
        while True:
            response = self.read_data('not_indexed_articles', {'engine': 'solr'})
            contents = response.json()['data']
            if len(contents) != 0:
                self.index_data_to_solr(contents)
                print('ok')
            else:
                time.sleep(60*30)
                print('There is no new data -- please wait 30 minute.')


class FuncInterface:
    def __init__(self,ip,port):
        self.solr_url = "http://{ip}:{port}/solr/TechDaily".format(ip = ip,port = port)
        response = requests.get('http://{ip}:{port}/solr/TechDaily/suggest?spellcheck.build=true'.format(ip = ip,port = port))

    #返回一个list：文章id
    def query(self,word,page,rows=10):
        query = '/select?fl=id&q={q}&start={start}&rows={rows}&sort=publish_time desc&wt=json'.format(q=word,start=page*10,rows=rows)
        print(self.solr_url+query)
        response = requests.get(self.solr_url+query,verify = False)
        response = response.json()['response']['docs']
        id_list = []
        for i in response:
            id_list.append(i['id'])
        return id_list

    # 返回一个list：推荐短语
    def suggest(self,word,count = 10):
        query = '/suggest?q={q}&spellcheck.count={count}&wt=json'.format(q=word,count=count)
        response = requests.get(self.solr_url+query,verify = False)
        suggestion = response.json()['spellcheck']['suggestions'][1]['suggestion']
        return suggestion

    # 返回一个list：文章id
    def morelikethis(self,id,count=10):
        query = '/select?df=id&mlt=true&mlt.fl=text&mlt.count={count}&q={id}&sort=publish_time desc&wt=json'.format(count=count,id=id)
        print(self.solr_url+query)
        response = requests.get(self.solr_url+query)
        response = response.json()['moreLikeThis'][id]['docs']
        id_list = []
        for i in response:
            id_list.append(i['id'])
        print(id_list)
        return id_list


if __name__ == '__main__':
    # index_search = IndexSearch('10.144.5.124',8983)
    # index_search.index_articles_to_solr()
    solr_func = FuncInterface('10.144.5.124',8983)
    ids = solr_func.query('区块链 比特币',1)
    print(ids)
    # sug = solr_func.suggest('区块')
    # print(sug)
    # ids = solr_func.morelikethis('138649')
