from analysis.models import ReportItem


def method_duplicate_duplicate_report(project_id, report):
    report_items = ReportItem.objects.filter(report=report)

    report.pk = None
    report.project_id = project_id
    report.save()

    for report_item in report_items:
        report_item.pk = None
        report_item.report = report
        report_item.save()


def time_window_to_sql(t):
    time_stamps = {
        ReportItem.LAST_MINUTE: 'TIMESTAMPADD(MINUTE, -1, CURRENT_TIMESTAMP)',
        ReportItem.LAST_10_MINUTES: 'TIMESTAMPADD(MINUTE, -10, CURRENT_TIMESTAMP)',
        ReportItem.LAST_HOUR: 'TIMESTAMPADD(HOUR, -1, CURRENT_TIMESTAMP)',
        ReportItem.LAST_DAY: 'TIMESTAMPADD(DAY, -1, CURRENT_TIMESTAMP)',
        ReportItem.LAST_WEEK: 'TIMESTAMPADD(WEEK, -1, CURRENT_TIMESTAMP)',
        ReportItem.LAST_YEAR: 'TIMESTAMPADD(YEAR, -1, CURRENT_TIMESTAMP)'
    }

    return time_stamps.get(t)


def filter_value_to_sql(f):
    filters = {
        ReportItem.FILTER_LESS_THAN: '<',
        ReportItem.FILTER_GREATER_THAN: '>',
        ReportItem.FILTER_EQUAL: '='
    }

    return filters.get(f)