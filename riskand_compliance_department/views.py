
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


def compliance_create(request):
    try:
        token = request.session['user_token']
        form=ComplianceLiveForm()
        

        if request.method == 'POST':
            form = ComplianceLiveForm(request.POST,)
            temp_form = ComplianceTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create compliance')
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
                    return redirect('compliance_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'Compliance', 'compliance': 'active', 'compliance_show': 'show'
        }
        template_name = 'compliance_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def compliance_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view compliance')
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
            "screen_name": 'Compliance', 'compliance': 'active', 'compliance_show': 'show'
        }
        template_name = 'compliance_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def compliance_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa compliance')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'Compliance',
            "compliance_id":pk
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
                    'model_name':'Compliance',
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
                    return redirect('compliance_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('compliance_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data Compliance')
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
                    return redirect('compliance_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('compliance_list')
            
            form = ComplianceTempPAForm(request.POST, inintial=master_view['compliance'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'Compliance'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('compliance_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'Compliance', 'compliance': 'active', 'compliance_show': 'show'
                }
                template_name = 'compliance_create.html'
                return render(request, template_name, context)
        else:
            #form = ComplianceTempPAForm(initial=master_view['Compliance'])
            form = ComplianceTempPAForm(
                initial={**master_view['compliance'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'Compliance',
            "pa": True, 'compliance': 'active', 'compliance_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'compliance_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def compliance_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'Compliance'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('compliance_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('compliance_list')
        

        MSID= get_service_plan('view compliance tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "compliance_id":code
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
 
        MSID= get_service_plan('view compliance live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "compliance_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update compliance temp')
            if MSID is None:
                print('MISID not found')
            form = ComplianceTempUpdateForm(request.POST,)
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
                    return redirect('compliance_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = ComplianceLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = ComplianceTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'Compliance', 'compliance': 'active', 'compliance_show': 'show'
            }
            template_name = 'compliance_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def compliance_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view compliance single')
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
        form = ComplianceLiveForm(initial=record)  

        if record:
            form = ComplianceLiveForm(initial=record)
        else:
            form = ComplianceLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'Compliance', 'compliance': 'active', 'compliance_show': 'show'
        }
        template_name = 'compliance_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def compliance_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'Compliance'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('compliance_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('compliance_list')
        
        MSID= get_service_plan('delete compliance')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'Compliance',
            "compliance_id":pk       
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
            return redirect('compliance_list')
        if workflow_authorize is True:
            return redirect('compliance_list')

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
                    'model_name':'Compliance'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('compliance_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('compliance_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete Compliance')
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
                    return redirect('compliance_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('compliance_list')
            
            form = ComplianceTempPAForm(request.POST, inintial=record['Compliance'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'Compliance'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('compliance_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'compliance_create.html'
                return render(request, template_name, context)
        else:
            #form = ComplianceTempPAForm(initial=record)
            form = ComplianceTempPAForm(
                initial={**record['Compliance'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'Compliance',
            'data':record,
            "pa": True, 'compliance': 'active', 'compliance_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'compliance_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def compliance_authorize_request(request, pk):
    """
    Processes a request to update an existing Compliance entry and move it to the live table.
    Retrieves the entry from ComplianceTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to ComplianceLive
    and an optional history record is created in ComplianceHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the Compliance entry to be processed.

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
                'model_name':'Compliance'
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
                return redirect('compliance_list') 
            return redirect('compliance_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'compliance_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def fraudmonitoring_create(request):
    try:
        token = request.session['user_token']
        form=FraudMonitoringLiveForm()
        

        if request.method == 'POST':
            form = FraudMonitoringLiveForm(request.POST,)
            temp_form = FraudMonitoringTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create fraudmonitoring')
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
                    return redirect('fraudmonitoring_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'FraudMonitoring', 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show'
        }
        template_name = 'fraudmonitoring_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def fraudmonitoring_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view fraudmonitoring')
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
            "screen_name": 'FraudMonitoring', 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show'
        }
        template_name = 'fraudmonitoring_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def fraudmonitoring_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa fraudmonitoring')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'FraudMonitoring',
            "fraudmonitoring_id":pk
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
                    'model_name':'FraudMonitoring',
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
                    return redirect('fraudmonitoring_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('fraudmonitoring_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data FraudMonitoring')
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
                    return redirect('fraudmonitoring_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('fraudmonitoring_list')
            
            form = FraudMonitoringTempPAForm(request.POST, inintial=master_view['fraudmonitoring'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'FraudMonitoring'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('fraudmonitoring_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'FraudMonitoring', 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show'
                }
                template_name = 'fraudmonitoring_create.html'
                return render(request, template_name, context)
        else:
            #form = FraudMonitoringTempPAForm(initial=master_view['FraudMonitoring'])
            form = FraudMonitoringTempPAForm(
                initial={**master_view['fraudmonitoring'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'FraudMonitoring',
            "pa": True, 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'fraudmonitoring_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def fraudmonitoring_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'FraudMonitoring'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('fraudmonitoring_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('fraudmonitoring_list')
        

        MSID= get_service_plan('view fraudmonitoring tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "fraudmonitoring_id":code
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
 
        MSID= get_service_plan('view fraudmonitoring live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "fraudmonitoring_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update fraudmonitoring temp')
            if MSID is None:
                print('MISID not found')
            form = FraudMonitoringTempUpdateForm(request.POST,)
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
                    return redirect('fraudmonitoring_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = FraudMonitoringLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = FraudMonitoringTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'FraudMonitoring', 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show'
            }
            template_name = 'fraudmonitoring_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def fraudmonitoring_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view fraudmonitoring single')
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
        form = FraudMonitoringLiveForm(initial=record)  

        if record:
            form = FraudMonitoringLiveForm(initial=record)
        else:
            form = FraudMonitoringLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'FraudMonitoring', 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show'
        }
        template_name = 'fraudmonitoring_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def fraudmonitoring_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'FraudMonitoring'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('fraudmonitoring_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('fraudmonitoring_list')
        
        MSID= get_service_plan('delete fraudmonitoring')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'FraudMonitoring',
            "fraudmonitoring_id":pk       
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
            return redirect('fraudmonitoring_list')
        if workflow_authorize is True:
            return redirect('fraudmonitoring_list')

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
                    'model_name':'FraudMonitoring'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('fraudmonitoring_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('fraudmonitoring_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete FraudMonitoring')
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
                    return redirect('fraudmonitoring_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('fraudmonitoring_list')
            
            form = FraudMonitoringTempPAForm(request.POST, inintial=record['FraudMonitoring'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'FraudMonitoring'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('fraudmonitoring_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'fraudmonitoring_create.html'
                return render(request, template_name, context)
        else:
            #form = FraudMonitoringTempPAForm(initial=record)
            form = FraudMonitoringTempPAForm(
                initial={**record['FraudMonitoring'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'FraudMonitoring',
            'data':record,
            "pa": True, 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'fraudmonitoring_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def fraudmonitoring_authorize_request(request, pk):
    """
    Processes a request to update an existing FraudMonitoring entry and move it to the live table.
    Retrieves the entry from FraudMonitoringTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to FraudMonitoringLive
    and an optional history record is created in FraudMonitoringHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the FraudMonitoring entry to be processed.

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
                'model_name':'FraudMonitoring'
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
                return redirect('fraudmonitoring_list') 
            return redirect('fraudmonitoring_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'fraudmonitoring_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def riskassessment_create(request):
    try:
        token = request.session['user_token']
        form=RiskAssessmentLiveForm()
        

        if request.method == 'POST':
            form = RiskAssessmentLiveForm(request.POST,)
            temp_form = RiskAssessmentTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create riskassessment')
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
                    return redirect('riskassessment_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'RiskAssessment', 'riskassessment': 'active', 'riskassessment_show': 'show'
        }
        template_name = 'riskassessment_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def riskassessment_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view riskassessment')
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
            "screen_name": 'RiskAssessment', 'riskassessment': 'active', 'riskassessment_show': 'show'
        }
        template_name = 'riskassessment_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def riskassessment_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa riskassessment')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'RiskAssessment',
            "riskassessment_id":pk
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
                    'model_name':'RiskAssessment',
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
                    return redirect('riskassessment_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('riskassessment_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data RiskAssessment')
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
                    return redirect('riskassessment_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('riskassessment_list')
            
            form = RiskAssessmentTempPAForm(request.POST, inintial=master_view['riskassessment'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'RiskAssessment'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('riskassessment_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'RiskAssessment', 'riskassessment': 'active', 'riskassessment_show': 'show'
                }
                template_name = 'riskassessment_create.html'
                return render(request, template_name, context)
        else:
            #form = RiskAssessmentTempPAForm(initial=master_view['RiskAssessment'])
            form = RiskAssessmentTempPAForm(
                initial={**master_view['riskassessment'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'RiskAssessment',
            "pa": True, 'riskassessment': 'active', 'riskassessment_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'riskassessment_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def riskassessment_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'RiskAssessment'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('riskassessment_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('riskassessment_list')
        

        MSID= get_service_plan('view riskassessment tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "riskassessment_id":code
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
 
        MSID= get_service_plan('view riskassessment live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "riskassessment_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update riskassessment temp')
            if MSID is None:
                print('MISID not found')
            form = RiskAssessmentTempUpdateForm(request.POST,)
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
                    return redirect('riskassessment_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = RiskAssessmentLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = RiskAssessmentTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'RiskAssessment', 'riskassessment': 'active', 'riskassessment_show': 'show'
            }
            template_name = 'riskassessment_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def riskassessment_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view riskassessment single')
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
        form = RiskAssessmentLiveForm(initial=record)  

        if record:
            form = RiskAssessmentLiveForm(initial=record)
        else:
            form = RiskAssessmentLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'RiskAssessment', 'riskassessment': 'active', 'riskassessment_show': 'show'
        }
        template_name = 'riskassessment_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def riskassessment_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'RiskAssessment'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('riskassessment_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('riskassessment_list')
        
        MSID= get_service_plan('delete riskassessment')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'RiskAssessment',
            "riskassessment_id":pk       
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
            return redirect('riskassessment_list')
        if workflow_authorize is True:
            return redirect('riskassessment_list')

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
                    'model_name':'RiskAssessment'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('riskassessment_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('riskassessment_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete RiskAssessment')
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
                    return redirect('riskassessment_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('riskassessment_list')
            
            form = RiskAssessmentTempPAForm(request.POST, inintial=record['RiskAssessment'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'RiskAssessment'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('riskassessment_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'riskassessment_create.html'
                return render(request, template_name, context)
        else:
            #form = RiskAssessmentTempPAForm(initial=record)
            form = RiskAssessmentTempPAForm(
                initial={**record['RiskAssessment'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'RiskAssessment',
            'data':record,
            "pa": True, 'riskassessment': 'active', 'riskassessment_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'riskassessment_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def riskassessment_authorize_request(request, pk):
    """
    Processes a request to update an existing RiskAssessment entry and move it to the live table.
    Retrieves the entry from RiskAssessmentTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to RiskAssessmentLive
    and an optional history record is created in RiskAssessmentHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the RiskAssessment entry to be processed.

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
                'model_name':'RiskAssessment'
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
                return redirect('riskassessment_list') 
            return redirect('riskassessment_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'riskassessment_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})
