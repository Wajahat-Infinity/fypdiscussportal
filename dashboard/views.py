from django.shortcuts import redirect,render
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia



def home(request):
    return render(request,'dashboard/home.html')
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} successfully")
    else:
        form=NotesForm
    notes=Notes.objects.filter(user=request.user)
    context={
        'notes': notes ,'form': form
    }
    return render(request,'dashboard/notes.html',context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes

def homework(request):
    if request.method == "POST":
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished==False
            except:
                finished==False
            homework=Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )         
            homework.save()   
            messages.success(request,f"Homework  added from {request.user.username} successfully")
    else:
        form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context={
        'homeworks':homework, 'homework_done':homework_done,'form':form
    }

    return render(request,'dashboard/homework.html',context)

def update_homework(request,pk=None):
    if homework.is_finfished == True:
        homework.is_finished = False
    else:
        homework.is_finished =True
    homework.save()
    return redirect('homework')
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")
    
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
                result_dict['description'] = desc
            
            result_list.append(result_dict)  # Append each video to the result list
        
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/youtube.html', context)  # Render the template after processing all videos

    else:
        form = DashboardForm()
        context = {
            'form': form
        }
        return render(request, 'dashboard/youtube.html', context)  # Render the template with an empty form

def todo(request):
    if request.method == 'POST':
        form =TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST["is_finished"]
                if finished =='on':
                    finished =True
                else:
                    finished=False
               
            except:
                    finished=False
            todos=Todo(
                    user=request.user,
                    title=request.POST['title'],
                    is_finished=finished
                )
            todos.save()
            messages.success(request,f"Todo added from {request.user.username} successfully")

    else:
              
        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo)== 0:
        todos_done=True
    else:
        todos_done=False
    context={
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }

    return render(request,'dashboard/todo.html',context)
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")



def book(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list = []
        
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('count'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('rating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
           
            result_list.append(result_dict)  
        
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/books.html', context)  # Render the template after processing all videos

    else:
        form = DashboardForm()
        context = {
            'form': form
        }
        return render(request, 'dashboard/books.html', context) 
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
            try:
                r = requests.get(url)
                r.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                answer = r.json()
                phonetics = answer[0]['phonetics'][0]['text']
                audio = answer[0]['phonetics'][0]['audio']
                definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                example = answer[0]['meanings'][0].get('example', '')  # Example might not exist
                synonyms = answer[0]['meanings'][0].get('synonyms', [])  # Synonyms might not exist
                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms,
                }

                return render(request, 'dashboard/dictionary.html', context)
            except requests.exceptions.RequestException as e:
                error_message = f"Error fetching data from the API: {e}"
                context = {'form': form, 'error_message': error_message}
                return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
    
    context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form=DashboardForm()
        context={
             'form':form
        }
    return render(request,'dashboard/wiki.html',context)



def blackbox(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            # Make a request to the Black Box AI API
            api_url = 'https://api.blackbox.com/search'
            params = {'q': query}
            headers = {'Authorization': 'Bearer YOUR_API_KEY'}  # Replace 'YOUR_API_KEY' with your actual API key
            response = requests.get(api_url, params=params, headers=headers)
            if response.status_code == 200:
                result = response.json()
                context = {'form': form, 'response': result}
                return render(request, 'dashboard/blackbox.html', context)
            else:
                error_message = f"Error: {response.status_code}. Failed to retrieve data from Black Box AI API."
                context = {'form': form, 'error_message': error_message}
                return render(request, 'dashboard/blackbox.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/blackbox.html', context)