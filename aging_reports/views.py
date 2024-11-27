
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


def loanaging_create(request):
    try:
        token = request.session['user_token']
        form=LoanAgingLiveForm()
        

        if request.method == 'POST':
            form = LoanAgingLiveForm(request.POST,)
            temp_form = LoanAgingTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create loanaging')
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
                    return redirect('loanaging_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'LoanAging', 'loanaging': 'active', 'loanaging_show': 'show'
        }
        template_name = 'loanaging_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def loanaging_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view loanaging')
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
            "screen_name": 'LoanAging', 'loanaging': 'active', 'loanaging_show': 'show'
        }
        template_name = 'loanaging_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loanaging_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa loanaging')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'LoanAging',
            "loanaging_id":pk
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
                    'model_name':'LoanAging',
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
                    return redirect('loanaging_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('loanaging_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data LoanAging')
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
                    return redirect('loanaging_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('loanaging_list')
            
            form = LoanAgingTempPAForm(request.POST, inintial=master_view['loanaging'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LoanAging'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('loanaging_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'LoanAging', 'loanaging': 'active', 'loanaging_show': 'show'
                }
                template_name = 'loanaging_create.html'
                return render(request, template_name, context)
        else:
            #form = LoanAgingTempPAForm(initial=master_view['LoanAging'])
            form = LoanAgingTempPAForm(
                initial={**master_view['loanaging'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LoanAging',
            "pa": True, 'loanaging': 'active', 'loanaging_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'loanaging_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loanaging_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'LoanAging'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('loanaging_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('loanaging_list')
        

        MSID= get_service_plan('view loanaging tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "loanaging_id":code
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
 
        MSID= get_service_plan('view loanaging live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "loanaging_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update loanaging temp')
            if MSID is None:
                print('MISID not found')
            form = LoanAgingTempUpdateForm(request.POST,)
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
                    return redirect('loanaging_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = LoanAgingLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = LoanAgingTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'LoanAging', 'loanaging': 'active', 'loanaging_show': 'show'
            }
            template_name = 'loanaging_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loanaging_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view loanaging single')
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
        form = LoanAgingLiveForm(initial=record)  

        if record:
            form = LoanAgingLiveForm(initial=record)
        else:
            form = LoanAgingLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'LoanAging', 'loanaging': 'active', 'loanaging_show': 'show'
        }
        template_name = 'loanaging_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def loanaging_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'LoanAging'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('loanaging_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('loanaging_list')
        
        MSID= get_service_plan('delete loanaging')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'LoanAging',
            "loanaging_id":pk       
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
            return redirect('loanaging_list')
        if workflow_authorize is True:
            return redirect('loanaging_list')

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
                    'model_name':'LoanAging'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('loanaging_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('loanaging_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete LoanAging')
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
                    return redirect('loanaging_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('loanaging_list')
            
            form = LoanAgingTempPAForm(request.POST, inintial=record['LoanAging'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LoanAging'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('loanaging_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'loanaging_create.html'
                return render(request, template_name, context)
        else:
            #form = LoanAgingTempPAForm(initial=record)
            form = LoanAgingTempPAForm(
                initial={**record['LoanAging'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LoanAging',
            'data':record,
            "pa": True, 'loanaging': 'active', 'loanaging_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'loanaging_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def loanaging_authorize_request(request, pk):
    """
    Processes a request to update an existing LoanAging entry and move it to the live table.
    Retrieves the entry from LoanAgingTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to LoanAgingLive
    and an optional history record is created in LoanAgingHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the LoanAging entry to be processed.

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
                'model_name':'LoanAging'
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
                return redirect('loanaging_list') 
            return redirect('loanaging_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'loanaging_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def accountsreceivableaging_create(request):
    try:
        token = request.session['user_token']
        form=AccountsReceivableAgingLiveForm()
        

        if request.method == 'POST':
            form = AccountsReceivableAgingLiveForm(request.POST,)
            temp_form = AccountsReceivableAgingTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create accountsreceivableaging')
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
                    return redirect('accountsreceivableaging_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'AccountsReceivableAging', 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show'
        }
        template_name = 'accountsreceivableaging_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def accountsreceivableaging_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view accountsreceivableaging')
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
            "screen_name": 'AccountsReceivableAging', 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show'
        }
        template_name = 'accountsreceivableaging_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def accountsreceivableaging_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa accountsreceivableaging')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'AccountsReceivableAging',
            "accountsreceivableaging_id":pk
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
                    'model_name':'AccountsReceivableAging',
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
                    return redirect('accountsreceivableaging_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('accountsreceivableaging_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data AccountsReceivableAging')
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
                    return redirect('accountsreceivableaging_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('accountsreceivableaging_list')
            
            form = AccountsReceivableAgingTempPAForm(request.POST, inintial=master_view['accountsreceivableaging'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'AccountsReceivableAging'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('accountsreceivableaging_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'AccountsReceivableAging', 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show'
                }
                template_name = 'accountsreceivableaging_create.html'
                return render(request, template_name, context)
        else:
            #form = AccountsReceivableAgingTempPAForm(initial=master_view['AccountsReceivableAging'])
            form = AccountsReceivableAgingTempPAForm(
                initial={**master_view['accountsreceivableaging'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'AccountsReceivableAging',
            "pa": True, 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'accountsreceivableaging_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def accountsreceivableaging_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'AccountsReceivableAging'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('accountsreceivableaging_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('accountsreceivableaging_list')
        

        MSID= get_service_plan('view accountsreceivableaging tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "accountsreceivableaging_id":code
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
 
        MSID= get_service_plan('view accountsreceivableaging live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "accountsreceivableaging_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update accountsreceivableaging temp')
            if MSID is None:
                print('MISID not found')
            form = AccountsReceivableAgingTempUpdateForm(request.POST,)
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
                    return redirect('accountsreceivableaging_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = AccountsReceivableAgingLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = AccountsReceivableAgingTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'AccountsReceivableAging', 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show'
            }
            template_name = 'accountsreceivableaging_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def accountsreceivableaging_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view accountsreceivableaging single')
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
        form = AccountsReceivableAgingLiveForm(initial=record)  

        if record:
            form = AccountsReceivableAgingLiveForm(initial=record)
        else:
            form = AccountsReceivableAgingLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'AccountsReceivableAging', 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show'
        }
        template_name = 'accountsreceivableaging_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def accountsreceivableaging_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'AccountsReceivableAging'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('accountsreceivableaging_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('accountsreceivableaging_list')
        
        MSID= get_service_plan('delete accountsreceivableaging')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'AccountsReceivableAging',
            "accountsreceivableaging_id":pk       
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
            return redirect('accountsreceivableaging_list')
        if workflow_authorize is True:
            return redirect('accountsreceivableaging_list')

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
                    'model_name':'AccountsReceivableAging'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('accountsreceivableaging_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('accountsreceivableaging_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete AccountsReceivableAging')
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
                    return redirect('accountsreceivableaging_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('accountsreceivableaging_list')
            
            form = AccountsReceivableAgingTempPAForm(request.POST, inintial=record['AccountsReceivableAging'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'AccountsReceivableAging'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('accountsreceivableaging_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'accountsreceivableaging_create.html'
                return render(request, template_name, context)
        else:
            #form = AccountsReceivableAgingTempPAForm(initial=record)
            form = AccountsReceivableAgingTempPAForm(
                initial={**record['AccountsReceivableAging'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'AccountsReceivableAging',
            'data':record,
            "pa": True, 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'accountsreceivableaging_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def accountsreceivableaging_authorize_request(request, pk):
    """
    Processes a request to update an existing AccountsReceivableAging entry and move it to the live table.
    Retrieves the entry from AccountsReceivableAgingTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to AccountsReceivableAgingLive
    and an optional history record is created in AccountsReceivableAgingHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the AccountsReceivableAging entry to be processed.

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
                'model_name':'AccountsReceivableAging'
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
                return redirect('accountsreceivableaging_list') 
            return redirect('accountsreceivableaging_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'accountsreceivableaging_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})
