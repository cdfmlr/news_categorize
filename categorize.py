import jieba.analyse as jba
import re

class Text(object):
    '''
    ## 初始化

    - text_data: 文本
    - words_libs: 词库文件路径列表

    ## 方法

    - getText() 获取文本
    - getWordsLibs() 获取词库文件路径列表
    - getKeywords() 提取文本关键词
    - getCategories() 提取文本分类 
    '''

    def __init__(self, text_data, words_libs):
        self.data = str(text_data)
        self.wordsLibs = list(words_libs)

    def getText(self):
        return self.data or ''

    def getWordsLibs(self):
        return self.wordsLibs

    def getKeywords(self, num=10):
        '''
        # 提取文本关键词
        
        ## 参数
        - int num  : 输出的关键词数

        ## 算法选择
            判断文本长度，选则使用 TF-IDF 或 TextRank 算法：

            - 短文本，使用 TextRank 算法
            - 长文本，使用 TF-IDF 算法

        ## 输出
        
        ```
        # jba.textrank(data, topK=num, withWeight=True)
        [('关键词', 权重), ...]

        # jba.textrank(data, topK=num)
        ['关键词', ...]
        ```
        现采用第二种策略
        '''

        length = len(self.getText())
        if length < 50:     # 短文本，使用 TextRank 算法
            res = jba.textrank(self.getText(), topK=num) 
        else:               # 长文本，使用 TF-IDF 算法
            res = jba.extract_tags(self.getText(), topK=num)
        return res

    def getCategories(self):
        '''
        遍历词库，寻找合适的分类
        '''
        libs = self.getWordsLibs()
        keys = self.getKeywords()
        res = []

        for lib in libs:
            with open(lib) as f:
                for libWord in f:
                    for keyWord in keys:
                        if libWord.split() == keyWord.split():
                            category = re.findall('【(.*?)】', lib)[0]
                            if category not in res:
                                res.append(category)

        return res


if __name__ == "__main__":
    with open('test_text/b.txt') as f:
        data = f.read()

    wordslib = []
    with open('words_lib/index.txt') as f:
        for line in f:
            wordslib.append('words_lib/' + line.split()[0])

    t = Text(data, wordslib)
    print('Keywords:', t.getKeywords())
    print('Categories:', t.getCategories())
