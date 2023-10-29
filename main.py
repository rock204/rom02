def on_button_pressed_a(): #Aボタンで測定開始
    global mode
    mode = 1
    OLED12864_I2C.clear()
    OLED12864_I2C.show_string(0, 0, "Start Measur.", 1)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab(): #A+Bボタンでキャリブレーション呼び出し
    basic.show_string("reset ROM")
    syokika()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b(): #Bボタンで測定角度再表示
    basic.show_number(Math.round(m_deg))
input.on_button_pressed(Button.B, on_button_pressed_b)

def syokika(): #キャリブレーション
    OLED12864_I2C.clear()
    OLED12864_I2C.show_string(0, 0, "Start Cal", 1)
    global deg_0, deg_180, mode
    OLED12864_I2C.show_string(0, 1, "move to 0", 1)
    #basic.show_string("move 0")
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.UNTIL_DONE)
    while pins.digital_read_pin(DigitalPin.P1) == 0:
        pass
    deg_0 = pins.analog_read_pin(AnalogPin.P0)
    OLED12864_I2C.show_string(0, 1, "move to 180", 1)
    #basic.show_string("move 180")
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.UNTIL_DONE)
    while pins.digital_read_pin(DigitalPin.P1) == 0:
        pass
    deg_180 = pins.analog_read_pin(AnalogPin.P0)
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.UNTIL_DONE)
    mode = 0
    basic.show_icon(IconNames.YES)
    OLED12864_I2C.show_string(0, 2, "END Cal", 1)
    basic.pause(1000)
    OLED12864_I2C.clear()
    OLED12864_I2C.show_string(0, 0, "Measurement  Ready", 1)
    OLED12864_I2C.show_string(0, 2, "Start->A", 1)
#最初に実行する
OLED12864_I2C.init(60)
OLED12864_I2C.show_string(0, 0, "Pro. ROM3", 1)
basic.pause(1000)
bf = 0 #使い捨てのバッファー
deg_180 = 0 #180゜の位置のアナログ値を入れる
deg_0 = 0   #0゜の位置のアナログ値を入れる
m_deg = 0   #角度の測定値を入れる
mode = 999  #測定過程を入れる(999:準備状態 1:測定中 0:停止)
pins.set_pull(DigitalPin.P1, PinPullMode.PULL_DOWN)
#タクトスイッチの入力を安定化させる
syokika() #キャリブレーション呼び出し

#測定ルーチン
def on_forever():
    global bf, m_deg, mode
    if mode == 1: #測定中
        basic.show_icon(IconNames.HEART)
        #タクトスイッチが押されるまで待つ
        while pins.digital_read_pin(DigitalPin.P1) == 0:
            pass
        bf = pins.analog_read_pin(AnalogPin.P0) #可変抵抗の電圧を取得
        #取得したアナログ値をキャリブレーション値で角度に変換
        m_deg = Math.map(bf, deg_0, deg_180, 0, 180)
        music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)),
            music.PlaybackMode.UNTIL_DONE)
        bf=Math.round(m_deg) #角度を四捨五入
        string_bf=bf+" deg"
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0, 0,string_bf, 1)
        OLED12864_I2C.show_string(0, 2,"measur->A", 1)
        mode = 0 #測定停止
basic.forever(on_forever)
