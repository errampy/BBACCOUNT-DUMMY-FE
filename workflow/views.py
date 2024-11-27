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
from django.db.models import Max
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.forms import modelformset_factory
from mainapp.views import *
import random


def id_generation(prefix=None):
    print('prefix ', prefix)
    if prefix is not None:
        return str(str(prefix) + '-' + str(random.randint(1111, 9999)))
    else:
        return str('NA' + '-' + str(random.randint(1111, 9999)))
    

APP_NAME = __name__.split('.')[0]



BASEURL = 'http://127.0.0.1:9000/'
#BASEURL = settings.BASEURL

# BASEURL = settings.BASEURL
ENDPOINT = 'micro-service/'

    


def send_authorized_request_custom(request,table_name_id,record_id,sender_user,approval_user_id):
    try:
        token = request.session['user_token']
        
        MSID= get_service_plan('send authorized request custom')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
        "table_name_id":table_name_id,
        "record_id":record_id,
        "sender_user":sender_user,
        "approval_user_id":approval_user_id
        }    

        data={
                'ms_id':MSID,
                'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

        if response['status_code'] ==  0:                  
                messages.info(request, "Well Done..! Application Submitted..")
                print('data is saved sucessfully',response['data'])

    except Exception as error:
        print('Error Function Name : send_authorized_request_custom : Error Is : ', error)
        return render(request,'500.html',{'error':error})




def approval_count(request,model_name):
    try:
        token = request.session['user_token']
        
        MSID= get_service_plan('approval count')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            "model_name":model_name
        }    

        data={
                'ms_id':MSID,
                'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

        if response['status_code'] ==  0:                  
            messages.info(request, "Well Done..! Application Submitted..")
            return response['data'][0]
        print('response',response['data'])
    except Exception as error:
        print('Error Function Name : send_authorized_request_custom : Error Is : ', error)
        return render(request,'500.html',{'error':error})

# ==================== Sequence =======================

def sequence_list(request):
    try:
        token = request.session['user_token']
            
        MSID= get_service_plan('sequence list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        sequences = response['data']
        
        context = {'sequences': sequences}
        template_name = 'workflow_setup_app/sequence_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def sequence_create(request):
    try:
        token = request.session['user_token']
        # form=SequenceForm()
        if request.method == 'POST':
            form = SequenceForm(request.POST)
            if form.is_valid():
                MSID= get_service_plan('sequence create')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = form.cleaned_data
        
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('sequence_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
                return render(request,'500.html',{'error':form.errors})
        else:
            form = SequenceForm()
        context = {'form': form}
        template_name = 'workflow_setup_app/sequence_form.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def sequence_update(request, pk):
    try:

        token = request.session['user_token']
                
        MSID= get_service_plan('sequence list')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            "pk":pk
        }    

        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
       
        if response['status_code'] ==  1:                  
                messages.info(request, "Well Done..! Application Submitted..")
                sequence=[]
        sequence=response['data'][0]
           

        if request.method == 'POST':
            form = SequenceForm(request.POST, initial=sequence)
            if form.is_valid():
                MSID= get_service_plan('sequence update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data = form.cleaned_data
                cleaned_data['pk']=pk
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:    
                    return redirect('sequence_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})  
        else:
            form = SequenceForm(initial=sequence)

        context = {'form': form}
        template_name = 'workflow_setup_app/sequence_edit.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def sequence_delete(request, pk):
    try:
        token = request.session['user_token']

        MSID= get_service_plan('sequence delete')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            "pk":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] == 0:
            
            messages.info(request, "Well Done..! Application Submitted..")
            return redirect('sequence_list')
        else:
            messages.info(request, "Oops..! Application Failed to Submitted..")
            return redirect('sequence_list')
            
    except Exception as error:
        return render(request,'500.html',{'error':error})


# -------------------------- dropdown option within db limit



def get_next_sequence(request):
    print('function is working')
    token = request.session.get('user_token')
    if not token:
        return JsonResponse({'error': 'User token not found'}, status=401)

    if request.method == 'GET':
        workflow_group_id = request.GET.get('workflow_group_id')
        print('Workflow Group ID:', workflow_group_id)
        
        MSID = get_service_plan('get next sequence')
        if MSID is None:
            print('MSID not found')
            return JsonResponse({'error': 'Service plan not found'}, status=404)

        payload_form = {'workflow_group_id': workflow_group_id}
        data = {
            'ms_id': MSID,
            'ms_payload': payload_form
        }
        json_data = json.dumps(data)
        
        response = call_post_method_with_token_v2(BASEURL, ENDPOINT, json_data, token)
        if 'data' not in response or not response['data']:
            return JsonResponse({'error': 'No data received'}, status=500)
        print('response data',response['data'])
        next_sequences = response['data']
        return JsonResponse({'next_sequences': next_sequences})


 # ====================Workflow Category =======================

def workflow_category_list(request):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('workflow category list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        categories = response['data']
        
        template_name = 'workflow_setup_app/workflow_category_list.html'
        return render(request, template_name, {'categories': categories})
    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_category_create(request):
    try:
        token = request.session['user_token']
        if request.method == 'POST':
            form = WorkflowCategoryForm(request.POST)
            if form.is_valid():

                MSID= get_service_plan('workflow category create')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = form.cleaned_data
                print('cleaned data',cleaned_data)
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('workflow_category_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
                #return render(request,'500.html',{'error':form.errors})
        else:
            generated_code = id_generation(prefix='WFC') 
            form = WorkflowCategoryForm(initial={"code":generated_code})
        context = {'form': form}
        template_name = 'workflow_setup_app/workflow_category_form.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_category_update(request, pk):
    try:
        token = request.session['user_token']
                
        MSID= get_service_plan('workflow category list')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            "pk":pk
        }    

        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
       
        if response['status_code'] ==  1:                  
                messages.info(request, "Well Done..! Application Submitted..")
                category=[]
        category=response['data'][0]
           
        if request.method == 'POST':
            form = WorkflowCategoryForm(request.POST, initial=category)
            if form.is_valid():
                MSID= get_service_plan('workflow category update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data = form.cleaned_data
                cleaned_data['pk']=pk
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:    
                    return redirect('workflow_category_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})  
        else:
            form = WorkflowCategoryForm(initial=category)

        context = {'form': form}
        template_name = 'workflow_setup_app/workflow_category_edit.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_category_delete(request, pk):
    try:
        token = request.session['user_token']

        MSID= get_service_plan('workflow category delete')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            "pk":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] == 0: 
            messages.info(request, "Well Done..! Application Submitted..")
            return redirect('workflow_category_list')
        else:
            messages.info(request, "Oops..! Application Failed to Submitted..")
            return redirect('workflow_category_list')
            
    except Exception as error:
        return render(request,'500.html',{'error':error})


#  =============Workflow Group =============================

def workflow_group_list(request):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('workflow group list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        groups = response['data']
        print('data is comming',groups)
        context = {'groups': groups}
        template_name = 'workflow_setup_app/workflow_group_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_group_create(request):
    try:
        token = request.session['user_token']
        if request.method == 'POST':
            form = WorkflowGroupForm(request.POST)
            if form.is_valid():

                MSID= get_service_plan('workflow group create')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = form.cleaned_data
                print('cleaned data',cleaned_data)
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('workflow_group_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
        else:
            generated_code = id_generation(prefix='WFC') 
            form = WorkflowGroupForm(initial={"code":generated_code})

        context = {'form': form}
        template_name = 'workflow_setup_app/workflow_group_form.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_group_update(request, pk):
    try:
        token = request.session['user_token']
                
        MSID= get_service_plan('workflow group list')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            "pk":pk
        }    

        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
       
        if response['status_code'] ==  1:                  
                messages.info(request, "Well Done..! Application Submitted..")
                group=[]
        group=response['data'][0]

        if request.method == 'POST':
            form = WorkflowGroupForm(request.POST, initial=group)
            if form.is_valid():
                MSID= get_service_plan('workflow group update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data = form.cleaned_data
                cleaned_data['pk']=pk
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:    
                    return redirect('workflow_group_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})  
        else:
            form = WorkflowGroupForm(initial=group)

        context = {'form': form}
        template_name = 'workflow_setup_app/workflow_group_edit.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_group_delete(request, pk):
    try:
        token = request.session['user_token']

        MSID= get_service_plan('workflow group delete')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            "pk":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] == 0:
            messages.info(request, "Well Done..! Application Submitted..")
            return redirect('workflow_group_list')
        else:
            messages.info(request, "Oops..! Application Failed to Submitted..")
            return redirect('workflow_group_list')
            
    except Exception as error:
        return render(request,'500.html',{'error':error})



# # ============== Workflow User Group mapping ====================

# # -----------------------    # Order by the code of the workflow group in ascending order ------------------------>

def workflow_user_group_mapping_list(request):

    try:
        token = request.session['user_token']
        MSID= get_service_plan('workflow user group mapping list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        mappings = response['data']

        context = {'mappings': mappings}
        template_name = 'workflow_setup_app/workflow_user_group_mapping_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})



def workflow_user_group_mapping_create(request):
    try:
        token = request.session['user_token']

        MSID= get_service_plan('workflow group list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        workflow_group = response['data']

        MSID= get_service_plan('get user')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        user = response['data']


        MSID= get_service_plan('sequence list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        sequence = response['data']

        if request.method == 'POST':
            form = WorkflowUserGroupMappingForm(request.POST)
            if form.is_valid():
                MSID= get_service_plan('workflow user group mapping create')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = form.cleaned_data
                print('cleaned data',cleaned_data)
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('workflow_user_group_mapping_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
        else:
            form = WorkflowUserGroupMappingForm()

        context = {'form': form,'workflow_group':workflow_group,'user':user,'sequence':sequence}
        template_name = 'workflow_setup_app/workflow_user_group_mapping_form.html'
        return render(request, template_name, context) 
    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_user_group_mapping_update(request, pk):
    try:
        token = request.session['user_token']
                
        MSID= get_service_plan('workflow user group mapping list')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            "pk":pk
        }    

        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
       
        if response['status_code'] ==  1:                  
                messages.info(request, "Well Done..! Application Submitted..")
                mapping=[]
        mapping=response['data'][0]
        
        MSID= get_service_plan('workflow group list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        workflow_group = response['data']

        MSID= get_service_plan('get user')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        user = response['data']


        MSID= get_service_plan('sequence list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        sequence = response['data']

        #mapping = get_object_or_404(WorkflowUserGroupMapping, pk=pk)
        if request.method == 'POST':
            form = WorkflowUserGroupMappingForm(request.POST, initial=mapping)
            if form.is_valid():
                MSID= get_service_plan('workflow user group mapping update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data = form.cleaned_data
                cleaned_data['pk']=pk
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:    
                    return redirect('workflow_user_group_mapping_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})
            else:
                print(form.errors)
        else:
            form = WorkflowUserGroupMappingForm(initial=mapping)

        context = {'form': form,'workflow_group':workflow_group,'user':user,'sequence':sequence,'mapping':mapping}
        template_name = 'workflow_setup_app/workflow_user_group_mapping_edit.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})



def workflow_user_group_mapping_delete(request, pk):
    try:
        token = request.session['user_token']

        MSID= get_service_plan('workflow user group mapping delete')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            "pk":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] == 0:
            messages.info(request, "Well Done..! Application Submitted..")
            return redirect('workflow_user_group_mapping_list')
        else:
            messages.info(request, "Oops..! Application Failed to Submitted..")
            return redirect('workflow_user_group_mapping_list')
            
    except Exception as error:
        return render(request,'500.html',{'error':error})



# # ================== Workflow Setup ==================================


def workflow_setup_list(request):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('workflow setup list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        setups = response['data']
        print('setup --',setups)
        context = {'setups': setups}
        template_name = 'workflow_setup_app/workflow_setup_list.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})

  

def workflow_setup_create(request):
    try:
        token = request.session['user_token']

        MSID= get_service_plan('workflow category list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        category_list = response['data']

        MSID= get_service_plan('get user')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        user_list = response['data']

        MSID= get_service_plan('workflow group list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        group_list = response['data']

        if request.method == 'POST':
            form = WorkflowSetupForm(request.POST)
            if form.is_valid():
                
                MSID= get_service_plan('workflow setup create')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = form.cleaned_data
                print('cleaned data',cleaned_data)
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('workflow_setup_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors)
        else:
            generated_code = id_generation(prefix='WFC') 

            form = WorkflowSetupForm(initial={"code":generated_code})

        context = {
            'form': form,
            'category_list': category_list,
            'user_list': user_list,
            'group_list': group_list,
        }
        template_name = 'workflow_setup_app/workflow_setup_form.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})



def workflow_setup_update(request, pk):
    try:
        token = request.session['user_token']
                
        MSID= get_service_plan('workflow setup list')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            "pk":pk
        }    

        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
       
        if response['status_code'] ==  1:                  
                messages.info(request, "Well Done..! Application Submitted..")
                setup=[]
        setup=response['data'][0]

        MSID= get_service_plan('workflow category list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        category_list = response['data']

        MSID= get_service_plan('get user')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        user_list = response['data']

        MSID= get_service_plan('workflow group list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        group_list = response['data']

        if request.method == 'POST':
            form = WorkflowSetupForm(request.POST, initial=setup)
            if form.is_valid():
                MSID= get_service_plan('workflow setup update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data = form.cleaned_data
                cleaned_data['pk']=pk
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:    
                    return redirect('workflow_setup_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})
            else:
                print(form.errors)
                return redirect('workflow_setup_list')
        else:
            form = WorkflowSetupForm(initial=setup)
        print('setup data',setup)
        context = {
            'form': form,
            'category_list': category_list,
            'user_list': user_list,
            'group_list': group_list,
            'setup':setup
        }
        return render(request, 'workflow_setup_app/workflow_setup_update.html', context)
    except Exception as error:
        return render(request,'500.html',{'error':error})



def workflow_setup_delete(request, pk):
    try:
        token = request.session['user_token']

        MSID= get_service_plan('workflow setup delete')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            "pk":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] == 0:
            messages.info(request, "Well Done..! Application Submitted..")
            return redirect('workflow_setup_list')
        else:
            messages.info(request, "Oops..! Application Failed to Submitted..")
            return redirect('workflow_setup_list')
            
    except Exception as error:
        return render(request,'500.html',{'error':error})


def show_users(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('check workflow')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            "pk":pk
        }    

        data={
                'ms_id':MSID,
                'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

        if response['status_code'] ==  1:                  
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        user_data = response['data']
        print(user_data)

        context = {'user_data': user_data}
        template_name = 'show_users.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

 

#=========================WorkFlow Mapping - 12/11/24==============================


def workflow_model_list(request):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('workflow model list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        models = response['data']
    
        context = {'models': models}
        template_name = 'workflow_setup_app/workflow_model_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def workflow_mapping_update(request,pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('workflow mapping list')
        if MSID is None:
                print('MISID not found')      

        payload_form = {
            'pk':pk
        }    

        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        } 
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

        if response['status_code'] ==  1:                  
            messages.info(request, "Well Done..! Application Submitted..")
            print('error in backend',response['data'])
        models = response['data']

        MSID= get_service_plan('workflow setup list')
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
                messages.info(request, "Well Done..! Application Submitted..")
                print('error in backend',response['data'])
        workflows = response['data']

        if request.method == 'POST':
          
            form = WorkflowMappingForm(request.POST)
            if form.is_valid():
                create_authorization=request.POST.get('create_authorization')
                create_model=request.POST.get('create_model')
                create_workflow=request.POST.get('create_workflow')
                
                update_authorization=request.POST.get('update_authorization')
                update_model=request.POST.get('update_model')
                update_workflow=request.POST.get('update_workflow')
      
                delete_authorization=request.POST.get('delete_authorization')
                delete_model=request.POST.get('delete_model')
                delete_workflow=request.POST.get('delete_workflow')
             
                self_authorized=False
                same_user_authorized=False
                send_to_authorize=False
                workflow_authorize=False
                if create_authorization=='self_authorized':
                    self_authorized=True
                if create_authorization=='same_user_authorized':
                    same_user_authorized=True
                if create_authorization=='send_to_authorize':
                    send_to_authorize=True
                if create_authorization=='workflow_authorize':
                    workflow_authorize=True
               
                MSID= get_service_plan('workflow mapping update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data={
                    'self_authorized':self_authorized,
                    'same_user_authorized':same_user_authorized,
                    'send_to_authorize':send_to_authorize,
                    'workflow_authorize':workflow_authorize,
                    'pk':create_model,
                    'workflow':create_workflow
                }
                cleaned_data['model_id']=pk

                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                self_authorized=False
                same_user_authorized=False
                send_to_authorize=False
                workflow_authorize=False
                if update_authorization=='self_authorized':
                    self_authorized=True
                if update_authorization=='same_user_authorized':
                    same_user_authorized=True
                if update_authorization=='send_to_authorize':
                    send_to_authorize=True
                if update_authorization=='workflow_authorize':
                    workflow_authorize=True
                MSID= get_service_plan('workflow mapping update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data={
                    'self_authorized':self_authorized,
                    'same_user_authorized':same_user_authorized,
                    'send_to_authorize':send_to_authorize,
                    'workflow_authorize':workflow_authorize,
                    'pk':update_model,
                    'workflow':update_workflow
                }
                cleaned_data['model_id']=pk

                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
  
                self_authorized=False
                same_user_authorized=False
                send_to_authorize=False
                workflow_authorize=False
                if delete_authorization=='self_authorized':
                    self_authorized=True
                if delete_authorization=='same_user_authorized':
                    same_user_authorized=True
                if delete_authorization=='send_to_authorize':
                    send_to_authorize=True
                if delete_authorization=='workflow_authorize':
                    workflow_authorize=True

                MSID= get_service_plan('workflow mapping update')
                if MSID is None:
                    print('MISID not found')
                
                cleaned_data={
                    'self_authorized':self_authorized,
                    'same_user_authorized':same_user_authorized,
                    'send_to_authorize':send_to_authorize,
                    'workflow_authorize':workflow_authorize,
                    'pk':delete_model,
                    'workflow':delete_workflow
                }
                cleaned_data['model_id']=pk

                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                
                if response['status_code'] == 0:    
                    return redirect('workflow_model_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})
            else:
                print(form.errors)
        else:
            form = WorkflowMappingForm()
        context = {'models': models,'workflows':workflows,'form':form}
        template_name = 'workflow_setup_app/workflow_mapping_update.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

 


