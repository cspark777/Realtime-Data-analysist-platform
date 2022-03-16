def choice_to_value_name(choices):
    value_name_list = []
    length = len(choices[0]) if choices else 0
    if length == 3:
        for value, name, description in choices:
            value_name_list.append({'value': value, 'name': name, 'description': description})
    elif length == 2:
        for value, name in choices:
            value_name_list.append({'value': value, 'name': name})
    return value_name_list


INBOUND = 'inbound'
INBOUNDTIMER = 'inboundtimer'
INBOUNDHTTP = 'inboundttp'
INBOUNDKPI = 'inboundkpi'
OUTBOUND = 'outbound'
OUTBOUNDEMAIL = 'outboundemail'
OUTBOUNDSMS = 'outboundsms'
OUTBOUNDWEB = 'outboundweb'
FILTER = 'filter'
SELECTFIELDS = 'select'
COMPLEX = 'complex'
MAP = 'map'
MAP_EVENT = 'map_event'
EVENT = 'event'
LOOKUP = 'lookup'
EXECUTE_SEARCH = 'execute_search'
LOOKUP_MULTI_VALUE = 'lookup_multi_value'
KEY = 'key'
WORKFLOW = 'workflow'
SENTIMENT = 'sentiment'
TRANSCRIBE = 'transcribe'
EXTERNAL = 'external'
FIELD_ADD = 'add'
FIELD_REMOVE = 'remove'
FIELD_COPY = 'copy'
FIELD_RENAME = 'rename'
FUNCTION = 'function'
SLEEP = 'sleep'
PYTHON = 'python'
RESET = 'reset'
DICT = 'dict'
ADJUST = 'adjust'
VALUE = 'value'
STEP_TYPES = (
    (INBOUND, 'Inbound Event - Stream', 'Begin Stream Processing Based On Inbound Events From Kafka'),
    (INBOUNDTIMER, 'Inbound Event - Timer Task', 'Begin Stream Processing Based On A Timer'),
    (INBOUNDHTTP, 'Inbound Event - Load From API', 'Begin Stream Processing Based On Inbound API Call'),
    (INBOUNDKPI, 'Inbound Event - KPI Change', 'Begin Stream Processing Based On A KPI Change'),

    (OUTBOUND, 'Outbound Event - Stream', 'End Stream Processing By Placing Message Onto A Stream'),
    (OUTBOUNDEMAIL, 'Outbound Event - E-Mail', 'End Stream Processing By Sending An Email'),
    (OUTBOUNDSMS, 'Outbound Event - SMS', 'End Stream Processing By Sending an SMS'),
    (OUTBOUNDWEB, 'Outbound Event - API Call', 'End Stream Processing By Calling An Outbound API'),

    (FILTER, 'Processor - Simple Filter', 'Filter The Event Stream'),
    # (COMPLEX, 'Processor - Complex Filter', 'placeholder'),
    (LOOKUP, 'Processor - Stream Lookup', 'Lookup Events From A Stream'),
    (EXECUTE_SEARCH, 'Processor - Execute Search', 'Execute A Saved Search'),
    (FUNCTION, 'Processor - Execute Function', 'Execute A DATA Function'),
    (SELECTFIELDS, 'Processor - Select Fields', 'Select Fields From The Event'),
    (MAP, 'Processor - Map Function', 'Process A Field Within the Event'),
    
    (KEY, 'Processor - Record Key Performance Indicator', 'Record a KPI Or Metric'),
    (WORKFLOW, 'Processor - Create Workflow Task', 'Create A Workflow Task'),
    (SENTIMENT, 'Processor - AWS Comprehend Sentiment Analysis', 'Sentiment Analysis Of Text Data'),
    (TRANSCRIBE, 'Processor - Transcribe Audio', 'Transcribe An Audio File'),
    (EVENT, 'Processor - Create New Event Of Type', 'Create A New Type Of Event In The Stream'),
    (MAP_EVENT, 'Processor - Map Event To Event Type', 'Change The Type Of Event In The Stream'),
    (EXTERNAL, 'Processor - External API Call', 'Execute An External API Call'),
    (FIELD_ADD, 'Processor - Add Or Update Field', 'Add Or Update Field On The Event'),
    (FIELD_REMOVE, 'Processor - Remove Field', 'Remove A Field From The Event'),
    (FIELD_COPY, 'Processor - Copy Field', 'Copy Values Between Fields'),
    # (FIELD_RENAME, 'Processor - Rename Field', 'placeholder'),
    (SLEEP, 'Processor - Sleep Step', 'Sleep For Specified Period'),
    # (PYTHON, 'Processor - Python Step', 'placeholder'),
    (RESET, 'Processor - Reset Timestamp', 'Reset A Timestamp Field'),
    (DICT, 'Processor - Data Dictionary Lookup & Replace', 'Replace A Value Using A Data Dictionary'),
    (ADJUST, 'Processor - Perform Calculation', 'Perform A Calculation'),
    # (VALUE, 'Processor - If Value In Set', 'placeholder'),
)

