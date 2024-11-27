
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


def dataaccuracy_create(request):
    try:
        token = request.session['user_token']
        form=DataAccuracyLiveForm()
        

        if request.method == 'POST':
            form = DataAccuracyLiveForm(request.POST,)
            temp_form = DataAccuracyTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create dataaccuracy')
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
                    return redirect('dataaccuracy_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'DataAccuracy', 'dataaccuracy': 'active', 'dataaccuracy_show': 'show'
        }
        template_name = 'dataaccuracy_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def dataaccuracy_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view dataaccuracy')
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
            "screen_name": 'DataAccuracy', 'dataaccuracy': 'active', 'dataaccuracy_show': 'show'
        }
        template_name = 'dataaccuracy_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def dataaccuracy_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa dataaccuracy')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'DataAccuracy',
            "dataaccuracy_id":pk
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
                    'model_name':'DataAccuracy',
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
                    return redirect('dataaccuracy_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('dataaccuracy_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data DataAccuracy')
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
                    return redirect('dataaccuracy_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('dataaccuracy_list')
            
            form = DataAccuracyTempPAForm(request.POST, inintial=master_view['dataaccuracy'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'DataAccuracy'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('dataaccuracy_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'DataAccuracy', 'dataaccuracy': 'active', 'dataaccuracy_show': 'show'
                }
                template_name = 'dataaccuracy_create.html'
                return render(request, template_name, context)
        else:
            #form = DataAccuracyTempPAForm(initial=master_view['DataAccuracy'])
            form = DataAccuracyTempPAForm(
                initial={**master_view['dataaccuracy'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'DataAccuracy',
            "pa": True, 'dataaccuracy': 'active', 'dataaccuracy_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'dataaccuracy_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def dataaccuracy_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'DataAccuracy'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('dataaccuracy_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('dataaccuracy_list')
        

        MSID= get_service_plan('view dataaccuracy tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "dataaccuracy_id":code
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
 
        MSID= get_service_plan('view dataaccuracy live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "dataaccuracy_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update dataaccuracy temp')
            if MSID is None:
                print('MISID not found')
            form = DataAccuracyTempUpdateForm(request.POST,)
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
                    return redirect('dataaccuracy_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = DataAccuracyLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = DataAccuracyTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'DataAccuracy', 'dataaccuracy': 'active', 'dataaccuracy_show': 'show'
            }
            template_name = 'dataaccuracy_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def dataaccuracy_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view dataaccuracy single')
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
        form = DataAccuracyLiveForm(initial=record)  

        if record:
            form = DataAccuracyLiveForm(initial=record)
        else:
            form = DataAccuracyLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'DataAccuracy', 'dataaccuracy': 'active', 'dataaccuracy_show': 'show'
        }
        template_name = 'dataaccuracy_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def dataaccuracy_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'DataAccuracy'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('dataaccuracy_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('dataaccuracy_list')
        
        MSID= get_service_plan('delete dataaccuracy')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'DataAccuracy',
            "dataaccuracy_id":pk       
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
            return redirect('dataaccuracy_list')
        if workflow_authorize is True:
            return redirect('dataaccuracy_list')

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
                    'model_name':'DataAccuracy'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('dataaccuracy_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('dataaccuracy_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete DataAccuracy')
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
                    return redirect('dataaccuracy_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('dataaccuracy_list')
            
            form = DataAccuracyTempPAForm(request.POST, inintial=record['DataAccuracy'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'DataAccuracy'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('dataaccuracy_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'dataaccuracy_create.html'
                return render(request, template_name, context)
        else:
            #form = DataAccuracyTempPAForm(initial=record)
            form = DataAccuracyTempPAForm(
                initial={**record['DataAccuracy'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'DataAccuracy',
            'data':record,
            "pa": True, 'dataaccuracy': 'active', 'dataaccuracy_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'dataaccuracy_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def dataaccuracy_authorize_request(request, pk):
    """
    Processes a request to update an existing DataAccuracy entry and move it to the live table.
    Retrieves the entry from DataAccuracyTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to DataAccuracyLive
    and an optional history record is created in DataAccuracyHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the DataAccuracy entry to be processed.

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
                'model_name':'DataAccuracy'
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
                return redirect('dataaccuracy_list') 
            return redirect('dataaccuracy_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'dataaccuracy_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def systemuptime_create(request):
    try:
        token = request.session['user_token']
        form=SystemUptimeLiveForm()
        

        if request.method == 'POST':
            form = SystemUptimeLiveForm(request.POST,)
            temp_form = SystemUptimeTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create systemuptime')
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
                    return redirect('systemuptime_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'SystemUptime', 'systemuptime': 'active', 'systemuptime_show': 'show'
        }
        template_name = 'systemuptime_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def systemuptime_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view systemuptime')
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
            "screen_name": 'SystemUptime', 'systemuptime': 'active', 'systemuptime_show': 'show'
        }
        template_name = 'systemuptime_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def systemuptime_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa systemuptime')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'SystemUptime',
            "systemuptime_id":pk
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
                    'model_name':'SystemUptime',
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
                    return redirect('systemuptime_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('systemuptime_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data SystemUptime')
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
                    return redirect('systemuptime_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('systemuptime_list')
            
            form = SystemUptimeTempPAForm(request.POST, inintial=master_view['systemuptime'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'SystemUptime'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('systemuptime_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'SystemUptime', 'systemuptime': 'active', 'systemuptime_show': 'show'
                }
                template_name = 'systemuptime_create.html'
                return render(request, template_name, context)
        else:
            #form = SystemUptimeTempPAForm(initial=master_view['SystemUptime'])
            form = SystemUptimeTempPAForm(
                initial={**master_view['systemuptime'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'SystemUptime',
            "pa": True, 'systemuptime': 'active', 'systemuptime_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'systemuptime_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def systemuptime_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'SystemUptime'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('systemuptime_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('systemuptime_list')
        

        MSID= get_service_plan('view systemuptime tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "systemuptime_id":code
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
 
        MSID= get_service_plan('view systemuptime live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "systemuptime_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update systemuptime temp')
            if MSID is None:
                print('MISID not found')
            form = SystemUptimeTempUpdateForm(request.POST,)
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
                    return redirect('systemuptime_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = SystemUptimeLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = SystemUptimeTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'SystemUptime', 'systemuptime': 'active', 'systemuptime_show': 'show'
            }
            template_name = 'systemuptime_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def systemuptime_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view systemuptime single')
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
        form = SystemUptimeLiveForm(initial=record)  

        if record:
            form = SystemUptimeLiveForm(initial=record)
        else:
            form = SystemUptimeLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'SystemUptime', 'systemuptime': 'active', 'systemuptime_show': 'show'
        }
        template_name = 'systemuptime_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def systemuptime_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'SystemUptime'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('systemuptime_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('systemuptime_list')
        
        MSID= get_service_plan('delete systemuptime')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'SystemUptime',
            "systemuptime_id":pk       
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
            return redirect('systemuptime_list')
        if workflow_authorize is True:
            return redirect('systemuptime_list')

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
                    'model_name':'SystemUptime'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('systemuptime_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('systemuptime_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete SystemUptime')
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
                    return redirect('systemuptime_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('systemuptime_list')
            
            form = SystemUptimeTempPAForm(request.POST, inintial=record['SystemUptime'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'SystemUptime'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('systemuptime_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'systemuptime_create.html'
                return render(request, template_name, context)
        else:
            #form = SystemUptimeTempPAForm(initial=record)
            form = SystemUptimeTempPAForm(
                initial={**record['SystemUptime'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'SystemUptime',
            'data':record,
            "pa": True, 'systemuptime': 'active', 'systemuptime_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'systemuptime_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def systemuptime_authorize_request(request, pk):
    """
    Processes a request to update an existing SystemUptime entry and move it to the live table.
    Retrieves the entry from SystemUptimeTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to SystemUptimeLive
    and an optional history record is created in SystemUptimeHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the SystemUptime entry to be processed.

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
                'model_name':'SystemUptime'
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
                return redirect('systemuptime_list') 
            return redirect('systemuptime_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'systemuptime_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

def itticketresolution_create(request):
    try:
        token = request.session['user_token']
        form=ITTicketResolutionLiveForm()
        

        if request.method == 'POST':
            form = ITTicketResolutionLiveForm(request.POST,)
            temp_form = ITTicketResolutionTempForm(request.POST,)
            if form.is_valid() and temp_form.is_valid():
                MSID= get_service_plan('create itticketresolution')
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
                    return redirect('itticketresolution_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
            else:
                print('errorss',form.errors) 
    
        context = {
            "form": form,
            "screen_name": 'ITTicketResolution', 'itticketresolution': 'active', 'itticketresolution_show': 'show'
        }
        template_name = 'itticketresolution_create.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def itticketresolution_list(request):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('view itticketresolution')
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
            "screen_name": 'ITTicketResolution', 'itticketresolution': 'active', 'itticketresolution_show': 'show'
        }
        template_name = 'itticketresolution_list.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def itticketresolution_pa(request, pk):
    try:

        token = request.session['user_token']

        MSID= get_service_plan('pa itticketresolution')
        if MSID is None:
                print('MISID not found')
        payload_form = {
            'model_name':'ITTicketResolution',
            "itticketresolution_id":pk
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
                    'model_name':'ITTicketResolution',
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
                    return redirect('itticketresolution_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('itticketresolution_list')
     
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data ITTicketResolution')
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
                    return redirect('itticketresolution_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('itticketresolution_list')
            
            form = ITTicketResolutionTempPAForm(request.POST, inintial=master_view['itticketresolution'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'ITTicketResolution'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('itticketresolution_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'ITTicketResolution', 'itticketresolution': 'active', 'itticketresolution_show': 'show'
                }
                template_name = 'itticketresolution_create.html'
                return render(request, template_name, context)
        else:
            #form = ITTicketResolutionTempPAForm(initial=master_view['ITTicketResolution'])
            form = ITTicketResolutionTempPAForm(
                initial={**master_view['itticketresolution'],},
                 # Ensure list is passed
            )

        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'ITTicketResolution',
            "pa": True, 'itticketresolution': 'active', 'itticketresolution_show': 'show',
            'is_same_user_authorized': master_view['workflow_data']['same_user_authorized'],'is_send_to_authorize':master_view['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'itticketresolution_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def itticketresolution_update(request, code):
    try:

        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
             'code':code,
             'app_name':APP_NAME,
             'model_name':'ITTicketResolution'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('itticketresolution_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('itticketresolution_list')
        

        MSID= get_service_plan('view itticketresolution tempdata')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "itticketresolution_id":code
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
 
        MSID= get_service_plan('view itticketresolution live')
        if MSID is None:
            print('MISID not found')
        payload_form = {
            "itticketresolution_id":code
        }    
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
    
        master_type_live = response['data'][0]
        

        if request.method == 'POST':
            
            MSID= get_service_plan('update itticketresolution temp')
            if MSID is None:
                print('MISID not found')
            form = ITTicketResolutionTempUpdateForm(request.POST,)
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
                    return redirect('itticketresolution_list')
                else:
                    print('error i get',response['status_code'])
                    return render(request,'500.html',{'error':response['status_code']})  
            else:
                print(form.errors)
                return render(request,'500.html',{'error':form.errors})

        else:
            if master_type_live:
                form = ITTicketResolutionLiveUpdateForm(initial=master_type_live,)
            if master_type_temp and master_type_live:
                form = ITTicketResolutionTempUpdateForm(initial=master_type_temp,)

            context = {
                "message": "Update the details as needed.",
                "form": form,
                "screen_name": 'ITTicketResolution', 'itticketresolution': 'active', 'itticketresolution_show': 'show'
            }
            template_name = 'itticketresolution_update.html'
            return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def itticketresolution_view(request, code):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('view itticketresolution single')
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
        form = ITTicketResolutionLiveForm(initial=record)  

        if record:
            form = ITTicketResolutionLiveForm(initial=record)
        else:
            form = ITTicketResolutionLiveForm()
      
        context = {
            "message": "Update the details as needed.",
            "form": form,'view':True,
            "screen_name": 'ITTicketResolution', 'itticketresolution': 'active', 'itticketresolution_show': 'show'
        }
        template_name = 'itticketresolution_view.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})


def itticketresolution_delete(request, pk):
    try:
        token = request.session['user_token']
        MSID= get_service_plan('have permission')
        if MSID is None:
            print('MISID not found')
        payload_form = {   
            'code':pk,
            'app_name':APP_NAME,
            'model_name':'ITTicketResolution'
        }
        data={
            'ms_id':MSID,
            'ms_payload':payload_form
        }
        json_data = json.dumps(data)
        response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
        if response['status_code'] ==  1:   
            messages.success(request, 'Success')
            return redirect('itticketresolution_list')
        data=response['data'][0] 
        if data == False: 
            messages.success(request, 'Successfully')
            return redirect('itticketresolution_list')
        
        MSID= get_service_plan('delete itticketresolution')
        if MSID is None:
            print('MISID not found') 
        payload_form = {
            'model_name':'ITTicketResolution',
            "itticketresolution_id":pk       
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
            return redirect('itticketresolution_list')
        if workflow_authorize is True:
            return redirect('itticketresolution_list')

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
                    'model_name':'ITTicketResolution'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:                  
                    messages.info(request, "Well Done..! Application Submitted..")
                    return redirect('itticketresolution_list')
                else:
                    messages.info(request, "Oops..! Application Failed to Submitted..")
                    return redirect('itticketresolution_list')
                
            if send_to_authorized == 's2a':
                MSID= get_service_plan('authorize request data delete ITTicketResolution')
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
                    return redirect('itticketresolution_list')
                else:
                    messages.info(request, "Not Sent To authorization")
                    return redirect('itticketresolution_list')
            
            form = ITTicketResolutionTempPAForm(request.POST, inintial=record['ITTicketResolution'])
            if form.is_valid():

                MSID= get_service_plan('check with data')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                    "pk":pk,
                    'app_name':APP_NAME,
                    'model_name':'ITTicketResolution'
                }    
                data={
                    'ms_id':MSID,
                    'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                

                if response['status_code'] ==  0:                  
                    messages.info(request, "Sent for authorization")
                    return redirect('itticketresolution_list')
                else:
                    messages.info(request, "Error in maker checker validation")
                    print('Error in maker checker validation', )

                context = {
                    "message": 'You did not have access to approve this record',
                    "screen_name": 'country', 'country': 'active', 'country_show': 'show'
                }
                template_name = 'itticketresolution_create.html'
                return render(request, template_name, context)
        else:
            #form = ITTicketResolutionTempPAForm(initial=record)
            form = ITTicketResolutionTempPAForm(
                initial={**record['ITTicketResolution'],},
                 # Ensure list is passed
            )
      
        context = {
            "message": "Update the details as needed.",
            "form": form, 'user_record': user_data,
            "screen_name": 'ITTicketResolution',
            'data':record,
            "pa": True, 'itticketresolution': 'active', 'itticketresolution_show': 'show',
            'is_same_user_authorized': record['workflow_data']['same_user_authorized'],'is_send_to_authorize':record['workflow_data']['send_to_authorized'], 'code': pk,
        }
        print('context ', context)
        template_name = 'itticketresolution_delete.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})

            

def itticketresolution_authorize_request(request, pk):
    """
    Processes a request to update an existing ITTicketResolution entry and move it to the live table.
    Retrieves the entry from ITTicketResolutionTemp by primary key and processes form submission
    to update it. On successful form submission, the record is moved to ITTicketResolutionLive
    and an optional history record is created in ITTicketResolutionHistory.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the ITTicketResolution entry to be processed.

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
                'model_name':'ITTicketResolution'
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
                return redirect('itticketresolution_list') 
            return redirect('itticketresolution_list')
        
        context = {
            'record_details': record_details,
            'is_for_authorize': True,
            'pk': pk,
            'table_name': table_name,
            'record_id': record_id
        }

        template_name = 'itticketresolution_create.html'
        return render(request, template_name, context)
    except Exception as error:
        return render(request,'500.html',{'error':error})
def accountsreceivableaging_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('accountsreceivableaging report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'AccountsReceivableAging', 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show','report':report_data
                    }
                    template_name = 'accountsreceivableagingreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'AccountsReceivableAging', 'accountsreceivableaging': 'active', 'accountsreceivableaging_show': 'show'
        }
        template_name = 'accountsreceivableagingreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def assetmanagement_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('assetmanagement report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'AssetManagement', 'assetmanagement': 'active', 'assetmanagement_show': 'show','report':report_data
                    }
                    template_name = 'assetmanagementreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'AssetManagement', 'assetmanagement': 'active', 'assetmanagement_show': 'show'
        }
        template_name = 'assetmanagementreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def balancesheet_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('balancesheet report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'BalanceSheet', 'balancesheet': 'active', 'balancesheet_show': 'show','report':report_data
                    }
                    template_name = 'balancesheetreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'BalanceSheet', 'balancesheet': 'active', 'balancesheet_show': 'show'
        }
        template_name = 'balancesheetreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def branchperformance_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('branchperformance report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'BranchPerformance', 'branchperformance': 'active', 'branchperformance_show': 'show','report':report_data
                    }
                    template_name = 'branchperformancereport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'BranchPerformance', 'branchperformance': 'active', 'branchperformance_show': 'show'
        }
        template_name = 'branchperformancereport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def cashflowstatement_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('cashflowstatement report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'CashFlowStatement', 'cashflowstatement': 'active', 'cashflowstatement_show': 'show','report':report_data
                    }
                    template_name = 'cashflowstatementreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'CashFlowStatement', 'cashflowstatement': 'active', 'cashflowstatement_show': 'show'
        }
        template_name = 'cashflowstatementreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def clientacquisition_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('clientacquisition report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'ClientAcquisition', 'clientacquisition': 'active', 'clientacquisition_show': 'show','report':report_data
                    }
                    template_name = 'clientacquisitionreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'ClientAcquisition', 'clientacquisition': 'active', 'clientacquisition_show': 'show'
        }
        template_name = 'clientacquisitionreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def clientoutreach_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('clientoutreach report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'ClientOutreach', 'clientoutreach': 'active', 'clientoutreach_show': 'show','report':report_data
                    }
                    template_name = 'clientoutreachreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'ClientOutreach', 'clientoutreach': 'active', 'clientoutreach_show': 'show'
        }
        template_name = 'clientoutreachreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def compliance_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('compliance report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'Compliance', 'compliance': 'active', 'compliance_show': 'show','report':report_data
                    }
                    template_name = 'compliancereport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'Compliance', 'compliance': 'active', 'compliance_show': 'show'
        }
        template_name = 'compliancereport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def customersatisfaction_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('customersatisfaction report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'CustomerSatisfaction', 'customersatisfaction': 'active', 'customersatisfaction_show': 'show','report':report_data
                    }
                    template_name = 'customersatisfactionreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'CustomerSatisfaction', 'customersatisfaction': 'active', 'customersatisfaction_show': 'show'
        }
        template_name = 'customersatisfactionreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def dataaccuracy_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('dataaccuracy report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'DataAccuracy', 'dataaccuracy': 'active', 'dataaccuracy_show': 'show','report':report_data
                    }
                    template_name = 'dataaccuracyreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'DataAccuracy', 'dataaccuracy': 'active', 'dataaccuracy_show': 'show'
        }
        template_name = 'dataaccuracyreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def feedbackandcomplaints_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('feedbackandcomplaints report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'FeedbackAndComplaints', 'feedbackandcomplaints': 'active', 'feedbackandcomplaints_show': 'show','report':report_data
                    }
                    template_name = 'feedbackandcomplaintsreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'FeedbackAndComplaints', 'feedbackandcomplaints': 'active', 'feedbackandcomplaints_show': 'show'
        }
        template_name = 'feedbackandcomplaintsreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def fraudmonitoring_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('fraudmonitoring report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'FraudMonitoring', 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show','report':report_data
                    }
                    template_name = 'fraudmonitoringreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'FraudMonitoring', 'fraudmonitoring': 'active', 'fraudmonitoring_show': 'show'
        }
        template_name = 'fraudmonitoringreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def incomestatement_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('incomestatement report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'IncomeStatement', 'incomestatement': 'active', 'incomestatement_show': 'show','report':report_data
                    }
                    template_name = 'incomestatementreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'IncomeStatement', 'incomestatement': 'active', 'incomestatement_show': 'show'
        }
        template_name = 'incomestatementreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def itticketresolution_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('itticketresolution report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'ITTicketResolution', 'itticketresolution': 'active', 'itticketresolution_show': 'show','report':report_data
                    }
                    template_name = 'itticketresolutionreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'ITTicketResolution', 'itticketresolution': 'active', 'itticketresolution_show': 'show'
        }
        template_name = 'itticketresolutionreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def leavemanagement_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('leavemanagement report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'LeaveManagement', 'leavemanagement': 'active', 'leavemanagement_show': 'show','report':report_data
                    }
                    template_name = 'leavemanagementreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'LeaveManagement', 'leavemanagement': 'active', 'leavemanagement_show': 'show'
        }
        template_name = 'leavemanagementreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def loanaging_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('loanaging report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'LoanAging', 'loanaging': 'active', 'loanaging_show': 'show','report':report_data
                    }
                    template_name = 'loanagingreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'LoanAging', 'loanaging': 'active', 'loanaging_show': 'show'
        }
        template_name = 'loanagingreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def loandisbursement_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('loandisbursement report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'LoanDisbursement', 'loandisbursement': 'active', 'loandisbursement_show': 'show','report':report_data
                    }
                    template_name = 'loandisbursementreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'LoanDisbursement', 'loandisbursement': 'active', 'loandisbursement_show': 'show'
        }
        template_name = 'loandisbursementreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def loanlossprovision_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('loanlossprovision report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'LoanLossProvision', 'loanlossprovision': 'active', 'loanlossprovision_show': 'show','report':report_data
                    }
                    template_name = 'loanlossprovisionreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'LoanLossProvision', 'loanlossprovision': 'active', 'loanlossprovision_show': 'show'
        }
        template_name = 'loanlossprovisionreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def logisticsandfleetmanagement_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('logisticsandfleetmanagement report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'LogisticsAndFleetManagement', 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show','report':report_data
                    }
                    template_name = 'logisticsandfleetmanagementreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'LogisticsAndFleetManagement', 'logisticsandfleetmanagement': 'active', 'logisticsandfleetmanagement_show': 'show'
        }
        template_name = 'logisticsandfleetmanagementreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def officeexpense_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('officeexpense report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'OfficeExpense', 'officeexpense': 'active', 'officeexpense_show': 'show','report':report_data
                    }
                    template_name = 'officeexpensereport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'OfficeExpense', 'officeexpense': 'active', 'officeexpense_show': 'show'
        }
        template_name = 'officeexpensereport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def portfolioquality_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('portfolioquality report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'PortfolioQuality', 'portfolioquality': 'active', 'portfolioquality_show': 'show','report':report_data
                    }
                    template_name = 'portfolioqualityreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'PortfolioQuality', 'portfolioquality': 'active', 'portfolioquality_show': 'show'
        }
        template_name = 'portfolioqualityreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def riskassessment_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('riskassessment report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'RiskAssessment', 'riskassessment': 'active', 'riskassessment_show': 'show','report':report_data
                    }
                    template_name = 'riskassessmentreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'RiskAssessment', 'riskassessment': 'active', 'riskassessment_show': 'show'
        }
        template_name = 'riskassessmentreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffproductivity_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('staffproductivity report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'StaffProductivity', 'staffproductivity': 'active', 'staffproductivity_show': 'show','report':report_data
                    }
                    template_name = 'staffproductivityreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'StaffProductivity', 'staffproductivity': 'active', 'staffproductivity_show': 'show'
        }
        template_name = 'staffproductivityreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def staffturnover_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('staffturnover report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'StaffTurnover', 'staffturnover': 'active', 'staffturnover_show': 'show','report':report_data
                    }
                    template_name = 'staffturnoverreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'StaffTurnover', 'staffturnover': 'active', 'staffturnover_show': 'show'
        }
        template_name = 'staffturnoverreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def systemuptime_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('systemuptime report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'SystemUptime', 'systemuptime': 'active', 'systemuptime_show': 'show','report':report_data
                    }
                    template_name = 'systemuptimereport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'SystemUptime', 'systemuptime': 'active', 'systemuptime_show': 'show'
        }
        template_name = 'systemuptimereport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


def trainingdevelopment_report(request):
    try:
        token = request.session['user_token']

        if request.method == 'POST':
                from_date=request.POST.get('from_date')
                to_date=request.POST.get('to_date')

                MSID= get_service_plan('trainingdevelopment report')
                if MSID is None:
                        print('MISID not found')
                payload_form = {
                        'from_date':from_date,
                        'to_date':to_date
                }    
                data={
                'ms_id':MSID,
                'ms_payload':payload_form
                }
                json_data = json.dumps(data)
                response = call_post_method_with_token_v2(BASEURL,ENDPOINT,json_data,token)
                if response['status_code'] ==  0:   
                    report_data=response['data']               
                   
                    context = {
                    "screen_name": 'TrainingDevelopment', 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show','report':report_data
                    }
                    template_name = 'trainingdevelopmentreport_report.html'
                    return render(request, template_name, context)
                else:
                    messages.info(request, "Data's Not Found")
        context = {
                "screen_name": 'TrainingDevelopment', 'trainingdevelopment': 'active', 'trainingdevelopment_show': 'show'
        }
        template_name = 'trainingdevelopmentreport_report.html'
        return render(request, template_name, context)

    except Exception as error:
        return render(request,'500.html',{'error':error})


