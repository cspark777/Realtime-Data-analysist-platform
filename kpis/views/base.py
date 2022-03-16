from django.contrib.auth.mixins import LoginRequiredMixin

from projects.mixins import ProjectsListMixin


class KPIBaseView(LoginRequiredMixin, ProjectsListMixin):
    @staticmethod
    def get_payload_filter(slice_field, slice_value, kpi_metric):
        if slice_field and slice_value:
            return {
                'type': 'and',
                'fields': [
                    {
                        "type": "selector",
                        "dimension": "metric",
                        "value": kpi_metric
                    },
                    {
                        "type": "selector",
                        "dimension": "slice_field",
                        "value": slice_field
                    },
                    {
                        "type": "selector",
                        "dimension": "slice_value",
                        "value": slice_value
                    }]
            }
        return {
            "type": "selector",
            "dimension": "metric",
            "value": kpi_metric
        }