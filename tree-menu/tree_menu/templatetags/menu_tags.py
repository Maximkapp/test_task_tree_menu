# tree_menu/templatetags/menu_tags.py
from django import template
from django.urls import reverse, NoReverseMatch
from tree_menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    # 1 DB query: получаем все элементы меню по имени меню
    items_qs = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')
    items = list(items_qs)  # выполняется запрос здесь

    # build map id -> node dict
    nodes = {}
    children_map = {}
    for it in items:
        nodes[it.id] = {
            'obj': it,
            'children': [],
            'parent_id': it.parent_id,
            'url_resolved': None,
            'is_active': False,
            'expanded': False,
        }
        children_map.setdefault(it.parent_id, []).append(it.id)

    # attach children
    for node_id, node in nodes.items():
        for child_id in children_map.get(node_id, []):
            node['children'].append(nodes[child_id])

    # helper: resolve url
    def resolve_url(it):
        if it.url:
            return it.url
        if it.named_url:
            try:
                return reverse(it.named_url)
            except NoReverseMatch:
                return None
        return None

    # resolve urls and find active item(s)
    active_node_id = None
    if request is not None:
        path = request.path
        # resolve urls for all nodes and compare to request.path
        for nid, node in nodes.items():
            node['url_resolved'] = resolve_url(node['obj'])
            if node['url_resolved'] and node['url_resolved'] == path:
                node['is_active'] = True
                active_node_id = nid

    # mark ancestors of active node as expanded
    if active_node_id:
        cur = nodes[active_node_id]
        # активный пункт
        cur['expanded'] = True

        # предки
        parent_id = cur['parent_id']
        while parent_id:
            parent_node = nodes.get(parent_id)
            if not parent_node:
                break
            parent_node['expanded'] = True
            parent_id = parent_node['parent_id']

        # первый уровень детей активного пункта раскрыт
        for child in cur['children']:
            # раскрываем только сами пункты, но их дети остаются скрытыми
            child['expanded'] = False
            # если нужно, можно сразу выставить is_active для детей, если их URL совпадает с path
            if child['url_resolved'] == path:
                child['is_active'] = True

    # prepare top-level nodes (parent_id == None)
    tree = [nodes[nid] for nid in children_map.get(None, [])]

    return {'menu_tree': tree, 'request': request}