ONE = 'one'
FROM_EVENT = 'from_event'
STATIC_VALUE = 'static_value'
FROM_VARIABLE = 'from_variable'

KEY_TYPES = (
    (FROM_EVENT, 'A Value From Event'),
    (STATIC_VALUE, 'A Static Value'),
)

INCREMENT_KEY_TYPES = (
    (ONE, 'Increment By One'),
    (FROM_EVENT, 'Increment By A Value From The Event'),
    (STATIC_VALUE, 'Increment By A Static Value')
)

UPDATE_KEY_TYPES = (
    (FROM_EVENT, 'Update To Value From event'),
    (STATIC_VALUE, 'Update To Static Value'),
    (FROM_VARIABLE, 'Update To Registered Variable'),
)

FILTER_KEY_TYPES = (
    (STATIC_VALUE, 'A Static Value'),
    (FROM_EVENT, 'A Value From Event'),
    (FROM_VARIABLE, 'A Value From A Registered Variable'),
)

FILTER_KEY_TYPES_REV = (
    (FROM_EVENT, 'A Value From Event'),
    (STATIC_VALUE, 'A Static Value'),
    (FROM_VARIABLE, 'A Value From A Registered Variable'),
)

MAP_KEY_TYPES = (
    (STATIC_VALUE, 'A Static Value'),
    (FROM_VARIABLE, 'A Value From A Registered Variable'),
)

AGGREGATE = 'aggregate'
JOIN = 'join'
JOININBOUND = 'joininbound'
REPLACE = 'replace'
RESULT_PLACEMENTS = (
    (AGGREGATE, 'Aggregate Results'),
    # (JOIN, 'Join Results To Inbound'),
    # (JOININBOUND, 'Join Inbound To Results'),
    (REPLACE, 'Replace Inbound Event With Results'),
)

SUM = 'sum'
COUNT = 'count'
MIN = 'min'
MAX = 'max'
AVERAGE = 'average'
FUNCTIONS = (
    (SUM, 'Sum'),
    (COUNT, 'Count'),
    (MIN, 'Min'),
    (MAX, 'Max'),
    (AVERAGE, 'Average')
)

ONTO_EVENT = 'event'
REGISTER_VAR = 'variable'
DESTINATIONS = (
    (ONTO_EVENT, 'Update Field On The Event'),
    (REGISTER_VAR, 'Register Result As Variable'),
)

GREATER = '>'
LESS = '<'
EQUAL = '='
NOT_EQUAL = '!='
REGULAR = 're'
MORE_THAN_GREATER = '>%>'
LESS_THAN_GREATER = '<%>'
MORE_THAN_LESS = '>%<'
LESS_THAN_LESS = '<%<'
OPERATORS = (
    (EQUAL, 'Equal To'),
    (NOT_EQUAL, 'Not Equal To'),
    (GREATER, 'Greater Than'),
    (LESS, 'Less Than'),
    (REGULAR, 'Regular Expression'),
    (MORE_THAN_GREATER, 'More Than N% Greater'),
    (LESS_THAN_GREATER, 'Less Than N% Greater'),
    (MORE_THAN_LESS, 'More Than N% Less'),
    (LESS_THAN_LESS, 'Less Than N% Less'),
)

LAST_EVENTS = 'last_events'
TIME_WINDOW = 'time_window'
LAST_EVENTS_TYPES = (
    (TIME_WINDOW, 'Time Window'),
    (LAST_EVENTS, 'Last N Events'),
)

ADD_FIELD = 'add_field'
DUPLICATE_FIELD = 'duplicate_field'
REMOVE_FIELD = 'remove_field'
OPERATION_TYPES = (
    (ADD_FIELD, 'Add Field'),
    (DUPLICATE_FIELD, 'Duplicate Field'),
    (REMOVE_FIELD, 'Remove Field'),
)

