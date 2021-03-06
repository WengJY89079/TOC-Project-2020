# TOC Project 2020 - 日本麻將算翻機

## 簡介

日本麻將除了胡牌形式複雜，點數、翻數的算法也會因為莊閒家、門清與否而改變。
這個linebot整合了所有胡排排形、寶牌、與莊閒家門清的組合，適合對翻數組合不熟悉的玩家進行初步的計算。

## 流程

1. 輸入胡牌者為莊家或閒家
2. 輸入是否門清
3. 分別輸入役種，直到輸入end
4. 輸出結果

## 執行圖片

![](https://i.imgur.com/KeWs5c3.png)

## Finite State Machine

![fsm](./fsm.png)
![fsm1](./fsm1.png)

這個fsm可分為四個部分:
1. init分出莊家或閒家
2. 莊家和閒家分出是否門清
3. 共4條的累積翻數器
4. 輸入end後，輸出結果並轉移到init

## 役種列表

https://zh.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E9%BA%BB%E5%B0%87%E7%9A%84%E5%92%8C%E7%89%8C%E7%89%8C%E5%9E%8B%E5%88%97%E8%A1%A8
