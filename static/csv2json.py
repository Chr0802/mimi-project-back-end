import csv
import json
import pandas as pd
import os
# from keji import settings
# STATIC_ID = 10000


def get_rdf_fromlabeldata(filename0, filename1):
    # 取得标注数据里面正确的三元组数据
    # 'sr_biaozhu_hezuoall_n=2.csv'
    # 'wt_biaozhu_hezuoall_n=n.csv'
    # filename1 = 'wt_biaozhu_hezuoall_n=n.csv'
    # filename2 = 'org_rdf_hezuon=n.csv'
    # filename3 = "lz_biaozhu_jingzhengall_n=n1.csv"
    # filename4 = 'org_rdf_jingzhengn=n.csv'
    # with open(filename3,encoding='gb18030',errors='ignore') as f1:
    with open(filename0, 'r') as f0:
        with open(filename1, 'a', newline='', encoding='utf-8-sig') as f1:
            f0_reader = csv.reader(f0)
            f2_writer = csv.writer(f1)
            # f2_writer.writerow(["e1", "e2", "label"])
            print(f0_reader)
            try:
                for row_list in f0_reader:
                    e1 = row_list[1]
                    e2 = row_list[2]
                    label = row_list[3]
                    # print([e1, e2, label])
                    if label == str(1):
                        print([e1, e2, label])
                        f2_writer.writerow([e1, e2, label])
            except Exception as e:
                print(e.args, row_list)


def save2org_rdf(filename0, filename1, relation):
    # 把标注数据里面正确的三元组写到rdf表中，relation是“竞争”或“合作”或“供应”
    with open(filename0, encoding='utf-8') as f0:
        with open(filename1, 'a', newline='', encoding='utf-8') as f1:
            f0_reader = csv.reader(f0)
            f1_writer = csv.writer(f1)
            # f1_writer.writerow(['e1', 'e2', 'rel'])
            for e1, e2, label in f0_reader:
                if label == 'label':
                    continue
                f1_writer.writerow([e1, e2, relation])


def ge_eid(filename0):
    # 没成功，因为csv没法把符合条件的e1id写进去。只能写入列表。
    with open(filename0, encoding='utf-8') as f0:
        f0_reader = csv.reader(f0)
        e_list = []  # 存储所有实体，无重复
        for row in f0_reader:
            e1 = row[0]
            e2 = row[1]
            if e1 not in e_list:
                e_list.append(e1)
            if e2 not in e_list:
                e_list.append(e2)


# 改变一下思路，把三元组（rdf）表拆开，单独写一个节点表，可避免往CSV中某一行的空给内插入内容。
# 写一个函数，每次把rdf表的三元组对应生成节点表，然后读出节点表的实体id得到e_list，
# 从rdf表读出实体对和关系，然后从e_list中取得实体对对应的id，生成关系表。写e_dict统计每个实体出现的次数

# rdf表设计 e1|e2|rel|
# 实体表设计 e1|e2|rel|e1id|e2id|e1value|e2value


def get_mid_li_dic(filename0):
    e_list = []  # 存储所有实体，无重复,实体id为e_list.index()+1，这样没有id==0的
    e_dict = {}
    # 生成所有实体的id以及出现的次数。
    with open(filename0, encoding='gb18030') as f0:
        f0_reader = csv.reader(f0)
        for row in f0_reader:
            e1 = row[0]
            e2 = row[1]
            rel = row[2]
            if e1 == 'e1':
                # 不把表头统计进来
                continue
            # 把没有出现过的实体加入列表
            if e1 not in e_list:
                e_list.append(e1)
            if e2 not in e_list:
                e_list.append(e2)
            # 统计出现的次数
            if e_dict.get(e1) is None:
                # 初始化加入的时候，已经出现了一次，所以是1
                e_dict[e1] = 1
            else:
                e_dict[e1] += 1
            if e_dict.get(e2) is None:
                e_dict[e2] = 1
            else:
                e_dict[e2] += 1

        print("e_list:", e_list)
        print("e_dict:", e_dict)
        # e_list: ['e1', 'e2', '泰克', 'Coherent Solutions', '高通', '微软', '诺基亚' ]
        # e_dict: {e_dict: {'e1': 1, 'e2': 1, '泰克': 1, 'Coherent Solutions': 1, '高通': 48}
        # 接下来要考虑实体指代消解的问题。如 高通，高通公司
        return e_list,e_dict


