import csv

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseForbidden
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.serializers import serialize
import json
import os
# import MySQLdb
# import demjson
from keji import settings
from django.shortcuts import render, redirect
# from py2neo import Graph, Node
import re
from numpy import *
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
import pandas as pd
import requests
from bs4 import BeautifulSoup
# Create your views here.


def get_index(request):
    if request.user.is_anonymous:
        # return render(request, 'index.html', locals())
        return render(request, 'denglu.html', locals())
    else:
        return render(request, 'chaxun.html', locals())
    # return render(request, 'index.html', locals())


def loginView(request):
    title = '用户登录'
    classContent = 'logins'
    code = 1
    res_json = {}
    if request.method == 'POST':
        username = request.POST.get('loginUsername', '')
        password = request.POST.get('loginPassword', '')
        print("username:", username)
        print("password:", password)
        print(User.objects.all()[0])
        if User.objects.filter(username=username):
            print("1")
            user = authenticate(username=username, password=password)
            if user:
                print("2")
                login(request, user)
                res_json['code'] = '999'
                # return redirect(reverse('index:index'))
                return JsonResponse(res_json)
            else:
                print("-1:密码错误")
        else:
            print("-2:用户名不存在，需要注册")
            # state = '注册成功'
            # d = dict(username=username, password=password, is_staff=1, is_active=1)
            # user = User.objects.create_user(**d)
            # user.save()
    return render(request, 'denglu.html', locals())


def registerView(request):
    res_json={}
    if request.method == 'POST':
        username = request.POST.get('registerUsername', '')
        password = request.POST.get('registerPassword', '')
        repassword = request.GET.get('registerWellPassword',"")
        print("username:", username)
        print("password:", password)
        if password == repassword:
            state = '注册成功'
            d = dict(username=username, password=password, is_staff=1, is_active=1)
            user = User.objects.create_user(**d)
            user.save()
            res_json["state"] = state
            return JsonResponse(res_json)
    return render(request, 'denglu.html', locals())


@login_required(login_url="/login")
def get_ciyun(request):
    return render(request, 'ciyun.html', locals())


# @login_required(login_url="/login")
# def get_yuqing(request):
#     center_datas = JRYQDB.objects.all()[34:66]  # 中间实时信息
#     # for item in jsqbs:
#     #     print(item.title)
#     length = JRYQDB.objects.all().count()
#     left_datas = JRYQDB.objects.all()[length-18:length]  # 左侧热点排行，最新动态，查询数据库最后更新的20条
#     # left_datas = JRYQDB.objects.all()[20:38]
#     right_datas = JRYQDB.objects.all()[:15]  # 右侧敏感信息
#
#     return render(request, 'yuqing.html', locals())


def get_shejiao(request):
    return render(request, 'shejiao.html', locals())


def get_redian(request):
    return render(request, 'redian.html', locals())


def get_navigator(request):
    return render(request, 'gnavigator.html', locals())


def get_explorer(request):
    return render(request, 'gexplorer.html', locals())


def grelfinderView(request):
    return render(request, 'grelfinder.html', locals())


@login_required(login_url="/login")
def chaxun(request):
    # if request.GET.get('wd', ''):
    #     wd = request.GET.get('wd', '')
    #     wd = str(wd).replace("'", '')
    #     likewd = wd + '%'
    #     print(likewd)
    #     connection = MySQLdb.connect('202.114.74.167', 'root', 'zhirong123', 'F_CL_ENTERPRISE_DB', charset='utf8')
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute('SELECT * FROM enterprise_t_unique WHERE E_ENAME like %s LIMIT 0,10000', [likewd, ])
    #         data = dictfetchall(cursor)
    #     except Exception as e:
    #         print(e)
    #         connection.rollback()
    #     finally:
    #         cursor.close()
    #         connection.close()
    #     # print('data的数据类型',type(data))
    #     ss = '{"code":0,"msg":"","count":10000,"data":'
    #     res_dic = {}
    #     res_dic["code"] = 0
    #     res_dic["msg"] = ""
    #     res_dic["count"] = "1000"
    #     res_dic["data"] = data
    #
    #     return JsonResponse(res_dic, safe=False, json_dumps_params={'ensure_ascii': False})
    # else:
    return render(request, 'chaxun.html', locals())


