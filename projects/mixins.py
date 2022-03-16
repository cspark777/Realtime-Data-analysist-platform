from django.conf import settings
from django.db.models import Q

from core.utils import get_database_data
from projects.models import Project
from schemas.models import Schema
from streams.models import Stream


kafka_url = settings.KAFKA_URL
druid_host, druid_port = get_database_data()


def rows_to_json(curs):
    json_objects = []
    for row in curs:
        record = {}
        for field in row._fields:
            record[field] = getattr(row, field)
        json_objects.append(record)
    return json_objects


class ProjectsListMixin:
    current_project = None

    def set_projects(self, context, request=None):
        user = self.request.user if hasattr(self, 'request') else request.user
        context['projects'] = Project.objects.filter(
            Q(created_by=user) | Q(collaboration__email=user)
        )
        self.current_project = context['projects'].filter(is_current=True).first()
        context['current_project'] = self.current_project
        schemas = Schema.objects.filter(project=self.current_project)
        context["event_definition_exists"] = schemas.exists()
        context["event_stream_exists"] = Stream.objects.filter(schema__in=schemas).exists()

        """ In old design we had "All logs" nav.bar button with badge 
        indicated top 50 project messages with high priority.
        """
        # if self.current_project:
        #     conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
        #     curs = conn.cursor()
        #     query = "SELECT COUNT(*) FROM (SELECT DISTINCT * FROM DATA_logs WHERE project_id = " + str(
        #         self.current_project.id) + " AND priority = 'HIGH' LIMIT 50)"
        #     try:
        #         res = curs.execute(query).fetchone()
        #         if res:
        #             context['high_log_number'] = res._0
        #             query = "SELECT * FROM DATA_logs WHERE project_id = " + str(self.current_project.id) + \
        #                     " AND priority = 'HIGH' ORDER BY __time DESC LIMIT 20"
        #             curs.execute(query)
        #             context['high_logs'] = rows_to_json(curs)
        #             for obj in context['high_logs']:
        #                 if '_0' in obj.keys():
        #                     obj['date'] = datetime.strptime(obj['_0'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime(
        #                         '%m-%d-%Y %H:%M')
        #                     obj.pop('_0')
        #                 if 'streamprocessor_id' in obj.keys() and obj['streamprocessor_id'].isdigit():
        #                     try:
        #                         streamprocess = StreamProcessor.objects.get(id=obj['streamprocessor_id'])
        #                         obj['streamprocessor'] = streamprocess.name
        #                     except:
        #                         pass
        #         else:
        #             context['high_log_number'] = ""
        #     except:
        #         pass
        return context


set_projects = ProjectsListMixin().set_projects