def rdf2eid(filename0, filename1):
    # 读出filename0的rdf数据，写入包含eid和vaule的filename1
    # rdf表设计 e1|e2|rel|
    # 实体表设计 e1|e2|rel|e1id|e2id|e1value|e2value
    e_list, e_dict = get_mid_li_dic(filename0)
    with open(filename0, encoding='gb18030') as f0:
        with open(filename1, 'a', newline='', encoding='utf-8-sig') as f1:
            f0_reader = csv.reader(f0)
            f1_writer = csv.writer(f1)
            # 写表头只在第一次调用
            f1_writer.writerow(['e1', 'e2', 'rel', 'e1id', 'e2id', 'e1value', 'e2value'])
            for row in f0_reader:
                e1 = row[0]
                e2 = row[1]
                rel = row[2]
                if e1 == 'e1':
                    # 跳过表头
                    continue
                e1id = e_list.index(e1)+1  # 这样没有id==0的
                e2id = e_list.index(e2)+1
                e1value = e_dict[e1]
                e2value = e_dict[e2]
                f1_writer.writerow([e1, e2, rel, e1id, e2id, e1value, e2value])
    # 接下来要通过实体表写node和edge的json文件
    # 需要解决的问题：三元组数据完全重复，如何写入边，更改边的粗细？


def json_test(filename0, filename1, jsonfile):
    # 用org_rdf.csv生成e_lisr e_dict，用org_rdf_all.csv生成边列表json
    # e_list就是节点列表，可根据它生成node的json文件，label为列表元素，id为index+1，
    # value为元素对应的e_dict的值
    # 生成边json需要实体表，from e1id，to e2id，label为rel,但是边的id需要新生成。
    e_list, e_dict = get_mid_li_dic(filename0)
    STATIC_ID = 3000
    json_dict = {}
    # data_dict = {}
    nodes_list = []  # 节点列表
    edges_list = []  # 边列表
    # 生成节点列表
    for i, item in enumerate(e_list):
        node_dict = {}
        node_dict["label"] = item
        node_dict["value"] = e_dict[item]
        node_dict["id"] = i+1
        node_dict["categories"] = ["company"]
        node_dict["info"] = "暂无介绍"
        nodes_list.append(node_dict)

    # 生成边列表
    only_list = []  # 三元组有重复，加入一个唯一列表，过滤三元组。
    with open(filename1, encoding='utf-8') as f1:
        f1_reader = csv.reader(f1)
        for row in f1_reader:
            tem_list = []  # ['高通微软合作','高通华为竞争']
            tem_list.append(row[0])  # ‘高通’
            tem_list.append(row[1])  # ‘微软’
            tem_list.append(row[2])  # ‘合作’
            if ''.join(tem_list) not in only_list:
                only_list.append(''.join(tem_list))

                if row[3] == 'e1id':
                    # 跳过表头
                    continue
                edge_dict = {}
                STATIC_ID = STATIC_ID+1
                edge_dict["id"] = STATIC_ID
                edge_dict["label"] = row[2]
                edge_dict["from"] = int(row[3])
                edge_dict["to"] = int(row[4])
                edges_list.append(edge_dict)
            else:
                continue

    json_dict["categories"] = {
        "person": "人物",
        "company": "公司",
        "org": "组织",
        "tech": "技术",
        "domain": "领域"
    }
    tem_dict = {"nodes": nodes_list, "edges": edges_list}
    json_dict["data"] = tem_dict
    with open(jsonfile, "w", encoding="utf-8") as ft:
        json.dump(json_dict, ft, indent=2, sort_keys=False, ensure_ascii=False)  # 写为多行