@login_required(login_url="/login")
def guquan(request):
    return render(request, 'guquan.html', locals())


def wanxiangxi(request):
    return render(request, 'wanxiangxi.html', locals())


def jrjg(request):
    return render(request, 'jrjg_zhanshi.html', locals())


def get_data(request):
    try:
        path = os.path.join(settings.BASE_DIR, "static/org_data_all_only.json")
        with open(path, encoding='utf-8') as f:  # 打开‘static/org_data.json’的json文件
            res = f.read()  # 读文件
            org_dict = json.loads(res)  # 把json串变成python的数据类型：字典
        # print("这是request",request.path)
        return JsonResponse(org_dict)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


def company_data(request):
    try:
        path = os.path.join(settings.BASE_DIR, "static/org_data_all_only.json")
        with open(path, encoding='utf-8') as f:  # 打开‘static/org_data.json’的json文件
            res = f.read()  # 读文件
            org_dict = json.loads(res)  # 把json串变成python的数据类型：字典
        # print("这是request",request.path)
        return JsonResponse(org_dict)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


def qiemi_data(request):
    try:
        path = os.path.join(settings.BASE_DIR, "static/qiemitupu.json")
        with open(path, encoding='utf-8') as f:  # 打开‘static/org_data.json’的json文件
            res = f.read()  # 读文件
            org_dict = json.loads(res)  # 把json串变成python的数据类型：字典
        # print("这是request",request.path)
        return JsonResponse(org_dict)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


def get_photo(request, html_str):
    """
       : 读取图片
       :param request:
       :return:
       """
    try:
        image_path = os.path.join(settings.BASE_DIR, "static/images/photo/{}".format(html_str))  # 图片路径
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/jpg")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


# @login_required(login_url="/login")
# def search_jrjg(request):
#     # 查询金融机构数据接口
#     jrjgInfos = fi2020_eidhid1.objects.all()
#     res = serialize("json", jrjgInfos)
#
#     ss = '{"code":0,"msg":"","count":1000,"data":'
#     str_json = ss+res+'}'
#
#     res = json.loads(str_json)
#     return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# @login_required(login_url="/login")
# def search_jrjg2(request):
#     page = request.GET.get('page', '')
#     limit = request.GET.get('limit', '')
#     connection = MySQLdb.connect('localhost', 'root', 'whu@2020', 'zhirong2_data', charset='utf8')
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM index_fi2020_eidhid1 LIMIT ' + str(int(limit)*int(page)) + ',' + str(limit))
#         data = dictfetchall(cursor)
#         ss = '{"code":0,"msg":"","count":10000,"data":'
#         res = ss + str(data) + '}'
#         res = res.replace("'", '"')
#         # print(len(ss))
#         # res = json.loads(res)
#         res = demjson.decode(res)
#     return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})


# @login_required(login_url="/login")
# def jrjgView(request):
#     title = '金融机构列表'
#     classContent = 'jrjg'
#     # 根据模型Types生成商品分类列表
#     # firsts = fi2020_eidhid1.objects.values('firsts').distinct()
#     # typesList = fi2020_eidhid1.objects.all()
#     # 获取请求参数
#     t = request.GET.get('t', '')
#     # s = request.GET.get('s', 'sold')
#     p = request.GET.get('p', 1)
#     n = request.GET.get('n', '')
#
#     # 根据请求参数查询商品信息
#     jrjgInfos = fi2020_eidhid1.objects.all()
#     if t:
#         types = jrjgInfos.objects.filter(id=t).first()
#         jrjgInfos = jrjgInfos.filter(types=types.seconds)
#     # if s:
#     #     jrjgInfos = jrjgInfos.order_by('-' + s)
#     if n:
#         jrjgInfos = jrjgInfos.filter(name__contains=n)
#
#     # 分页功能
#     # paginator = Paginator(jrjgInfos, 20)
#     # try:
#     #     pages = paginator.page(p)
#     # except PageNotAnInteger:
#     #     pages = paginator.page(1)
#     # except EmptyPage:
#     #     pages = paginator.page(paginator.num_pages)
#
#     return render(request, 'jrjg_zhanshi2.html', locals())


