from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.font_manager import FontProperties
from django.http import HttpResponse
import io
from matplotlib import pyplot
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from django_pandas.io import read_frame
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Source, Author, Article, Topic,Article_content

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_sources = Source.objects.all().count()
    num_articles = Article.objects.all().count()
    
    
    num_topic = Topic.objects.all().count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
   

    context = {
        'num_sources': num_sources,
        'num_articles': num_articles,
        'num_topic': num_topic,
        'num_authors': num_authors,
       
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
from django.views import generic
class ArticleListView(generic.ListView):
    model = Article
    paginate_by = 10
    
class ArticleDetailView(generic.DetailView):
    model = Article
   
    
   
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
class AuthorDetailView(generic.DetailView):
    model = Author
   

def report(request):
    term_count = {}
    for i in Article_content.objects.all():
        words = Article_content.key_word(i)
        for word in words:
            if word not in term_count:
                term_count[word] = 1
            else:
                term_count[word] = term_count[word] + 1
    data = pd.DataFrame.from_dict(term_count, orient='index')
    data = data.reset_index()
    data.columns = ['Terms','Count']
    terms =data.sort_values(by = ['Count'],ascending = False).head(20)
    terms = terms[2:]
    terms1=terms.sort_index()
    T1=terms.iloc[0,0]
    T2=terms.iloc[1,0]
    T3=terms.iloc[2,0]
    T4=terms.iloc[0,1]
    T5=terms.iloc[1,1]
    T6=terms.iloc[2,1]
    context = {
        'T1':T1,
        'T2':T2,
        'T3':T3,
        'T4':T4,
        'T5':T5,
        'T6':T6,
        
    }
    return render(request, 'report_home.html', context=context)

def comentionfigure(request):
    term_count = {}
    for i in Article_content.objects.all():
        words = Article_content.key_word(i)
        for word in words:
            if word not in term_count:
                term_count[word] = 1
            else:
                term_count[word] = term_count[word] + 1
    data = pd.DataFrame.from_dict(term_count, orient='index')
    data = data.reset_index()
    data.columns = ['Terms','Count']
    terms =data.sort_values(by = ['Count'],ascending = False).head(20)
    terms = terms[2:]
    terms1=terms.sort_index()
    qs = Article_content.objects.all()
    df = read_frame(qs)
    text = " ".join(content for content in df.content)
    stopwords1 = set(STOPWORDS)
    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords1, background_color="white",colormap = 'viridis').generate(text)
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Arial Rounded MT')
    font.set_style('italic')
    plt.figure(figsize=(40,60),facecolor='white')
    fig, ax= plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    response=HttpResponse(buf.getvalue(),content_type='image/png')
    # if required clear the figure for reuse 
    fig.clear()
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))
    return response

def report_fig1(request):
    term_count = {}
    for i in Article_content.objects.all():
        words = Article_content.key_word(i)
        for word in words:
            if word not in term_count:
                term_count[word] = 1
            else:
                term_count[word] = term_count[word] + 1
    data = pd.DataFrame.from_dict(term_count, orient='index')
    data = data.reset_index()
    data.columns = ['Terms','Count']
    terms =data.sort_values(by = ['Count'],ascending = False).head(20)
    terms = terms[2:]
    terms1=terms.sort_index()
    fig,ax=plt.subplots()
    sns.set(rc={'figure.figsize':(15,10)})
    sns.set_context("poster", font_scale = 0.8, rc={"grid.linewidth": 1})
    ax = sns.barplot(x="Terms", y="Count", data=terms1, palette="rocket")
    for item in ax.get_xticklabels():
        item.set_rotation(80)
    plt.grid(False)
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    response=HttpResponse(buf.getvalue(),content_type='image/png')
    # if required clear the figure for reuse 
    fig.clear()
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))
    return response

class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 10
class TopicDetailView(generic.DetailView):
    model = Topic
#Still working on it
#def competiter(request):
    #if 'pk' in request.get and request.get['pk'] != '':
        #Id=int(request.get['pk'])
       # content = Article_content.objects.get(id=Id)
        #r=Article_content.competiter_fig(content)
        #return r
   