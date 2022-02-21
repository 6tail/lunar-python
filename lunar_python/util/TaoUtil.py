# -*- coding: utf-8 -*-
from ..TaoFestival import TaoFestival


class TaoUtil:
    """
    道历工具
    """

    # 三会日
    SAN_HUI = ("1-7", "7-7", "10-15")

    # 三元日
    SAN_YUAN = ("1-15", "7-15", "10-15")

    # 五腊日
    WU_LA = ("1-1", "5-5", "7-7", "10-1", "12-8")

    # 暗戊
    AN_WU = ("未", "戌", "辰", "寅", "午", "子", "酉", "申", "巳", "亥", "卯", "丑")

    # 八会日
    BA_HUI = {
        "丙午": "天会",
        "壬午": "地会",
        "壬子": "人会",
        "庚午": "日会",
        "庚申": "月会",
        "辛酉": "星辰会",
        "甲辰": "五行会",
        "甲戌": "四时会"
    }

    # 八节日
    BA_JIE = {
        "立春": "东北方度仙上圣天尊同梵炁始青天君下降",
        "春分": "东方玉宝星上天尊同青帝九炁天君下降",
        "立夏": "东南方好生度命天尊同梵炁始丹天君下降",
        "夏至": "南方玄真万福天尊同赤帝三炁天君下降",
        "立秋": "西南方太灵虚皇天尊同梵炁始素天君下降",
        "秋分": "西方太妙至极天尊同白帝七炁天君下降",
        "立冬": "西北方无量太华天尊同梵炁始玄天君下降",
        "冬至": "北方玄上玉宸天尊同黑帝五炁天君下降"
    }

    # 日期对应的节日
    FESTIVAL = {
        "1-1": [TaoFestival("天腊之辰", "天腊，此日五帝会于东方九炁青天")],
        "1-3": [TaoFestival("郝真人圣诞"), TaoFestival("孙真人圣诞")],
        "1-5": [TaoFestival("孙祖清静元君诞")],
        "1-7": [TaoFestival("举迁赏会", "此日上元赐福，天官同地水二官考校罪福")],
        "1-9": [TaoFestival("玉皇上帝圣诞")],
        "1-13": [TaoFestival("关圣帝君飞升")],
        "1-15": [TaoFestival("上元天官圣诞"), TaoFestival("老祖天师圣诞")],
        "1-19": [TaoFestival("长春邱真人(邱处机)圣诞")],
        "1-28": [TaoFestival("许真君(许逊天师)圣诞")],
        "2-1": [TaoFestival("勾陈天皇大帝圣诞"), TaoFestival("长春刘真人(刘渊然)圣诞")],
        "2-2": [TaoFestival("土地正神诞"), TaoFestival("姜太公圣诞")],
        "2-3": [TaoFestival("文昌梓潼帝君圣诞")],
        "2-6": [TaoFestival("东华帝君圣诞")],
        "2-13": [TaoFestival("度人无量葛真君圣诞")],
        "2-15": [TaoFestival("太清道德天尊(太上老君)圣诞")],
        "2-19": [TaoFestival("慈航真人圣诞")],
        "3-1": [TaoFestival("谭祖(谭处端)长真真人圣诞")],
        "3-3": [TaoFestival("玄天上帝圣诞")],
        "3-6": [TaoFestival("眼光娘娘圣诞")],
        "3-15": [TaoFestival("天师张大真人圣诞"), TaoFestival("财神赵公元帅圣诞")],
        "3-16": [TaoFestival("三茅真君得道之辰"), TaoFestival("中岳大帝圣诞")],
        "3-18": [TaoFestival("王祖(王处一)玉阳真人圣诞"), TaoFestival("后土娘娘圣诞")],
        "3-19": [TaoFestival("太阳星君圣诞")],
        "3-20": [TaoFestival("子孙娘娘圣诞")],
        "3-23": [TaoFestival("天后妈祖圣诞")],
        "3-26": [TaoFestival("鬼谷先师诞")],
        "3-28": [TaoFestival("东岳大帝圣诞")],
        "4-1": [TaoFestival("长生谭真君成道之辰")],
        "4-10": [TaoFestival("何仙姑圣诞")],
        "4-14": [TaoFestival("吕祖纯阳祖师圣诞")],
        "4-15": [TaoFestival("钟离祖师圣诞")],
        "4-18": [TaoFestival("北极紫微大帝圣诞"), TaoFestival("泰山圣母碧霞元君诞"), TaoFestival("华佗神医先师诞")],
        "4-20": [TaoFestival("眼光圣母娘娘诞")],
        "4-28": [TaoFestival("神农先帝诞")],
        "5-1": [TaoFestival("南极长生大帝圣诞")],
        "5-5": [TaoFestival("地腊之辰", "地腊，此日五帝会于南方三炁丹天"), TaoFestival("南方雷祖圣诞"), TaoFestival("地祗温元帅圣诞"), TaoFestival("雷霆邓天君圣诞")],
        "5-11": [TaoFestival("城隍爷圣诞")],
        "5-13": [TaoFestival("关圣帝君降神"), TaoFestival("关平太子圣诞")],
        "5-18": [TaoFestival("张天师圣诞")],
        "5-20": [TaoFestival("马祖丹阳真人圣诞")],
        "5-29": [TaoFestival("紫青白祖师圣诞")],
        "6-1": [TaoFestival("南斗星君下降")],
        "6-2": [TaoFestival("南斗星君下降")],
        "6-3": [TaoFestival("南斗星君下降")],
        "6-4": [TaoFestival("南斗星君下降")],
        "6-5": [TaoFestival("南斗星君下降")],
        "6-6": [TaoFestival("南斗星君下降")],
        "6-10": [TaoFestival("刘海蟾祖师圣诞")],
        "6-15": [TaoFestival("灵官王天君圣诞")],
        "6-19": [TaoFestival("慈航(观音)成道日")],
        "6-23": [TaoFestival("火神圣诞")],
        "6-24": [TaoFestival("南极大帝中方雷祖圣诞"), TaoFestival("关圣帝君圣诞")],
        "6-26": [TaoFestival("二郎真君圣诞")],
        "7-7": [TaoFestival("道德腊之辰", "道德腊，此日五帝会于西方七炁素天"), TaoFestival("庆生中会", "此日中元赦罪，地官同天水二官考校罪福")],
        "7-12": [TaoFestival("西方雷祖圣诞")],
        "7-15": [TaoFestival("中元地官大帝圣诞")],
        "7-18": [TaoFestival("王母娘娘圣诞")],
        "7-20": [TaoFestival("刘祖(刘处玄)长生真人圣诞")],
        "7-22": [TaoFestival("财帛星君文财神增福相公李诡祖圣诞")],
        "7-26": [TaoFestival("张三丰祖师圣诞")],
        "8-1": [TaoFestival("许真君飞升日")],
        "8-3": [TaoFestival("九天司命灶君诞")],
        "8-5": [TaoFestival("北方雷祖圣诞")],
        "8-10": [TaoFestival("北岳大帝诞辰")],
        "8-15": [TaoFestival("太阴星君诞")],
        "9-1": [TaoFestival("北斗九皇降世之辰")],
        "9-2": [TaoFestival("北斗九皇降世之辰")],
        "9-3": [TaoFestival("北斗九皇降世之辰")],
        "9-4": [TaoFestival("北斗九皇降世之辰")],
        "9-5": [TaoFestival("北斗九皇降世之辰")],
        "9-6": [TaoFestival("北斗九皇降世之辰")],
        "9-7": [TaoFestival("北斗九皇降世之辰")],
        "9-8": [TaoFestival("北斗九皇降世之辰")],
        "9-9": [TaoFestival("北斗九皇降世之辰"), TaoFestival("斗姥元君圣诞"), TaoFestival("重阳帝君圣诞"), TaoFestival("玄天上帝飞升"), TaoFestival("酆都大帝圣诞")],
        "9-22": [TaoFestival("增福财神诞")],
        "9-23": [TaoFestival("萨翁真君圣诞")],
        "9-28": [TaoFestival("五显灵官马元帅圣诞")],
        "10-1": [TaoFestival("民岁腊之辰", "民岁腊，此日五帝会于北方五炁黑天"), TaoFestival("东皇大帝圣诞")],
        "10-3": [TaoFestival("三茅应化真君圣诞")],
        "10-6": [TaoFestival("天曹诸司五岳五帝圣诞")],
        "10-15": [TaoFestival("下元水官大帝圣诞"), TaoFestival("建生大会", "此日下元解厄，水官同天地二官考校罪福")],
        "10-18": [TaoFestival("地母娘娘圣诞")],
        "10-19": [TaoFestival("长春邱真君飞升")],
        "10-20": [TaoFestival("虚靖天师(即三十代天师弘悟张真人)诞")],
        "11-6": [TaoFestival("西岳大帝圣诞")],
        "11-9": [TaoFestival("湘子韩祖圣诞")],
        "11-11": [TaoFestival("太乙救苦天尊圣诞")],
        "11-26": [TaoFestival("北方五道圣诞")],
        "12-8": [TaoFestival("王侯腊之辰", "王侯腊，此日五帝会于上方玄都玉京")],
        "12-16": [TaoFestival("南岳大帝圣诞"), TaoFestival("福德正神诞")],
        "12-20": [TaoFestival("鲁班先师圣诞")],
        "12-21": [TaoFestival("天猷上帝圣诞")],
        "12-22": [TaoFestival("重阳祖师圣诞")],
        "12-23": [TaoFestival("祭灶王", "最适宜谢旧年太岁，开启拜新年太岁")],
        "12-25": [TaoFestival("玉帝巡天"), TaoFestival("天神下降")],
        "12-29": [TaoFestival("清静孙真君(孙不二)成道")]
    }

    def __init__(self):
        pass
