# SmartphoneGuideBot

## 概要
Redmi 12というスマートフォンの使い方およびその他有用な情報をガイドするLINEボット。

## 経緯
今までデジタルに全く触れてこなかった祖母がスマホを持ち始めるため、
スマートフォンの使い方がわからなくなった時に気軽にLINEで質問できるボットが必要になると考えた。

## 使用技術
GPT-2をQ&Aデータによって一からファインチューニングすることは困難かつ性能も見込めないと考えたため、
ChatGPTのAPIを用いてチャットボットを作成した。  
また、iPhoneやGoogle Pixelなどといったメジャーなスマートフォンであれば、
ChatGPTの学習データセットの中に使い方が記載されている文章があるはずなので、そのまま使えば問題はない。
しかし、祖母が持つのはRedmi 12というマイナーなスマートフォンであるため、
使い方を聞いても一般的なAndroidに共通した内容しか答えなかった。  
![image](https://github.com/StupidYoshiaki/SmartphoneGuideBot/issues/2#issue-2144017012)




祖母の持つスマートフォンが