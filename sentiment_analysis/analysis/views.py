from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
#from .sentiment_model import SentimentModel, analyze_and_verify_conversation
from .forms import AddChatForm
from .forms import SignUpForm 
from .sentiment_model import sentiment_model
from .models import Record
import openai
from .forms import RecordForm 
from django.shortcuts import render, get_object_or_404


def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "YOU HAVE BEEN LOGGED IN!")
            return redirect('home')
        else:
            messages.success(request, "THERE WAS AN ERROR LOGGING IN, PLEASE TRY AGAIN..")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "YOU HAVE BEEN LOGGED OUT....")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and log in 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username , password = password)
            login(request,user)
            messages.success(request,'You have Sucessfully Registered! Welcome!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

openai.api_key = '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'  # Replace with your actual API key


def analyze_conversation_with_chatgpt(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the following conversation and provide insights on context understanding, customer satisfaction, response quality, and tone:\n\n{conversation}"}
        ],
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].message['content'].strip()



def view_chat(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    chat_full = record.chat_file
    sentiment_score = record.sentiment_score

    # Get both analyses
    detailed_analysis = analyze_conversation_with_chatgpt(chat_full)
    audit_analysis = check_audit_requirement(chat_full, sentiment_score)

    context = {
        'chat_full': chat_full,
        'sentiment_score': sentiment_score,
        'detailed_analysis': detailed_analysis,
        'audit_analysis': audit_analysis,
        'created_at': record.created_at,
    }

    return render(request, 'view_chat.html', context)


'''def view_chat(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    chat_full = record.chat_file
    sentiment_score = record.sentiment_score

    print('Sentiment Score:', sentiment_score)
    analysis_result = analyze_conversation_with_chatgpt(chat_full)  # Call the analysis function

    context = {
        'chat_full': chat_full,
        'sentiment_score': sentiment_score,
        'analysis_result': analysis_result,
        'created_at': record.created_at,
    }

    return render(request, 'view_chat.html', context)'''


def delete_record(request, pk):
    if request.user.is_authenticated:
        try:
            delete_it = Record.objects.get(id=pk)
            delete_it.delete()
    #        messages.success(request, 'Record Deleted Successfully!')
        except Record.DoesNotExist:
            messages.error(request, 'Record does not exist.')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to delete records.')
        return redirect('home')


def update_record(request, pk):
    # Get the record to update
    record = get_object_or_404(Record, id=pk)
    
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully!')
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = RecordForm(instance=record)
    
    return render(request, 'update_record.html', {'form': form, 'record': record})


# Assuming sentiment_model.analyze returns a dictionary with the required structure
def add_chat(request):
    if request.method == 'POST':
        form = AddChatForm(request.POST)
        if form.is_valid():
            chat_content = form.cleaned_data['chat_file']
            
            # Analyze the chat content using the sentiment model
            sentiment_scores = sentiment_model.analyze(chat_content)
            
            # Check if the sentiment_scores contains the right keys
            if 'neg' in sentiment_scores and 'neu' in sentiment_scores and 'pos' in sentiment_scores:
                # Save the record with the chat and sentiment scores
                new_record = Record(chat_file=chat_content, sentiment_score=sentiment_scores)
                new_record.save()

                messages.success(request, 'Chat Uploaded and Sentiment Analyzed Successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid sentiment score data.')
    else:
        form = AddChatForm()

    return render(request, 'add_chat.html', {'form': form})



def analyze_conversation_with_chatgpt(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the following conversation and provide insights on context understanding, customer satisfaction, response quality, and tone:\n\n{conversation}"}
        ],
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].message['content'].strip()


def check_audit_requirement(conversation, sentiment_score):
    if sentiment_score['pos'] < 0.5:
        audit_prompt = "YOU ARE A CS AUDITOR. THIS IS THE CHAT. CAN YOU PLEASE TELL ME IF WE NEED TO AUDIT THIS CHAT BECAUSE OF BAD BEHAVIOUR OR IF IT IS OKAY?"
    else:
        audit_prompt = "This chat does not require auditing based on sentiment analysis."

    full_prompt = f"""
    {audit_prompt}
    
    Chat content:
    {conversation}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=500,
        temperature=0.5
    )

    return response.choices[0].message['content'].strip()










