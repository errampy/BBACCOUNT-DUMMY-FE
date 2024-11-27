from django import forms

class SequenceForm(forms.Form):
    sequence_series = forms.IntegerField(
        label="Sequence Series",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter sequence number',"class": "form-control"})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'placeholder': 'Enter description', 'rows': 3, 'maxlength': 100,"class": "form-control"})
    )


class WorkflowCategoryForm(forms.Form):
    code = forms.CharField(
        label="Code",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Code number', "class": "form-control"})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'placeholder': 'Enter description', 'rows': 3, 'maxlength': 100, "class": "form-control"})
    )


class WorkflowGroupForm(forms.Form):
    code = forms.CharField(
        label="Code",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Code number', "class": "form-control"})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'placeholder': 'Enter description', 'rows': 3, 'maxlength': 100, "class": "form-control"})
    )


class WorkflowUserGroupMappingForm(forms.Form):
    workflow_group = forms.CharField(label="Workflow Group")
    user = forms.CharField(label="User")
    sequence = forms.CharField(label="Sequence")


class WorkflowSetupForm(forms.Form):
    code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter workflow code'}))
    description = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter description'}))
    category = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Category'}))
    enabled = forms.BooleanField(required=False, initial=False)
    approver_type = forms.ChoiceField(
        choices=[
            ('Approver', 'Approver'),
            ('Workflow_User_Group', 'Workflow User Group')
        ],
        required=True
    )
    approver_limit_type = forms.ChoiceField(
        choices=[
            ('Specific_Approver', 'Specific Approver'),
            ('Group_Approver', 'Group Approver')
        ],
        required=False
    )
    approver_id = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter appprover code'}))
    user_group_mapping = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter user group mapping'}))



#======================12-11-24===================================

class WorkflowMappingForm(forms.Form):
    WORKFLOW_TYPE = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete')
    )
    
    #table_name = forms.CharField(max_length=20,required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Table Name'}))
    self_authorized = forms.BooleanField(
        required=False,
        label="Self Authorized"
    )
    same_user_authorized = forms.BooleanField(
        required=False,
        label="Same User Authorized"
    )
    send_to_authorized = forms.BooleanField(
        required=False,
        label="Send to Authorized"
    )
    workflow = forms.CharField(max_length=20,required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter Workflow'}))

    workflow_authorize = forms.BooleanField(
        required=False,
        label="Workflow Authorize"
    )
 