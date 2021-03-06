import os
import logging

# ------------------------------------------------------------------------------------------------------------------
# Development settings for environment variables
# ------------------------------------------------------------------------------------------------------------------

if not os.getenv('AUTH_SERVICE_HOST'):
    os.environ['AUTH_SERVICE_HOST'] = '0.0.0.0'
    os.environ['AUTH_SERVICE_PORT'] = '5000'

if not os.getenv('COMPUTE_SERVICE_HOST'):
    os.environ['COMPUTE_SERVICE_HOST'] = '0.0.0.0'
    os.environ['COMPUTE_SERVICE_PORT'] = '5001'

if not os.getenv('STORAGE_SERVICE_HOST'):
    os.environ['STORAGE_SERVICE_HOST'] = '192.168.99.100'
    os.environ['STORAGE_SERVICE_PORT'] = '5002'

if not os.getenv('BROKER_URL'):
    os.environ['BROKER_URL'] = 'amqp://guest:guest@192.168.99.100:5672//'

if not os.getenv('CELERY_RESULT_BACKEND'):
    os.environ['CELERY_RESULT_BACKEND'] = 'redis://192.168.99.100:6379/0'

# ------------------------------------------------------------------------------------------------------------------
# Log settings
# ------------------------------------------------------------------------------------------------------------------

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# ------------------------------------------------------------------------------------------------------------------
# Flask settings
# ------------------------------------------------------------------------------------------------------------------

PROPAGATE_EXCEPTIONS = True
RESTFUL_JSON = {'indent': 2, 'sort_keys': True}

# ------------------------------------------------------------------------------------------------------------------
# Celery settings
# ------------------------------------------------------------------------------------------------------------------

BROKER_URL = os.getenv('BROKER_URL')

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_CHORD_PROPAGATES = True

# ------------------------------------------------------------------------------------------------------------------
# Pipelines
# ------------------------------------------------------------------------------------------------------------------

PIPELINES = {
    'svm_train': {
        'display_name': 'Support Vector Machine (Training)',
        'module_path': 'service.compute.pipelines.stats.classification.svm_train',
        'tasks_module_path': 'service.compute.pipelines.stats.classification.svm_train',
        'class_name': 'SupportVectorMachineTraining',
        'params': {
            'file_id': {'type': 'int', 'min_value': 1},
            'subject_labels': {'type': 'str_list', 'min_length': 10},
            'nr_folds': {'type': 'int', 'min_value': 2, 'default': 10},
            'index_column': {'type': 'str'},
            'target_column': {'type': 'str'},
            'excluded_columns': {'type': 'str_list', 'default': []},
            'kernel': {'type': 'str', 'allowed_values': ['linear', 'rbf', 'poly'], 'default': 'rbf'},
            'repository_id': {'type': 'int', 'min_value': 1},
        },
        'outputs': {
            'accuracy': {'type': 'int'},
            'C': {'type': 'float'},
            'gamma': {'type': 'float'},
            'classifier_id': {'type': 'str'},
        },
    },
    'svm_predict': {
        'display_name': 'Support Vector Machine (Prediction)',
        'module_path': 'service.compute.pipelines.stats.classification.svm_predict',
        'tasks_module_path': 'service.compute.pipelines.stats.classification.svm_predict',
        'class_name': 'SupportVectorMachinePrediction',
        'params': {},
        'outputs': {},
    },
}

# ------------------------------------------------------------------------------------------------------------------
# Security settings
# ------------------------------------------------------------------------------------------------------------------

SERVICE_USERNAME = 'compute'
SERVICE_PASSWORD = 'secret'
SERVICE_WORKER_USERNAME = 'worker'
SERVICE_WORKER_PASSWORD = 'secret'