ADD = '+'
SUBSTRACT = '-'
MULTIPLE = '*'
DIVIDE = '/'
FIELD_OPERATIONS = (
    (ADD, 'Add To'),
    (SUBSTRACT, 'Substract From'),
    (MULTIPLE, 'Multiple By'),
    (DIVIDE, 'Divide By'),
)

SELECT = 'select'
REPLACE = 'replace'
RESULT_PLACEMENTS_NUMERIC = (
    (SELECT, ' Add To A New Field'),
    (REPLACE, ' Replace In Place'),
)

KEYS = 'keys'
VALUES = 'values'
KEYS_OR_VALUES = (
    (KEYS, 'Keys'),
    (VALUES, 'Values'),
)

POPOVER_POSITION = 'right'

LATEST = 'latest'
EARLIEST = 'earliest'

OFFSETS = (
    (LATEST, 'Process Events That Occur After Deployment'),
    (EARLIEST, 'Process All Historical Events'),
)

EVERY_X_MINUTES = 'every_x_minutes'
EVERY_DAY_AT = 'every_day_at'

SCHEDULE_TYPES = (
    (EVERY_X_MINUTES, 'Every x minutes'),
    (EVERY_DAY_AT, 'Every day at'),
)

REPLACE_INBOUND = 'replace_inbound'
PUBLISH_ANOTHER_STREAM = 'publish_another_stream'

SEARCH_RESULT_PLACEMENTS = (
    (REPLACE_INBOUND, 'Replace Inbound Events With Results'),
    (PUBLISH_ANOTHER_STREAM, 'Publish Onto Another Stream')
)

INFORMATION = 'information'
WARNING = 'warning'
ALERT = 'alert'
TASK_TYPES = (
    (INFORMATION, 'Information'),
    (WARNING, 'Warning'),
    (ALERT, 'Alert'),
)

BASE_FILTER_BLOCK = [
    {
        'name': 'value',
        'input_type': 'select',
        'choices': [list(x) for x in OPERATORS],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {},
        'popover': {
            'top_text': 'operator Top text',
            'bottom_text': 'operator Bottom text',
        },
    },
    {
        'name': 'percent',
        'input_type': 'text',
        'choices': [],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {
            'field': 'value',
            'value': [
                '>%>',
                '<%>',
                '>%<',
                '<%<',
            ],
        },
        'popover': {
            'top_text': 'percent Top text',
            'bottom_text': 'percent Bottom text',
        },
    },
    {
        'name': 'key_type',
        'input_type': 'select',
        'choices': [list(x) for x in FILTER_KEY_TYPES],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {},
        'popover': {
            'top_text': 'key type Top text',
            'bottom_text': 'key type Bottom text',
        },
    },
    {
        'name': 'static_value',
        'input_type': 'text',
        'choices': [],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {
            'field': 'key_type',
            'value': [
                'static_value',
            ],
        },
        'popover': {
            'top_text': 'static_value Top text',
            'bottom_text': 'static_value Bottom text',
        },
    },
    {
        'name': 'event_field_name',
        'input_type': 'select',
        'choices': [],
        'is_need_fetch': 'schema_fields',
        'changes_schema_block': 0,
        'related_to': {
            'field': 'key_type',
            'value': [
                'from_event',
            ],
        },
        'popover': {
            'top_text': 'event field name value Top text',
            'bottom_text': 'event field name value Bottom text',
        },
    },
    {
        'name': 'variable_name',
        'input_type': 'text',
        'choices': [],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {
            'field': 'key_type',
            'value': [
                'from_variable',
            ],
        },
        'popover': {
            'top_text': 'event field name value Top text',
            'bottom_text': 'event field name value Bottom text',
        },
    },
]

FILTER_BLOCK_LOOKUP = [
    {
        'name': 'field_name',
        'input_type': 'select',
        'choices': [],
        'is_need_fetch': 'schema_fields',
        'changes_schema_block': 0,
        'related_to': {},
        'popover': {
            'top_text': 'field name Top text',
            'bottom_text': 'field name Bottom text',
        },
    },
] + BASE_FILTER_BLOCK

