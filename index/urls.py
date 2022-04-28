from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_navigator, name='index'),
    path('login', views.loginView, name='login'),  # 返回denglu.html页面
    path("register/", views.registerView, name='register'),
    # path('ciyun/', views.get_ciyun, name='ciyun'),  # 词云页面
    # path('yuqing/', views.get_yuqing, name='yuqing'),  # 舆情页面
    # path('shejiao/', views.get_shejiao, name='shejiao'),  # 社交网络分析页面
    # path('redian/', views.get_redian, name='redian'),  # 热点分析页面
    path('gnavigator/', views.get_navigator, name='gnavigator'),  # 企业关系查询页面显示所有节点和边
    path('gexplorer/', views.get_explorer, name='gexplorer'),
    path('grelfinder/', views.grelfinderView, name='grelfinder'),  # 企业关系查询
    # path('chaxun/', views.chaxun, name='chaxun'),  # 查询金融实体页面
    # path('guquan/', views.guquan, name='guquan'),  # 股权页面
    # path('wanxiangxi/', views.wanxiangxi, name='wanxiangxi'),  # 资本系的万向系页面
    # path('jrjg/', views.jrjgView, name='jrjg'),  # 金融机构查询页面
    # path('chaxunjieguo/', views.chaxunjieguo, name='chaxunjieguo'),  # 查询企业工商信息页面

    # path('jrjg/search_jrjg/', views.search_jrjg, name='search_jrjg'),  # python的ORM操作数据库，然后转为json数据返回
    # path('jrjg/search_jrjg2/', views.search_jrjg2, name='search_jrjg'),  # 纯sql查询数据库返回
    # path('neo4j_data/', views.neo4j_data, name='neo4j_data'),  # 查询neo4j数据库接口，一层股权
    # path('neo4j_datas/', views.neo4j_datas, name='neo4j_datas'),  # 查询neo4j数据库接口,多层股权
    # path('shzq_data/', views.shzq_data, name='shzq_data'),  # 查询上海证券交易所的图数据
    # path('chaxunjiekou/', views.chaxunjiekou, name='chaxunjiekou'),  # 查询工商企业数据接口
    path('org_data/', views.get_data, name='orgdata'),  # 查询人物关系数据接口，改文件url的时候也要修改view函数里面的文件路径
    path('company_data/', views.company_data, name='company_data'),  # 查询企业关系数据接口
    path('qiemi_data/', views.qiemi_data, name='qiemi_data'),  
    path('gnavigator/images/photo/<html_str>', views.get_photo, name='imagepage'),
    # path('shuaxin/', views.get_index3, name='shuaxin'),  # 刷新昨天和今天的，‘一天调用一次’
    # path('charts/', views.get_charts),  # 查询某个节点，双击显示关联节点
    # path('forms/', views.get_forms),  # 查询两个节点之间的关系路径
    # path('register/', views.get_register),
    # path('tables/', views.get_tables),

    # path('org_data.json/', views.get_data, name='orgdata'), # 改文件url的时候也要修改view函数里面的文件路径
    # path('images/photo/<html_str>', views.get_photo, name='imagepage'),
    path('gexplorer/images/photo/<html_str>', views.get_photo, name='imagepage'),
    path('grelfinder/images/photo/<html_str>', views.get_photo, name='imagepage'),
    path('images/photo/<html_str>', views.get_photo, name='imagepage'),
    path('api/cases/', views.anlis, name='anlis'),
    path('api/caseDetail/', views.anliid, name='anliid'),
    path('api/caseGraph/', views.linekg, name='linekg'),
    path('api/sizhi/', views.sizhi_data, name='sizhi'),
    path('api/currentUser/', views.currentUser_view, name='currentUser'),
    path('api/login/account/', views.loginAccount_view, name='loginAccount'),
    path('api/login/outLogin/', views.outLogin_view, name='outLogin'),
    path('api/500/', views.page500_view, name='page500'),
    path('api/401/', views.page401_view, name='page401'),
    path('api/403/', views.page403_view, name='page403'),
    path('api/404/', views.page404_view, name='page404'),
    
]