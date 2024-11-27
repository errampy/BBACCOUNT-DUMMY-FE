
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


def officeexpense_create(request):
    try:
        token = request.session['user_token']
        form=OfficeExpenseLiveForm()
        

        if request.method == 'POST':
            form = OfficeExpenseLiveForm(request.POST,)
            temp_form = OfficeExpenseTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create officeexpense')
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
                    return redirect('officeexpense_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'OfficeExpense', 'officeexpense': 'active', 'officeexpense_show': 'show'
        }
        template_name = 'officeexpense_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def officeexpense_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view officeexpense')
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
            "screen_name": 'OfficeExpense', 'officeexpense': 'active', 'officeexpense_show': 'show'
        }
        template_name = 'officeexpense_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def officeexpense_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa officeexpense')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'OfficeExpense',
            "officeexpense_id":pk
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
                    'model_name':'OfficeExpense',
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
                    return redirect('officeexpense_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('officeexpense_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data OfficeExpense')
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
                    return redirect('officeexpense_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('officeexpense_list')
            
            form = OfficeExpenseTempPAForm(request.POST, inintial=master_view['officeexpense'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'OfficeExpense'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('officeexpense_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'OfficeExpense', 'officeexpense': 'active', 'officeexpense_show': 'show'
                }
                template_name = 'officeexpense_create.html'
                return render(request, template_name, context)
        else:
            #form = OfficeExpenseTempPAForm(initial=master_view['OfficeExpense'])
            form = OfficeExpenseTempPAForm(
                initial={**master_view['officeexpense'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'OfficeExpense',
            "pa": True, 'officeexpense': 'active', 'officeexpense_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'officeexpense_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def officeexpense_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'OfficeExpense'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('officeexpense_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('officeexpense_list')
        

        MSID= get_service_plan('view officeexpense tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "officeexpense_id":code
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
 
        MSID= get_service_plan('view officeexpense live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "officeexpense_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update officeexpense temp')
            if MSID is None:
                print('MISID not found')
            form = OfficeExpenseTempUpdateForm(request.POST,)
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
                    return redirect('officeexpense_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = OfficeExpenseLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = OfficeExpenseTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'OfficeExpense', 'officeexpense': 'active', 'officeexpense_show': 'show'
            }
            template_name = 'officeexpense_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def officeexpense_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view officeexpense single')
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
        form = OfficeExpenseLiveForm(initial=record)  

        if record:
            form = OfficeExpenseLiveForm(initial=record)
        else:
            form = OfficeExpenseLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'OfficeExpense', 'officeexpense': 'active', 'officeexpense_show': 'show'
        }
        template_name = 'officeexpense_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def officeexpense_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'OfficeExpense'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('officeexpense_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('officeexpense_list')
        
        MSID= get_service_plan('delete officeexpense')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'OfficeExpense',
            "officeexpense_id":pk       
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
            return redirect('officeexpense_list')
        if workflow_authorize is True:
            return redirect('officeexpense_list')

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
                    'model_name':'OfficeExpense'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('officeexpense_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('officeexpense_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete OfficeExpense')
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
                    return redirect('officeexpense_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('officeexpense_list')
            
            form = OfficeExpenseTempPAForm(request.POST, inintial=record['OfficeExpense'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'OfficeExpense'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('officeexpense_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'officeexpense_create.html'
                return render(request, template_name, context)
        else:
            #form = OfficeExpenseTempPAForm(initial=record)
            form = OfficeExpenseTempPAForm(
                initial={**record['OfficeExpense'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'OfficeExpense',
            'data':record,
            "pa": True, 'officeexpense': 'active', 'officeexpense_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'officeexpense_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def officeexpense_authorize_request(request, pk):
    """
    Processes a request to update an existing OfficeExpense entry and move it to the live table.
    Retrieves the entry from OfficeExpenseTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to OfficeExpenseLive
    and an optional history record is created in OfficeExpenseHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the OfficeExpense entry to be processed.

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
                'model_name':'OfficeExpense'
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
                return redirect('officeexpense_list') 
            return redirect('officeexpense_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'officeexpense_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def assetmanagement_create(request):
    try:
        token = request.session['user_token']
        form=AssetManagementLiveForm()
        

        if request.method == 'POST':
            form = AssetManagementLiveForm(request.POST,)
            temp_form = AssetManagementTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create assetmanagement')
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
                    return redirect('assetmanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'AssetManagement', 'assetmanagement': 'active', 'assetmanagement_show': 'show'
        }
        template_name = 'assetmanagement_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def assetmanagement_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view assetmanagement')
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
            "screen_name": 'AssetManagement', 'assetmanagement': 'active', 'assetmanagement_show': 'show'
        }
        template_name = 'assetmanagement_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def assetmanagement_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa assetmanagement')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'AssetManagement',
            "assetmanagement_id":pk
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
                    'model_name':'AssetManagement',
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
                    return redirect('assetmanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('assetmanagement_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data AssetManagement')
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
                    return redirect('assetmanagement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('assetmanagement_list')
            
            form = AssetManagementTempPAForm(request.POST, inintial=master_view['assetmanagement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'AssetManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('assetmanagement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'AssetManagement', 'assetmanagement': 'active', 'assetmanagement_show': 'show'
                }
                template_name = 'assetmanagement_create.html'
                return render(request, template_name, context)
        else:
            #form = AssetManagementTempPAForm(initial=master_view['AssetManagement'])
            form = AssetManagementTempPAForm(
                initial={**master_view['assetmanagement'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'AssetManagement',
            "pa": True, 'assetmanagement': 'active', 'assetmanagement_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'assetmanagement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def assetmanagement_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'AssetManagement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('assetmanagement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('assetmanagement_list')
        

        MSID= get_service_plan('view assetmanagement tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "assetmanagement_id":code
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
 
        MSID= get_service_plan('view assetmanagement live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "assetmanagement_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update assetmanagement temp')
            if MSID is None:
                print('MISID not found')
            form = AssetManagementTempUpdateForm(request.POST,)
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
                    return redirect('assetmanagement_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = AssetManagementLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = AssetManagementTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'AssetManagement', 'assetmanagement': 'active', 'assetmanagement_show': 'show'
            }
            template_name = 'assetmanagement_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def assetmanagement_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view assetmanagement single')
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
        form = AssetManagementLiveForm(initial=record)  

        if record:
            form = AssetManagementLiveForm(initial=record)
        else:
            form = AssetManagementLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'AssetManagement', 'assetmanagement': 'active', 'assetmanagement_show': 'show'
        }
        template_name = 'assetmanagement_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def assetmanagement_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'AssetManagement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('assetmanagement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('assetmanagement_list')
        
        MSID= get_service_plan('delete assetmanagement')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'AssetManagement',
            "assetmanagement_id":pk       
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
            return redirect('assetmanagement_list')
        if workflow_authorize is True:
            return redirect('assetmanagement_list')

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
                    'model_name':'AssetManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('assetmanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('assetmanagement_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete AssetManagement')
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
                    return redirect('assetmanagement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('assetmanagement_list')
            
            form = AssetManagementTempPAForm(request.POST, inintial=record['AssetManagement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'AssetManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('assetmanagement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'assetmanagement_create.html'
                return render(request, template_name, context)
        else:
            #form = AssetManagementTempPAForm(initial=record)
            form = AssetManagementTempPAForm(
                initial={**record['AssetManagement'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'AssetManagement',
            'data':record,
            "pa": True, 'assetmanagement': 'active', 'assetmanagement_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'assetmanagement_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def assetmanagement_authorize_request(request, pk):
    """
    Processes a request to update an existing AssetManagement entry and move it to the live table.
    Retrieves the entry from AssetManagementTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to AssetManagementLive
    and an optional history record is created in AssetManagementHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the AssetManagement entry to be processed.

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
                'model_name':'AssetManagement'
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
                return redirect('assetmanagement_list') 
            return redirect('assetmanagement_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'assetmanagement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def logisticsandfleetmanagement_create(request):
    try:
        token = request.session['user_token']
        form=LogisticsAndFleetManagementLiveForm()
        

        if request.method == 'POST':
            form = LogisticsAndFleetManagementLiveForm(request.POST,)
            temp_form = LogisticsAndFleetManagementTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create logisticsandfleetmanagement')
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
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'LogisticsAndFleetManagement', 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show'
        }
        template_name = 'logisticsandfleetmanagement_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def logisticsandfleetmanagement_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view logisticsandfleetmanagement')
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
            "screen_name": 'LogisticsAndFleetManagement', 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show'
        }
        template_name = 'logisticsandfleetmanagement_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def logisticsandfleetmanagement_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa logisticsandfleetmanagement')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'LogisticsAndFleetManagement',
            "logisticsandfleetmanagement_id":pk
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
                    'model_name':'LogisticsAndFleetManagement',
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
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('logisticsandfleetmanagement_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data LogisticsAndFleetManagement')
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
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('logisticsandfleetmanagement_list')
            
            form = LogisticsAndFleetManagementTempPAForm(request.POST, inintial=master_view['logisticsandfleetmanagement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LogisticsAndFleetManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'LogisticsAndFleetManagement', 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show'
                }
                template_name = 'logisticsandfleetmanagement_create.html'
                return render(request, template_name, context)
        else:
            #form = LogisticsAndFleetManagementTempPAForm(initial=master_view['LogisticsAndFleetManagement'])
            form = LogisticsAndFleetManagementTempPAForm(
                initial={**master_view['logisticsandfleetmanagement'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LogisticsAndFleetManagement',
            "pa": True, 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'logisticsandfleetmanagement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def logisticsandfleetmanagement_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'LogisticsAndFleetManagement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('logisticsandfleetmanagement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('logisticsandfleetmanagement_list')
        

        MSID= get_service_plan('view logisticsandfleetmanagement tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "logisticsandfleetmanagement_id":code
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
 
        MSID= get_service_plan('view logisticsandfleetmanagement live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "logisticsandfleetmanagement_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update logisticsandfleetmanagement temp')
            if MSID is None:
                print('MISID not found')
            form = LogisticsAndFleetManagementTempUpdateForm(request.POST,)
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
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = LogisticsAndFleetManagementLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = LogisticsAndFleetManagementTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'LogisticsAndFleetManagement', 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show'
            }
            template_name = 'logisticsandfleetmanagement_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def logisticsandfleetmanagement_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view logisticsandfleetmanagement single')
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
        form = LogisticsAndFleetManagementLiveForm(initial=record)  

        if record:
            form = LogisticsAndFleetManagementLiveForm(initial=record)
        else:
            form = LogisticsAndFleetManagementLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'LogisticsAndFleetManagement', 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show'
        }
        template_name = 'logisticsandfleetmanagement_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def logisticsandfleetmanagement_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'LogisticsAndFleetManagement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('logisticsandfleetmanagement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('logisticsandfleetmanagement_list')
        
        MSID= get_service_plan('delete logisticsandfleetmanagement')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'LogisticsAndFleetManagement',
            "logisticsandfleetmanagement_id":pk       
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
            return redirect('logisticsandfleetmanagement_list')
        if workflow_authorize is True:
            return redirect('logisticsandfleetmanagement_list')

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
                    'model_name':'LogisticsAndFleetManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('logisticsandfleetmanagement_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete LogisticsAndFleetManagement')
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
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('logisticsandfleetmanagement_list')
            
            form = LogisticsAndFleetManagementTempPAForm(request.POST, inintial=record['LogisticsAndFleetManagement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LogisticsAndFleetManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('logisticsandfleetmanagement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'logisticsandfleetmanagement_create.html'
                return render(request, template_name, context)
        else:
            #form = LogisticsAndFleetManagementTempPAForm(initial=record)
            form = LogisticsAndFleetManagementTempPAForm(
                initial={**record['LogisticsAndFleetManagement'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LogisticsAndFleetManagement',
            'data':record,
            "pa": True, 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'logisticsandfleetmanagement_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def logisticsandfleetmanagement_authorize_request(request, pk):
    """
    Processes a request to update an existing LogisticsAndFleetManagement entry and move it to the live table.
    Retrieves the entry from LogisticsAndFleetManagementTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to LogisticsAndFleetManagementLive
    and an optional history record is created in LogisticsAndFleetManagementHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the LogisticsAndFleetManagement entry to be processed.

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
                'model_name':'LogisticsAndFleetManagement'
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
                return redirect('logisticsandfleetmanagement_list') 
            return redirect('logisticsandfleetmanagement_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'logisticsandfleetmanagement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})
