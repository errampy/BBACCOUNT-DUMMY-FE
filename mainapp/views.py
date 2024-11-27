import json
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from .decorator import custom_login_required
from .models import *
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import requests
from django.conf import settings
from .forms import *
from django.urls import NoReverseMatch


#BASEURL = 'http://127.0.0.1:9000/'
BASEURL = settings.BASEURL
ENDPOINT = 'micro-service/'

def get_service_plan(service_plan_id):
    try:
        # Attempt to retrieve the service plan object by description
        ms_table = MS_ServicePlan.objects.get(description=service_plan_id)
        return ms_table.ms_id
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        raise ValueError("Multiple service plans found for description: {}".format(service_plan_id))
    except Exception as error:
        return None
    
def call_post_method_without_token(URL,data):
    api_url = URL
    headers = { "Content-Type": "application/json"}
    response = requests.post(api_url,data=data,headers=headers)
    return response



def call_post_method_with_token_v2(URL, endpoint, data, access_token, files=None):
    api_url = URL + endpoint
    headers = {"Authorization": f'Bearer {access_token}'}
    
    if files:
        response = requests.post(api_url, data=data, files=files, headers=headers)
    else:
        headers["Content-Type"] = "application/json"
        response = requests.post(api_url, data=data, headers=headers)

    if response.status_code in [200, 201]:
        try:
            return {'status_code': 0, 'data': response.json()}
        except json.JSONDecodeError:
            return {'status_code': 1, 'data': 'Invalid JSON response'}
    else:
        try:
            return {'status_code': 1, 'data': response.json()}
        except json.JSONDecodeError:
            return {'status_code': 1, 'data': 'Something went wrong'}



def get_data(request):
    service_name = request.GET.get('service_name')
    field_name = request.GET.get('field_name')
    field_value = request.GET.get('field_value')
    link_table_name = request.GET.get('link_table_name')
    
    try:
        token = request.session['user_token']
        MSID = get_service_plan(service_name)
        if MSID is None:
            print('MSID not found')
            return JsonResponse({'error': 'Service plan not found'}, status=400)
        # Prepare the payload to fetch states
        
        payload_form = {
            field_name: field_value
            }
        
        data = {
            'ms_id': MSID,
            'ms_payload': payload_form
        }
        
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL, ENDPOINT, json_data, token)
        
        if response['status_code'] == 0:
            value = response['data']
            value_dropdown = get_dropdown(value, link_table_name)
            print('value_dropdown',value_dropdown)
            return JsonResponse({'value': value_dropdown}, status=200)
        else:
            return JsonResponse({'error': 'Failed to fetch value'}, status=400)

    except Exception as error:
        return JsonResponse({'error': str(error)}, status=500)

def get_dropdown(states, name_key):
    return [{'id': state['code'], 'name': state[name_key]} for state in states]

  
def unauthorized_return(request,app_name,model_name,url):

    try:
        token = request.session['user_token']

        if request.method == 'POST':
            notes = request.POST.get('notes')
            pk = request.POST.get('pk')
            record_id = request.POST.get('record_id')
     
            MSID= get_service_plan('unauthorized return')
            if MSID is None:
                print('MISID not found')
            payload_form = {   
                'notes':notes,
                'record_id':record_id,
                'app_name':app_name,
                'model_name':model_name,
                'pk':pk    
            }
            data={
                'ms_id':MSID,
                'ms_payload':payload_form
            }
            json_data = json.dumps(data)
            response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
            print('responmse',response)
            if response['status_code'] ==  0:   
                messages.success(request, 'Unauthorized return')
                return redirect(url)

            else:
                messages.info(request, "Oops..! Application Failed to Submitted..")
    except Exception as error:
        return render(request,'500.html',{'error':error})

      
def delegate_record(request,app_name, pk, model_name,url):
    try:
        token = request.session['user_token']
        
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk ,
            'model_name':model_name,
            'app_name': app_name
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

        if response['status_code'] ==  1 :  
            messages.success(request, 'Successfully')
            return redirect(url)
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect(url)

        MSID= get_service_plan('get record from the various models')
        if MSID is None:
            print('MISID not found')
        payload_form = {
             'model_name':model_name,
             'app_name': app_name,
             'code':pk    
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Successfully')
            return redirect(url)
      
        record_details=response['data'][0]
  

        MSID= get_service_plan('get user record')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Successfully')
            return redirect(url)

        user_record=response['data']
        
        if request.method == 'POST':
            pk = request.POST.get('pk')

            model_name = request.POST.get('model_name')
  
            user_id = request.POST.get('user_id')
         
            MSID= get_service_plan('delegate user data')
            if MSID is None:
                print('MISID not found')
            payload_form = {  
                'user_id':user_id,
                'model_name':model_name,
                'pk':pk
            }
            data={
                'ms_id':MSID,
                'ms_payload':payload_form
            }
            json_data = json.dumps(data)
            response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
            if response['status_code'] ==  1:   
                messages.success(request, 'Successfully')
                return redirect(url)
            resp=response['data'][0]

            if resp:
                messages.success(request, 'Successfully User Delegated')
                try:
                    return redirect(url)
                except NoReverseMatch:
                    # Handle URL not found error
                    messages.error(request, 'Redirect URL not found.')
                    return redirect('dashboard') 
            else:
                messages.success(request, 'Un Successful User Delegate')
                # return redirect(request.META.get('HTTP_REFERER'))
                return redirect(url)
        else:
            context = {
                "message": 'An error occurred while processing your request.',
                "screen_name": model_name,
                "record_details": record_details,
                "model_name": model_name,
                "pk": pk, "user_record": user_record,
            }
            template_name = 'delegate_record.html'
            return render(request, template_name, context)
        
    except Exception as error:
        return render(request,'500.html',{'error':error})
  
    except Http404:
        return render(request, '500.html')

    except NoReverseMatch:
        # Handle URL not found when rendering
        return redirect('dashboard') 

