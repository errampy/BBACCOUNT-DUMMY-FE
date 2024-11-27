from django.urls import path,include
from .views import *

urlpatterns = [
    # Sequence URLs
    path('sequences/', sequence_list, name='sequence_list'),
    path('sequences-create/', sequence_create, name='sequence_create'),
    path('sequences-update/<int:pk>/', sequence_update, name='sequence_update'),
    path('sequences-delete/<int:pk>/', sequence_delete, name='sequence_delete'),
    path('get-next-sequence/', get_next_sequence, name='get_next_sequence'),
    

    # WorkflowCategory URLs
    path('workflow_categories/', workflow_category_list, name='workflow_category_list'),
    path('workflow_categories-create/', workflow_category_create, name='workflow_category_create'),
    path('workflow_categories-update/<str:pk>/', workflow_category_update, name='workflow_category_update'),
    path('workflow_categories-delete/<str:pk>/', workflow_category_delete, name='workflow_category_delete'),
    # path('workflow_categories-view/<str:pk>/', workflow_category_delete, name='workflow_category_view'),

    # WorkflowGroup URLs
    path('workflow_groups/', workflow_group_list, name='workflow_group_list'),
    path('workflow_groups-create/', workflow_group_create, name='workflow_group_create'),
    path('workflow_groups-update/<str:pk>/', workflow_group_update, name='workflow_group_update'),
    path('workflow_groups-delete/<str:pk>/', workflow_group_delete, name='workflow_group_delete'),

    # WorkflowUserGroupMapping URLs
    path('user_group_mappings/', workflow_user_group_mapping_list, name='workflow_user_group_mapping_list'),
    path('user_group_mappings-create/', workflow_user_group_mapping_create, name='workflow_user_group_mapping_create'),
    path('user_group_mappings-update/<str:pk>/', workflow_user_group_mapping_update,
         name='workflow_user_group_mapping_update'),
    path('user_group_mappings-delete/<str:pk>/', workflow_user_group_mapping_delete,
         name='workflow_user_group_mapping_delete'),

    # WorkflowSetup URLs
    path('workflow_setups/', workflow_setup_list, name='workflow_setup_list'),
    path('workflow_setups-create/', workflow_setup_create, name='workflow_setup_create'),
    path('workflow_setups-update/<str:pk>/', workflow_setup_update, name='workflow_setup_update'),
    path('workflow_setups-delete/<str:pk>/', workflow_setup_delete, name='workflow_setup_delete'),

    #model registration
    path('workflow-models/', workflow_model_list, name='workflow_model_list'),
    path('workflow_mapping/update/<str:pk>/',workflow_mapping_update,name='workflow_mapping_update'),
    path('workflow_mapping/show_user/<str:pk>',show_users,name='show_user')

]