def method_duplicate_search(project_id, search):
    search.pk = None
    search.project_id = project_id
    search.save()

