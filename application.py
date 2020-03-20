# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:20:46 2020

@author: Aishwarya
"""

from flask import Flask, request, jsonify, make_response,json,send_from_directory
from newsapi import NewsApiClient
import re
from collections import Counter
from newsapi.newsapi_exception import NewsAPIException

application = Flask(__name__)
newsapi = NewsApiClient(api_key = 'bef3eb6a79b3419fa86cf190efab817f')

# =============================================================================
# #test
# @app.route('/')
# @app.route('/test')
# def fetch_all_articles():
#     all_articles=newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)
#     return jsonify(all_articles)
# 
# =============================================================================


@application.route('/<path:path>')
def send_file(path):
    return send_from_directory('static',path)

@application.route('/')
def index():
    application.send_static_file('front.css');
    return application.send_static_file('frontend.html')



#Top 5 Headlines from Google News
@application.route('/home/headlines')
def fetch_top_headlines():
    #print ("hi")
    top_headlines = newsapi.get_top_headlines(language='en',page_size=30)
    #print (len(top_headlines['articles']))
    top_headlines=json.dumps(top_headlines)
    #print (type(top_headlines))
    top_headlines=json.loads(top_headlines)
    #print (type(top_headlines))
    articles=top_headlines['articles']
    print (len(articles))
    count=0
    filtered_articles=[]
    
    for i in articles:
        if count==5:
            break
        # for a in i.items():
        #     print(a)
        flag=0
        if ("author" in i) and ("content" in i) and ("description" in i) and ("publishedAt" in i) and ("source" in i)and ("title" in i) and ("url" in i) and ("urlToImage" in i):
            for val1 in i.values():
                if not val1:
                    flag=1
                    break
            if flag==1:
                continue
            if ("id" in i["source"]) and ("name" in i["source"]):
                for val2 in i["source"].values():
                    if not val2:
                        flag=1
                        break
            if flag==1:
                continue
            count+=1
            filtered_articles.append(i)
        
                
    top_headlines['articles']=filtered_articles
    #top_headlines=json.dumps(top_headlines,indent=4)
    top_headlines = jsonify(top_headlines)
    #print (top_headlines)
    return top_headlines



#Top Headlines from CNN or Fox News
@application.route('/home/<news_source>')
def top_news(news_source):
    news_headlines=newsapi.get_top_headlines(sources=news_source,language='en',page_size=30)
    news_headlines=json.dumps(news_headlines)
    #print (type(top_headlines))
    news_headlines=json.loads(news_headlines)
    #print (type(top_headlines))
    articles=news_headlines['articles']
    
    
    count=0
    filtered_articles=[]
    
    for i in articles:
        if count==4:
            break
        # for a in i.items():
        #     print(a)
        flag=0
        if ("author" in i) and ("content" in i) and ("description" in i) and ("publishedAt" in i) and ("source" in i)and ("title" in i) and ("url" in i) and ("urlToImage" in i):
            for val1 in i.values():
                if not val1:
                    flag=1
                    break
            if flag==1:
                continue
            if ("id" in i["source"]) and ("name" in i["source"]):
                for val2 in i["source"].values():
                    if not val2:
                        flag=1
                        break
            if flag==1:
                continue
            count+=1
            filtered_articles.append(i)
        
                
    news_headlines['articles']=filtered_articles
    #top_headlines=json.dumps(top_headlines,indent=4)
    news_headlines = jsonify(news_headlines)
    print (news_headlines)
    return news_headlines
    
    #return jsonify(news_headlines)


#Sources for a given category
@application.route('/home/search/source')
def get_sources():
    category_name = request.args.get("category_name")
    sources=newsapi.get_sources(category=category_name, language='en',
                                country='us')
    top_sources=sources["sources"]
    return jsonify(top_sources[:10])
    
    


#Search Results
@application.route('/home/search')
def news_search_results():
    try:
        keyword = request.args.get('keyword')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        source_name = request.args.get('source_name')
        search_results=newsapi.get_everything(q=keyword, from_param=from_date, 
                                              to=to_date, sources=source_name, 
                                              language='en' ,sort_by='publishedAt',
                                              page_size=30)
        search_articles=search_results["articles"]
    except NewsAPIException as e:
        return jsonify({"error": e.get_message()})
    count=0
    filtered_articles=[]
    
    for i in search_articles:
        if count==15:
            break
        # for a in i.items():
        #     print(a)
        flag=0
        if ("author" in i) and ("content" in i) and ("description" in i) and ("publishedAt" in i) and ("source" in i)and ("title" in i) and ("url" in i) and ("urlToImage" in i):
            for val1 in i.values():
                if not val1:
                    flag=1
                    break
            if flag==1:
                continue
            if ("id" in i["source"]) and ("name" in i["source"]):
                for val2 in i["source"].values():
                    if not val2:
                        flag=1
                        break
            if flag==1:
                continue
            count+=1
            filtered_articles.append(i)
            
    search_results['articles']=filtered_articles
    #top_headlines=json.dumps(top_headlines,indent=4)
    search_results = jsonify(search_results)
    #print (search_results)
    #return news_headlines
    
    
    return search_results


#handle 404
@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    

#Word Cloud
@application.route('/home/wordCloud')
def wordCloud():
    ans=[]
    final_result=[]
    news = newsapi.get_top_headlines(language='en',page_size=100)
    news=json.dumps(news)
    news=json.loads(news)
    news_articles=news["articles"]
    print (len(news_articles))
    
    file=open("stopwords_en.txt","r")
    data=file.readlines()
    stopwords=[]
    for i in range(len(data)):
        stopwords.append(data[i].strip())
    #print (stopwords)
    #words={}
    title=""
    for i in range(len(news_articles)):
        title+=" "+news_articles[i]["title"]

    #title="They'll work"
    title=re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\\\:"|<,./<>?\s]', title)
    #print (title)
    for i in title:
        if i and i.lower() not in stopwords:
            ans.append(i)
    #ans=list(map(lambda x:x.lower(),ans))
    counter=Counter(ans)
    occurences=counter.most_common(30)
    #print (title)
    
    for i in occurences:
        a={}
        
        a['size']=i[1]*5
        a['word']=i[0]
        final_result.append(a)
    #print(final_result)
        
        
    
    return jsonify(final_result)
    




#main method
if __name__=="__main__":
    
    application.run(debug=True)