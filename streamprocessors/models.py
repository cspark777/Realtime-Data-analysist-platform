from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from account.models import CustomUser
from core.models import ProjectModelMixin, DateInfoModelMixin, GroupMixin
from groups.models import StreamProcessorGroup
from kpis.models import KPI
from streams.models import Stream


class StreamProcessor(GroupMixin):
    name = models.CharField(
        _('Name'),
        max_length=200,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )
    replicas = models.PositiveIntegerField(
        _('Count Of Replicas'),
        default=1,
    )
    is_running = models.BooleanField(
        _('Running'),
        default=False
    )
    dsl = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )
    owning_user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    invocations = models.IntegerField(
        _('Invocations'),
        default=0,
    )
    status = models.IntegerField(
        _('Status'),
        default=0,
    )
    pub_date = models.DateTimeField(
        _('Date published'),
        null=True,
    )
    additional_integrity_checks = models.BooleanField(
        default=False,
        verbose_name='Additional Integrity Checks',
    )

    delay_on_uuid_failure = models.PositiveIntegerField(
        _('Delay On uuid Failure'),
        default=50,
    )

    retry_on_uuid_failure_count = models.PositiveIntegerField(
        _('Retry On uuid Failure Count'),
        default=10,
    )

    group = models.ForeignKey("groups.StreamProcessorGroup", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('StreamProcessor')
        verbose_name_plural = _('StreamProcessors')
        ordering = ('id',)

    def __str__(self):
        return self.name


class StreamProcessorStep(MPTTModel):
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
    MANIPULATE = 'manipulate'
    FIELD_ADD = 'add'
    FIELD_REMOVE = 'remove'
    FIELD_COPY = 'copy'
    FIELD_RENAME = 'rename'
    FIELD_SUM = 'sum'
    FUNCTION = 'function'
    SLEEP = 'sleep'
    PYTHON = 'python'
    RESET = 'reset'
    DICT = 'dict'
    ADJUST = 'adjust'
    VALUE = 'value'
    STEP_TYPES = (
        (INBOUND, 'Inbound Event - Stream'),
        (INBOUNDTIMER, 'Inbound Event - Timer Task'),
        (INBOUNDHTTP, 'Inbound Event - Load From API'),
        (INBOUNDKPI, 'Inbound Event - KPI Change'),
        (OUTBOUND, 'Outbound Event - Stream'),
        (OUTBOUNDEMAIL, 'Outbound Event - E-Mail'),
        (OUTBOUNDSMS, 'Outbound Event - SMS'),
        (OUTBOUNDWEB, 'Outbound Event - Web Hook'),
        (FILTER, 'Processor - Simple Filter'),
        (COMPLEX, 'Processor - Complex Filter'),
        (LOOKUP, 'Processor - Stream Lookup'),
        (EXECUTE_SEARCH, 'Processor - Execute Search'),
        (FUNCTION, 'Processor - Execute Function'),
        (SELECTFIELDS, 'Processor - Select Fields'),
        (MAP, 'Processor - Map Function'),
        (EVENT, 'Processor - Create New Event Of Type'),
        (MAP_EVENT, 'Processor - Map Event To Event Type'),
        (KEY, 'Processor - Record Key Performance Indicator'),
        (WORKFLOW, 'Processor - Create Workflow Task'),
        (SENTIMENT, 'Processor - AWS Comprehend Sentiment Analysis'),
        (TRANSCRIBE, 'Processor - AWS Transcribe Task'),
        (EXTERNAL, 'Processor - External API Call'),
        (FIELD_ADD, 'Processor - Add Or Update Field'),
        (FIELD_REMOVE, 'Processor - Remove Field'),
        (FIELD_COPY, 'Processor - Copy Field'),
        (FIELD_RENAME, 'Processor - Rename Field'),
        # (FIELD_SUM, 'Processor - Sum Field'),
        (SLEEP, 'Processor - Sleep Step'),
        (PYTHON, 'Processor - Python Step'),
        (RESET, 'Processor - Reset Timestamp'),
        (DICT, 'Processor - Data Dictionary Lookup & Replace'),
        (ADJUST, 'Processor - Perform Calculation'),
        (VALUE, 'Processor - If Value In Set'),
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

    UPDATE_FROM_EVENT = 'update_from_event'
    UPDATE_TO_STATIC_VALUE = 'update_to_static_value'
    UPDATE_TO_REGISTERED_VARIABLE = 'update_to_registered_variable'
    UPDATE_KEY_TYPES = (
        (UPDATE_FROM_EVENT, 'Update To Value From event'),
        (UPDATE_TO_STATIC_VALUE, 'Update To Static Value'),
        (UPDATE_TO_REGISTERED_VARIABLE, 'Update To Registered Variable'),
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
    AGGREGATEREGISTER = 'aggregateregister'
    JOIN = 'join'
    JOININBOUND = 'joininbound'
    PUBLISH = 'publish'
    REPLACE = 'replace'
    REGISTER = 'replace'
    RESULT_PLACEMENTS = (
        (AGGREGATE, 'Aggregate Results'),
        # (AGGREGATEREGISTER, 'Aggregate Results and Register In Variable'),
        (JOIN, 'Join Results To Inbound'),
        (JOININBOUND, 'Join Inbound To Results'),
        # (PUBLISH, 'Publish Onto Stream'),
        (REPLACE, 'Replace Inbound Event With Results'),
        # (REGISTER, 'Register Results In A Variable'),
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
        (ONTO_EVENT, 'Add Result Onto Event'),
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

    EVERY_X_MILLISECOND = 'every_x_millisecond'
    EVERY_X_SECOND = 'every_x_second'
    EVERY_X_MINUTES = 'every_x_minutes'
    EVERY_X_HOUR = 'every_x_hour'
    EVERY_X_DAY = 'every_x_day'
    EVERY_DAY_AT = 'every_day_at'

    SCHEDULE_TYPES = (
        (EVERY_X_MILLISECOND, 'Every x milliseconds'),
        (EVERY_X_SECOND, 'Every x seconds'),
        (EVERY_X_MINUTES, 'Every x minutes'),
        (EVERY_X_HOUR, 'Every x hours'),
        (EVERY_X_DAY, 'Every x days'),
        (EVERY_DAY_AT, 'Every day at'),
    )

    REPLACE_INBOUND = 'replace_inbound'
    PUBLISH_ANOTHER_STREAM = 'publish_another_stream'

    SEARCH_RESULT_PLACEMENTS = (
        (REPLACE_INBOUND, 'Replace Inbound Events With Results'),
        (PUBLISH_ANOTHER_STREAM, 'Publish Onto Another Stream')
    )

    BASE_FILTER_BLOCK = [
        {
            'name': 'value',
            'input_type': 'select',
            'choices': [list(x) for x in OPERATORS],
            'popover': {
                'top_text': 'operator Top text',
                'bottom_text': 'operator Bottom text',
            },
        },
        {
            'name': 'percent',
            'input_type': 'text',
            'choices': [],
            'popover': {
                'top_text': 'percent Top text',
                'bottom_text': 'percent Bottom text',
            },
        },
        {
            'name': 'key_type',
            'input_type': 'select',
            'choices': [list(x) for x in FILTER_KEY_TYPES],
            'popover': {
                'top_text': 'key type Top text',
                'bottom_text': 'key type Bottom text',
            },
        },
        {
            'name': 'static_value',
            'input_type': 'text',
            'choices': [],
            'popover': {
                'top_text': 'static_value Top text',
                'bottom_text': 'static_value Bottom text',
            },
        },
        {
            'name': 'event_field_name',
            'input_type': 'select',
            'choices': [],
            'popover': {
                'top_text': 'event field name value Top text',
                'bottom_text': 'event field name value Bottom text',
            },
        },
        {
            'name': 'variable_name',
            'input_type': 'text',
            'choices': [],
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
            'popover': {
                'top_text': 'key type Top text',
                'bottom_text': 'key type Bottom text',
            },
        },
        {
            'name': 'static_value_from',
            'input_type': 'text',
            'choices': [],
            'popover': {
                'top_text': 'static_value Top text',
                'bottom_text': 'static_value Bottom text',
            },
        },
        {
            'name': 'event_field_name_from',
            'input_type': 'select',
            'choices': [],
            'popover': {
                'top_text': 'event field name value Top text',
                'bottom_text': 'event field name value Bottom text',
            },
        },
        {
            'name': 'variable_name_from',
            'input_type': 'text',
            'choices': [],
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
            'popover': {
                'top_text': 'field name Top text',
                'bottom_text': 'field name Bottom text',
            },
        },
        {
            'name': 'target_field_name',
            'input_type': 'select',
            'choices': [],
            'popover': {
                'top_text': 'Target Field Name Top text',
                'bottom_text': 'Target Field Name Bottom text',
                'position': POPOVER_POSITION,
            },
        },
    ]

    STEP_TYPES_DATA = {
        INBOUND: {
            'step_type_name': 'Inbound Event',
            'fields': [
                {
                    'name': 'topic',
                    'input_type': 'select',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'Offset Top text',
                        'bottom_text': 'Offset Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        INBOUNDTIMER: {
            'step_type_name': 'Inbound Timer',
            'fields': [
                {
                    'name': 'schedule_type',
                    'input_type': 'select',
                    'choices': [list(x) for x in SCHEDULE_TYPES],
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
                    'popover': {
                        'top_text': 'schedule Top text',
                        'bottom_text': 'schedule Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        INBOUNDHTTP: {
            'step_type_name': 'Inbound Events From API',
            'fields': [
                {
                    'name': 'url',
                    'input_type': 'text',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'Path to events Top text',
                        'bottom_text': 'Path to events Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        INBOUNDKPI: {
            'step_type_name': 'Inbound Events From KPI',
            'fields': [
                {
                    'name': 'category_name',
                    'input_type': 'select',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'kpi metric Top text',
                        'bottom_text': 'kpi metric Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        OUTBOUND: {
            'step_type_name': 'Outbound Event',
            'fields': [
                {
                    'name': 'topic',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'topic Top text',
                        'bottom_text': 'topic Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        OUTBOUNDEMAIL: {
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
                    'popover': {
                        'top_text': 'key type Top text',
                        'bottom_text': 'key type Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'field_name',
                    'input_type': 'text',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'filter_value Top text',
                        'bottom_text': 'filter_value Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        OUTBOUNDSMS: {
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
                    'popover': {
                        'top_text': 'key type Top text',
                        'bottom_text': 'key type Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'field_name',
                    'input_type': 'text',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'filter_value Top text',
                        'bottom_text': 'filter_value Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        FUNCTION: {
            'step_type_name': 'Execute Function',
            'fields': [
                {
                    'name': 'function_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'category metric Top text',
                        'bottom_text': 'category metric Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'endpoint_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'key type Top text',
                        'bottom_text': 'key type Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'result_placement',
                    'input_type': 'select',
                    'choices': [list(x) for x in RESULT_PLACEMENTS],
                    'popover': {
                        'top_text': 'result placement Top text',
                        'bottom_text': 'result placement Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        FILTER: {
            'step_type_name': 'Simple Filter',
            'fields': [
                {
                    'name': 'block',
                    'input_type': 'block',
                    'fields': FILTER_BLOCK
                },
            ],
        },
        SELECTFIELDS: {
            'step_type_name': 'Select Fields',
            'fields': [
                {
                    'name': 'block',
                    'input_type': 'block',
                    'fields': [
                        {
                            'name': 'select_field_name',
                            'input_type': 'select',
                            'choices': [],
                            'popover': {
                                'top_text': 'Select Field Name Top text',
                                'bottom_text': 'Select Field Name Bottom text',
                            },
                        }
                    ]
                },
            ],
        },
        COMPLEX: {
            'step_type_name': 'Complex Filter',
            'popover': {
                'top_text': 'Complex Filter Top text',
                'bottom_text': 'Complex Filter Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'search_field_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Search Field Name Top text',
                        'bottom_text': 'Search Field Name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'formula',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'Formula Top text',
                        'bottom_text': 'Formula Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        MAP: {
            'step_type_name': 'Map',
            'fields': [
                {
                    'name': 'record',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'record Top text',
                        'bottom_text': 'record Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'source',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'source Top text',
                        'bottom_text': 'source Bottom text',
                    },
                },
                {
                    'name': 'destination',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'destination Top text',
                        'bottom_text': 'destination Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'expression',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'expression Top text',
                        'bottom_text': 'expression Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        MAP_EVENT: {
            'step_type_name': 'Map Event',
            'fields': [
                {
                    'name': 'event_type',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Event type Top text',
                        'bottom_text': 'Event type Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'block',
                    'input_type': 'block',
                    'fields': SCHEMA_FIELD_BLOCK,
                },
            ],
        },
        EVENT: {
            'step_type_name': 'Create New Event',
            'fields': [
                {
                    'name': 'event_type',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Event type Top text',
                        'bottom_text': 'Event type Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        LOOKUP: {
            'step_type_name': 'Stream Lookup',
            'fields': [
                {
                    'name': 'record_type',
                    'input_type': 'select',
                    'choices': [],
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
                    'fields': FILTER_BLOCK_LOOKUP,
                },
                # -----------------------------------------------------------------------
                {
                    'name': 'last_event_type',
                    'input_type': 'select',
                    'choices': [list(x) for x in LAST_EVENTS_TYPES],
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
                    'popover': {
                        'top_text': 'variable name Top text',
                        'bottom_text': 'variable name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                # {
                #     'name': 'lookup_stream',
                #     'input_type': 'select',
                #     'choices': [],
                #     'popover': {
                #         'top_text': 'stream Top text',
                #         'bottom_text': 'stream type Bottom text',
                #         'position': POPOVER_POSITION,
                #     },
                # },
            ]
        },
        EXECUTE_SEARCH: {
            'step_type_name': 'Execute Saved Search',
            'fields': [
                {
                    'name': 'search_name',
                    'input_type': 'select',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'search name Top text',
                        'bottom_text': 'search name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        KEY: {
            'step_type_name': 'Record Key Performance Indicator',
            'fields': [
                {
                    'name': 'category_name',
                    'input_type': 'select',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'key type Top text',
                        'bottom_text': 'key type Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'field_name',
                    'input_type': 'text',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'slicing field Top text',
                        'bottom_text': 'slicing field Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        SENTIMENT: {
            'step_type_name': 'AWS Comprehend',
            'popover': {
                'top_text': 'AWS Comprehend Top text',
                'bottom_text': 'AWS Comprehend Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'field_to_process',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'field to process Top text',
                        'bottom_text': 'field to process Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        TRANSCRIBE: {
            'step_type_name': 'AWS Transcribe',
            'popover': {
                'top_text': 'AWS Transcribe Top text',
                'bottom_text': 'AWS Transcribe Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'topic',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'topic Top text',
                        'bottom_text': 'topic Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'file_path',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'file path Top text',
                        'bottom_text': 'file path Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        EXTERNAL: {
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
                    'popover': {
                        'top_text': 'Field List Top text',
                        'bottom_text': 'Field List Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        MANIPULATE: {
            'step_type_name': 'Manipulate Fields',
            'popover': {
                'top_text': 'Manipulate Top text',
                'bottom_text': 'Manipulate Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'operation',
                    'input_type': 'select',
                    'choices': [list(x) for x in OPERATION_TYPES],
                    'popover': {
                        'top_text': 'Operation Url Top text',
                        'bottom_text': 'Operation Url Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'field_name',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'Field Name Top text',
                        'bottom_text': 'Field Name url Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        FIELD_ADD: {
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
                    'popover': {
                        'top_text': 'key type Top text',
                        'bottom_text': 'key type Bottom text',
                    },
                },
                {
                    'name': 'static_value',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'static_value Top text',
                        'bottom_text': 'static_value Bottom text',
                    },
                },
                {
                    'name': 'variable_name',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'event field name value Top text',
                        'bottom_text': 'event field name value Bottom text',
                    },
                },
            ],
        },
        FIELD_REMOVE: {
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
                    'popover': {
                        'top_text': 'Remove Field Name Top text',
                        'bottom_text': 'Remove Field Bottom Name text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        FIELD_COPY: {
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
                    'popover': {
                        'top_text': 'Destination Field Name Top text',
                        'bottom_text': 'Destination Field Name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        FIELD_RENAME: {
            'step_type_name': 'Rename Field',
            'popover': {
                'top_text': 'Rename Field Top text',
                'bottom_text': 'Rename Field Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'rename_field_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Rename Field Name Top text',
                        'bottom_text': 'Rename Field Name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'new_field_name',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'New Field Name Top text',
                        'bottom_text': 'New Field Name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        FIELD_SUM: {
            'step_type_name': 'Sum Field',
            'popover': {
                'top_text': 'Sum Field Top text',
                'bottom_text': 'Sum Field Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'target_field_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Target Field Name Top text',
                        'bottom_text': 'Target Field Name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'sum_fields',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'Sum Field Names Top text',
                        'bottom_text': 'Sum Field Names Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        SLEEP: {
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
                    'popover': {
                        'top_text': 'Duration Top text',
                        'bottom_text': 'Duration Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        PYTHON: {
            'step_type_name': 'Python Step',
            'popover': {
                'top_text': 'External API Call Top text',
                'bottom_text': 'External API Call Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'code',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'Code url Top text',
                        'bottom_text': 'Code Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ]
        },
        RESET: {
            'step_type_name': 'Reset Timestamp',
            'popover': {
                'top_text': 'Reset Timestamp Top text',
                'bottom_text': 'Reset Timestamp Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'timestamp_field_name',
                    'input_type': 'text',
                    'choices': [],
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
                    'popover': {
                        'top_text': 'Offset in seconds Top text',
                        'bottom_text': 'Offset in seconds Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        DICT: {
            'step_type_name': 'Data Dictionary Lookup & Replace',
            'popover': {
                'top_text': 'Data Dictionary Lookup & Replace Top text',
                'bottom_text': 'Data Dictionary Lookup & Replace Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'dictionary_field_name',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'Dictionary field name Top text',
                        'bottom_text': 'Dictionary field name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'data_dictionary_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Data dictionary name Top text',
                        'bottom_text': 'Data dictionary name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        ADJUST: {
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
                    'popover': {
                        'top_text': 'static_value Top text',
                        'bottom_text': 'static_value Bottom text',
                    },
                },
                {
                    'name': 'event_field_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'event field name value Top text',
                        'bottom_text': 'event field name value Bottom text',
                    },
                },
                {
                    'name': 'variable_name',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'event field name value Top text',
                        'bottom_text': 'event field name value Bottom text',
                    },
                },
                {
                    'name': 'destinations',
                    'input_type': 'select',
                    'choices': [list(x) for x in DESTINATIONS],
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
                    'popover': {
                        'top_text': 'variable name Top text',
                        'bottom_text': 'variable name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
        VALUE: {
            'step_type_name': 'If Value In Set',
            'popover': {
                'top_text': 'If Value In Set Top text',
                'bottom_text': 'If Value In Set Bottom text',
                'position': POPOVER_POSITION,
            },
            'fields': [
                {
                    'name': 'set_field_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Field name Top text',
                        'bottom_text': 'Field name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'data_dictionary_name',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'Data dictionary name Top text',
                        'bottom_text': 'Data dictionary name Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
                {
                    'name': 'keys_or_values',
                    'input_type': 'select',
                    'choices': [list(x) for x in KEYS_OR_VALUES],
                    'popover': {
                        'top_text': 'Keys or values Top text',
                        'bottom_text': 'Keys or values Bottom text',
                        'position': POPOVER_POSITION,
                    },
                },
            ],
        },
    }

    name = models.CharField(
        _('Name'),
        max_length=200,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=False,
    )
    variable_name = models.CharField(
        _('Variable Name'),
        max_length=100,
        blank=True,
        null=False,
    )
    variable_name_to = models.CharField(
        _('Variable Name'),
        max_length=100,
        blank=True,
        null=False,
    )
    variable_name_from = models.CharField(
        _('Variable Name'),
        max_length=100,
        blank=True,
        null=False,
    )
    event_field_name_from = models.CharField(
        _('Event Field Name'),
        max_length=100,
        blank=True,
        null=False,
    )
    static_value_from = models.CharField(
        _('Static Value'),
        max_length=100,
        blank=True,
        null=False,
    )
    destinations = models.CharField(
        _('Destinations'),
        max_length=100,
        blank=True,
        null=False,
    )
    event_type = models.CharField(
        _('Schema drop down'),
        max_length=100,
        blank=True,
        null=False,
    )
    add_field_name = models.CharField(
        _('Add Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    field_value = models.CharField(
        _('Add Field Value'),
        max_length=200,
        blank=True,
        null=False,
    )
    remove_field_name = models.CharField(
        _('Remove Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    copy_field_name = models.CharField(
        _('Copy Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    destination_field_name = models.CharField(
        _('Destination Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    rename_field_name = models.CharField(
        _('Rename Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    new_field_name = models.CharField(
        _('New Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    target_field_name = models.CharField(
        _('Target Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    select_field_name = models.CharField(
        _('Select Field Name'),
        max_length=200,
        blank=True,
        null=False,
    )
    sum_fields = models.CharField(
        _('Sum Field Names'),
        max_length=400,
        blank=True,
        null=False,
    )
    steptype = models.CharField(
        _('Type'),
        max_length=100,
        choices=STEP_TYPES,
    )
    streamprocessor = models.ForeignKey(
        'streamprocessors.StreamProcessor',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        #related_name='steps',
    )
    ordering = models.IntegerField(
        _('Ordering steps'),
        default=1,
    )
    topic = models.CharField(
        _('Topic'),
        max_length=200,
        blank=True,
        null=True,
    )
    field = models.CharField(
        _('Field'),
        max_length=200,
        blank=True,
        null=True,
    )
    value = models.CharField(  # -----------------------------------------------------------------------
        _('Value'),
        max_length=200,
        blank=True,
        null=True,
    )
    event_field_name = models.CharField(
        _('Event Field Name'),
        max_length=200,
        blank=True,
        null=True,
    )
    percent = models.CharField(
        _('Percent'),
        max_length=200,
        blank=True,
        null=True,
    )
    filter_value = models.CharField(
        _('Filter Value'),
        max_length=400,
        blank=True,
        null=True,
    )
    expression = models.CharField(
        _('Expression'),
        max_length=400,
        blank=True,
        null=True,
    )
    record_type = models.CharField(
        _('Record Type'),
        max_length=200,
        blank=True,
        null=True,
    )
    lookup_field = models.CharField(  # -----------------------------------------------------------------------
        _('Lookup field'),
        max_length=200,
        blank=True,
        null=True,
    )
    lookup_value = models.CharField(
        _('Lookup Value'),
        max_length=200,
        blank=True,
        null=True,
    )
    search_name = models.CharField(
        _('Search name'),
        max_length=200,
        blank=True,
        null=True,
    )
    search_result_placement = models.CharField(
        _('Search Result Placement'),
        max_length=200,
        blank=True,
        null=True,
    )
    record = models.CharField(
        _('Record'),
        max_length=200,
        blank=True,
        null=True,
    )
    category_name = models.CharField(
        _('Category name'),
        max_length=200,
        blank=True,
        null=True,
    )
    metric = models.CharField(
        _('Metric'),
        max_length=200,
        blank=True,
        null=True,
    )
    source = models.CharField(
        _('Source'),
        max_length=400,
        blank=True,
        null=True,
    )
    destination = models.CharField(
        _('Destination'),
        max_length=400,
        blank=True,
        null=True,
    )
    template = models.TextField(
        _('SMS/Email template'),
        blank=True,
        null=True,
    )
    field_to_process = models.CharField(
        _('Field To Process'),
        max_length=400,
        blank=True,
        null=True,
    )
    file_path = models.CharField(
        _('File Path'),
        max_length=400,
        blank=True,
        null=True,
    )
    key_type = models.CharField(  # -----------------------------------------------------------------------
        _('Key Type'),
        max_length=40,
        choices=FILTER_KEY_TYPES_REV+INCREMENT_KEY_TYPES+UPDATE_KEY_TYPES,
        blank=True,
        null=True,
    )
    key_type_from = models.CharField(  # -----------------------------------------------------------------------
        _('Key Type'),
        max_length=20,
        choices=FILTER_KEY_TYPES_REV,
        blank=True,
        null=True,
    )
    field_name = models.CharField(  # -----------------------------------------------------------------------
        _('Key Value'),
        max_length=200,
        blank=True,
        null=True,
    )
    offset_in_seconds = models.IntegerField(
        _('Offset in seconds'),
        default=0,
    )
    offset = models.CharField(
        _('Offset'),
        max_length=200,
        choices=OFFSETS,
        default=LATEST,
    )
    static_value = models.CharField(
        _('Static Value'),
        max_length=200,
        blank=True,
        null=True,
    )
    last_event_type = models.CharField(
        _('Last Event Type'),
        max_length=200,
        blank=True,
        null=True,
    )
    time_window = models.CharField(
        _('Time Window'),
        max_length=200,
        blank=True,
        null=True,
    )
    last_events = models.CharField(
        _('Last N Events'),
        max_length=200,
        blank=True,
        null=True,
    )
    result_placement = models.CharField(
        _('Result Placement'),
        max_length=20,
        choices=RESULT_PLACEMENTS,
        blank=True,
        null=True,
    )
    operator = models.CharField(
        _('Operator'),
        max_length=20,
        choices=FUNCTIONS,
        blank=True,
        null=True,
    )
    lookup_stream = models.CharField(
        _('Publish Onto Stream'),
        max_length=200,
        blank=True,
        null=True,
    )
    column_name = models.CharField(
        _('Column Name'),
        max_length=200,
        blank=True,
        null=True,
    )
    url = models.CharField(
        _('HTTP Endpoint URL'),
        max_length=300,
        blank=True,
        null=True,
    )
    url_template = models.CharField(
        _('URL Template'),
        max_length=300,
        blank=True,
        null=True,
    )
    field_list = models.CharField(
        _('Field List'),
        max_length=300,
        blank=True,
        null=True,
    )
    schedule = models.CharField(
        _('Schedule'),
        max_length=200,
        blank=True,
        null=True,
    )

    poll_interval = models.CharField(
        _('Poll interval'),
        max_length=200,
        blank=True,
        null=True,
    )

    duration = models.CharField(
        _('Duration'),
        max_length=200,
        blank=True,
        null=True,
    )

    code = models.TextField(
        _('Code'),
        max_length=200,
        blank=True,
        null=True,
    )
    timestamp_field_name = models.CharField(
        _('Timestamp field name'),
        max_length=200,
        blank=True,
        null=True,
    )
    dictionary_field_name = models.CharField(
        _('Dictionary field name'),
        max_length=200,
        blank=True,
        null=True,
    )
    data_dictionary_name = models.CharField(
        _('Data dictionary name'),
        max_length=200,
        blank=True,
        null=True,
    )
    adjust_field_name = models.CharField(
        _('Field Name'),
        max_length=200,
        blank=True,
        null=True,
    )
    field_operation = models.CharField(
        _('Field Operation'),
        max_length=100,
        choices=FIELD_OPERATIONS,
        blank=True,
        null=True,
    )
    result_placement_numeric = models.CharField(
        _('Result Placement'),
        max_length=100,
        choices=RESULT_PLACEMENTS_NUMERIC,
        blank=True,
        null=True,
    )
    set_field_name = models.CharField(
        _('Field Name'),
        max_length=100,
        blank=True,
        null=True,
    )
    keys_or_values = models.CharField(
        _('Keys Or Values'),
        max_length=100,
        choices=KEYS_OR_VALUES,
        blank=True,
        null=True,
    )
    path_to_events = models.CharField(
        _('Path To Events'),
        max_length=200,
        blank=True,
        null=True,
    )
    search_field_name = models.CharField(
        _('Search Field Name'),
        max_length=200,
        blank=True,
        null=True,
    )
    field_to_replace = models.CharField(
        _('Replace Field Name'),
        max_length=200,
        blank=True,
        null=True,
    )
    formula = models.CharField(
        _('Formula'),
        max_length=200,
        blank=True,
        null=True,
    )
    function_name = models.CharField(
        _('Function Name'),
        max_length=200,
        blank=True,
        null=True,
    )
    endpoint_name = models.CharField(
        _('Function Endpoint'),
        max_length=200,
        blank=True,
        null=True,
    )
    schedule_value = models.IntegerField(
        _('Schedule Value'),
        default=0
    )
    schedule_type = models.CharField(
        _('Schedule Type'),
        max_length=100,
        choices=SCHEDULE_TYPES,
        blank=True,
        null=True,
    )

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')

    def _get_stream(self):
        step = self._get_inner_step

        topic = self._get_topic(step)

        if not topic:
            prev_ordering = step.ordering - 1
            while prev_ordering > 0 and not topic:
                prev_step = StreamProcessorStep.objects.filter(streamprocessor=step.streamprocessor,
                                                               ordering=prev_ordering).first()
                if prev_step:
                    topic = self._get_topic(prev_step, is_prev=True)
                elif not prev_step and prev_ordering >= 2:
                    prev_ordering -= 1
                    continue
                if not topic:
                    prev_ordering = prev_step.ordering - 1

        stream = Stream.objects.filter(name=topic).first()
        return stream

    @property
    def stream(self):
        if self.parent:
            result_placement = self.parent.result_placement
        else:
            result_placement = self.result_placement

        if result_placement != self.REPLACE:
            if self.topic:
                second_part = self.topic
            elif self.record_type:
                second_part = self.record_type
            elif hasattr(self.parent, 'topic') and self.parent.topic:
                second_part = self.parent.topic
            elif hasattr(self.parent, 'record_type') and self.parent.record_type:
                second_part = self.parent.record_type
            else:
                second_part = None
        else:
            if self.parent:
                parent = self.parent
            else:
                parent = self

            prev_step = StreamProcessorStep.objects.filter(
                streamprocessor=parent.streamprocessor, ordering__lt=parent.ordering
            ).order_by('-ordering').first()
            if prev_step:
                second_part = prev_step.stream[0].name if prev_step.stream[0] else None
            else:
                second_part = None

        return self._get_stream(), second_part

    @property
    def kpi(self):
        kpi = KPI.objects.filter(category=self.category_name, metric=self.metric)
        if kpi.exists():
            return kpi.first()

    @property
    def schema(self):
        stream = self.stream[0]
        if hasattr(stream, 'schema'):
            return stream.schema.name

    @property
    def _get_inner_step(self):
        if self.streamprocessor:
            return self
        return self.parent

    @property
    def prev_step(self):
        step = self._get_inner_step
        prev_step = StreamProcessorStep.objects.filter(
            streamprocessor=step.streamprocessor, ordering__lt=step.ordering
        ).order_by('-ordering').first()
        return prev_step if prev_step else step

    def _get_topic(self, step, is_prev=False):
        is_from_event = step.children.filter(key_type=self.FROM_EVENT).exists()
        record_type = step.record_type
        event_type = step.event_type

        if not is_from_event and record_type and (not is_prev or step.result_placement == self.REPLACE):
            return record_type

        if is_from_event and record_type and step.result_placement == self.REPLACE:
            return record_type

        if event_type:
            stream = Stream.objects.filter(display_name=event_type).first()
            if stream:
                return stream.name

        return step.topic

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['ordering']

    def __str__(self):
        return "%s (id: %s)" % (self.name, self.id)


class WorkflowTask(DateInfoModelMixin):
    INFORMATION = 'information'
    WARNING = 'warning'
    ALERT = 'alert'

    TASK_TYPES = (
        (INFORMATION, 'Information'),
        (WARNING, 'Warning'),
        (ALERT, 'Alert'),
    )

    STEP_TYPES_DATA = {
        StreamProcessorStep.WORKFLOW: {
            'step_type_name': 'Create Workflow Task',
            'fields': [
                {
                    'name': 'task_recipient_id',
                    'input_type': 'select',
                    'choices': [],
                    'popover': {
                        'top_text': 'recipient Top text',
                        'bottom_text': 'recipient Bottom text',
                        'position': StreamProcessorStep.POPOVER_POSITION,
                    },
                },
                {
                    'name': 'task_type',
                    'input_type': 'select',
                    'choices': [list(x) for x in TASK_TYPES],
                    'popover': {
                        'top_text': 'type Top text',
                        'bottom_text': 'type Bottom text',
                        'position': StreamProcessorStep.POPOVER_POSITION,
                    },
                },
                {
                    'name': 'task_title',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'task_title Top text',
                        'bottom_text': 'task_title Bottom text',
                        'position': StreamProcessorStep.POPOVER_POSITION,
                    },
                },
                {
                    'name': 'task_description',
                    'input_type': 'text',
                    'choices': [],
                    'popover': {
                        'top_text': 'task_description Top text',
                        'bottom_text': 'task_description Bottom text',
                        'position': StreamProcessorStep.POPOVER_POSITION,
                    },
                },
            ],
        },
    }

    title = models.CharField(
        _('Title'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=False,
    )

    recipient = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    type = models.CharField(
        _('Task Type'),
        max_length=100,
        choices=TASK_TYPES,
        default=INFORMATION,
    )

    streamprocessor_step = models.ForeignKey(
        StreamProcessorStep,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('WorkflowTask')
        verbose_name_plural = _('WorkflowTasks')
        ordering = ('id',)

    def __str__(self):
        return self.title


class TestSimulate:
    event = models.CharField(
        max_length=800,
        null=False,
    )
    stream = models.CharField(
        max_length=200,
        null=False,
    )