FROM_BLOCK = [
    {
        'name': 'key_type_from',
        'input_type': 'select',
        'choices': [list(x) for x in FILTER_KEY_TYPES_REV],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {},
        'popover': {
            'top_text': 'key type Top text',
            'bottom_text': 'key type Bottom text',
        },
    },
    {
        'name': 'static_value_from',
        'input_type': 'text',
        'choices': [],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {
            'field': 'key_type_from',
            'value': [
                'static_value',
            ],
        },
        'popover': {
            'top_text': 'static_value Top text',
            'bottom_text': 'static_value Bottom text',
        },
    },
    {
        'name': 'event_field_name_from',
        'input_type': 'select',
        'choices': [],
        'is_need_fetch': 'schema_fields',
        'changes_schema_block': 0,
        'related_to': {
            'field': 'key_type_from',
            'value': [
                'from_event',
            ],
        },
        'popover': {
            'top_text': 'event field name value Top text',
            'bottom_text': 'event field name value Bottom text',
        },
    },
    {
        'name': 'variable_name_from',
        'input_type': 'text',
        'choices': [],
        'is_need_fetch': '',
        'changes_schema_block': 0,
        'related_to': {
            'field': 'key_type_from',
            'value': [
                'from_variable',
            ],
        },
        'popover': {
            'top_text': 'event field name value Top text',
            'bottom_text': 'event field name value Bottom text',
        },
    },
]

FILTER_BLOCK = FROM_BLOCK + BASE_FILTER_BLOCK

SCHEMA_FIELD_BLOCK = [
    {
        'name': 'field_name',
        'input_type': 'select',
        'choices': [],
        'is_need_fetch': 'schema_fields',
        'changes_schema_block': 0,
        'related_to': {},
        'popover': {
            'top_text': 'field name Top text',
            'bottom_text': 'field name Bottom text',
        },
    },
    {
        'name': 'target_field_name',
        'input_type': 'select',
        'choices': [],
        'is_need_fetch': 'schema_fields',
        'changes_schema_block': 0,
        'related_to': {},
        'popover': {
            'top_text': 'Target Field Name Top text',
            'bottom_text': 'Target Field Name Bottom text',
            'position': POPOVER_POSITION,
        },
    },
]