def linekg(kid=1):
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
    lic = ["时间", "地点", "涉及行业", "商业秘密类别", "载体形式", "性质", "侵权人属性", "侵权方式", "侵权目的", "事件", "涉案人员", "组织机构", "法律条款", "正文"]
    nodes_list = []  # 节点列表
    edges_list = []  # 边列表
    s2id = {}
    s2count = {}
    STATIC_ID = 1500
    path = "qiemianli3.csv"
    csv_data = pd.read_csv(path, low_memory=False)
    r2 = csv_data.loc[kid]

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
    print(json_dict)


def anlis():
    path = "qiemianli3.csv"
    csv_data = pd.read_csv(path, low_memory=False).head()
    json_data = csv_data.to_json(orient='records', force_ascii=False)
    print(json_data)


def anliid(aid=1):
    path = "qiemianli4.csv"
    csv_data = pd.read_csv(path, low_memory=False)
    row = csv_data.loc[aid]
    # print(row[4])
    row[4] = row[4].split(',')
    # print(row[4])
    row[13] = row[13].split('/n')
    json_data = row.to_json(orient='index', force_ascii=False)
    print(json_data)


def newdata():
    with open(r'C:\Users\jason\PycharmProjects\gj-up\keji\static\qiemianli3.csv', 'r', encoding='utf8') as f:
        with open(r'C:\Users\jason\PycharmProjects\gj-up\keji\static\qiemianli4.csv', 'w', encoding='utf8', newline='') as fn:            
            fr = csv.reader(f)
            fw = csv.writer(fn)
            i = 0
            for row in fr:
                if row[0]=='时间':
                    li = ["time", "loc", "industry", "cate", "carrier", "nature", "pro", 'way', 'aim', 'event', 'people', 'org', 'law',
          'article', 'id']
                    fw.writerow(li)
                    i = i+1
                    continue
                print('row', row)
                print(type(row))
                row[3] = row[3].split(',')
                row[4] = row[4].split(',')
                row[13] = row[13].split('\u3000\u3000')
                lin = row+[str(i)]
                print(lin)
                i+=1
                fw.writerow(lin)
                                