# @login_required(login_url="/login")
# def chaxunjiekou(request):
#     wd = request.GET.get('wd', '')
#     wd = str(wd).replace("'", '')
#     likewd=wd+'%'
#     print(likewd)
#     connection = MySQLdb.connect('202.114.74.167', 'root', 'zhirong123', 'F_CL_ENTERPRISE_DB', charset='utf8')
#     cursor = connection.cursor()
#     try:
#         cursor.execute('SELECT * FROM enterprise_t_unique WHERE E_ENAME like %s LIMIT 0,1000', [likewd,])
#         data = dictfetchall(cursor)
#     except Exception as e:
#         print(e)
#         connection.rollback()
#     finally:
#         cursor.close()
#         connection.close()
#     # print('data的数据类型',type(data))
#     ss = '{"code":0,"msg":"","count":10000,"data":'
#     res_dic = {}
#     res_dic["code"] = 0
#     res_dic["msg"] = ""
#     res_dic["count"] = "1000"
#     res_dic["data"] = data

#     return JsonResponse(res_dic, safe=False, json_dumps_params={'ensure_ascii': False})


def chaxunjieguo(request):
    return render(request, 'gongshangzhuceqiye.html', locals())


# @login_required(login_url="/login")
# def neo4j_data(request):
#     wd = ""
#     wd = request.GET.get("wd", wd)
#     wd = wd.replace("'", '')
#     graph = Graph("bolt://202.114.74.167:7687", password="123456")
#     data = graph.run("MATCH (head:Node)-[edge:Hold]->(tail:Node) "
#                   "WHERE tail.H_NAME = {H_NAME}"
#                   "RETURN edge", {"H_NAME": wd}).to_ndarray()
#     # print(data)
#     res_json = {"categories": {"company": "公司"}, "data": {"nodes": [], "edges": []}}
#     node_dic = {'label': wd, "value": 20, "id": 1, "categories": ["company"], "info": wd}
#     node_dic_list = []
#     node_dic_list.append(node_dic)
#     edge_dic_list = []
#     i = 1
#     for path in data:
#         i += 1
#         # print(path)
#         sn = re.findall('H_NAME=\'(.*?)\'\)', str(path))
#         share = re.findall('H_HSHARE=\'(.*?)\'\)', str(path))
#         # print(share[0])
#         node_dic_tem = {'label': sn[0], "value": 10, "id": i, "categories": ["company"], "info": sn[0]}
#         node_dic_list.append(node_dic_tem)
#         edge_dic_tem = {"id": 1000+i, "label": "持股:"+str(share[0]), "from": i, "to": 1}
#         edge_dic_list.append(edge_dic_tem)
#     # print(node_dic_list)
#     # print(edge_dic_list)
#     res_json["data"]["nodes"] = node_dic_list
#     res_json["data"]["edges"] = edge_dic_list
#     # print(res_json)
#     return JsonResponse(res_json, safe=False, json_dumps_params={'ensure_ascii': False})


# @login_required(login_url="/login")
# def neo4j_datas(request):
#     wd = ""
#     wd = request.GET.get("wd", wd)
#     ceng = request.GET.get("ceng", 3)
#     print(ceng)
#     wd = wd.replace("'", '')

#     graph = Graph("bolt://202.114.74.167:7687", password="123456")

#     data = graph.run("MATCH (head:Node)-[edge:Hold*1.."+str(ceng)+"]->(tail:Node) "
#                   "WHERE tail.H_NAME = {H_NAME}"
#                   "RETURN edge, length(edge)", {"H_NAME": wd}).to_ndarray()