STEP_TYPES_DATA = {
    INBOUND: {
        'inherits_schema': 0,
        'step_type_name': 'Inbound Event',
        'fields': [
            {
                'name': 'topic',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'streams',
                'changes_schema_block': 1,
                'related_to': {},
                'popover': {
                    'top_text': 'topic Top text',
                    'bottom_text': 'topic Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'offset',
                'input_type': 'select',
                'choices': [list(x) for x in OFFSETS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Offset Top text',
                    'bottom_text': 'Offset Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    INBOUNDTIMER: {
        'inherits_schema': 0,
        'step_type_name': 'Inbound Timer',
        'fields': [
            {
                'name': 'schedule_type',
                'input_type': 'select',
                'choices': [list(x) for x in SCHEDULE_TYPES],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Schedule Type Top text',
                    'bottom_text': 'Schedule Type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'schedule',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'schedule Top text',
                    'bottom_text': 'schedule Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    INBOUNDHTTP: {
        'inherits_schema': 0,
        'step_type_name': 'Inbound Events From API',
        'fields': [
            {
                'name': 'url',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'URL Top text',
                    'bottom_text': 'URL Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'path_to_events',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Path to events Top text',
                    'bottom_text': 'Path to events Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    INBOUNDKPI: {
        'inherits_schema': 0,
        'step_type_name': 'Inbound Events From KPI',
        'fields': [
            {
                'name': 'category_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'kpi_category',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'kpi category Top text',
                    'bottom_text': 'kpi category Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'metric',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'kpi_metric',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'kpi metric Top text',
                    'bottom_text': 'kpi metric Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    OUTBOUND: {
        'inherits_schema': 0,
        'step_type_name': 'Outbound Event',
        'fields': [
            {
                'name': 'topic',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'streams',
                'changes_schema_block': 1,
                'related_to': {},
                'popover': {
                    'top_text': 'topic Top text',
                    'bottom_text': 'topic Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    OUTBOUNDEMAIL: {
        'inherits_schema': 1,
        'step_type_name': 'Outbound Email',
        'popover': {
            'top_text': 'FILTER main Top text',
            'bottom_text': 'FILTER main Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'key_type',
                'input_type': 'select',
                'choices': [list(x) for x in KEY_TYPES],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'key type Top text',
                    'bottom_text': 'key type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'from_event',
                    ],
                },
                'popover': {
                    'top_text': 'field name Top text',
                    'bottom_text': 'field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'static_value',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'static_value',
                    ],
                },
                'popover': {
                    'top_text': 'static value Top text',
                    'bottom_text': 'static value Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'template',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'filter_value Top text',
                    'bottom_text': 'filter_value Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    OUTBOUNDSMS: {
        'inherits_schema': 1,
        'step_type_name': 'Outbound SMS',
        'popover': {
            'top_text': 'FILTER main Top text',
            'bottom_text': 'FILTER main Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'key_type',
                'input_type': 'select',
                'choices': [list(x) for x in KEY_TYPES],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'key type Top text',
                    'bottom_text': 'key type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'from_event',
                    ],
                },
                'popover': {
                    'top_text': 'field name Top text',
                    'bottom_text': 'field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'static_value',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'static_value',
                    ],
                },
                'popover': {
                    'top_text': 'static value Top text',
                    'bottom_text': 'static value Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'template',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'filter_value Top text',
                    'bottom_text': 'filter_value Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    FUNCTION: {
        'inherits_schema': 1,
        'step_type_name': 'Execute Function',
        'fields': [
            {
                'name': 'function_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'functions',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'function Top text',
                    'bottom_text': 'function Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'endpoint_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'function_endpoints',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'endpoint Top text',
                    'bottom_text': 'endpoint Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'result_placement',
                'input_type': 'select',
                'choices': [list(x) for x in RESULT_PLACEMENTS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'result placement Top text',
                    'bottom_text': 'result placement Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    FILTER: {
        'inherits_schema': 1,
        'step_type_name': 'Simple Filter',
        'fields': [
            {
                'name': 'block',
                'input_type': 'block',
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'fields': FILTER_BLOCK
            },
        ],
    },
    SELECTFIELDS: {
        'inherits_schema': 1,
        'step_type_name': 'Select Fields',
        'fields': [
            {
                'name': 'block',
                'input_type': 'block',
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'fields': [
                    {
                        'name': 'field_name',
                        'input_type': 'select',
                        'choices': [],
                        'is_need_fetch': 'schema_fields',
                        'changes_schema_block': 0,
                        'related_to': {},
                        'popover': {
                            'top_text': 'Select Field Name Top text',
                            'bottom_text': 'Select Field Name Bottom text',
                        },
                    }
                ]
            },
        ],
    },
    # COMPLEX: {
    #     'inherits_schema': 1,
    #     'step_type_name': 'Complex Filter',
    #     'popover': {
    #         'top_text': 'Complex Filter Top text',
    #         'bottom_text': 'Complex Filter Bottom text',
    #         'position': POPOVER_POSITION,
    #     },
    #     'fields': [
    #         {
    #             'name': 'search_field_name',
    #             'input_type': 'select',
    #             'choices': [],
    #             'is_need_fetch': 'schema_fields',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'Search Field Name Top text',
    #                 'bottom_text': 'Search Field Name Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #         {
    #             'name': 'formula',
    #             'input_type': 'text',
    #             'choices': [],
    #             'is_need_fetch': '',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'Formula Top text',
    #                 'bottom_text': 'Formula Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #     ],
    # },
    MAP: {
        'inherits_schema': 1,
        'step_type_name': 'Map',
        'fields': [
            {
                'name': 'field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'field name text',
                    'bottom_text': 'field name text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'expression',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'expression Top text',
                    'bottom_text': 'expression Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    MAP_EVENT: {
        'inherits_schema': 1,
        'step_type_name': 'Map Event',
        'fields': [
            {
                'name': 'event_type',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schemas',
                'changes_schema_block': 1,
                'related_to': {},
                'popover': {
                    'top_text': 'Event type Top text',
                    'bottom_text': 'Event type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'block',
                'input_type': 'block',
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'fields': SCHEMA_FIELD_BLOCK,
            },
        ],
    },
    EVENT: {
        'inherits_schema': 0,
        'step_type_name': 'Create New Event',
        'fields': [
            {
                'name': 'event_type',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schemas',
                'changes_schema_block': 1,
                'related_to': {},
                'popover': {
                    'top_text': 'Event type Top text',
                    'bottom_text': 'Event type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    LOOKUP: {
        'inherits_schema': 1,
        'step_type_name': 'Stream Lookup',
        'fields': [
            {
                'name': 'record_type',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'streams',
                'changes_schema_block': 1,
                'related_to': {},
                'popover': {
                    'top_text': 'record type Top text',
                    'bottom_text': 'record type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            # -----------------------------------------------------------------------
            {
                'name': 'block',
                'input_type': 'block',
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'fields': FILTER_BLOCK_LOOKUP,
            },
            # -----------------------------------------------------------------------
            {
                'name': 'last_event_type',
                'input_type': 'select',
                'choices': [list(x) for x in LAST_EVENTS_TYPES],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'last event type Top text',
                    'bottom_text': 'last event type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'time_window',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'last_event_type',
                    'value': [
                        'time_window',
                    ],
                },
                'popover': {
                    'top_text': 'time window Top text',
                    'bottom_text': 'time window Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'last_events',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'last_event_type',
                    'value': [
                        'last_events',
                    ],
                },
                'popover': {
                    'top_text': 'last events Top text',
                    'bottom_text': 'last events Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'result_placement',
                'input_type': 'select',
                'choices': [list(x) for x in RESULT_PLACEMENTS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'result placement Top text',
                    'bottom_text': 'result placement Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'operator',
                'input_type': 'select',
                'choices': [list(x) for x in FUNCTIONS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'result_placement',
                    'value': [
                        'aggregate',
                    ],
                },
                'popover': {
                    'top_text': 'operator Top text',
                    'bottom_text': 'operator Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'column_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'result_placement',
                    'value': [
                        'aggregate',
                    ],
                },
                'popover': {
                    'top_text': 'column name Top text',
                    'bottom_text': 'column name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'destinations',
                'input_type': 'select',
                'choices': [list(x) for x in DESTINATIONS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'result_placement',
                    'value': [
                        'aggregate',
                    ],
                },
                'popover': {
                    'top_text': 'destinations Top text',
                    'bottom_text': 'destinations Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'destination_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'destinations',
                    'value': [
                        'event',
                    ],
                },
                'popover': {
                    'top_text': 'destination field name Top text',
                    'bottom_text': 'destination field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'variable_name_to',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'destinations',
                    'value': [
                        'variable',
                    ],
                },
                'popover': {
                    'top_text': 'variable name Top text',
                    'bottom_text': 'variable name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    EXECUTE_SEARCH: {
        'inherits_schema': 1,
        'step_type_name': 'Execute Saved Search',
        'fields': [
            {
                'name': 'search_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'searches',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'search name Top text',
                    'bottom_text': 'search name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'search_result_placement',
                'input_type': 'select',
                'choices': [list(x) for x in SEARCH_RESULT_PLACEMENTS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'search name Top text',
                    'bottom_text': 'search name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'topic',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'streams',
                'changes_schema_block': 1,
                'related_to': {
                    'field': 'search_result_placement',
                    'value': [
                        'publish_another_stream',
                    ],
                },
                'popover': {
                    'top_text': 'topic Top text',
                    'bottom_text': 'topic Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    KEY: {
        'inherits_schema': 1,
        'step_type_name': 'Record Key Performance Indicator',
        'fields': [
            {
                'name': 'category_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'kpi_category',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'kpi category Top text',
                    'bottom_text': 'kpi category Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'metric',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'kpi_metric',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'kpi metric Top text',
                    'bottom_text': 'kpi metric Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'key_type',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'key_types',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'key type Top text',
                    'bottom_text': 'key type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'from_event',
                        'update_from_event',
                    ],
                },
                'popover': {
                    'top_text': 'field name Top text',
                    'bottom_text': 'field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'variable_name',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'update_to_registered_variable',
                    ],
                },
                'popover': {
                    'top_text': 'field name Top text',
                    'bottom_text': 'field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'static_value',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'static_value',
                        'update_to_static_value',
                    ],
                },
                'popover': {
                    'top_text': 'static value Top text',
                    'bottom_text': 'static value Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'field_to_process',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'slicing field Top text',
                    'bottom_text': 'slicing field Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    WORKFLOW: {
        'inherits_schema': 1,
        'step_type_name': 'Create Workflow Task',
        'fields': [
            {
                'name': 'recipient',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'users',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'recipient Top text',
                    'bottom_text': 'recipient Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'type',
                'input_type': 'select',
                'choices': [list(x) for x in TASK_TYPES],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'type Top text',
                    'bottom_text': 'type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'title',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'task_title Top text',
                    'bottom_text': 'task_title Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'description',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'task_description Top text',
                    'bottom_text': 'task_description Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    SENTIMENT: {
        'inherits_schema': 1,
        'step_type_name': 'AWS Comprehend',
        'popover': {
            'top_text': 'AWS Comprehend Top text',
            'bottom_text': 'AWS Comprehend Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'field_to_process',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'field to process Top text',
                    'bottom_text': 'field to process Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    TRANSCRIBE: {
        'inherits_schema': 0,
        'step_type_name': 'AWS Transcribe',
        'popover': {
            'top_text': 'AWS Transcribe Top text',
            'bottom_text': 'AWS Transcribe Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'file_path',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'file path Top text',
                    'bottom_text': 'file path Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'destination_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'file path Top text',
                    'bottom_text': 'file path Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    EXTERNAL: {
        'inherits_schema': 1,
        'step_type_name': 'External API Call',
        'popover': {
            'top_text': 'External API Call Top text',
            'bottom_text': 'External API Call Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'url_template',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Url Template Top text',
                    'bottom_text': 'Url Template Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'field_list',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Field List Top text',
                    'bottom_text': 'Field List Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    FIELD_ADD: {
        'inherits_schema': 1,
        'step_type_name': 'Add Field',
        'popover': {
            'top_text': 'Add Field Top text',
            'bottom_text': 'Add Field Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'add_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Add Field Top text',
                    'bottom_text': 'Add Field Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'key_type',
                'input_type': 'select',
                'choices': [list(x) for x in MAP_KEY_TYPES],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'key type Top text',
                    'bottom_text': 'key type Bottom text',
                },
            },
            {
                'name': 'static_value',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'static_value',
                    ],
                },
                'popover': {
                    'top_text': 'static_value Top text',
                    'bottom_text': 'static_value Bottom text',
                },
            },
            {
                'name': 'variable_name',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'from_variable',
                    ],
                },
                'popover': {
                    'top_text': 'event field name value Top text',
                    'bottom_text': 'event field name value Bottom text',
                },
            },
        ],
    },
    FIELD_REMOVE: {
        'inherits_schema': 1,
        'step_type_name': 'Remove Field',
        'popover': {
            'top_text': 'Remove Field Top text',
            'bottom_text': 'Remove Field Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'remove_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Remove Field Name Top text',
                    'bottom_text': 'Remove Field Bottom Name text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    FIELD_COPY: {
        'inherits_schema': 1,
        'step_type_name': 'Copy Field',
        'popover': {
            'top_text': 'Copy Field Top text',
            'bottom_text': 'Copy Field Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'copy_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Copy Field Name Top text',
                    'bottom_text': 'Copy Field Name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'destination_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Destination Field Name Top text',
                    'bottom_text': 'Destination Field Name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    # FIELD_RENAME: {
    #     'inherits_schema': 1,
    #     'step_type_name': 'Rename Field',
    #     'popover': {
    #         'top_text': 'Rename Field Top text',
    #         'bottom_text': 'Rename Field Bottom text',
    #         'position': POPOVER_POSITION,
    #     },
    #     'fields': [
    #         {
    #             'name': 'rename_field_name',
    #             'input_type': 'select',
    #             'choices': [],
    #             'is_need_fetch': 'schema_fields',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'Rename Field Name Top text',
    #                 'bottom_text': 'Rename Field Name Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #         {
    #             'name': 'new_field_name',
    #             'input_type': 'text',
    #             'choices': [],
    #             'is_need_fetch': '',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'New Field Name Top text',
    #                 'bottom_text': 'New Field Name Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #     ],
    # },
    SLEEP: {
        'inherits_schema': 1,
        'step_type_name': 'Sleep Step',
        'popover': {
            'top_text': 'Sleep Step Top text',
            'bottom_text': 'Sleep Step Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'duration',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Duration Top text',
                    'bottom_text': 'Duration Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ]
    },
    # PYTHON: {
    #     'inherits_schema': 1,
    #     'step_type_name': 'Python Step',
    #     'popover': {
    #         'top_text': 'External API Call Top text',
    #         'bottom_text': 'External API Call Bottom text',
    #         'position': POPOVER_POSITION,
    #     },
    #     'fields': [
    #         {
    #             'name': 'code',
    #             'input_type': 'text',
    #             'choices': [],
    #             'is_need_fetch': '',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'Code url Top text',
    #                 'bottom_text': 'Code Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #     ]
    # },
    RESET: {
        'inherits_schema': 1,
        'step_type_name': 'Reset Timestamp',
        'popover': {
            'top_text': 'Reset Timestamp Top text',
            'bottom_text': 'Reset Timestamp Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'timestamp_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Timestamp field name Top text',
                    'bottom_text': 'Timestamp field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'offset_in_seconds',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Offset in seconds Top text',
                    'bottom_text': 'Offset in seconds Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    DICT: {
        'inherits_schema': 1,
        'step_type_name': 'Data Dictionary Lookup & Replace',
        'popover': {
            'top_text': 'Data Dictionary Lookup & Replace Top text',
            'bottom_text': 'Data Dictionary Lookup & Replace Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': [
            {
                'name': 'field_to_replace',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Replace field name Top text',
                    'bottom_text': 'Replace field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'data_dictionary_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'data_dictionaries',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Data dictionary name Top text',
                    'bottom_text': 'Data dictionary name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    ADJUST: {
        'inherits_schema': 1,
        'step_type_name': 'Perform Calculation',
        'popover': {
            'top_text': 'Perform Calculation Top text',
            'bottom_text': 'Perform Calculation Bottom text',
            'position': POPOVER_POSITION,
        },
        'fields': FROM_BLOCK + [
            {
                'name': 'field_operation',
                'input_type': 'select',
                'choices': [list(x) for x in FIELD_OPERATIONS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'Field operation Top text',
                    'bottom_text': 'Field operation Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'key_type',
                'input_type': 'select',
                'choices': [list(x) for x in FILTER_KEY_TYPES],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'key type Top text',
                    'bottom_text': 'key type Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'static_value',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'static_value',
                    ],
                },
                'popover': {
                    'top_text': 'static_value Top text',
                    'bottom_text': 'static_value Bottom text',
                },
            },
            {
                'name': 'event_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'from_event',
                    ],
                },
                'popover': {
                    'top_text': 'event field name value Top text',
                    'bottom_text': 'event field name value Bottom text',
                },
            },
            {
                'name': 'variable_name',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'key_type',
                    'value': [
                        'from_variable',
                    ],
                },
                'popover': {
                    'top_text': 'event field name value Top text',
                    'bottom_text': 'event field name value Bottom text',
                },
            },
            {
                'name': 'destinations',
                'input_type': 'select',
                'choices': [list(x) for x in DESTINATIONS],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {},
                'popover': {
                    'top_text': 'destinations Top text',
                    'bottom_text': 'destinations Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'destination_field_name',
                'input_type': 'select',
                'choices': [],
                'is_need_fetch': 'schema_fields',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'destinations',
                    'value': [
                        'event',
                    ],
                },
                'popover': {
                    'top_text': 'destination field name Top text',
                    'bottom_text': 'destination field name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
            {
                'name': 'variable_name_to',
                'input_type': 'text',
                'choices': [],
                'is_need_fetch': '',
                'changes_schema_block': 0,
                'related_to': {
                    'field': 'destinations',
                    'value': [
                        'variable',
                    ],
                },
                'popover': {
                    'top_text': 'variable name Top text',
                    'bottom_text': 'variable name Bottom text',
                    'position': POPOVER_POSITION,
                },
            },
        ],
    },
    # VALUE: {
    #     'inherits_schema': 1,
    #     'step_type_name': 'If Value In Set',
    #     'popover': {
    #         'top_text': 'If Value In Set Top text',
    #         'bottom_text': 'If Value In Set Bottom text',
    #         'position': POPOVER_POSITION,
    #     },
    #     'fields': [
    #         {
    #             'name': 'set_field_name',
    #             'input_type': 'select',
    #             'choices': [],
    #             'is_need_fetch': 'schema_fields',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'Field name Top text',
    #                 'bottom_text': 'Field name Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #         {
    #             'name': 'data_dictionary_name',
    #             'input_type': 'select',
    #             'choices': [],
    #             'is_need_fetch': 'data_dictionaries',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'Data dictionary name Top text',
    #                 'bottom_text': 'Data dictionary name Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #         {
    #             'name': 'keys_or_values',
    #             'input_type': 'select',
    #             'choices': [list(x) for x in KEYS_OR_VALUES],
    #             'is_need_fetch': '',
    #             'changes_schema_block': 0,
    #             'related_to': {},
    #             'popover': {
    #                 'top_text': 'Keys or values Top text',
    #                 'bottom_text': 'Keys or values Bottom text',
    #                 'position': POPOVER_POSITION,
    #             },
    #         },
    #     ],
    # },
}
