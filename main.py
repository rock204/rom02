def get_start_position():
    global bf,m_deg,deg_180,deg_0,start_deg
    OLED12864_I2C.clear()
    OLED12864_I2C.show_string(0, 1, "move to St.", 1)
    basic.show_icon(IconNames.ASLEEP)
    # タクトスイッチが押されるまで待つ
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
    OLED12864_I2C.show_string(0, 0,'Start deg', 1)
    OLED12864_I2C.show_string(0, 1,string_bf, 1)
    start_deg=bf

def on_button_pressed_a():
    global mode
    # Aボタンで測定開始
    #mode = 1
    OLED12864_I2C.clear()
    OLED12864_I2C.show_string(0, 0, "Start Position.", 1)
    get_start_position()
    mode=1
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    # A+Bボタンでキャリブレーション呼び出し
    syokika()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def syokika():
    global deg_0, deg_180, mode
    # キャリブレーション
    OLED12864_I2C.clear()
    OLED12864_I2C.show_string(0, 0, "Start Cal", 1)
    OLED12864_I2C.show_string(0, 1, "move to 0", 1)
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.UNTIL_DONE)
    while pins.digital_read_pin(DigitalPin.P1) == 0:
        pass
    deg_0 = pins.analog_read_pin(AnalogPin.P0)
    OLED12864_I2C.show_string(0, 1, "move to 180", 1)
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

m_deg = 0
bf = 0
deg_180 = 0
deg_0 = 0
mode = 0
start_deg=0

# 最初に実行する
OLED12864_I2C.init(60)
OLED12864_I2C.show_string(0, 0, "ROM 3-78", 1)
basic.pause(3000)
# 角度の測定値を入れる
mode = 999
# 測定過程を入れる(999:準備状態 1:測定中 0:停止)
pins.set_pull(DigitalPin.P1, PinPullMode.PULL_DOWN)
# タクトスイッチの入力を安定化させる
syokika()
# キャリブレーション呼び出し
# 測定ルーチン
# 測定停止

def on_forever():
    global bf, m_deg, mode
    if mode == 1:
        # 測定中
        basic.show_icon(IconNames.HEART)
        # タクトスイッチが押されるまで待つ
        while pins.digital_read_pin(DigitalPin.P1) == 0:
            pass
        bf = pins.analog_read_pin(AnalogPin.P0)
        # 可変抵抗の電圧を取得
        # 取得したアナログ値をキャリブレーション値で角度に変換
        m_deg = Math.map(bf, deg_0, deg_180, 0, 180)
        music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)),
            music.PlaybackMode.UNTIL_DONE)
        bf = Math.round(m_deg)
        # 角度を四捨五入
        string_bf = "" + str(bf) + " deg"
        OLED12864_I2C.clear()
        OLED12864_I2C.show_string(0, 0, string_bf, 1)
        OLED12864_I2C.show_string(0, 2, "measur->A", 1)
        mode = 0
basic.forever(on_forever)
