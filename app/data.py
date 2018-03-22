# encoding: utf-8  
'''

所有对于数据的操作

'''
import webset
import yaml
import os

class Site:
    def getwebconf(self, confname):
        conffile = webset.ConfigFile + '/_config.yaml'
        config = []
        with open(conffile, 'r') as f:
            config = yaml.load(f)

        if confname == 'AdminDir':
            return config['basic']['admindir']
        elif confname == 'HexoDir':
            return config['basic']['hexodir']
        elif confname == 'StaticFile':
            return config['basic']['staticurl']
        elif confname == 'ConfigFile':
            return webset.ConfigFile


class Data:
    def getconfig(self, confname):
        if confname == 'author':
            return '吃着土豆坐地铁'
    
    def Blogs_Get_List(self):
        SiteConf = Site()
        path = SiteConf.getwebconf('HexoDir') + '/source/_posts'
        def compare(x, y):  
            stat_x = os.stat(path + "/" + x)  
            stat_y = os.stat(path + "/" + y)  
            if stat_x.st_mtime > stat_y.st_mtime:  
                return -1  
            elif stat_x.st_mtime < stat_y.st_mtime:  
                return 1  
            else:  
                return 0  
        iterms = os.listdir(path)  
        iterms.sort(compare)  
        return iterms


    def Drafts_Get_List(self):
        SiteConf = Site()
        path = SiteConf.getwebconf('HexoDir') + '/source/_drafts'
        files= os.listdir(path)
        return files

    def Pages_Get_List(self):
        SiteConf = Site()
        path = SiteConf.getwebconf('HexoDir') + '/source'
        def compare(x, y):  
            stat_x = os.stat(path + "/" + x + '/index.md')  
            stat_y = os.stat(path + "/" + y + '/index.md')  
            if stat_x.st_mtime > stat_y.st_mtime:  
                return -1  
            elif stat_x.st_mtime < stat_y.st_mtime:  
                return 1  
            else:  
                return 0  
        list = []
        files = os.listdir(path)  
        for file in files:  
            m = os.path.join(path,file)  
            if (os.path.isdir(m)):
                h = os.path.split(m)
                dname = h[1]
                if dname[0:1] != '_':
                    list.append(dname)  
        list.sort(compare)
        return list
