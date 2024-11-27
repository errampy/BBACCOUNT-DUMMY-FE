
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.forms import modelformset_factory
from mainapp.views import *

APP_NAME = __name__.split('.')[0]

BASEURL = settings.BASEURL

ENDPOINT = 'micro-service/'


def loandisbursement_create(request):
    try:
        token = request.session['user_token']
        form=LoanDisbursementLiveForm()
        

        if request.method == 'POST':
            form = LoanDisbursementLiveForm(request.POST,)
            temp_form = LoanDisbursementTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create loandisbursement')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = temp_form.cleaned_data
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
        
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('loandisbursement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'LoanDisbursement', 'loandisbursement': 'active', 'loandisbursement_show': 'show'
        }
        template_name = 'loandisbursement_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def loandisbursement_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view loandisbursement')
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
        record = response['data'][0]

        obj=record['obj']
        obj_pa=record['obj_pa']
        obj_wait_auth=record['auth_request']
  
        context = {
            'obj': obj,'app_name':APP_NAME,
            'obj_pa': obj_pa if obj_pa else None,
            'obj_wait_auth': obj_wait_auth if obj_wait_auth else None,
            "screen_name": 'LoanDisbursement', 'loandisbursement': 'active', 'loandisbursement_show': 'show'
        }
        template_name = 'loandisbursement_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loandisbursement_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa loandisbursement')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'LoanDisbursement',
            "loandisbursement_id":pk
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        master_view = response['data'][0]

        work_flow_type=master_view['workflow_data']['workflow_type']


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
        user_data = response['data']


        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')

            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LoanDisbursement',
                    'work_flow_type':work_flow_type
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('loandisbursement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('loandisbursement_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data LoanDisbursement')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":master_view['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('loandisbursement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('loandisbursement_list')
            
            form = LoanDisbursementTempPAForm(request.POST, inintial=master_view['loandisbursement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LoanDisbursement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('loandisbursement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'LoanDisbursement', 'loandisbursement': 'active', 'loandisbursement_show': 'show'
                }
                template_name = 'loandisbursement_create.html'
                return render(request, template_name, context)
        else:
            #form = LoanDisbursementTempPAForm(initial=master_view['LoanDisbursement'])
            form = LoanDisbursementTempPAForm(
                initial={**master_view['loandisbursement'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LoanDisbursement',
            "pa": True, 'loandisbursement': 'active', 'loandisbursement_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'loandisbursement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loandisbursement_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'LoanDisbursement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('loandisbursement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('loandisbursement_list')
        

        MSID= get_service_plan('view loandisbursement tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "loandisbursement_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
 
        if response['status_code'] ==  0:         
            master_type_temp = response['data'][0]
        else:
            messages.info(request, "Error in maker checker validation")
            print('Error in maker checker validation', )
            master_type_temp=[]
 
        MSID= get_service_plan('view loandisbursement live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "loandisbursement_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update loandisbursement temp')
            if MSID is None:
                print('MISID not found')
            form = LoanDisbursementTempUpdateForm(request.POST,)
            if form.is_valid():
                cleaned_data = form.cleaned_data          
                cleaned_data['code']=code
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:
                    return redirect('loandisbursement_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = LoanDisbursementLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = LoanDisbursementTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'LoanDisbursement', 'loandisbursement': 'active', 'loandisbursement_show': 'show'
            }
            template_name = 'loandisbursement_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loandisbursement_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view loandisbursement single')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            "code":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        form = LoanDisbursementLiveForm(initial=record)  

        if record:
            form = LoanDisbursementLiveForm(initial=record)
        else:
            form = LoanDisbursementLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'LoanDisbursement', 'loandisbursement': 'active', 'loandisbursement_show': 'show'
        }
        template_name = 'loandisbursement_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loandisbursement_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'LoanDisbursement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('loandisbursement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('loandisbursement_list')
        
        MSID= get_service_plan('delete loandisbursement')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'LoanDisbursement',
            "loandisbursement_id":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        self_authorize=record['workflow_data']['self_authorized']
        workflow_authorize=record['workflow_data']['workflow_authorize']
        if self_authorize is True:
            return redirect('loandisbursement_list')
        if workflow_authorize is True:
            return redirect('loandisbursement_list')

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
        user_data = response['data']
        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')
            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data for delete')
                if MSID is None:
                    print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LoanDisbursement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('loandisbursement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('loandisbursement_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete LoanDisbursement')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":record['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('loandisbursement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('loandisbursement_list')
            
            form = LoanDisbursementTempPAForm(request.POST, inintial=record['LoanDisbursement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LoanDisbursement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('loandisbursement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'loandisbursement_create.html'
                return render(request, template_name, context)
        else:
            #form = LoanDisbursementTempPAForm(initial=record)
            form = LoanDisbursementTempPAForm(
                initial={**record['LoanDisbursement'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LoanDisbursement',
            'data':record,
            "pa": True, 'loandisbursement': 'active', 'loandisbursement_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'loandisbursement_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def loandisbursement_authorize_request(request, pk):
    """
    Processes a request to update an existing LoanDisbursement entry and move it to the live table.
    Retrieves the entry from LoanDisbursementTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to LoanDisbursementLive
    and an optional history record is created in LoanDisbursementHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the LoanDisbursement entry to be processed.

    Returns:
        HTTPResponse: Redirects to the member category list on successful update,
                      or re-renders the form with current data for editing.
    """
    try:

        token = request.session['user_token']
        id=pk
        request.session['pk_ar'] = str(pk)

        MSID= get_service_plan('auth request data with obj')
        if MSID is None:
                print('MISID not found')
        payload_form = {    
            'pk':pk,
            'app_name':APP_NAME
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        data = response['data'][0]
      
        record_details=data['record_details']
        table_name=data['record_id']['table_name']
       
        record_data=data['record_id']
        record_id=record_data['record_id']

        if request.method == 'POST':
            pk = request.POST.get('code')

            MSID= get_service_plan('get record various models by pk data')
            if MSID is None:
                    print('MISID not found')
            payload_form = {
                'pk':pk,
                'id':id,
                'app_name':APP_NAME,
                'model_name':'LoanDisbursement'
            }
            data={
                'ms_id':MSID,
                'ms_payload':payload_form
            }
            json_data = json.dumps(data)
            response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
            move_temp_live = response['data']
            # record_id=move_temp_live['record_id']
            # table_name=move_temp_live['table_name']
            print('move_temp_live',move_temp_live)
            if response['status_code'] == 0:
                messages.info(request, "Well Done..! Application Submitted..")
                return redirect('loandisbursement_list') 
            return redirect('loandisbursement_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'loandisbursement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def portfolioquality_create(request):
    try:
        token = request.session['user_token']
        form=PortfolioQualityLiveForm()
        

        if request.method == 'POST':
            form = PortfolioQualityLiveForm(request.POST,)
            temp_form = PortfolioQualityTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create portfolioquality')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = temp_form.cleaned_data
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
        
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('portfolioquality_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'PortfolioQuality', 'portfolioquality': 'active', 'portfolioquality_show': 'show'
        }
        template_name = 'portfolioquality_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def portfolioquality_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view portfolioquality')
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
        record = response['data'][0]

        obj=record['obj']
        obj_pa=record['obj_pa']
        obj_wait_auth=record['auth_request']
  
        context = {
            'obj': obj,'app_name':APP_NAME,
            'obj_pa': obj_pa if obj_pa else None,
            'obj_wait_auth': obj_wait_auth if obj_wait_auth else None,
            "screen_name": 'PortfolioQuality', 'portfolioquality': 'active', 'portfolioquality_show': 'show'
        }
        template_name = 'portfolioquality_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def portfolioquality_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa portfolioquality')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'PortfolioQuality',
            "portfolioquality_id":pk
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        master_view = response['data'][0]

        work_flow_type=master_view['workflow_data']['workflow_type']


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
        user_data = response['data']


        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')

            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'PortfolioQuality',
                    'work_flow_type':work_flow_type
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('portfolioquality_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('portfolioquality_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data PortfolioQuality')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":master_view['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('portfolioquality_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('portfolioquality_list')
            
            form = PortfolioQualityTempPAForm(request.POST, inintial=master_view['portfolioquality'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'PortfolioQuality'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('portfolioquality_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'PortfolioQuality', 'portfolioquality': 'active', 'portfolioquality_show': 'show'
                }
                template_name = 'portfolioquality_create.html'
                return render(request, template_name, context)
        else:
            #form = PortfolioQualityTempPAForm(initial=master_view['PortfolioQuality'])
            form = PortfolioQualityTempPAForm(
                initial={**master_view['portfolioquality'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'PortfolioQuality',
            "pa": True, 'portfolioquality': 'active', 'portfolioquality_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'portfolioquality_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def portfolioquality_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'PortfolioQuality'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('portfolioquality_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('portfolioquality_list')
        

        MSID= get_service_plan('view portfolioquality tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "portfolioquality_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
 
        if response['status_code'] ==  0:         
            master_type_temp = response['data'][0]
        else:
            messages.info(request, "Error in maker checker validation")
            print('Error in maker checker validation', )
            master_type_temp=[]
 
        MSID= get_service_plan('view portfolioquality live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "portfolioquality_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update portfolioquality temp')
            if MSID is None:
                print('MISID not found')
            form = PortfolioQualityTempUpdateForm(request.POST,)
            if form.is_valid():
                cleaned_data = form.cleaned_data          
                cleaned_data['code']=code
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:
                    return redirect('portfolioquality_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = PortfolioQualityLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = PortfolioQualityTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'PortfolioQuality', 'portfolioquality': 'active', 'portfolioquality_show': 'show'
            }
            template_name = 'portfolioquality_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def portfolioquality_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view portfolioquality single')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            "code":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        form = PortfolioQualityLiveForm(initial=record)  

        if record:
            form = PortfolioQualityLiveForm(initial=record)
        else:
            form = PortfolioQualityLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'PortfolioQuality', 'portfolioquality': 'active', 'portfolioquality_show': 'show'
        }
        template_name = 'portfolioquality_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def portfolioquality_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'PortfolioQuality'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('portfolioquality_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('portfolioquality_list')
        
        MSID= get_service_plan('delete portfolioquality')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'PortfolioQuality',
            "portfolioquality_id":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        self_authorize=record['workflow_data']['self_authorized']
        workflow_authorize=record['workflow_data']['workflow_authorize']
        if self_authorize is True:
            return redirect('portfolioquality_list')
        if workflow_authorize is True:
            return redirect('portfolioquality_list')

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
        user_data = response['data']
        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')
            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data for delete')
                if MSID is None:
                    print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'PortfolioQuality'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('portfolioquality_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('portfolioquality_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete PortfolioQuality')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":record['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('portfolioquality_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('portfolioquality_list')
            
            form = PortfolioQualityTempPAForm(request.POST, inintial=record['PortfolioQuality'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'PortfolioQuality'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('portfolioquality_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'portfolioquality_create.html'
                return render(request, template_name, context)
        else:
            #form = PortfolioQualityTempPAForm(initial=record)
            form = PortfolioQualityTempPAForm(
                initial={**record['PortfolioQuality'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'PortfolioQuality',
            'data':record,
            "pa": True, 'portfolioquality': 'active', 'portfolioquality_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'portfolioquality_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def portfolioquality_authorize_request(request, pk):
    """
    Processes a request to update an existing PortfolioQuality entry and move it to the live table.
    Retrieves the entry from PortfolioQualityTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to PortfolioQualityLive
    and an optional history record is created in PortfolioQualityHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the PortfolioQuality entry to be processed.

    Returns:
        HTTPResponse: Redirects to the member category list on successful update,
                      or re-renders the form with current data for editing.
    """
    try:

        token = request.session['user_token']
        id=pk
        request.session['pk_ar'] = str(pk)

        MSID= get_service_plan('auth request data with obj')
        if MSID is None:
                print('MISID not found')
        payload_form = {    
            'pk':pk,
            'app_name':APP_NAME
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        data = response['data'][0]
      
        record_details=data['record_details']
        table_name=data['record_id']['table_name']
       
        record_data=data['record_id']
        record_id=record_data['record_id']

        if request.method == 'POST':
            pk = request.POST.get('code')

            MSID= get_service_plan('get record various models by pk data')
            if MSID is None:
                    print('MISID not found')
            payload_form = {
                'pk':pk,
                'id':id,
                'app_name':APP_NAME,
                'model_name':'PortfolioQuality'
            }
            data={
                'ms_id':MSID,
                'ms_payload':payload_form
            }
            json_data = json.dumps(data)
            response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
            move_temp_live = response['data']
            # record_id=move_temp_live['record_id']
            # table_name=move_temp_live['table_name']
            print('move_temp_live',move_temp_live)
            if response['status_code'] == 0:
                messages.info(request, "Well Done..! Application Submitted..")
                return redirect('portfolioquality_list') 
            return redirect('portfolioquality_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'portfolioquality_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def clientoutreach_create(request):
    try:
        token = request.session['user_token']
        form=ClientOutreachLiveForm()
        

        if request.method == 'POST':
            form = ClientOutreachLiveForm(request.POST,)
            temp_form = ClientOutreachTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create clientoutreach')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = temp_form.cleaned_data
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
        
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('clientoutreach_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'ClientOutreach', 'clientoutreach': 'active', 'clientoutreach_show': 'show'
        }
        template_name = 'clientoutreach_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def clientoutreach_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view clientoutreach')
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
        record = response['data'][0]

        obj=record['obj']
        obj_pa=record['obj_pa']
        obj_wait_auth=record['auth_request']
  
        context = {
            'obj': obj,'app_name':APP_NAME,
            'obj_pa': obj_pa if obj_pa else None,
            'obj_wait_auth': obj_wait_auth if obj_wait_auth else None,
            "screen_name": 'ClientOutreach', 'clientoutreach': 'active', 'clientoutreach_show': 'show'
        }
        template_name = 'clientoutreach_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def clientoutreach_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa clientoutreach')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'ClientOutreach',
            "clientoutreach_id":pk
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        master_view = response['data'][0]

        work_flow_type=master_view['workflow_data']['workflow_type']


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
        user_data = response['data']


        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')

            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'ClientOutreach',
                    'work_flow_type':work_flow_type
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('clientoutreach_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('clientoutreach_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data ClientOutreach')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":master_view['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('clientoutreach_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('clientoutreach_list')
            
            form = ClientOutreachTempPAForm(request.POST, inintial=master_view['clientoutreach'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'ClientOutreach'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('clientoutreach_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'ClientOutreach', 'clientoutreach': 'active', 'clientoutreach_show': 'show'
                }
                template_name = 'clientoutreach_create.html'
                return render(request, template_name, context)
        else:
            #form = ClientOutreachTempPAForm(initial=master_view['ClientOutreach'])
            form = ClientOutreachTempPAForm(
                initial={**master_view['clientoutreach'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'ClientOutreach',
            "pa": True, 'clientoutreach': 'active', 'clientoutreach_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'clientoutreach_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def clientoutreach_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'ClientOutreach'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('clientoutreach_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('clientoutreach_list')
        

        MSID= get_service_plan('view clientoutreach tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "clientoutreach_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
 
        if response['status_code'] ==  0:         
            master_type_temp = response['data'][0]
        else:
            messages.info(request, "Error in maker checker validation")
            print('Error in maker checker validation', )
            master_type_temp=[]
 
        MSID= get_service_plan('view clientoutreach live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "clientoutreach_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update clientoutreach temp')
            if MSID is None:
                print('MISID not found')
            form = ClientOutreachTempUpdateForm(request.POST,)
            if form.is_valid():
                cleaned_data = form.cleaned_data          
                cleaned_data['code']=code
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:
                    return redirect('clientoutreach_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = ClientOutreachLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = ClientOutreachTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'ClientOutreach', 'clientoutreach': 'active', 'clientoutreach_show': 'show'
            }
            template_name = 'clientoutreach_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def clientoutreach_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view clientoutreach single')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            "code":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        form = ClientOutreachLiveForm(initial=record)  

        if record:
            form = ClientOutreachLiveForm(initial=record)
        else:
            form = ClientOutreachLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'ClientOutreach', 'clientoutreach': 'active', 'clientoutreach_show': 'show'
        }
        template_name = 'clientoutreach_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def clientoutreach_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'ClientOutreach'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('clientoutreach_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('clientoutreach_list')
        
        MSID= get_service_plan('delete clientoutreach')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'ClientOutreach',
            "clientoutreach_id":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        self_authorize=record['workflow_data']['self_authorized']
        workflow_authorize=record['workflow_data']['workflow_authorize']
        if self_authorize is True:
            return redirect('clientoutreach_list')
        if workflow_authorize is True:
            return redirect('clientoutreach_list')

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
        user_data = response['data']
        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')
            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data for delete')
                if MSID is None:
                    print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'ClientOutreach'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('clientoutreach_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('clientoutreach_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete ClientOutreach')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":record['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('clientoutreach_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('clientoutreach_list')
            
            form = ClientOutreachTempPAForm(request.POST, inintial=record['ClientOutreach'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'ClientOutreach'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('clientoutreach_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'clientoutreach_create.html'
                return render(request, template_name, context)
        else:
            #form = ClientOutreachTempPAForm(initial=record)
            form = ClientOutreachTempPAForm(
                initial={**record['ClientOutreach'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'ClientOutreach',
            'data':record,
            "pa": True, 'clientoutreach': 'active', 'clientoutreach_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'clientoutreach_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def clientoutreach_authorize_request(request, pk):
    """
    Processes a request to update an existing ClientOutreach entry and move it to the live table.
    Retrieves the entry from ClientOutreachTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to ClientOutreachLive
    and an optional history record is created in ClientOutreachHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the ClientOutreach entry to be processed.

    Returns:
        HTTPResponse: Redirects to the member category list on successful update,
                      or re-renders the form with current data for editing.
    """
    try:

        token = request.session['user_token']
        id=pk
        request.session['pk_ar'] = str(pk)

        MSID= get_service_plan('auth request data with obj')
        if MSID is None:
                print('MISID not found')
        payload_form = {    
            'pk':pk,
            'app_name':APP_NAME
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        data = response['data'][0]
      
        record_details=data['record_details']
        table_name=data['record_id']['table_name']
       
        record_data=data['record_id']
        record_id=record_data['record_id']

        if request.method == 'POST':
            pk = request.POST.get('code')

            MSID= get_service_plan('get record various models by pk data')
            if MSID is None:
                    print('MISID not found')
            payload_form = {
                'pk':pk,
                'id':id,
                'app_name':APP_NAME,
                'model_name':'ClientOutreach'
            }
            data={
                'ms_id':MSID,
                'ms_payload':payload_form
            }
            json_data = json.dumps(data)
            response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
            move_temp_live = response['data']
            # record_id=move_temp_live['record_id']
            # table_name=move_temp_live['table_name']
            print('move_temp_live',move_temp_live)
            if response['status_code'] == 0:
                messages.info(request, "Well Done..! Application Submitted..")
                return redirect('clientoutreach_list') 
            return redirect('clientoutreach_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'clientoutreach_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def branchperformance_create(request):
    try:
        token = request.session['user_token']
        form=BranchPerformanceLiveForm()
        

        if request.method == 'POST':
            form = BranchPerformanceLiveForm(request.POST,)
            temp_form = BranchPerformanceTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create branchperformance')
                if MSID is None:
                    print('MISID not found')      
                cleaned_data = temp_form.cleaned_data
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
        
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                } 
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)

                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('branchperformance_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'BranchPerformance', 'branchperformance': 'active', 'branchperformance_show': 'show'
        }
        template_name = 'branchperformance_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def branchperformance_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view branchperformance')
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
        record = response['data'][0]

        obj=record['obj']
        obj_pa=record['obj_pa']
        obj_wait_auth=record['auth_request']
  
        context = {
            'obj': obj,'app_name':APP_NAME,
            'obj_pa': obj_pa if obj_pa else None,
            'obj_wait_auth': obj_wait_auth if obj_wait_auth else None,
            "screen_name": 'BranchPerformance', 'branchperformance': 'active', 'branchperformance_show': 'show'
        }
        template_name = 'branchperformance_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def branchperformance_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa branchperformance')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'BranchPerformance',
            "branchperformance_id":pk
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        master_view = response['data'][0]

        work_flow_type=master_view['workflow_data']['workflow_type']


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
        user_data = response['data']


        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')

            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'BranchPerformance',
                    'work_flow_type':work_flow_type
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('branchperformance_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('branchperformance_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data BranchPerformance')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":master_view['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('branchperformance_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('branchperformance_list')
            
            form = BranchPerformanceTempPAForm(request.POST, inintial=master_view['branchperformance'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'BranchPerformance'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('branchperformance_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'BranchPerformance', 'branchperformance': 'active', 'branchperformance_show': 'show'
                }
                template_name = 'branchperformance_create.html'
                return render(request, template_name, context)
        else:
            #form = BranchPerformanceTempPAForm(initial=master_view['BranchPerformance'])
            form = BranchPerformanceTempPAForm(
                initial={**master_view['branchperformance'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'BranchPerformance',
            "pa": True, 'branchperformance': 'active', 'branchperformance_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'branchperformance_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def branchperformance_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'BranchPerformance'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('branchperformance_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('branchperformance_list')
        

        MSID= get_service_plan('view branchperformance tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "branchperformance_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
 
        if response['status_code'] ==  0:         
            master_type_temp = response['data'][0]
        else:
            messages.info(request, "Error in maker checker validation")
            print('Error in maker checker validation', )
            master_type_temp=[]
 
        MSID= get_service_plan('view branchperformance live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "branchperformance_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update branchperformance temp')
            if MSID is None:
                print('MISID not found')
            form = BranchPerformanceTempUpdateForm(request.POST,)
            if form.is_valid():
                cleaned_data = form.cleaned_data          
                cleaned_data['code']=code
                if cleaned_data['reported_date'] is not None:           
                                    cleaned_data['reported_date'] = cleaned_data['reported_date'].strftime('%Y-%m-%d')
                data={
                    'ms_id':MSID,
                    'ms_payload':cleaned_data
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] == 0:
                    return redirect('branchperformance_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = BranchPerformanceLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = BranchPerformanceTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'BranchPerformance', 'branchperformance': 'active', 'branchperformance_show': 'show'
            }
            template_name = 'branchperformance_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def branchperformance_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view branchperformance single')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            "code":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        form = BranchPerformanceLiveForm(initial=record)  

        if record:
            form = BranchPerformanceLiveForm(initial=record)
        else:
            form = BranchPerformanceLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'BranchPerformance', 'branchperformance': 'active', 'branchperformance_show': 'show'
        }
        template_name = 'branchperformance_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def branchperformance_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'BranchPerformance'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('branchperformance_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('branchperformance_list')
        
        MSID= get_service_plan('delete branchperformance')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'BranchPerformance',
            "branchperformance_id":pk       
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        record = response['data'][0]
        self_authorize=record['workflow_data']['self_authorized']
        workflow_authorize=record['workflow_data']['workflow_authorize']
        if self_authorize is True:
            return redirect('branchperformance_list')
        if workflow_authorize is True:
            return redirect('branchperformance_list')

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
        user_data = response['data']
        if request.method == 'POST':
            send_to_authorized = request.POST.get('send_to_authorized')
            approval_user_id = request.POST.get('user_id')
            authorize_btn = request.POST.get('authorize')
            if authorize_btn == 'authorize':
                MSID= get_service_plan('authorize data for delete')
                if MSID is None:
                    print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'BranchPerformance'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('branchperformance_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('branchperformance_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete BranchPerformance')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "table_name":record['table_data']['id'],
                    "pk":pk,
                    "approval_user_id":approval_user_id
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('branchperformance_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('branchperformance_list')
            
            form = BranchPerformanceTempPAForm(request.POST, inintial=record['BranchPerformance'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'BranchPerformance'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('branchperformance_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'branchperformance_create.html'
                return render(request, template_name, context)
        else:
            #form = BranchPerformanceTempPAForm(initial=record)
            form = BranchPerformanceTempPAForm(
                initial={**record['BranchPerformance'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'BranchPerformance',
            'data':record,
            "pa": True, 'branchperformance': 'active', 'branchperformance_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'branchperformance_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def branchperformance_authorize_request(request, pk):
    """
    Processes a request to update an existing BranchPerformance entry and move it to the live table.
    Retrieves the entry from BranchPerformanceTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to BranchPerformanceLive
    and an optional history record is created in BranchPerformanceHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the BranchPerformance entry to be processed.

    Returns:
        HTTPResponse: Redirects to the member category list on successful update,
                      or re-renders the form with current data for editing.
    """
    try:

        token = request.session['user_token']
        id=pk
        request.session['pk_ar'] = str(pk)

        MSID= get_service_plan('auth request data with obj')
        if MSID is None:
                print('MISID not found')
        payload_form = {    
            'pk':pk,
            'app_name':APP_NAME
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        data = response['data'][0]
      
        record_details=data['record_details']
        table_name=data['record_id']['table_name']
       
        record_data=data['record_id']
        record_id=record_data['record_id']

        if request.method == 'POST':
            pk = request.POST.get('code')

            MSID= get_service_plan('get record various models by pk data')
            if MSID is None:
                    print('MISID not found')
            payload_form = {
                'pk':pk,
                'id':id,
                'app_name':APP_NAME,
                'model_name':'BranchPerformance'
            }
            data={
                'ms_id':MSID,
                'ms_payload':payload_form
            }
            json_data = json.dumps(data)
            response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
            move_temp_live = response['data']
            # record_id=move_temp_live['record_id']
            # table_name=move_temp_live['table_name']
            print('move_temp_live',move_temp_live)
            if response['status_code'] == 0:
                messages.info(request, "Well Done..! Application Submitted..")
                return redirect('branchperformance_list') 
            return redirect('branchperformance_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'branchperformance_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})
