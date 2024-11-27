
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


def leavemanagement_create(request):
    try:
        token = request.session['user_token']
        form=LeaveManagementLiveForm()
        

        if request.method == 'POST':
            form = LeaveManagementLiveForm(request.POST,)
            temp_form = LeaveManagementTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create leavemanagement')
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
                    return redirect('leavemanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'LeaveManagement', 'leavemanagement': 'active', 'leavemanagement_show': 'show'
        }
        template_name = 'leavemanagement_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def leavemanagement_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view leavemanagement')
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
            "screen_name": 'LeaveManagement', 'leavemanagement': 'active', 'leavemanagement_show': 'show'
        }
        template_name = 'leavemanagement_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def leavemanagement_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa leavemanagement')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'LeaveManagement',
            "leavemanagement_id":pk
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
                    'model_name':'LeaveManagement',
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
                    return redirect('leavemanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('leavemanagement_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data LeaveManagement')
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
                    return redirect('leavemanagement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('leavemanagement_list')
            
            form = LeaveManagementTempPAForm(request.POST, inintial=master_view['leavemanagement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LeaveManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('leavemanagement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'LeaveManagement', 'leavemanagement': 'active', 'leavemanagement_show': 'show'
                }
                template_name = 'leavemanagement_create.html'
                return render(request, template_name, context)
        else:
            #form = LeaveManagementTempPAForm(initial=master_view['LeaveManagement'])
            form = LeaveManagementTempPAForm(
                initial={**master_view['leavemanagement'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LeaveManagement',
            "pa": True, 'leavemanagement': 'active', 'leavemanagement_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'leavemanagement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def leavemanagement_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'LeaveManagement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('leavemanagement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('leavemanagement_list')
        

        MSID= get_service_plan('view leavemanagement tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "leavemanagement_id":code
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
 
        MSID= get_service_plan('view leavemanagement live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "leavemanagement_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update leavemanagement temp')
            if MSID is None:
                print('MISID not found')
            form = LeaveManagementTempUpdateForm(request.POST,)
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
                    return redirect('leavemanagement_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = LeaveManagementLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = LeaveManagementTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'LeaveManagement', 'leavemanagement': 'active', 'leavemanagement_show': 'show'
            }
            template_name = 'leavemanagement_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def leavemanagement_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view leavemanagement single')
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
        form = LeaveManagementLiveForm(initial=record)  

        if record:
            form = LeaveManagementLiveForm(initial=record)
        else:
            form = LeaveManagementLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'LeaveManagement', 'leavemanagement': 'active', 'leavemanagement_show': 'show'
        }
        template_name = 'leavemanagement_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def leavemanagement_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'LeaveManagement'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('leavemanagement_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('leavemanagement_list')
        
        MSID= get_service_plan('delete leavemanagement')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'LeaveManagement',
            "leavemanagement_id":pk       
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
            return redirect('leavemanagement_list')
        if workflow_authorize is True:
            return redirect('leavemanagement_list')

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
                    'model_name':'LeaveManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('leavemanagement_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('leavemanagement_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete LeaveManagement')
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
                    return redirect('leavemanagement_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('leavemanagement_list')
            
            form = LeaveManagementTempPAForm(request.POST, inintial=record['LeaveManagement'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'LeaveManagement'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('leavemanagement_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'leavemanagement_create.html'
                return render(request, template_name, context)
        else:
            #form = LeaveManagementTempPAForm(initial=record)
            form = LeaveManagementTempPAForm(
                initial={**record['LeaveManagement'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'LeaveManagement',
            'data':record,
            "pa": True, 'leavemanagement': 'active', 'leavemanagement_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'leavemanagement_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def leavemanagement_authorize_request(request, pk):
    """
    Processes a request to update an existing LeaveManagement entry and move it to the live table.
    Retrieves the entry from LeaveManagementTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to LeaveManagementLive
    and an optional history record is created in LeaveManagementHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the LeaveManagement entry to be processed.

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
                'model_name':'LeaveManagement'
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
                return redirect('leavemanagement_list') 
            return redirect('leavemanagement_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'leavemanagement_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def staffproductivity_create(request):
    try:
        token = request.session['user_token']
        form=StaffProductivityLiveForm()
        

        if request.method == 'POST':
            form = StaffProductivityLiveForm(request.POST,)
            temp_form = StaffProductivityTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create staffproductivity')
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
                    return redirect('staffproductivity_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'StaffProductivity', 'staffproductivity': 'active', 'staffproductivity_show': 'show'
        }
        template_name = 'staffproductivity_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffproductivity_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view staffproductivity')
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
            "screen_name": 'StaffProductivity', 'staffproductivity': 'active', 'staffproductivity_show': 'show'
        }
        template_name = 'staffproductivity_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffproductivity_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa staffproductivity')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'StaffProductivity',
            "staffproductivity_id":pk
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
                    'model_name':'StaffProductivity',
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
                    return redirect('staffproductivity_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('staffproductivity_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data StaffProductivity')
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
                    return redirect('staffproductivity_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('staffproductivity_list')
            
            form = StaffProductivityTempPAForm(request.POST, inintial=master_view['staffproductivity'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'StaffProductivity'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('staffproductivity_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'StaffProductivity', 'staffproductivity': 'active', 'staffproductivity_show': 'show'
                }
                template_name = 'staffproductivity_create.html'
                return render(request, template_name, context)
        else:
            #form = StaffProductivityTempPAForm(initial=master_view['StaffProductivity'])
            form = StaffProductivityTempPAForm(
                initial={**master_view['staffproductivity'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'StaffProductivity',
            "pa": True, 'staffproductivity': 'active', 'staffproductivity_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'staffproductivity_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffproductivity_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'StaffProductivity'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('staffproductivity_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('staffproductivity_list')
        

        MSID= get_service_plan('view staffproductivity tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "staffproductivity_id":code
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
 
        MSID= get_service_plan('view staffproductivity live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "staffproductivity_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update staffproductivity temp')
            if MSID is None:
                print('MISID not found')
            form = StaffProductivityTempUpdateForm(request.POST,)
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
                    return redirect('staffproductivity_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = StaffProductivityLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = StaffProductivityTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'StaffProductivity', 'staffproductivity': 'active', 'staffproductivity_show': 'show'
            }
            template_name = 'staffproductivity_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffproductivity_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view staffproductivity single')
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
        form = StaffProductivityLiveForm(initial=record)  

        if record:
            form = StaffProductivityLiveForm(initial=record)
        else:
            form = StaffProductivityLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'StaffProductivity', 'staffproductivity': 'active', 'staffproductivity_show': 'show'
        }
        template_name = 'staffproductivity_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffproductivity_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'StaffProductivity'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('staffproductivity_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('staffproductivity_list')
        
        MSID= get_service_plan('delete staffproductivity')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'StaffProductivity',
            "staffproductivity_id":pk       
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
            return redirect('staffproductivity_list')
        if workflow_authorize is True:
            return redirect('staffproductivity_list')

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
                    'model_name':'StaffProductivity'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('staffproductivity_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('staffproductivity_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete StaffProductivity')
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
                    return redirect('staffproductivity_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('staffproductivity_list')
            
            form = StaffProductivityTempPAForm(request.POST, inintial=record['StaffProductivity'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'StaffProductivity'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('staffproductivity_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'staffproductivity_create.html'
                return render(request, template_name, context)
        else:
            #form = StaffProductivityTempPAForm(initial=record)
            form = StaffProductivityTempPAForm(
                initial={**record['StaffProductivity'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'StaffProductivity',
            'data':record,
            "pa": True, 'staffproductivity': 'active', 'staffproductivity_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'staffproductivity_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def staffproductivity_authorize_request(request, pk):
    """
    Processes a request to update an existing StaffProductivity entry and move it to the live table.
    Retrieves the entry from StaffProductivityTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to StaffProductivityLive
    and an optional history record is created in StaffProductivityHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the StaffProductivity entry to be processed.

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
                'model_name':'StaffProductivity'
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
                return redirect('staffproductivity_list') 
            return redirect('staffproductivity_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'staffproductivity_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def trainingdevelopment_create(request):
    try:
        token = request.session['user_token']
        form=TrainingDevelopmentLiveForm()
        

        if request.method == 'POST':
            form = TrainingDevelopmentLiveForm(request.POST,)
            temp_form = TrainingDevelopmentTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create trainingdevelopment')
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
                    return redirect('trainingdevelopment_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'TrainingDevelopment', 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show'
        }
        template_name = 'trainingdevelopment_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def trainingdevelopment_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view trainingdevelopment')
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
            "screen_name": 'TrainingDevelopment', 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show'
        }
        template_name = 'trainingdevelopment_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def trainingdevelopment_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa trainingdevelopment')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'TrainingDevelopment',
            "trainingdevelopment_id":pk
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
                    'model_name':'TrainingDevelopment',
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
                    return redirect('trainingdevelopment_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('trainingdevelopment_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data TrainingDevelopment')
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
                    return redirect('trainingdevelopment_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('trainingdevelopment_list')
            
            form = TrainingDevelopmentTempPAForm(request.POST, inintial=master_view['trainingdevelopment'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'TrainingDevelopment'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('trainingdevelopment_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'TrainingDevelopment', 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show'
                }
                template_name = 'trainingdevelopment_create.html'
                return render(request, template_name, context)
        else:
            #form = TrainingDevelopmentTempPAForm(initial=master_view['TrainingDevelopment'])
            form = TrainingDevelopmentTempPAForm(
                initial={**master_view['trainingdevelopment'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'TrainingDevelopment',
            "pa": True, 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'trainingdevelopment_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def trainingdevelopment_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'TrainingDevelopment'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('trainingdevelopment_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('trainingdevelopment_list')
        

        MSID= get_service_plan('view trainingdevelopment tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "trainingdevelopment_id":code
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
 
        MSID= get_service_plan('view trainingdevelopment live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "trainingdevelopment_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update trainingdevelopment temp')
            if MSID is None:
                print('MISID not found')
            form = TrainingDevelopmentTempUpdateForm(request.POST,)
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
                    return redirect('trainingdevelopment_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = TrainingDevelopmentLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = TrainingDevelopmentTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'TrainingDevelopment', 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show'
            }
            template_name = 'trainingdevelopment_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def trainingdevelopment_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view trainingdevelopment single')
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
        form = TrainingDevelopmentLiveForm(initial=record)  

        if record:
            form = TrainingDevelopmentLiveForm(initial=record)
        else:
            form = TrainingDevelopmentLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'TrainingDevelopment', 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show'
        }
        template_name = 'trainingdevelopment_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def trainingdevelopment_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'TrainingDevelopment'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('trainingdevelopment_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('trainingdevelopment_list')
        
        MSID= get_service_plan('delete trainingdevelopment')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'TrainingDevelopment',
            "trainingdevelopment_id":pk       
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
            return redirect('trainingdevelopment_list')
        if workflow_authorize is True:
            return redirect('trainingdevelopment_list')

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
                    'model_name':'TrainingDevelopment'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('trainingdevelopment_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('trainingdevelopment_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete TrainingDevelopment')
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
                    return redirect('trainingdevelopment_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('trainingdevelopment_list')
            
            form = TrainingDevelopmentTempPAForm(request.POST, inintial=record['TrainingDevelopment'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'TrainingDevelopment'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('trainingdevelopment_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'trainingdevelopment_create.html'
                return render(request, template_name, context)
        else:
            #form = TrainingDevelopmentTempPAForm(initial=record)
            form = TrainingDevelopmentTempPAForm(
                initial={**record['TrainingDevelopment'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'TrainingDevelopment',
            'data':record,
            "pa": True, 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'trainingdevelopment_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def trainingdevelopment_authorize_request(request, pk):
    """
    Processes a request to update an existing TrainingDevelopment entry and move it to the live table.
    Retrieves the entry from TrainingDevelopmentTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to TrainingDevelopmentLive
    and an optional history record is created in TrainingDevelopmentHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the TrainingDevelopment entry to be processed.

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
                'model_name':'TrainingDevelopment'
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
                return redirect('trainingdevelopment_list') 
            return redirect('trainingdevelopment_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'trainingdevelopment_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def staffturnover_create(request):
    try:
        token = request.session['user_token']
        form=StaffTurnoverLiveForm()
        

        if request.method == 'POST':
            form = StaffTurnoverLiveForm(request.POST,)
            temp_form = StaffTurnoverTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create staffturnover')
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
                    return redirect('staffturnover_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'StaffTurnover', 'staffturnover': 'active', 'staffturnover_show': 'show'
        }
        template_name = 'staffturnover_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffturnover_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view staffturnover')
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
            "screen_name": 'StaffTurnover', 'staffturnover': 'active', 'staffturnover_show': 'show'
        }
        template_name = 'staffturnover_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffturnover_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa staffturnover')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'StaffTurnover',
            "staffturnover_id":pk
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
                    'model_name':'StaffTurnover',
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
                    return redirect('staffturnover_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('staffturnover_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data StaffTurnover')
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
                    return redirect('staffturnover_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('staffturnover_list')
            
            form = StaffTurnoverTempPAForm(request.POST, inintial=master_view['staffturnover'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'StaffTurnover'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('staffturnover_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'StaffTurnover', 'staffturnover': 'active', 'staffturnover_show': 'show'
                }
                template_name = 'staffturnover_create.html'
                return render(request, template_name, context)
        else:
            #form = StaffTurnoverTempPAForm(initial=master_view['StaffTurnover'])
            form = StaffTurnoverTempPAForm(
                initial={**master_view['staffturnover'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'StaffTurnover',
            "pa": True, 'staffturnover': 'active', 'staffturnover_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'staffturnover_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffturnover_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'StaffTurnover'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('staffturnover_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('staffturnover_list')
        

        MSID= get_service_plan('view staffturnover tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "staffturnover_id":code
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
 
        MSID= get_service_plan('view staffturnover live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "staffturnover_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update staffturnover temp')
            if MSID is None:
                print('MISID not found')
            form = StaffTurnoverTempUpdateForm(request.POST,)
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
                    return redirect('staffturnover_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = StaffTurnoverLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = StaffTurnoverTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'StaffTurnover', 'staffturnover': 'active', 'staffturnover_show': 'show'
            }
            template_name = 'staffturnover_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffturnover_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view staffturnover single')
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
        form = StaffTurnoverLiveForm(initial=record)  

        if record:
            form = StaffTurnoverLiveForm(initial=record)
        else:
            form = StaffTurnoverLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'StaffTurnover', 'staffturnover': 'active', 'staffturnover_show': 'show'
        }
        template_name = 'staffturnover_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffturnover_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'StaffTurnover'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('staffturnover_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('staffturnover_list')
        
        MSID= get_service_plan('delete staffturnover')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'StaffTurnover',
            "staffturnover_id":pk       
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
            return redirect('staffturnover_list')
        if workflow_authorize is True:
            return redirect('staffturnover_list')

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
                    'model_name':'StaffTurnover'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('staffturnover_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('staffturnover_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete StaffTurnover')
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
                    return redirect('staffturnover_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('staffturnover_list')
            
            form = StaffTurnoverTempPAForm(request.POST, inintial=record['StaffTurnover'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'StaffTurnover'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('staffturnover_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'staffturnover_create.html'
                return render(request, template_name, context)
        else:
            #form = StaffTurnoverTempPAForm(initial=record)
            form = StaffTurnoverTempPAForm(
                initial={**record['StaffTurnover'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'StaffTurnover',
            'data':record,
            "pa": True, 'staffturnover': 'active', 'staffturnover_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'staffturnover_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def staffturnover_authorize_request(request, pk):
    """
    Processes a request to update an existing StaffTurnover entry and move it to the live table.
    Retrieves the entry from StaffTurnoverTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to StaffTurnoverLive
    and an optional history record is created in StaffTurnoverHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the StaffTurnover entry to be processed.

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
                'model_name':'StaffTurnover'
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
                return redirect('staffturnover_list') 
            return redirect('staffturnover_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'staffturnover_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})