#     node_dic = {'label': wd, "value": 20, "id": 1, "categories": ["company"], "info": wd}
#     node_dic_id = {wd: 1}  # {'中国证券金融股份有限公司': 1, '上海证券交易所': 2, '华宝信托有限责任公司': 3,
#     node_dic_list = []
#     #[{'label': '中国证券金融股份有限公司', 'value': 20, 'id': 1, 'categories': ['company']
#     # , 'info': '中国证券金融股份有限公司'}, {'label': '上海证券交易所', 'value': 10, 'id': 2, 'categories': ['company1'], 'info': '上海证券交易所'},
#     node_dic_list.append(node_dic)
#     edge_dic_list = []
#     edge_tup_id = {}  # 边字典，键是（开始节点，终止节点，股权）
#     # {('华宝信托有限责任公司', '上海证券交易所', '0.0'): 1000, ('浙江省舟山市财政局', '华宝信托有限责任公司', '0.02'): 1001,
#     i = 1
#     k = 1000
#     company_count_max = 1
#     # 因为多层股权查询的时候，返回结果是以列表返回，列表的每一项都是一条path，所以第一次遍历要统计所有公司，并分配id，然后在遍历每条边生成前端需要的json边数据
#     for path in data:
#         # print(path)  # [list([Hold(Node('Node', H_HCLASS='qgov', H_ID='2e589b5b-7235-11e9-aa66-0242ac120002', H_NAME='中国船东互保协会'), Node('Node', H_ETYPE='2', H_ID='a757e79c-1817-466c-be31-3241393ed443', H_NAME='中国民生银行股份有限公司'), H_HCAPCAMT='36485000000', H_HCAPCCRY='CNY', H_HSHARE='0.0298')])]
#         # [list([Hold(Node('Node', H_ID='3c22477e-6ab7-4e59-9423-0fb8ba784db4', H_NAME='中国泛海控股集团有限公司'), Node('Node', H_ETYPE='2', H_ID='a757e79c-1817-466c-be31-3241393ed443', H_NAME='中国民生银行股份有限公司'), H_HCAPCAMT='36485000000', H_HCAPCCRY='CNY', H_HSHARE='0.0461')])]
#         # [list([Hold(Node('Node', H_ID='71131404-242a-4433-9bfd-b1a3b908dac4', H_NAME='山东泛海集团公司'), Node('Node', H_ID='3c22477e-6ab7-4e59-9423-0fb8ba784db4', H_NAME='中国泛海控股集团有限公司'), H_HCAPCAMT='19600000000', H_HCAPCCRY='***未知***', H_HCAPPAMT='0', H_HCAPPCRY='***未知***', H_HSDATE='Wed Mar 01 00:00:00 CST 2017', H_HSHARE='0.98'), Hold(Node('Node', H_ID='3c22477e-6ab7-4e59-9423-0fb8ba784db4', H_NAME='中国泛海控股集团有限公司'), Node('Node', H_ETYPE='2', H_ID='a757e79c-1817-466c-be31-3241393ed443', H_NAME='中国民生银行股份有限公司'), H_HCAPCAMT='36485000000', H_HCAPCCRY='CNY', H_HSHARE='0.0461')])]
#         sns = re.findall('H_NAME=\'(.*?)\'\)', str(path))
#         share = re.findall('H_HSHARE=\'(.*?)\'\)', str(path))
#         # neo数据库有的节点有问题，没有H_NAME属性。如果路径中节点不为偶数，说明是无效路径，直接跳过
#         if len(sns)%2 != 0:
#             continue
#         # 每条path包含的节点数不同，要找到最大path，以便设定前端框架的节点类型（每一层公司算作一个节点类型，前端才能以不同的颜色显示）
#         if len(sns) / 2 > company_count_max:
#             company_count_max = int(len(sns)/2)
#         # 遍历每条路径的节点，节点列表[A,B,B,C,C,D]意思是A->B，B->C,C->X，六个节点，C是一层持股，B是二层持股，A是三层持股
#         for j, sn in enumerate(sns):
#             # 生成企业名和id的字典，用于后续生成边的对应关系的时候，根据公司名找公司ID
#             # {'中国证券金融股份有限公司': 1, '上海证券交易所': 2, '华宝信托有限责任公司': 3,
#             if not node_dic_id.get(sn, ''):
#                 i += 1
#                 node_dic_id[sn] = i
#                 company_count = len(sns) / 2
#                 node_dic_tem = {'label': sn, "value": 10, "id": i, "categories": ["company"+str(int(company_count))], "info": sn}
#                 node_dic_list.append(node_dic_tem)
#                 company_count -= 1
#             # print(j,sn)
#             # 生成关系字典。{(('上海证券交易所', '中国证券金融股份有限公司'), '0.205'): 1023,
#             # (('华宝信托有限责任公司', '上海证券交易所'), '0.0'): 1001, (('申万宏源集团股份有限公司', '上海证券交易所'), '0.0'): 1003,
#             if j+1 == len(sns):
#                 break
#             if j%2 == 0:
#                 if not edge_tup_id.get((sns[j], sns[j+1], share[int(j/2)]), ''):
#                     edge_tup_id[(sns[j], sns[j+1], share[int(j/2)])] = k
#                     k += 1

