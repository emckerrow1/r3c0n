from django import template
register = template.Library()

@register.filter
def __count_page_visits(all_metrics, home_count):
    count = home_count
    for article in all_metrics:
    	count += article.metric_count_set.first().visit_count
    return count