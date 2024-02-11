from .Printer import Printer
import numpy as np

class DictSearcher:
    @classmethod
    def PrintStr(cls,hist:list,message:str):
        return (('>'.join(hist) + " ") if len(hist) > 0 else '') + message
    @classmethod
    def check(cls,top,key,hist=[]):
        assert (isinstance(top,dict) and key in top) or (isinstance(top,list) and isinstance(key,int) and key < len(top)), cls.PrintStr(hist,Printer.err(f"invalid key: {key}"))
    @classmethod
    def SearchKeyList(cls,top:dict,keys:list,hist=[]):
        if len(keys) == 0:
            return top
        cls.check(top,keys[0],hist)
        if len(keys) > 1:
            return cls.SearchKeyList(top[keys[0]],keys[1:],hist + [keys[0]])
        else:
            return top[keys[0]]
    @staticmethod
    def Search(top:dict,key):
        if isinstance(key,list):
            return DictSearcher.SearchKeyList(top,key)
        elif isinstance(key,tuple):
            return DictSearcher.SearchKeyList(top,list(*key))
        else:
            DictSearcher.check(top,key)
            return top[key]
    @staticmethod
    def SumChildValue(top:dict,key=None):
        if key is not None:
            parent = DictSearcher.Search(top,key)
        else:
            parent = top
        allroot = parent
        # print("all root:",allroot)
        allroot = DictSearcher.getAllLeaf(allroot)
        # print("flatten:",allroot)
        return sum(allroot) if isinstance(allroot,list) else allroot
            
    @staticmethod
    def getAllLeaf(top):
        # 空のリストを作成
        values = []
        if isinstance(top,list):
            for value in top:
                # 返ってきたリーフノードの値をリストに追加する
                values.extend(DictSearcher.getAllLeaf(value))
        elif isinstance(top,dict):
            # 辞書のキーと値を順に取り出す
            for key, value in top.items():
                # 返ってきたリーフノードの値をリストに追加する
                values.extend(DictSearcher.getAllLeaf(value))
            # 値が辞書でなければ、リーフノードの値としてリストに追加する
        else:
            values.append(top)
        # リーフノードの値のリストを返す
        return values
    
    @staticmethod
    def flattenlist(l):
        if isinstance(l,list):
            return np.sum(l, axis=0,dtype=object)
        else:
            return l