#     # 遍历关系列表，生成用于前端显示的关系列表数据格式
#     m = 0
#     for k,v in edge_tup_id.items():
#         edge_dic_tem = {"id": 10000 + m, "label": "持股:" + k[2], "from": node_dic_id[k[0]], "to": node_dic_id[k[1]]}
#         edge_dic_list.append(edge_dic_tem)
#         m += 1

#     # 生成用于前端显示的categories的字典，一个键值对对应一层股权上节点不同颜色
#     categories_dic = {"company": "公司"}
#     for i in range(1, company_count_max+1):
#         categories_dic["company"+str(i)] = str(i)+"层持股公司"

#     res_json = {"categories": categories_dic, "data": {"nodes": [], "edges": []}}
#     # print(node_dic_id)
#     # print(edge_tup_id)
#     # print(node_dic_list)
#     # print(edge_dic_list)
#     # print(res_json)

#     res_json["data"]["nodes"] = node_dic_list
#     res_json["data"]["edges"] = edge_dic_list
#     # print(res_json)
#     return JsonResponse(res_json, safe=False, json_dumps_params={'ensure_ascii': False})


@login_required(login_url="/login")
def shzq_data(request):
    # 上海证券的静态信息
    try:
        path = os.path.join(settings.BASE_DIR, "static/上海证券.json")
        with open(path, encoding='utf-8') as f:  # 打开‘static/上海证券.json’的json文件
            res = f.read()  # 读文件
            data_dict = json.loads(res)  # 把json串变成python的数据类型：字典
        # print("这是request",request.path)
        return JsonResponse(data_dict)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