if __name__ == '__main__':
    # linekg()
    # anliid(1)
    newdata()
    # json_dict = {}
    # json_dict["categories"] = {
    #     "time": "时间",
    #     "loc": "地点",
    #     "industry": "涉及行业",
    #     "cate": "商业秘密类别",
    #     "carrier": "载体形式",
    #     "nature": "性质",
    #     "pro": "侵权人属性",
    #     "way": "侵权方式",
    #     "aim": "侵权目的",
    #     "event": "事件",
    #     "people": "涉案人员",
    #     "org": "组织机构",
    #     "law": "法律条款",
    # }
    # li = ["time", "loc", "industry", "cate", "carrier", "nature", "pro", 'way', 'aim', 'event', 'people', 'org', 'law']
    # lic = ["时间", "地点", "涉及行业", "商业秘密类别", "载体形式", "性质", "侵权人属性", "侵权方式", "侵权目的", "事件", "涉案人员", "组织机构", "法律条款"]
    # nodes_list = []  # 节点列表
    # edges_list = []  # 边列表
    # s2id = {}
    # s2count = {}
    # STATIC_ID = 1500
    #
    # with open('qiemianli2.csv', 'r') as f:
    #     fr = csv.reader(f)
    #     i = 1
    #     for row in fr:
    #         if row == ['发生/审判时间：', '发生地点：', '涉及行业：', '商业秘密类别：', '载体形式：', '性质：', '侵权人：', '侵权方式：', '侵权目的：', '题目', '涉案人员', '组织机构', '法律条款']:
    #             continue
    #
    #         for item in row:
    #             if item not in s2id.keys():
    #                 s2id[item] = i
    #                 s2count[item] = 1
    #                 i += 1
    #             else:
    #                 s2count[item] += 1
    #
    # with open('qiemianli2.csv', 'r') as f:
    #     fr = csv.reader(f)
    #
    #     for row in fr:
    #         if row == ['发生/审判时间：', '发生地点：', '涉及行业：', '商业秘密类别：', '载体形式：', '性质：', '侵权人：', '侵权方式：', '侵权目的：', '题目', '涉案人员',
    #                    '组织机构', '法律条款']:
    #             continue
    #         for j in range(len(row)):
    #             node_dict = {}
    #             node_dict["label"] = row[j]
    #             node_dict["value"] = s2count[row[j]]
    #             node_dict["id"] = s2id[row[j]]
    #             node_dict["categories"] = li[j]
    #             node_dict["info"] = row[j]
    #             print(node_dict)
    #             nodes_list.append(node_dict)
    #             if row[j] == row[9]:
    #                 continue
    #             edge_dict = {}
    #             edge_dict["id"] = STATIC_ID
    #             STATIC_ID = STATIC_ID + 1
    #             edge_dict["label"] = lic[j]
    #             edge_dict["from"] = s2id[row[9]]
    #             edge_dict["to"] = s2id[row[j]]
    #             print(edge_dict)
    #             edges_list.append(edge_dict)
    # tem_dict = {"nodes": nodes_list, "edges": edges_list}
    # json_dict["data"] = tem_dict
    # with open('qiemitupu.json', "w", encoding="utf-8") as ft:
    #     json.dump(json_dict, ft, indent=2, sort_keys=False, ensure_ascii=False)  # 写为多行




    # rdf表设计 e1|e2|rel|
    # 实体表设计 e1|e2|rel|e1id|e2id|e1value|e2value
    # filename0 = 'org_rdf.csv'  # 用空格替换？之后不能用utf8读取了，改为encoding='gb18030'
    # filename1 = 'org_rdf_hezuon=2.csv'
    # filename2 = 'org_rdf_hezuon=n.csv'
    # filename3 = 'org_rdf_jingzhengn=n.csv'
    # filename4 = 'org_rdf_all.csv'

    # 统计value  Top30的公司名，写入json文件
    # e_list, e_dict = get_mid_li_dic(filename0)
    # dic_200 = {k: v for k, v in e_dict.items() if v >= 30}
    # print("个数", len(dic_200), ":", dic_200)
    # with open('rdf_orglist.json', "w", encoding="utf-8") as ft:
    #     json.dump(dic_200, ft, indent=2, sort_keys=False, ensure_ascii=False)  # 写为多行

    # rdf2eid(filename0, filename4)

    # e_list就是节点列表，可根据它生成node的json文件，label为列表元素，id为index+1，value为元素对应的e_dict的值
    # 生成边json需要实体表，from e1id，to e2id，label为rel,但是边的id需要新生成。

    # 新增数据的流程，先用get_rdf_fromlabeldata得到标注正确的实体对，然后save2org_rdf增加三元组e1 e2 rel
    # 然后get_mid_li_dic得到中间e_list e_dict，然后用rdf2eid生成实体表。
    # 最后用json_test生成json文件。
    # get_rdf_fromlabeldata("wj_biaozhu_jingzhengall_n=2.csv", "org_label=1_jingzhengn=2.csv")
    # save2org_rdf("org_label=1_hezuon=2.csv", "org_rdf.csv", "合作")
    # save2org_rdf("org_label=1_hezuon=n.csv", "org_rdf.csv", "合作")
    # save2org_rdf("org_label=1_jingzhengn=n.csv", "org_rdf.csv", "竞争")
    # save2org_rdf("org_label=1_gongyingn=2.csv", "org_rdf.csv", "供应")
    # 这之前都是utf-8编码，然后要手动把？替换成空格，org_rdf.csv就变成了encoding='gb18030'
    # rdf2eid("org_rdf.csv", "org_rdf_all.csv")  # 这里用gb18030读取，然后用utf8写入，得到org_rdf_all是utf8
    # 存json的时候要用到get_mid_li_dic读取org_rdf.csv，是gb18030编码的
    # json_test("org_rdf.csv", "org_rdf_all.csv", "org_data_all_only.json")



