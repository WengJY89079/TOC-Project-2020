from transitions.extensions import GraphMachine

from utils import send_text_message

class MagjongFSM(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_dealer(self, event):
        text = event.message.text
        return text == "莊家"
    def on_enter_dealer(self, event):
        print("bookmaker")
        reply_token = event.reply_token
        send_text_message(reply_token, "莊家和 是否門清?")

    def is_going_to_elseplayer(self, event):
        text = event.message.text
        return text == "閒家"
    def on_enter_elseplayer(self, event):
        print("elseplayer")
        reply_token = event.reply_token
        send_text_message(reply_token, "閒家和 是否門清?")

    def is_going_to_clear(self, event):
        text = event.message.text
        return text == "是"
    def on_enter_dealerclear(self, event):
        print("dealer clear")
        replay_token = event.reply_token
        send_text_message(replay_token, "門清 請個別輸入役種(輸入end結束)")
        #self.go_han(event)
    def on_enter_elseclear(self, event):
        print("else clear")
        replay_token = event.reply_token
        send_text_message(replay_token, "門清 請個別輸入役種(輸入end結束)")
        #self.go_han(event)

    def is_going_to_notclear(self, event):
        text = event.message.text
        return text == "否"
    def on_enter_dealernotclear(self, event):
        print("dealer not clear")
        replay_token = event.reply_token
        send_text_message(replay_token, "非門清 請個別輸入役種(輸入end結束)")
        #self.go_han(event)
    def on_enter_elsenotclear(self, event):
        print("else not clear")
        replay_token = event.reply_token
        send_text_message(replay_token, "門清 請個別輸入役種(輸入end結束)")
        #self.go_han(event)

    ''' full han '''
    def on_enter_dealerfullhan(self, event):
        print("dealer fullhan")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家役滿 48000pt 16000-all.")
        self.go_back(event)
    def on_enter_elsefullhan(self, event):
        print("else player fullhan")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家役滿 32000pt 8000-16000.")
        self.go_back(event)
    ''' san-bai '''
    def on_enter_dealersanbai(self, event):
        print("dealer sanbai")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家三倍滿 36000pt 12000-all.")
        self.go_back(event)
    def on_enter_elsesanbai(self, event):
        print("else player sanbai")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家三倍滿 24000pt 6000-12000.")
        self.go_back(event)
    ''' bai '''
    def on_enter_dealerbai(self, event):
        print("dealer bai")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家倍滿 24000pt 8000-all.")
        self.go_back(event)
    def on_enter_elsebai(self, event):
        print("else player fullhan")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家倍滿 16000pt 4000-8000.")
        self.go_back(event)
    ''' hane '''
    def on_enter_dealerhane(self, event):
        print("dealer hane")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家跳滿 18000pt 6000-all.")
        self.go_back(event)
    def on_enter_elsehane(self, event):
        print("else player hane")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家跳滿 12000pt 3000-6000.")
        self.go_back(event)
    ''' mangan '''
    def on_enter_dealermangan(self, event):
        print("dealer mangan")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家滿貫 12000pt 4000-all.")
        self.go_back(event)
    def on_enter_elsemangan(self, event):
        print("else player mangan")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家滿貫 8000pt 2000-4000.")
        self.go_back(event)
    ''' 4 han '''
    def on_enter_dealer4han(self, event):
        print("dealer 4han")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家4翻 計算符數--\n20符(平胡自摸) : 2600-all\n25符(七對子) : 9600pt 3200-all\n30符 : 11600pt 3900-all\n以上 : 莊家滿貫 12000pt 4000-all")
        self.go_back(event)
    def on_enter_else4han(self, event):
        print("else player 4han")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家4翻 計算符數--\n20符(平胡自摸) : 1300-2600\n25符(七對子) : 6400pt 1600-3200\n30符 : 7700pt 2000-3900\n以上 : 閒家滿貫 8000pt 2000-4000")
        self.go_back(event)
    ''' 3 han '''
    def on_enter_dealer3han(self, event):
        print("dealer 3han")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家3翻 計算符數--\n20符(平胡自摸) : 1300-all\n25符(七對子) : 4800pt 1600-all\n30符 : 5800pt 2000-all\n40符 : 7700pt 2600-all\n50符 : 9600pt 3200-all\n60符 : 11600pt 3900-all\n以上 : 莊家滿貫 12000pt 4000-all")
        self.go_back(event)
    def on_enter_else3han(self, event):
        print("else player 3han")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家3翻 計算符數--\n20符(平胡自摸) : 700-1300\n25符(七對子) : 3200pt 800-1600\n30符 : 3900pt 1000-2000\n40符 : 5200pt 1300-2600\n50符 : 6400pt 1600-3200\n60符 : 7700pt 2000-3900\n以上 : 閒家滿貫 8000pt 2000-4000")
        self.go_back(event)
    ''' 2 han '''
    def on_enter_dealer2han(self, event):
        print("dealer 2han")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家2翻 計算符數--\n20符(平胡自摸) : 700-all\n25符(七對子) : 2400pt\n30符 : 2900pt 1000-all\n40符 : 3900pt 1300-all\n50符 : 4800pt 1600-all\n60符 : 5800pt 2000-all\n70符 : 6800pt 2300-all\n80符 : 7700pt 2600-all\n90符 : 8700pt 2900-all\n100符 : 9600pt 3200-all\n110符 : 10600pt 3600-all")
        self.go_back(event)
    def on_enter_else2han(self, event):
        print("else player 2han")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家2翻 計算符數--\n20符(平胡自摸) : 400-700\n25符(七對子) : 1600pt\n30符 : 2000pt 500-1000\n40符 : 2600pt 700-1300\n50符 : 3200pt 800-1600\n60符 : 3900pt 1000-2000\n70符 : 4500pt 1200-2300\n80符 : 5200pt 1300-2600\n90符 : 5800pt 1500-2900\n100符 : 6400pt 1600-3200\n110符 : 7100pt 1800-3600")
        self.go_back(event)
    ''' 1 han '''
    def on_enter_dealer1han(self, event):
        print("dealer 1han")
        replay_token = event.reply_token
        send_text_message(replay_token, "莊家1翻 計算符數--\n30符 : 1500pt 500-all\n40符 : 2000pt 700-all\n50符 : 2400pt 800-all\n60符 : 2900pt 1000-all\n70符 : 3400pt 1200-all\n80符 : 3900pt 1300-all\n90符 : 4400 1500-all\n100符 : 4800pt 1600-all\n110符 : 5300pt")
        self.go_back(event)
    def on_enter_else1han(self, event):
        print("else player 1han")
        replay_token = event.reply_token
        send_text_message(replay_token, "閒家1翻 計算符數--\n30符 : 1000pt 300-500\n40符 : 1300pt 400-700\n50符 : 1600pt 400-800\n60符 : 2000pt 500-1000\n70符 : 2300pt 600-1200\n80符 : 2600pt 700-1300\n90符 : 2900pt 800-1500\n100符 : 3200pt 800-1600\n110符 : 3600pt")
        self.go_back(event)

    def on_enter_fart(self, event):
        print("fart")
        replay_token = event.reply_token
        send_text_message(replay_token, "無法胡牌 請重新開始輸入.")
        self.go_back(event)

    ''' 1 han conditions '''
    def clear_han1(self, event):
        text = event.message.text
        return text in ["立直", "一發", "門前清自摸", "斷么九", "平胡", "一盃口", "嶺上開花", "槍槓", "海底撈月", "河底撈魚"]
    def notclear_han1(self, event):
        text = event.message.text
        return text in ["斷么九", "嶺上開花", "槍槓", "海底撈月", "河底撈魚", "三色同順", "一氣通貫", "混全帶么九"]

    ''' 2 han conditions '''
    def clear_han2(self, event):
        text = event.message.text
        return text in ["三色同順", "三色同刻", "一氣通貫", "對對胡", "三暗刻", "三槓子", "七對子", "混全帶么九", "混老頭", "小三元", "雙立直"]
    def notclear_han2(self, event):
        text = event.message.text
        return text in ["三色同刻", "對對胡", "三暗刻", "三槓子", "混老頭", "小三元", "混一色", "二盃口"]

    ''' 3 han conditions '''
    def clear_han3(self, event):
        text = event.message.text
        return text in ["混一色", "純全帶么九", "二盃口"]

    ''' 5 han conditions '''
    def clear_han5(self, event):
        text = event.message.text
        return text in ["清一色"]

    ''' 6 han conditions '''
    def clear_han6(self, event):
        text = event.message.text
        return text in ["清一色"]

    ''' full han conditions '''
    def clear_full_han(self, event):
        text = event.message.text
        return text in ["國士無雙", "大三元", "四暗刻", "字一色", "綠一色", "小四喜", "大四喜", "清老頭", "九蓮寶燈", "四槓子", "天胡"]
    def not_clear_full_han(self, event):
        text = event.message.text
        return text in ["大三元", "字一色", "綠一色", "小四喜", "大四喜", "清老頭", "四槓子"]

    ''' bao conditions '''

    def bao1(self, event):
        text = event.message.text
        return text == "1寶牌"
    def bao2(self, event):
        text = event.message.text
        return text == "2寶牌"
    def bao3(self, event):
        text = event.message.text
        return text == "3寶牌"
    def bao4(self, event):
        text = event.message.text
        return text == "4寶牌"
    def bao5(self, event):
        text = event.message.text
        return text == "5寶牌"
    def bao6(self, event):
        text = event.message.text
        return text == "6寶牌"
    def bao7(self, event):
        text = event.message.text
        return text == "7寶牌"
    def bao8(self, event):
        text = event.message.text
        return text == "8寶牌"
    def bao9(self, event):
        text = event.message.text
        return text == "9寶牌"
    def bao10(self, event):
        text = event.message.text
        return text == "10寶牌"
    def bao11(self, event):
        text = event.message.text
        return text == "11寶牌"
    def bao12(self, event):
        text = event.message.text
        return text == "12寶牌"

    ''' end condition '''

    def end(self, event):
        text = event.message.text
        return text == "end"