def linekg(request):
    aid=1
    aid = request.GET.get("aid", aid)
    aid = int(aid)
    json_dict = {}
    json_dict["categories"] = {
        "time": "时间",
        "loc": "地点",
        "industry": "涉及行业",
        "cate": "商业秘密类别",
        "carrier": "载体形式",
        "nature": "性质",
        "pro": "侵权人属性",
        "way": "侵权方式",
        "aim": "侵权目的",
        "event": "事件",
        "people": "涉案人员",
        "org": "组织机构",
        "law": "法律条款",
        "article": "正文",
    }
    li = ["time", "loc", "industry", "cate", "carrier", "nature", "pro", 'way', 'aim', 'event', 'people', 'org', 'law',
          'article']
    lic = ["时间", "地点", "涉及行业", "商业秘密类别", "载体形式", "性质", "侵权人属性", "侵权方式", "侵权目的", "事件", "窃密方", "失密方", "法律条款", "正文"]
    nodes_list = []  # 节点列表
    edges_list = []  # 边列表
    s2id = {}
    s2count = {}
    STATIC_ID = 1500
    path = os.path.join(settings.BASE_DIR, "static/qiemianli3.csv")
    # csv_data = pd.read_csv(path, low_memory=False)
    # r2 = csv_data.loc[aid]
    r2 = ''
    with open(path, 'r', encoding='utf8') as f:
        csv_reader = csv.reader(f)
        for i, row in enumerate(csv_reader):
            if i == aid:
                r2 = row

    i = 0
    for item in r2:
        if i == 13:
            break
        s2id[item] = i
        node_dict = {}
        node_dict['id'] = i
        node_dict['label'] = item
        node_dict['group'] = li[i]
        nodes_list.append(node_dict)
        i += 1
    print(nodes_list)
    print(s2id)
    j = 0
    for item in r2:
        if j == 13:
            break
        if j == 9:
            j += 1
            continue
        edge_dict = {}
        edge_dict['source'] = s2id[r2[9]]
        edge_dict['target'] = s2id[item]
        edge_dict['label'] = lic[j]
        edges_list.append(edge_dict)
        j += 1
    print('edges_list:', edges_list)
    json_dict['nodes'] = nodes_list
    json_dict['edges'] = edges_list
    # print(json_dict)
    # json_dict = json.loads(json_dict)
    # return JsonResponse(json_dict, safe=False)
    return JsonResponse(json_dict, safe=False, json_dumps_params={'ensure_ascii': False})


def anlis(request):
    path = os.path.join(settings.BASE_DIR, "static/qiemianli4.csv")
    csv_data = pd.read_csv(path, low_memory=False).iloc[:100].dropna()
    csv_data['category'] = csv_data['category'].apply(lambda x: eval(x))
    csv_data['content'] = csv_data['content'].apply(lambda x: eval(x))
    csv_data['form'] = csv_data['form'].apply(lambda x: eval(x)[0])
    json_data = eval(csv_data.to_json(orient='records', force_ascii=False))
    print(json_data)
    return JsonResponse({"data": json_data}, safe=False)


def anliid(request):
    aid=1
    aid = request.GET.get("caseId", aid)
    aid = int(aid) - 1
    path = os.path.join(settings.BASE_DIR, "static/qiemianli4.csv")
    csv_data = pd.read_csv(path, low_memory=False)
    row = csv_data.loc[aid]
    row['category'] = eval(row['category'])
    row['content'] = eval(row['content'])
    row['form'] = eval(row['form'])[0]
    json_data = eval(row.to_json(orient='index', force_ascii=False))
    # print(json_data)
    return JsonResponse(json_data, safe=False)


def sizhi_data(request):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    }
    wd = "泄密事件"
    wd = request.GET.get("wd", wd)
    url = "https://api.ownthink.com/kg/knowledge?entity=" + wd
    reqs = requests.get(url, headers=headers)
    # print(reqs)
    html = reqs.content
    # saveHTML("t1", html)
    # print("html:", html)
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    # print(soup.find('p').string)
    data_dic = json.loads(soup.find('p').string)
    res_json = {"categories": {"cate1": "类别1", "cate2": "类别2"}, "nodes": [], "edges": []}
    node_dic = {'label': wd, "value": 20, "id": 1, "categories": ["cate1"], "info": data_dic['data']['desc']}

    node_dic_list = []
    node_dic_list.append(node_dic)
    edge_dic_list = []
    i = 1
    for item in data_dic["data"]["avp"]:
        i += 1
        # print(path)

        node_dic_tem = {'label': item[1], "value": 10, "id": i, "categories": ["cate2"], "info": item[1]}
        node_dic_list.append(node_dic_tem)
        edge_dic_tem = {"id": 1000 + i, "label": item[0], "source": 1, "target": i}
        edge_dic_list.append(edge_dic_tem)
    res_json["nodes"] = node_dic_list
    res_json["edges"] = edge_dic_list
    return JsonResponse(res_json, safe=False, json_dumps_params={'ensure_ascii': False})


