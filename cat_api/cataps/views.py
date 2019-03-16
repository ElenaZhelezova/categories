from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from .forms import GetDataForm
from .models import Category, CategoryChildren

import json
import re


def get_data(request):
    form = GetDataForm()
    if request.method == 'POST':
        form = GetDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['tree_data']
            for line in data:
                ''.join(re.sub("^\s+|\n|\r|\s+$", '', line))
            try:
                data = json.loads(data)
            except ValueError:
                #return JsonResponse({"Error": "expected JSON"})
                return render(request,  'cataps/get_data.html', {
                    'msg' : json.dumps({"error": "expected JSON"}),
                    'form': form,
                })

            if not isinstance(data, list):
                data_list = []
                data_list.append(data)
                data = data_list

            while data:
                new_data = []
                for item in data:
                    try:
                        category = Category.objects.get(name=item['name'])
                    except Category.DoesNotExist:
                        category = Category(name=item['name'])
                        category.save()
                    try:
                        parent = CategoryChildren.objects.get(category_name=category)
                    except CategoryChildren.DoesNotExist:
                        parent = CategoryChildren(category_name=category)
                        parent.save()

                    if 'children' in item:
                        for child in item['children']:
                            try:
                                child_cat = Category.objects.get(name=child['name'])
                            except Category.DoesNotExist:
                                child_cat = Category.objects.create(name=child['name'])
                                child_cat.save()
                            parent.category_children.add(child_cat)

                            new_data.append(child)

                data = new_data

            return HttpResponseRedirect('submit_data')
    else:
        form = GetDataForm()

    return render(request, 'cataps/get_data.html', {
        'form': form,
    })


def submit_data(request):
    return render(request, 'cataps/submit.html')


def category_detail(request, pk):
    answer = {"parents":[], "children":[],"sibblings":[]}
    category = get_object_or_404(Category, pk=pk)
    children = CategoryChildren.objects.get(category_name=category).category_children.values()
    for child in children:
        answer["children"].append(child)
    cat = category

    while cat:
        try:
            parent_id = CategoryChildren.objects.get(category_children=cat).category_name.pk
            parent_category = Category.objects.get(pk=parent_id)
            answer['parents'].append({"id": parent_category.id, "name": parent_category.name})
            sibblings = CategoryChildren.objects.get(category_name=parent_category).category_children.values().\
                exclude(name=cat.name)
            for sib in sibblings:
                answer["sibblings"].append(sib)
            cat= parent_category

        except CategoryChildren.DoesNotExist:
            break



    return render(request, 'cataps/category_detail.html',
                      {
                          'category': category,
                          'parents': answer['parents'],
                          'children': answer['children'],
                          'sibblings': answer['sibblings']

                      })