def currentUser_view(request):
    data = {
      "success": True,
      "data": {
        "name": 'admin',
        "avatar": 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png',
        "userid": '00000001',
        "email": 'antdesign@alipay.com',
        "signature": '海纳百川，有容乃大',
        "title": '交互专家',
        "group": '蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED',
        "tags": [
          {
            "key": '0',
            "label": '很有想法的',
          },
          {
            "key": '1',
            "label": '专注设计',
          },
          {
            "key": '2',
            "label": '辣~',
          },
          {
            "key": '3',
            "label": '大长腿',
          },
          {
            "key": '4',
            "label": '川妹子',
          },
          {
            "key": '5',
            "label": '海纳百川',
          },
        ],
        "notifyCount": 12,
        "unreadCount": 11,
        "country": 'China',
        "access": "admin",
        "geographic": {
          "province": {
            "label": '浙江省',
            "key": '330000',
          },
          "city": {
            "label": '杭州市',
            "key": '330100',
          },
        },
        "address": '西湖区工专路 77 号',
        "phone": '0752-268888888',
      }
    }
    return JsonResponse(data, safe=False)


def loginAccount_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Content-type为application/json时，Django不支持request.POST.get()，但可以通过request.body来获取string类型的参数
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # type = request.POST.get("type")
        username = data.get("username")
        password = data.get("password")
        type = data.get("type")
        res_json = {}
        # if User.objects.filter(username=username):
        if username == 'admin' or username == 'user':
            print("1")
            # user = authenticate(username=username, password=password)
            # if user:
            if password == 'ant.design':
                print("2")
                # login(request, user)
                res_json['status'] = 'ok'
                res_json['type'] = type
                res_json['currentAuthority'] = 'admin'
                # return redirect(reverse('index:index'))
                return JsonResponse(res_json)
            else:
                print("-1:密码错误")
                res = {
                    "status": "error",
                    "type": type,
                    "currentAuthority": "guest",
                    "info": "-1:密码错误"
                }
                return JsonResponse(res, safe=False)
        else:
            print("-2:用户名不存在，需要注册")
            res = {
                "status": "error",
                "type": type,
                "currentAuthority": "guest",
                "info": "-2:用户名不存在，需要注册"
            }
            return JsonResponse(res, safe=False)
            # state = '注册成功'
            # d = dict(username=username, password=password, is_staff=1, is_active=1)
            # user = User.objects.create_user(**d)
            # user.save()

    # if password == "ant.design" and username == "admin":
    #     res = {
    #         "status": "ok",
    #         "type": type,
    #         "currentAuthority": "admin"
    #     }
    #     return JsonResponse(res, safe=False)
    # elif password == "ant.design" and username == "user":
    #     res = {
    #         "status": "ok",
    #         "type": type,
    #         "currentAuthority": "user"
    #     }
    #     return JsonResponse(res, safe=False)
    # else:
    #     res = {
    #         "status": "error",
    #         "type": type,
    #         "currentAuthority": "guest"
    #     }
    #     return JsonResponse(res, safe=False)


def outLogin_view(request):
    res = {
        "data": {},
        "success": True
    }
    return JsonResponse(res, safe=False)


def page500_view(request):
    res = {
        "timestamp": 1513932555104,
        "status": 500,
        "error": 'error',
        "message": 'error',
        "path": '/base/category/list',
    }
    return JsonResponse(res, safe=False)


def page404_view(request):
    res = {
        "timestamp": 1513932643431,
        "status": 404,
        "error": 'Not Found',
        "message": 'No message available',
        "path": '/base/category/list/2121212',
    }
    return JsonResponse(res, safe=False)


def page401_view(request):
    res = {
        "timestamp": 1513932555104,
        "status": 401,
        "error": 'Unauthorized',
        "message": 'Unauthorized',
        "path": '/base/category/list',
    }
    return JsonResponse(res, safe=False)


def page403_view(request):
    res = {
        "timestamp": 1513932555104,
        "status": 403,
        "error": 'Unauthorized',
        "message": 'Unauthorized',
        "path": '/base/category/list',
    }
    return JsonResponse(res, safe=False)
